
#
# py by the c
#

#
# a cross platform build system for c/c++
#
# glowtree.com/pybythec for documentation
#
# written by Tom Sirdevan
#
# contact: tom@glowtree.com
#

#
# builds c/c++ projects that create ...
#
# exe     (executable)
# static  (library)
# dynamic (library)  
# plugin  (a dynamic library that is loaded on demand, not linked to executables)
#

from pybythec import utils
from pybythec.BuildStatus import *
from pybythec.BuildElements import *

import os
import sys
import shutil
import time
import logging
from threading import Thread

log = logging.getLogger('pybythec')


def build(argv):
  '''
    the main function, does the heavy lifting
  
    argv (in): command line arguments
  '''
  
  #
  # cleaning
  #
  if '-cl' in argv:
    return clean(argv)
  if '-cla' in argv:
    return cleanall(argv)
  
  try:
    be = BuildElements(argv)
  except Exception as e:
    log.error(str(e))
    return False

  # lock - early return
  if be.locked and os.path.exists(be.targetInstallPath):
    buildStatus.writeInfo('locked', be.target + ' is locked')
    return True

  #
  # building
  #
  startTime = time.time()
  
  threading = True
  
  log.info('building {0} ({1} {2} {3})'.format(be.target, be.buildType, be.compiler, be.binaryFormat))

  if not os.path.exists(be.installPath):
    utils.createDirs(be.installPath)

  if not os.path.exists(be.buildPath):
    os.makedirs(be.buildPath)

  incPathList = []
  for incPath in be.incPaths:
    incPathList += ['-I', incPath]
  
  definesList = []
  for define in be.defines:
    definesList += ['-D', define]
  
  buildStatus = BuildStatus(be.target, be.buildPath) # final build status

  #
  # qt moc file compilation
  #
  mocPaths = []
  for qtClass in be.qtClasses:
    found = False
    mocPath  = '{0}/moc_{1}.cpp'.format(be.buildPath, qtClass)
    qtClassHeader = qtClass + '.h'
    
    for incPath in be.incPaths:  # find the header file, # TODO: should there be a separate list of headers ie be.mocIncPaths?
      includePath = incPath + '/' + qtClassHeader
      if not os.path.exists(includePath):
        continue

      if os.path.exists(mocPath) and float(os.stat(mocPath).st_mtime) < float(os.stat(includePath).st_mtime) or not os.path.exists(mocPath):
        buildStatus.description = 'qt moc: ' + utils.runCmd(['moc'] + definesList + [includePath, '-o', mocPath])
      
      if not os.path.exists(mocPath):
        buildStatus.writeError(buildStatus.description)
        return False
        
      mocPaths.append(mocPath)
      found = True
          
    if not found:
      buildStatus.writeError('can\'t find {0} for qt moc compilation'.format(qtClassHeader))
      return False

  for mocPath in mocPaths:
    be.sources.append(mocPath)

  buildStatusDeps = [] # the build status for each dependency: objs and libs
  threads = []
  i = 0

  #
  # compile
  #
  objPaths = []
  cmd = [be.compilerCmd, be.objFlag] + incPathList + definesList + be.flags
  
  if threading:
    for source in be.sources:
      buildStatusDep = BuildStatus(source)
      buildStatusDeps.append(buildStatusDep)
      thread = Thread(None, target = _compileSrc, args = (be, cmd, source, objPaths, buildStatusDep))
      thread.start()
      threads.append(thread)
      i += 1
  else:
    for source in be.sources:
      buildStatusDep = BuildStatus(source)
      buildStatusDeps.append(buildStatusDep)
      _compileSrc(be, cmd, source, objPaths, buildStatusDep)
      i += 1

  #
  # build library dependencies
  #
  libCmds = []
  libsBuilding = []
  if be.binaryType == 'exe' or be.binaryType == 'plugin':
    for lib in be.libs:
      libName = lib
      if be.compiler.startswith('msvc'):
        libCmds += [libName + be.staticExt] # you need to link against the .lib stub file even if it's ultimately a .dll that gets linked
      else:
        libCmds += [be.libFlag, libName]
        
      # check if the lib has a directory for building
      if threading:
        for libSrcDir in be.libSrcPaths:
          libSrcDir = os.path.join(libSrcDir, lib)
          if os.path.exists(libSrcDir):
            libsBuilding.append(lib)
            buildStatusDep = BuildStatus(lib)
            buildStatusDeps.append(buildStatusDep)
            thread = Thread(None, target = _buildLib, args = (be, libSrcDir, buildStatusDep))
            thread.start()
            threads.append(thread)
            i += 1
            break
      else:
        for libSrcPath in be.libSrcPaths:
          libSrcPath = os.path.join(libSrcPath, lib)
          if os.path.exists(libSrcPath):
            libsBuilding.append(lib)
            buildStatusDep = BuildStatus(lib)
            buildStatusDeps.append(buildStatusDep)
            _buildLib(be, libSrcDir, buildStatusDep)
            i += 1
            break

  # wait for all the threads before checking the results
  for thread in threads:
    thread.join()

  allUpToDate = True
  for buildStatusDep in buildStatusDeps:
    if buildStatusDep.status == 'failed':
      buildStatus.writeError('{0} ({1} {2} {3}) failed because {4} failed because...\n\n{5}\n...determined in seconds\n\n'.format(be.target, be.buildType, be.compiler, be.binaryFormat, buildStatusDep.name, buildStatusDep.description.encode('ascii', 'ignore'), str(int(time.time() - startTime))))
      return False
    elif buildStatusDep.status == 'built':
      allUpToDate = False

  # revise the library paths
  for i in range(len(be.libPaths)):
    revisedLibPath = be.libPaths[i] + be.binaryRelPath
    if os.path.exists(revisedLibPath):
      be.libPaths[i] = revisedLibPath
    else: # in case there's also lib paths that don't have buildType, ie for external libraries that only ever have the release version
      revisedLibPath = '{0}/{1}{2}/{3}'.format(be.libPaths[i], be.compilerRoot, be.compilerVersion, be.binaryFormat)
      if os.path.exists(revisedLibPath):
        be.libPaths[i] = revisedLibPath

  #
  # linking
  #
  linkCmd = []
  
  if allUpToDate and os.path.exists(be.targetInstallPath):
    buildStatus.writeInfo('up to date', '{0} ({1} {2} {3}) is up to date, determined in {4} seconds\n'.format(be.target, be.buildType, be.compiler, be.binaryFormat, str(int(time.time() - startTime))))
    return True
  
  # microsoft's compiler / linker can only handle so many characters on the command line
  msvcLinkCmdFilePath = be.buildPath + '/linkCmd'
  if be.compiler.startswith('msvc'):
    msvcLinkCmd = '{0}"{1}" {2} {3}'.format(be.targetFlag, be.targetInstallPath, ' '.join(objPaths), ' '.join(libCmds))
    msvcLinkCmdFp = open(msvcLinkCmdFilePath, 'w')
    msvcLinkCmdFp.write(msvcLinkCmd)
    msvcLinkCmdFp.close()
    linkCmd += [be.linker, '@' + msvcLinkCmdFilePath]
    if be.showLinkerCmds:
      log.info('\nmsvcLinkCmd: {0}\n'.format(msvcLinkCmd))
  else:
    linkCmd += [be.linker, be.targetFlag, be.targetInstallPath] + objPaths + libCmds

  if be.binaryType != 'static': # TODO: is this the case for msvc?
    linkCmd += be.linkFlags

  if be.binaryType == 'exe' or be.binaryType == 'plugin' or (be.compilerRoot == 'msvc' and be.binaryType == 'dynamic'):
          
    for libPath in be.libPaths:
      if be.compiler.startswith('msvc'):
        linkCmd += [be.libPathFlag + os.path.normpath(libPath)]
      else:
        linkCmd += [be.libPathFlag, os.path.normpath(libPath)]
  
  # get the timestamp of the existing target if it exists
  linked = False
  targetExisted = False
  oldTargetTimeStamp = None
  if os.path.exists(be.targetInstallPath):
    oldTargetTimeStamp = float(os.stat(be.targetInstallPath).st_mtime)
    targetExisted = True
  
  if be.showLinkerCmds:
    log.info('\n{0}\n'.format(' '.join(linkCmd)))
  
  buildStatus.description = utils.runCmd(linkCmd)

  if os.path.exists(be.targetInstallPath):
    if targetExisted:
      if float(os.stat(be.targetInstallPath).st_mtime) > oldTargetTimeStamp:
        linked = True
    else:
      linked = True
  
  if linked:
    log.info('linked {0} ({1} {2} {3})'.format(be.target, be.buildType, be.binaryFormat, be.compiler))
  else:
    buildStatus.writeError('linking failed because ' + buildStatus.description)
    return False

  # copy dynamic library dependencies (built by this build) to the install path   
  if be.binaryType == 'exe' or be.binaryType == 'plugin':
    for lib in libsBuilding:
      for libPath in be.libPaths:
        dynamicPath = libPath + '/'
        if be.compilerRoot == 'gcc' or be.compilerRoot == 'clang':
          dynamicPath += 'lib'
        dynamicPath += lib + be.dynamicExt
        if os.path.exists(dynamicPath):
          utils.copyfile(dynamicPath, be.installPath)
  
  
  # TODO ?
  # if be.compiler.startswith('msvc') and be.multithread and (be.binaryType == 'exe' or be.binaryType == 'dynamic' or be.binaryType == 'plugin'):
    # # TODO: figure out what this #2 shit is, took 4 hours of bullshit to find out it's needed for maya plugins
    # buildStatus.description = utils.runCmd(['mt', '-nologo', '-manifest', be.targetInstallPath + '.manifest', '-outputresource:', be.targetInstallPath + ';#2'])      
  
  buildStatus.writeInfo('built', '{0} ({1} {2} {3}) built {4}\ncompleted in {5} seconds\n'.format(be.target, be.buildType, be.binaryFormat, be.compiler,  be.targetInstallPath, str(int(time.time() - startTime))))
  
  sys.stdout.flush()

  return True


def clean(argv):
  '''
    cleans the build for the current project
    
    argv (in): command line arguments
  '''
  try:
    be = BuildElements(argv)
  except Exception as e:
    log.error(str(e))
    return False
  return _clean(be)


def cleanall(argv):
  '''
    cleans the build for the current project and all it's dependencies
    
    argv (in): command line arguments
  '''
  try:
    be = BuildElements(argv)
  except Exception as e:
    log.error(str(e))
    return False
  return _cleanall(be)


#
# private functions
#
def _compileSrc(be, compileCmd, source, objPaths, buildStatus):
  '''
    be (in): BuildElements object
    compileCmd (in): the compile command so far 
    source (in): the c or cpp source file to compile (every source file gets it's own object file)
    objPaths (out): list of all object paths that will be passed to the linker
    buildStatus (out): build status for this particular compile
  '''

  if not os.path.exists(source):
    buildStatus.writeError(source + ' is missing, exiting build')
    return

  objFile = os.path.basename(source)
  objFile = objFile.replace(os.path.splitext(source)[1], be.objExt)
  objPath = os.path.join(be.buildPath, objFile)
  objPaths.append(objPath)
  
  # check if it's up to date
  objExisted = os.path.exists(objPath)
  if objExisted:
    objTimestamp = float(os.stat(objPath).st_mtime)
    if not utils.sourceNeedsBuilding(be.incPaths, source, objTimestamp):
      buildStatus.status = 'up to date'
      return

  # Microsoft Visual C has to have the objPathFlag cuddled up directly next to the objPath - no space in between them (grrr)
  if be.compiler.startswith('msvc'):
    cmd = compileCmd + [source, be.objPathFlag + objPath]
  else:
    cmd = compileCmd + [source, be.objPathFlag, objPath]
  
  if be.showCompilerCmds:
    log.info('\n' + ' '.join(cmd) + '\n')
  
  buildStatus.description = utils.runCmd(cmd)

  if os.path.exists(objPath):
    if objExisted:
      if float(os.stat(objPath).st_mtime) > objTimestamp:
        buildStatus.status = 'built'
    else:
      buildStatus.status = 'built'

  if buildStatus.status == 'built':
    buildStatus.description = 'compiled ' + os.path.basename(source)
    

def _buildLib(be, libSrcDir, buildStatus):
  
  jsonPath = os.path.join(libSrcDir, 'pybythec.json')
  if not os.path.exists(jsonPath):
    jsonPath = os.path.join(libSrcDir, '.pybythec.json')
  if not os.path.exists(jsonPath):
    buildStatus.writeError(libSrcDir + ' does not have a pybythec.json file')
    return
  
  # build
  args = ['', '-d', libSrcDir, '-os', be.osType, '-b', be.buildType, '-c', be.compiler, '-bf', be.binaryFormat]
  
  projectCf = be.cwDir + '/pybythecProject.json'
  projectCfHidden = be.cwDir + '/.pybythecProject.json'
  if os.path.exists(projectCf):
    args += ['-p', projectCf]
  elif os.path.exists(projectCfHidden):
    args += ['-p', projectCfHidden]
  
  build(args)
  
  # read the build status
  buildStatus.readFromFile('{0}/{1}/{2}/{3}/{4}'.format(libSrcDir, be.buildDir, be.buildType, be.compiler, be.binaryFormat))


def _clean(be):
  '''
    cleans the current project
    be (in): BuildElements object
  '''

  # remove any dynamic libs that are sitting next to the exe
  if os.path.exists(be.installPath) and (be.binaryType == 'exe' or be.binaryType == 'plugin'):
    for f in os.listdir(be.installPath):
      libName, ext = os.path.splitext(f)
      if ext == be.dynamicExt:
        if be.compilerRoot == 'gcc' or be.compilerRoot == 'clang':
          libName = libName.lstrip('lib')
        for lib in be.libs:
          if lib == libName:
            os.remove(be.installPath + '/' + f)
      elif ext == '.exp' or ext == '.ilk' or ext == '.lib' or ext == '.pdb': # msvc files
        os.remove(be.installPath + '/' + f)

  if not os.path.exists(be.buildPath): # canary in the coal mine
    log.info('{0} ({1} {2} {3}) already clean'.format(be.target, be.buildType, be.compiler, be.binaryFormat))
    return True
  
  for f in os.listdir(be.buildPath):
    os.remove(be.buildPath + '/' + f)
  os.removedirs(be.buildPath)

  if os.path.exists(be.targetInstallPath):
    os.remove(be.targetInstallPath)
  try:
    os.removedirs(be.installPath)
  except:
    pass

  log.info('{0} ({1} {2} {3}) all clean'.format(be.target, be.buildType, be.compiler, be.binaryFormat))
  return True


def _cleanall(be):
  '''
    cleans both the current project and also the dependencies
    be (input): BuildElements object
  '''
  projArgs = []
  projectCf = be.cwDir + '/pybythecProject.json'
  projectCfHidden = be.cwDir + '/.pybythecProject.json'
  if os.path.exists(projectCf):
    projArgs += ['-p', projectCf]
  elif os.path.exists(projectCfHidden):
    projArgs += ['-p', projectCfHidden]
  
  _clean(be)
  for lib in be.libs:
    for libSrcPath in be.libSrcPaths:
      libPath = os.path.join(libSrcPath, lib)
      if os.path.exists(libPath):
        clean(['', '-d', libPath, '-os', be.osType, '-b', be.buildType, '-c', be.compiler, '-bf', be.binaryFormat] + projArgs)


