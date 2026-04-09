@echo off
chcp 65001 >nul
echo ========================================
echo   APK Build Script for Cabin Altitude
echo ========================================
echo.

REM 检查 WSL 是否安装
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] WSL 未安装或未启用
    echo.
    echo 请先执行以下命令安装 WSL:
    echo   wsl --install -d Ubuntu-22.04
    echo.
    echo 安装后重启电脑，然后再次运行此脚本
    pause
    exit /b 1
)

echo [1/3] 检查 WSL 环境...
wsl bash -c "which buildozer" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 首次使用，正在安装依赖...
    echo 这可能需要较长时间（下载 Android SDK/NDK）
    echo.
    
    wsl bash -c "sudo apt update && sudo apt install -y python3-pip openjdk-17-jdk zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev"
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    
    wsl bash -c "pip3 install buildozer cython"
    if %errorlevel% neq 0 (
        echo [错误] Buildozer 安装失败
        pause
        exit /b 1
    )
    
    echo [完成] 环境安装成功
    echo.
)

echo [2/3] 开始构建 APK...
echo 这可能需要 10-30 分钟（首次构建需要下载大量文件）
echo.

REM 进入 APK 目录并执行构建
cd /d "%~dp0APK"
set CURRENT_DIR=%CD%
set WSL_PATH=/mnt/%CURRENT_DIR:~0,1%%CURRENT_DIR:~2%
set WSL_PATH=%WSL_PATH:\=/%

wsl bash -c "cd %WSL_PATH% && buildozer android debug"

if %errorlevel% neq 0 (
    echo.
    echo [错误] 构建失败，请检查上方错误信息
    pause
    exit /b 1
)

echo.
echo [3/3] 构建完成！
echo.
echo APK 文件位置:
dir /b "%~dp0APK\bin\*.apk" 2>nul
echo.
echo APK 已生成在 APK\bin\ 目录下
echo ========================================
