# interface.py

import wx
import mergeui
import aboutui

class AppFrame(wx.Frame): # AppFrame object inherits from wx.Frame
    #def __init__(self, *args, **kwargs):
    def __init__(self): ##Constructor
        super(AppFrame, self).__init__(None, title="PDF SwissTool", style=wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION) # Initializes parent constructor, set window title
        self.SetSize((930, 350)) # Set window size
        self.Centre() # Centers on screen
        self.panel = AppPanel(self) # Create an AppPanel object

class AppPanel(wx.Panel): # AppPanel inherits from wx.Panel
    def __init__(self, parent): ##Constructor, inherits parent
        super().__init__(parent) #calls wx.Panel constructor (as in defining wx.Panel object)
        # Next: Sizers, layout and interface controllers
        
        #p = wx.Panel(self)
        nb = wx.Notebook(self)

        # Create the tab windows
        tab1 = aboutui.AboutPanel(nb)
        tab2 = mergeui.MergePanel(nb)
        #tab3 = TabThree(nb)
        #tab4 = TabFour(nb)

        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "About")
        nb.AddPage(tab2, "Merger")
        #nb.AddPage(tab3, "Tab 3")
        #nb.AddPage(tab4, "Tab 4")

        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

#class TabOne(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
#        #t = wx.StaticText(self, -1, "This is the first tab", (20,20))
#        mergetab = mergeui.MergePanel(self)
#
#class TabTwo(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
#        t = wx.StaticText(self, -1, "This is the second tab", (20,20))
#
#class TabThree(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
#        t = wx.StaticText(self, -1, "This is the third tab", (20,20))
#
#class TabFour(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
#        t = wx.StaticText(self, -1, "This is the last tab", (20,20))