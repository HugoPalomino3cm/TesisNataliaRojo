Set WshShell = CreateObject("WScript.Shell")

' Obtener el directorio actual
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Cambiar al directorio del script
WshShell.CurrentDirectory = strPath

' Crear directorios si no existen
Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FolderExists(strPath & "\data\annotations") Then
    fso.CreateFolder(strPath & "\data\annotations")
End If

' Crear archivo de clases predefinidas si no existe
classesFile = strPath & "\data\annotations\predefined_classes.txt"
If Not fso.FileExists(classesFile) Then
    Set objFile = fso.CreateTextFile(classesFile, True)
    objFile.WriteLine "fibra"
    objFile.WriteLine "fragmento"
    objFile.WriteLine "pelicula"
    objFile.WriteLine "esfera"
    objFile.WriteLine "microplastico_irregular"
    objFile.WriteLine "aglomerado"
    objFile.Close
End If

' Ejecutar LabelImg sin mostrar ventana (ventana oculta = 0)
imagesDir = strPath & "\data\raw_images"
annotationsDir = strPath & "\data\annotations"

' Intentar con pythonw primero (sin ventana de consola)
On Error Resume Next
WshShell.Run "pythonw -m labelImg """ & imagesDir & """ """ & classesFile & """ """ & annotationsDir & """", 0, False

' Si falla, intentar con python normal
If Err.Number <> 0 Then
    Err.Clear
    WshShell.Run "python -m labelImg """ & imagesDir & """ """ & classesFile & """ """ & annotationsDir & """", 0, False
End If
