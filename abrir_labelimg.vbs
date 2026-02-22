Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener el directorio del script
strPath = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath

' Ejecutar con pythonw (sin ventana de consola), 0 = oculto, False = no esperar
WshShell.Run "venv_py311\Scripts\pythonw.exe launch_labelimg.py", 0, False
