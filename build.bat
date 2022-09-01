@echo off
py -m PyInstaller main.py --onefile --noconfirm --icon icon.ico -n WalletGuard
echo Build complete, press any key to exit
pause >nul
exit