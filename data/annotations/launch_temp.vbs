Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c labelImg ""c:\Users\xg645\Downloads\TesisNataliaRojo\data\raw_images"" ""c:\Users\xg645\Downloads\TesisNataliaRojo\data\annotations\predefined_classes.txt"" ""c:\Users\xg645\Downloads\TesisNataliaRojo\data\annotations""", 0, False
