#!/bin/bash  
#需要在工程下 bundleSetting中的Code Signing Resource Rules Path 添加 $(SDKROOT)/ResourceRules.plist
#参数判断  
if [ $# != 3 ];then  
    echo "Params error!"  
    echo "Need four params: 1.path of project 2.name of ipa file 3.target 4.certification 5. profile"  
    exit  
elif [ ! -d $1 ];then  
    echo "The first param is not a dictionary."  
    exit      
fi
      
      
#工程路径  
project_path=$1

project_name=$2

#IPA名称  
ipa_path=$3

mkdir ${ipa_path}

#xcode工程名
target="Unity-iPhone"

      
#build文件夹路径  
build_path=${project_path}/build  

      
#编译工程  
echo $target  
cd $project_path  
# xcodebuild clean -target ${target} -configuration Distribution 
xcodebuild -target ${target} -configuration Distribution || exit
      
#打包  
cd $build_path  
if [ -d ./ipa ];then  
    rm -rf ipa  
fi  
echo $build_path

xcrun -sdk iphoneos PackageApplication -v $build_path/Release-iphoneos/*.app -o ${project_path}/Unity-iPhone.ipa

mv -f ${project_path}/Unity-iPhone.ipa ${ipa_path}

