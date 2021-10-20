Sub BackupFriendlyMacro()
    Dim x As String
    
    strPath = "/Users/ilya/Desktop/backup/"

    On Error Resume Next
    x = GetAttr(strPath) And 0
    If Err = 0 Then
        strDate = Format(Now, "dd-mm-yy hh-mm")
        FileNameXls = strPath & "\" & Left(ActiveWorkbook.Name, InStrRev(ActiveWorkbook.Name, ".") - 1) & " " & strDate & ".xls"
        ActiveWorkbook.SaveCopyAs FileName:=FileNameXls
    Else
        MsgBox "Directory " & strPath & " does not exist or there are no permission to open it", vbCritical
    End If
End Sub

