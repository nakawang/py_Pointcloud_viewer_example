from PyQt5 import uic 
if __name__ == "__main__":
    with open(".\\mainWindow.ui") as ui_file:
        with open(".\\mainWindow.py","w") as py_ui_file:
            uic.compileUi(ui_file,py_ui_file)
    
    with open(".\\registration_dialog.ui") as ui_file:
        with open(".\\registration_dialog.py","w") as py_ui_file:
            uic.compileUi(ui_file,py_ui_file)
    
