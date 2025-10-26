
@echo off
setlocal enabledelayedexpansion
>nul chcp 65001
where pyside6-uic >nul 2>nul || (
    echo ❶ pyside6-uic 不在 PATH 里
    exit /b 1
)
where pyside6-rcc >nul 2>nul || (
    echo ❷ pyside6-rcc 不在 PATH 里
    exit /b 1
)

echo ====== 开始转换 .ui 文件 ======

:: ======  .ui → Ui_xxx.py  ======
set "ui_count=0"
for /r "." %%f in (*.ui) do (
    set /a ui_count+=1
    set "ui_file=%%f"
    set "py_file=%%~dpfUi_%%~nf.py"

    echo.
    echo [!ui_count!] 正在转换 UI 文件:
    echo     源文件: !ui_file!
    echo     目标文件: !py_file!

    pyside6-uic "!ui_file!" -o "!py_file!" -g python
    if !errorlevel! equ 0 (
        echo     ✅ 转换成功
    ) else (
        echo     ❌ 转换失败
    )
)

echo.
echo ====== 开始转换 .qrc 文件 ======

:: ======  .qrc → xxx_rc.py  ======
set "qrc_count=0"
for /r "." %%f in (*.qrc) do (
    set /a qrc_count+=1
    set "qrc_file=%%f"
    set "rc_py_file=%%~dpf%%~nf_rc.py"

    echo.
    echo [!qrc_count!] 正在转换资源文件:
    echo     源文件: !qrc_file!
    echo     目标文件: !rc_py_file!

    pyside6-rcc "!qrc_file!" -o "!rc_py_file!" -g python
    if !errorlevel! equ 0 (
        echo     ✅ 转换成功
    ) else (
        echo     ❌ 转换失败
    )
)

echo.
echo 转换完成统计:
echo   UI 文件转换: %ui_count% 个
echo.
echo   资源文件转换: %qrc_count% 个
echo.