# main.py

#import wx
import interface

def main(): # Run main stuff
    app = interface.wx.App() # Creates an wx.App object in app var
    frame = interface.AppFrame() # Creates a AppFrame (custom) object
    frame.SetIcon(interface.wx.Icon("pdfst.ico"))
    frame.Show() # Show frame
    app.MainLoop() # Enter MainLoop

if __name__ == '__main__': # Check if execution started from this file
    main()