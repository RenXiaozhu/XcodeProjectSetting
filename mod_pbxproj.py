
# make sure the arcFile is in your workSpace root dict

#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pbxproj import *
from pbxproj.pbxextensions import *
from frameworkConfig import *
import time
import os
import sys
import shutil

copyFileCounts = 0
def copyFiles(sourceDir, targetDir):
    global copyFileCounts
    print sourceDir
    print u"%s now work %s already copy %s count file" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), sourceDir,copyFileCounts)
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        
        if os.path.isfile(sourceF):
            #creat dir
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            copyFileCounts += 1
            
            #file not exist
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                #2 data
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print u"%s %s copy successful" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), targetF)
            else:
                print u"%s %s already exist" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), targetF)
        
        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)


# onlyCodeSign = True False
# codeSignType = "inhouse", "dist", "dev", "adhoc"

def modifyBundleVersion(newBundleVersion,projectPath):
    os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleShortVersionString %s" %s' %(newBundleVersion,projectPath+'/Info.plist'))
    os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleVersion %s" %s' %(newBundleVersion,projectPath+'/Info.plist'))

def modifyBundleID(bundleid,projectPath):
    os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleIdentifier %s" %s' %(bundleid,projectPath+'/Info.plist'))
    print "editor"+projectPath+'/Info.plist' + bundleid

def setConfigFlag( config, codeSignIdentity, areaMacro, profile, profile_specifier, bundleid, teamid, infoPath):
    
    buildSetting = config.buildSettings
    
    prefixHeader = buildSetting.__getitem__("GCC_PREFIX_HEADER")
    
    if prefixHeader == "Classes/Prefix.pch":
        
        config.add_flags("GCC_PREPROCESSOR_DEFINITIONS",areaMacro)

        if areaMacro == "SOUTHEAST=1":
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TRIDENT_INGAMENOTICE")
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TRIDENT_GPG_AUTH")
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TRIDENT_PUSH")
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TRIDENT_GROWTHY")
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TridentAppController=1")
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TridentPush=1")
        	config.add_flags("GCC_PREPROCESSOR_DEFINITIONS","USE_TRIDENT_GRAPH")

    
    config.set_flags("CODE_SIGN_IDENTITY",codeSignIdentity)

    config.set_flags("CODE_SIGN_IDENTITY[sdk=iphoneos*]",codeSignIdentity)

    config.set_flags("PROVISIONING_PROFILE",profile)
    
    config.set_flags("PROVISIONING_PROFILE_SPECIFIER",profile_specifier)
    
    config.set_flags("SDKROOT","iphoneos")
    
    config.set_flags("PRODUCT_BUNDLE_IDENTIFIER",bundleid)
    
    config.set_flags("DEVELOPMENT_TEAM",teamid)
    
    config.set_flags("ENABLE_BITCODE","NO")

    config.set_flags("CODE_SIGN_STYLE",u'Manual')
    
    modifyBundleID(bundleid,infoPath)

def setProject( project,pbxprojects, codeSignType , teamid):
    
    target = project.get_target_by_name(u'Unity-iPhone')
    
    for pbxproject in pbxprojects:
        
            if codeSignType == "inhouse":
            
                print("already into inhouse")
                
                pbxproject.set_provisioning_style(u'Manual',target)
                
                pbxproject.set_developmentTeam_name(u'T3PMSUWAJ2',target)
        
            else:
                
                pbxproject.set_provisioning_style(u'Manual',target)
                
                pbxproject.set_developmentTeam_name(teamid,target)


def modify(onlyCodeSign, codeSignType, path, areaType, packDir, gameID ,bundleVersion):

    reload(sys)
    sys.setdefaultencoding('utf-8')

    projectPath = path + "/Unity-iPhone.xcodeproj/project.pbxproj"
    
    print(projectPath)
    print(areaType)
    print(codeSignType)
    
    project = XcodeProject.load(projectPath)
    
    if onlyCodeSign == False:

        targetDir = path
        commonDir = packDir + "/Channel/Common/IOS/"
        uniqueDir = packDir + "/Channel/" + areaType + "/" + gameID + "/UnitySDK"
        imageDir  = packDir + "/Channel/" + areaType + "/" + gameID + "/Images.xcassets"

        copyFiles(commonDir, targetDir)
        copyFiles(uniqueDir, targetDir)
        
        # add files to project
        # add a file to it, force=false to not add it if it's already in the project
        #project.add_file('MyClass.swift', force=False)
        # os.chdir(path)
        
        # os.system('mv -f SDKs/SDKConnector/UnityAppController.mm Classes/')
        # os.system('mv -f SDKs/SDKConnector/UnityView.mm Classes/UI/')
        if os.path.exists(path + '/SDKs/SDKConnector/UnityAppController.mm'):
            shutil.copy(path + '/SDKs/SDKConnector/UnityAppController.mm', path + '/Classes/UnityAppController.mm')
        if os.path.exists(path + '/SDKs/SDKConnector/UnityView.mm'):
            shutil.copy(path + '/SDKs/SDKConnector/UnityView.mm', path + '/Classes/UI/UnityView.mm')
        if os.path.exists(imageDir):
            # shutil.copy(imageDir, path + '/Unity-iPhone')
            os.system('cp -R %s %s' %(imageDir, path + '/Unity-iPhone'))
        print "copy Images.xcassets"

        # file_options = FileOptions(weak=True)

        project.add_library_search_paths("$(SRCROOT)/Libraries")
        project.add_folder(targetDir+"/UnitySDK", excludes=["^.*\.DS_Store$"], recursive=True)
        project.add_folder(targetDir+"/SDKs", excludes=["^.*\.DS_Store$"], recursive=True)
        
        
        infoPlistPath = packDir + "/Channel/" + areaType +"/"+gameID+ "/infoplist/" +"Info.plist"

        shutil.copy(infoPlistPath, path + '/Info.plist')

        if codeSignType == "inhouse":

            os.system('/usr/libexec/PlistBuddy -c "Add :UIFileSharingEnabled bool true" %s' %(path+'/Info.plist'))
            print "Add config UIFileSharingEnabled"
            
        else:

            os.system('/usr/libexec/PlistBuddy -c "Delete :UIFileSharingEnabled" %s' %(path+'/Info.plist'))
            print "delete config UIFileSharingEnabled"


        frameworkconfig = FrameworkConfig()

        frameworkconfig.addFramework(XcodeProject,projectPath,project,areaType)

        projectNew = XcodeProject.load(projectPath)

        # AutoReference
        
        if areaType == "Southeast":


            arcPath = packDir + "/Channel/" + areaType + "/" + gameID +"/noArcFile.txt"
            
            f = open(arcPath,"r")
            
            lines = f.readlines()
            
            f.close()
            
            items = projectNew.objects.get_objects_in_section(u'PBXBuildFile')
            
            for item in items:
                
                setting = item._get_comment()

                if setting.encode('utf8').find(".mm") != -1:
                    
                    for line in lines:
                        
                        line = line.strip('\n')
                        
                        if setting.encode('utf8').find(line) != -1: 
                            
                            print("add file"+ line + "noARC")
                            
                            item.add_compiler_flags('-fno-objc-arc')

    # Macros Define
    
    if areaType == "Mainland" or areaType == "IOS_INTRANET_PUBLISH":
        
        print("already into mainland")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'3U574YMU7D')
        
        
        for config in configs:
            
            if codeSignType == "inhouse":
                
                setConfigFlag(config, "iPhone Distribution: xxx", "MAINLAND=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "xxxxxx", u'com.xxx.xxx', u'xxxxx', path)
        
# save the project, otherwise your changes won't be picked up by Xcode

    modifyBundleVersion(bundleVersion,path)
    
    projectNew.save()
    
    print ("save")

if __name__ == "__main__":
    onlyCodeSign = sys.argv[1] 
    codeSignType = sys.argv[2]
    path = sys.argv[3] 
    areaType = sys.argv[4]
    packDir = sys.argv[5]
    gameID = sys.argv[6]
    bundleVersion = sys.argv[7] 
    modify(onlyCodeSign, codeSignType, path, areaType, packDir, gameID, bundleVersion)
