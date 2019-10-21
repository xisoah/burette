from subprocess import check_output

uiFile = 'editor.ui'
pyFile = 'edit.py'
command = 'D:/Users/sohai/Desktop/burette/env/Scripts/pyuic5.exe -x ' + uiFile + ' -o ' + pyFile
check_output(command, shell=True).decode()
print('Converted ' + uiFile + ' to ' + pyFile)
