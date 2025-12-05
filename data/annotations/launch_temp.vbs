Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c labelImg ""C:\Users\xg645\Downloads\TesisNataliaRojo\data\raw_images"" ""C:\Users\xg645\Downloads\TesisNataliaRojo\data\annotations\predefined_classes.txt"" ""C:\Users\xg645\Downloads\TesisNataliaRojo\data\annotations""", 0, False
