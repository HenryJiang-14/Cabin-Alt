@echo off
chcp 65001 >nul
echo ========================================
echo   Clean Build Cache
echo ========================================
echo.

cd /d "%~dp0APK"

echo 正在清理构建缓存...
if exist ".buildozer" (
    echo - 删除 .buildozer 目录
    rmdir /s /q ".buildozer"
)

if exist "bin" (
    echo - 删除 bin 目录
    rmdir /s /q "bin"
)

echo.
echo 清理完成！可以重新构建了
echo ========================================
