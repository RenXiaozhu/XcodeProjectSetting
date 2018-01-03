
# make sure the arcFile is in your workSpace root dict
# use this script like python mod_pbxproj.py onlyCodeSign(yes/no) codeSignType(inhouse/dev/dist/adhoc) path/to/JYMF
#("Enter areaType Mainland:1 Taiwan:2 Korea:3 Southeast:4 Russian:5: Vietnam:6")

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
                
                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "MAINLAND=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "UE_InHouse_1", u'com.Company.SMTest', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":
                
                setConfigFlag(config, "iPhone Distribution: chong li (3U574YMU7D)", "MAINLAND=1", "db8d90e4-ccdc-4991-9132-a599c7eb4ee2", "jymf_adhoc_20171011", u'com.longtugame.jymf', u'3U574YMU7D', path)
            
            if codeSignType == "dev":
                
                setProject(projectNew,pbxprojects, codeSignType, u'HL2ME966K8')
                setConfigFlag(config, "iPhone Developer: chong li (HL2ME966K8)", "MAINLAND=1", "71b8dc99-4bbd-4e77-abe3-584daec01ccd", "jymf_dev_20171011", u'com.longtugame.jymf', u'3U574YMU7D', path)

            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution: chong li (3U574YMU7D)", "MAINLAND=1", "c1f83049-7ab0-4caf-b6cf-addd34e16759", "jymf_dist_20171011", u'com.longtugame.jymf', u'3U574YMU7D', path)

    if areaType == "Korea":
    
        print("already into korea")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'W75Z9VU8C8')
        
        for config in configs:
            
            if codeSignType == "inhouse":
                
                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "KOREA=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "UE_InHouse_1", u'com.Company.SMTest', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":
                
                setConfigFlag(config, "iPhone Distribution: LONGTU KOREA Inc. (W75Z9VU8C8)", "KOREA=1", "5b766b73-e47d-4036-807a-98b86f3dc5f7", "SNM Ad Hoc_0925", u'com.longtukorea.snm', u'W75Z9VU8C8', path)
            
            if codeSignType == "dev":
                
                setConfigFlag(config, "iPhone Developer: Jaegeun Oh (3WM9RVG3NZ)", "KOREA=1", "94c070d0-a250-4bc0-a607-0edc103c88d0", "SNM Dev_0925", u'com.longtukorea.snm', u'W75Z9VU8C8', path)
            
            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution: LONGTU KOREA Inc. (W75Z9VU8C8)", "KOREA=1", "a6686b44-2a97-4360-b82f-36d7f9baaf8f", "SNM Dist_0925", u'com.longtukorea.snm', u'W75Z9VU8C8', path)


    if areaType == "Taiwan":
    
        print("already into taiwan")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'6LNWXZNR47')
        
        for config in configs:
            
            if codeSignType == "inhouse":
                
                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "TAIWAN=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "UE_InHouse_1", u'com.Company.SMTest', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":
                
                setConfigFlag(config, "iPhone Distribution: Funapps TW Co., Ltd (6LNWXZNR47)", "TAIWAN=1", "8a700f45-e609-42fe-a982-66e914260050", "jianmo_adhoc_20170929", u'com.funapps.tw.sm', u'6LNWXZNR47', path)
            
            if codeSignType == "dev":
                
                setConfigFlag(config, "iPhone Developer", "TAIWAN=1", "9b22acd5-125e-482f-8a98-651f9f68cef6", "jianmo_dev_20170929", u'com.funapps.tw.sm', u'6LNWXZNR47', path)
            
            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution: Funapps TW Co., Ltd (6LNWXZNR47)", "TAIWAN=1", "8baed28d-4ace-486d-b152-59c9e1e35f11", "jianmo_dist_20170925", u'com.funapps.tw.sm', u'6LNWXZNR47', path)


    if areaType == "Southeast":
    
        print("already into Southeast")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'VUTU7AKEUR')
        
        for config in configs:
            
            config.set_flags("CLANG_ENABLE_OBJC_ARC",u'YES')

            config.add_flags(u'OTHER_LDFLAGS',u'-ObjC')

            config.set_flags("CODE_SIGN_ENTITLEMENTS",u'UnitySDK/TridentUnity/iOS/Trident.entitlements')
            
            if codeSignType == "inhouse":

                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "SOUTHEAST=1", "4d076c45-b8f3-4c91-b595-de7286cde780", "iOS: com.linecorp.LGSAMTH", u'com.linecorp.LGSAMTHUE', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":

                setConfigFlag(config, "iPhone Distribution: LINE Corporation (VUTU7AKEUR)", "SOUTHEAST=1", "a8dfa91e-d80f-4d3e-8baa-674f9db28643", "LGSAMTH Push Ad Hoc", u'com.linecorp.LGSAMTH', u'VUTU7AKEUR', path)
            
            if codeSignType == "dev":
                
                print("************  there is no dev profile ***************")
            #setConfigFlag(config, "iPhone Developer", "SOUTHEAST=1", "76b76cc1-9cbe-4b15-9bc8-10639c9b493e", "LGSAMTH Push Ad Hoc", u'com.linecorp.LGSAMTH', u'VUTU7AKEUR', path)
            
            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution: LINE Corporation (VUTU7AKEUR)", "SOUTHEAST=1", "3b82b111-e795-4a13-b730-c1dece823408", "LGSAMTH Push App Store", u'com.linecorp.LGSAMTH', u'VUTU7AKEUR', path)


    if areaType == "Russian":
    
        print("already into Russian")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'3U574YMU7D')
        
        for config in configs:

            if codeSignType == "inhouse":
                
                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "SOUTHEAST=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "UE_InHouse_1", u'com.Company.SMTest', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":
                
                setConfigFlag(config, "iPhone Distribution", "SOUTHEAST=1", "78bb3f3a-2011-4d3b-a6c4-adf6b0e2dcde", "jianmo_adhoc_20161002", u'com.fungame.jymf', u'3U574YMU7D', path)
            
            if codeSignType == "dev":
                
                setConfigFlag(config, "iPhone Developer", "SOUTHEAST=1", "76b76cc1-9cbe-4b15-9bc8-10639c9b493e", "jianmo_dev_20161002", u'com.fungame.jymf', u'3U574YMU7D', path)
            
            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution", "SOUTHEAST=1", "c5ca709e-cbaa-4ed7-94eb-35074ab77417", "jianmo_dist_20161002", u'com.fungame.jymf', u'3U574YMU7D', path)

    if areaType == "Vietnam":
    
        print("already into Vietnam")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'9UMYM473QR')
        
        for config in configs:
            
            if codeSignType == "inhouse":
                
                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "VIETNAM=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "UE_InHouse_1", u'com.Company.SMTest', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":
                
                print("there is no adhoc profile")
            
            #setConfigFlag(config, "iPhone Distribution", "VIETNAM=1", "4b1b4031-8928-4e64-9d22-154cf23f0988", "jianmo_adhoc_20161002", u'com.fungame.jymf', u'9UMYM473QR', path)
            
            if codeSignType == "dev":
                
                setConfigFlag(config, "iPhone Developer", "VIETNAM=1", "bf795404-c1f8-466f-801e-955485cd23aa", "sm_dev", u'com.veamobile.sm', u'9UMYM473QR', path)
            
            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution", "VIETNAM=1", "3fb5009d-fc94-4d70-8f42-2418fafee575", "sm_dis", u'com.veamobile.sm', u'9UMYM473QR', path)


    if  areaType == "NorthAmerica":

        print("already into NorthAmerica")
        
        configs = projectNew.objects.get_objects_in_section(u'XCBuildConfiguration')
        
        pbxprojects = projectNew.objects.get_objects_in_section(u'PBXProject')
        
        setProject(projectNew,pbxprojects, codeSignType, u'9UMYM473QR')
        
        for config in configs:
            
            config.add_flags(u'OTHER_LDFLAGS',u'-ObjC')
            
            if codeSignType == "inhouse":
                
                setConfigFlag(config, "iPhone Distribution: UEgame Co., Ltd.", "NORTHAMERICA=1", "e1c643df-e5f6-44a8-9c0f-65a381052180", "UE_InHouse_1", u'com.Company.SMTest', u'T3PMSUWAJ2', path)
        
            if codeSignType == "adhoc":
            
                setConfigFlag(config, "iPhone Distribution: G-MEI NETWORK TECHNOLOGY CO LIMITED (YG56WXQ497)", "NORTHAMERICA=1", "a98468b4-2979-4458-8809-813065189d95", "adhoc_eoa_20171012", u'com.games37.eoa.ios', u'YG56WXQ497', path)
            
            if codeSignType == "dev":
                
                setConfigFlag(config, "iPhone Developer: guizhi Chen (YVD883CFJ8)", "NORTHAMERICA=1", "1d213ff5-4047-4151-b592-0c279a040bcc", "dev_eoa_20171012", u'com.games37.eoa.ios', u'YG56WXQ497', path)
            
            if codeSignType == "dist":
                
                setConfigFlag(config, "iPhone Distribution: G-MEI NETWORK TECHNOLOGY CO LIMITED (YG56WXQ497)", "NORTHAMERICA=1", "aa7f68cd-3b33-483a-94ce-0d403e215e62", "appstore_eoa_20171011", u'com.games37.eoa.ios', u'YG56WXQ497', path)

    

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
