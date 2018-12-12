; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Bridgeutil"
#define MyAppVersion "1.0"
#define MyAppExeName "bridgeutil.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{86680C4D-03A6-416F-B26A-E220F6658CB0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=bridgeutil_setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\bridgeutil.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\Asdecoeur.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\python36.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Hubert\Dropbox\bridgetk\hquatreville\build\exe.win32-3.6\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

