#!/usr/bin/env python3
"""
Build Script for Mouse Gesture Control Installer
===============================================
Creates a Windows installer package using PyInstaller and NSIS.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required tools are installed."""
    print("Checking dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("SUCCESS: PyInstaller found")
    except ImportError:
        print("ERROR: PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check if NSIS is available
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe",
        r"C:\NSIS\makensis.exe"
    ]
    
    nsis_found = False
    for path in nsis_paths:
        if os.path.exists(path):
            print(f"SUCCESS: NSIS found at {path}")
            nsis_found = True
            break
    
    if not nsis_found:
        print("WARNING: NSIS not found. Please install NSIS from https://nsis.sourceforge.io/")
        print("   After installing NSIS, run this script again.")
        return False
    
    return True

def create_spec_file():
    """Create PyInstaller spec file."""
    print("Creating PyInstaller spec file...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main_gui.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('README.md', '.'),
        ('src/gesture_controller.py', 'src'),
        ('src/input_listener.py', 'src'),
        ('src/actions.py', 'src'),
    ],
    hiddenimports=[
        'pystray',
        'PIL',
        'tkinter',
        'pynput',
        'keyboard',
        'psutil',
        'gesture_controller',
        'input_listener',
        'actions'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MouseGestureControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'
)
'''
    
    with open('MouseGestureControl.spec', 'w') as f:
        f.write(spec_content)
    
    print("SUCCESS: Spec file created")

def create_icon():
    """Create application icon."""
    print("Creating application icon...")
    
    # Create assets directory
    os.makedirs('assets', exist_ok=True)
    
    # Create a simple icon using PIL
    try:
        from PIL import Image, ImageDraw
        
        # Create a 64x64 icon
        size = 64
        image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw mouse icon
        draw.ellipse([8, 8, 56, 56], fill=(0, 0, 0, 255), outline=(128, 128, 128, 255), width=2)
        draw.ellipse([16, 16, 48, 48], fill=(255, 255, 255, 255))
        
        # Save as ICO
        image.save('assets/icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        print("SUCCESS: Icon created")
        
    except ImportError:
        print("WARNING: PIL not available, skipping icon creation")
        # Create a placeholder
        with open('assets/icon.ico', 'w') as f:
            f.write('')

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Run PyInstaller
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "MouseGestureControl.spec"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("SUCCESS: Executable built successfully")
        return True
    else:
        print(f"ERROR: Build failed: {result.stderr}")
        return False

def create_nsis_script():
    """Create NSIS installer script."""
    print("Creating NSIS installer script...")
    
    nsis_script = '''!define APPNAME "Mouse Gesture Control"
!define COMPANYNAME "MouseGestureControl"
!define DESCRIPTION "Mouse gesture control for Windows desktop navigation"
!define VERSIONMAJOR 2
!define VERSIONMINOR 1
!define VERSIONBUILD 0
!define HELPURL "https://github.com/yourusername/MouseGestureControl"
!define UPDATEURL "https://github.com/yourusername/MouseGestureControl"
!define ABOUTURL "https://github.com/yourusername/MouseGestureControl"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${APPNAME}"
Name "${APPNAME}"
outFile "MouseGestureControl_Setup.exe"

!include LogicLib.nsh

page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    file "dist\\MouseGestureControl.exe"
    file "config.json"
    file "README.md"
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    createDirectory "$SMPROGRAMS\\${APPNAME}"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\MouseGestureControl.exe"
    createShortCut "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    # Add to startup (auto-detects startup mode)
    WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "MouseGestureControl" "$INSTDIR\\MouseGestureControl.exe"
    
    # Registry information for add/remove programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "uninstall"
    delete "$INSTDIR\\MouseGestureControl.exe"
    delete "$INSTDIR\\config.json"
    delete "$INSTDIR\\README.md"
    delete "$INSTDIR\\uninstall.exe"
    
    rmDir "$INSTDIR"
    
    delete "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk"
    delete "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk"
    rmDir "$SMPROGRAMS\\${APPNAME}"
    
    # Remove from startup
    DeleteRegValue HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "MouseGestureControl"
    
    # Remove uninstaller information from the registry
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"
sectionEnd
'''
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    print("SUCCESS: NSIS script created")

def build_installer():
    """Build the final installer."""
    print("Building installer...")
    
    # Find NSIS
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe",
        r"C:\NSIS\makensis.exe"
    ]
    
    nsis_exe = None
    for path in nsis_paths:
        if os.path.exists(path):
            nsis_exe = path
            break
    
    if not nsis_exe:
        print("ERROR: NSIS not found!")
        return False
    
    # Run NSIS
    cmd = [nsis_exe, "installer.nsi"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("SUCCESS: Installer built successfully: MouseGestureControl_Setup.exe")
        print("The installer will:")
        print("  - Install the application to Program Files")
        print("  - Add to Windows startup (minimized to tray)")
        print("  - Create desktop shortcuts")
        print("  - Add uninstaller to Add/Remove Programs")
        return True
    else:
        print(f"ERROR: Installer build failed: {result.stderr}")
        return False

def main():
    """Main build process."""
    print("Mouse Gesture Control - Installer Builder")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create icon
    create_icon()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        return
    
    # Create NSIS script
    create_nsis_script()
    
    # Build installer
    if build_installer():
        print("\nSUCCESS: Build completed successfully!")
        print("Installer: MouseGestureControl_Setup.exe")
        print("Users can now download and install the application.")
    else:
        print("\nERROR: Build failed!")

if __name__ == "__main__":
    main()
