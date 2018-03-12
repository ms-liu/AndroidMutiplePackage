import shutil
import zipfile
import os
import time
import sys
import subprocess
import io
import math

# App版本号
appVersion = "353"
# appName = "pengyou_for_360_publish"
# appName = "pengyou_for_pp_publish"
# appName = "pengyou_fix_bug"
# appName = "pengyou_with_suffix"
# APP名称
appName = "pengyou"

# srcFileName = "v352/app-pengyou_360_352_jiagu_sign.apk"
# srcFileName = "v352/app-pengyou_pp_352_jiagu_sign.apk"
# srcFileName = "v352/app-pengyou_352_jiagu_sign.apk"
# 源文件
srcFileName = "v353/app-release_353_jiagu_sign.apk"
destDir = os.path.abspath('.')

# 渠道配置文件
channelConfig = "channels.py"
# 空文件
emptyHolderFile = "pyChannel_holder"

# 签名文件
signedFileName = "pengyousigned.jks"
# 签名别名
signedAliasName = "pengyou"
# 签名密码
signedPWD = "hf666888"
# 多渠道未签名存放文件夹
sourcePath = 'apks'
# 多渠道签名后存放文件夹
signedPath = 'signedapks'


class PackageTools(object):
    # 打包
    def package(self, channel):
        # print(channel+time.clock())
        # 最终目标文件名称
        targetFile = "{appName}_{appVersion}_{channelName}.apk".format(appName=appName, channelName=channel,
                                                                       appVersion=appVersion)
        noSignedApk = self.copy_apk(srcFileName, targetFile)
        apkZip = zipfile.ZipFile(noSignedApk, 'a', zipfile.ZIP_DEFLATED)
        emptyChannelFile = "META-INF/pyChannel_{channelName}".format(channelName=channel)
        apkZip.write(emptyHolderFile, emptyChannelFile)
        apkZip.close()

    def get_time(self):
        return str(time.time())

    # 复制Apk，并返回复制后APK路径
    def copy_apk(self, srcFile, cp_name):
        dest_path = os.path.join('apks', cp_name)
        if os.path.exists(srcFile) and not os.path.exists(dest_path):
            return shutil.copy(srcFile, dest_path)
        return dest_path

    def remoe_files(self, path):
        for file in os.listdir(path):
            filePath = os.path.join(path, file)
            if os.path.isfile(filePath):
                os.remove(filePath)


class Loger(object):
    def log(self, info):
        print('>>>>:%s' % info)

    def log2(self, info):
        print(info)


# 定义程序入口
if __name__ == '__main__':
    loger = Loger()
    loger.log('MULTIPLE APK FOR CHANNEL')
    # 创建PackageTools对象
    package = PackageTools()
    # print(count(os.listdir(sourcePath)))
    package.remoe_files(sourcePath)
    package.remoe_files(signedPath)

    # 读取渠道配置文件信息
    loger.log('START CREATE')
    channels = open(channelConfig)
    # 遍历内容
    countChannel = 0
    for line in channels:
        # 获取每一行内容
        channel = line.strip("\n").strip()
        # 判断是否#开头，意味着注释的，不需要生成对应的渠道包
        if not channel.startswith("#"):
            countChannel += 1
            package.package(channel)
    loger.log('END CREATE')

    # 签名
    loger.log('START SIGNED')
    loger.log('You need close command window when the commands have been finished')
    p = subprocess.Popen("cd bat&start  AndroidApkSigned.bat", shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    curline = p.stdout.readline()
    while (curline != b''):
        curline = p.stdout.readline()
    p.wait()
    if p.returncode == 0:
        p.kill()
        loger.log('END SIGNED')
        # 添加压缩包
        loger.log('START ZIP')

        targetZipPath = '{appName}_multiple_chanel_v{appVersion}_apk.zip'.format(appName=appName, appVersion=appVersion)
        zipPackage = zipfile.ZipFile(file=targetZipPath, mode='a', compression=zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk('signedapks'):
            countFile = 0
            for filename in filenames:
                countFile += 1
                loger.log('%s%s%s' % ('PROGRESS：', (math.ceil(countFile / countChannel * 100)), '%'))
                zipPackage.write(os.path.join(dirpath, filename))
        loger.log('END ZIP')
    loger.log('MULTIPLE APK FOR CHANNEL')
