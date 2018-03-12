@ECHO OFF
REM ==========================================
REM 目标：对多APK签名(批处理)
REM 作者：M-Liu
REM 时间：2017-11-14
REM 邮箱：ms_liu163@163.com
REM ==========================================

REM 开启 延迟环境变量扩展
SETLOCAL ENABLEDELAYEDEXPANSION
ECHO START ANDROID SIGNED BAT
REM 签名文件秘钥
SET KEYSTORE_PATH=..\pengyousigned.jks
REM 别名
SET KEYSTORE_ALIAS=pengyou
REM 密码
SET KEYSTORE_PWD=hf666888
REM 存放APK文件夹位置
SET APK_FOLDER=..\apks
FOR %%i IN (!APK_FOLDER!\*.apk)DO (
    set sourceFile=%%i
    set targetFile=!sourceFile:.apk=_signed.apk!
    set targetFile=!targetFile:apks=signedapks!
    REM 启动签名文件(可以启动多个，开启"多线程")
    start /b signed.bat !KEYSTORE_PATH! !targetFile! !sourceFile! !KEYSTORE_ALIAS! !KEYSTORE_PWD!
    REM 启动签名命令
    REM JARSIGNER -VERBOSE -KEYSTORE !KEYSTORE_PATH! -SIGNEDJAR !targetFile!  !sourceFile! !KEYSTORE_ALIAS! -STOREPASS !KEYSTORE_PWD!
)
REM TODO是否需要删除源文件---->因为"异步"所以这里存在问题
REM if %1 == True(del /s /f /q apks\*.apk)
REM ECHO END ANDROID SIGNED BAT
@ECHO ON
