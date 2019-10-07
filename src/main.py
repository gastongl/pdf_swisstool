# main.py

#import wx
import interface
import os

#def resource_path(relative):
#    return os.path.join(
#        os.environ.get(
#            "_MEIPASS",
#            os.path.abspath(".")
#        ),
#        relative
#    )

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main(): # Run main stuff
    app = interface.wx.App() # Creates an wx.App object in app var
    frame = interface.AppFrame() # Creates a AppFrame (custom) object
    #frame.SetIcon(interface.wx.Icon("pdfst.ico"))
    #print (str(resource_path("pdfst.ico")))
    try:
        frame.SetIcon(interface.wx.Icon(resource_path("pdfst.ico")))
    except:
        interface.wx.LogError("Error retrieving window icon.")
    frame.Show() # Show frame
    app.MainLoop() # Enter MainLoop

if __name__ == '__main__': # Check if execution started from this file
    main()


