# aboutui.py

import wx
import wx.html
import webbrowser

class AboutPanel(wx.Panel):
    def __init__(self, parent): ##Constructor, inherits parent
        super().__init__(parent) #calls wx.Panel constructor (as in defining wx.Panel object)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        txt_style = wx.VSCROLL|wx.html.HW_NO_SELECTION
        html_display = wx.html.HtmlWindow(self, 0, size=(800, 300), style=txt_style)
        html_display.SetPage(self.raw_html())
        
        self.webpagebtn = wx.Button(self, label="Visit webpage")
        self.webpagebtn.Bind(wx.EVT_BUTTON, self.onwebpage)
        
        self.donatebtn = wx.Button(self, label="Donate")
        self.donatebtn.Bind(wx.EVT_BUTTON, self.ondonate)
        
        main_sizer.Add(html_display, 0, wx.ALL | wx.LEFT, 0)
        main_sizer.Add(right_sizer, 0, wx.ALL | wx.RIGHT, 0)
        right_sizer.Add(self.webpagebtn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(self.donatebtn, 0, wx.ALL | wx.CENTER, 5)
        
        self.SetSizer(main_sizer)
    
    def raw_html(self):
        #html = ('<p>Copyright <YEAR> <COPYRIGHT HOLDER></p>'
        html = ('<p>By using this software you agree to the following agreement:</p>'
                '<p>Copyright (c) 2019 Gastón Gallo</p>'
                '<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>'
                
                '<p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>'
                
                '<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>')
        return html
    
    def onwebpage(self, event):
        webbrowser.open("https://gastongallo.net", new=0, autoraise=True)
    
    def ondonate(self, event):
        dlg = wx.MessageDialog(self, "Not working yet", caption="Not working",style=wx.OK|wx.CENTRE)
        dlg.ShowModal()
        dlg.Destroy()