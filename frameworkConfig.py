
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pbxproj import *
from pbxproj.pbxextensions import *
import time

class FrameworkConfig:

    def addFramework(self,XcodeProject,projectPath,project,areaType):

        print "addFramework"

        project.add_file("System/Library/Frameworks/WebKit.framework",tree='SDKROOT',force=False)
        project.add_file("System/Library/Frameworks/JavaScriptCore.framework",tree='SDKROOT',force=False)
    
        if areaType == "Mainland":
            
            project.add_file("System/Library/Frameworks/Security.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/SystemConfiguration.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBook.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/CoreTelephony.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBookUI.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ImageIO.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++abi.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.tbd",tree='SDKROOT',force=False)
            project.save()

        if areaType == "Korea":
        
            # project.add_file("System/Library/Frameworks/CoreSpotlight.framework",tree='SDKROOT',force=False)
            # project.add_file("System/Library/Frameworks/ReplayKit.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBook.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBookUI.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ImageIO.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++abi.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.save()


        if areaType == "Taiwan":
        
            # project.add_file("System/Library/Frameworks/CoreSpotlight.framework",tree='SDKROOT',force=False)
            # project.add_file("System/Library/Frameworks/ReplayKit.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBook.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBookUI.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ImageIO.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++abi.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.save()
            projectNew = XcodeProject.load(projectPath)

        if areaType == "Southeast":
            
            project.add_file("System/Library/Frameworks/CoreSpotlight.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ReplayKit.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBook.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBookUI.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ImageIO.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++abi.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.save()
            projectNew = XcodeProject.load(projectPath)
            setWeak(projectNew,"CoreSpotlight.framework")
            setWeak(projectNew,"ReplayKit.framework")
            projectNew.save()

        if areaType == "Russian":
            
            # project.add_file("System/Library/Frameworks/CoreSpotlight.framework",tree='SDKROOT',force=False)
            # project.add_file("System/Library/Frameworks/ReplayKit.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBook.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBookUI.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ImageIO.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++abi.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.save()

        if areaType == "Vietnam":
        
            # project.add_file("System/Library/Frameworks/CoreSpotlight.framework",tree='SDKROOT',force=False)
            # project.add_file("System/Library/Frameworks/ReplayKit.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBook.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AddressBookUI.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/ImageIO.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++abi.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.save()

        if  areaType == "NorthAmerica":

            project.add_file("System/Library/Frameworks/CoreTelephony.framework",tree='SDKROOT',force=False)
            # project.add_file("System/Library/Frameworks/Messages.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/MessageUI.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/EventKit.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/EventKitUI.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/MobileCoreServices.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/CoreData.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libz.1.2.5.tbd",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AdSupport.framework",tree='SDKROOT',force=False)
            project.add_file("System/Library/Frameworks/AssetsLibrary.framework",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libc++.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.0.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libstdc++.6.0.9.tbd",tree='SDKROOT',force=False)
            project.add_file("usr/lib/libsqlite3.tbd",tree='SDKROOT',force=False)
            project.save()

def setWeak(project,framework):
        
    items = project.objects.get_objects_in_section(u'PBXBuildFile')
                
    for item in items:
                    
        setting = item._get_comment()

        if  setting.encode('utf8').find(framework) != -1:

            item.add_attributes(u'Weak')





