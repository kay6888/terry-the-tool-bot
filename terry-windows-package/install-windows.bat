@echo off
REM Terry-the-Tool-Bot Windows Installer

echo 🚀 Installing Terry-the-Tool-Bot on Windows...

REM Create installation directory
if not exist "%USERPROFILE%\\Terry" mkdir "%USERPROFILE%\\Terry"

REM Copy files
xcopy . "%USERPROFILE%\\Terry" /E /Y

REM Add to PATH
setx PATH "%PATH%;%USERPROFILE%\\Terry"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Terry Bot.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\Terry\\terry_gui.py'; $Shortcut.Save()"

REM Install dependencies
python -m pip install -r "%USERPROFILE%\\Terry\\requirements.txt"

echo ✅ Installation complete!
echo Run 'terry' from command line or use desktop shortcut
pause
