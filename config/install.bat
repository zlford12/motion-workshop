pyinstaller MotionWorkshop.py -w -i "config/icon.png" --noconfirm
xcopy "./config" "./dist/MotionWorkshop/config\" /s /y