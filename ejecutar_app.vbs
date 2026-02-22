Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener el directorio del script
strPath = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath

' Ejecutar sin mostrar ventana
WshShell.Run "venv_py311\Scripts\pythonw.exe main.py", 0, False
