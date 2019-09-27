# interface.py

import wx
import PyPDF4
import os

class AppFrame(wx.Frame): # AppFrame object inherits from wx.Frame
    #def __init__(self, *args, **kwargs):
    def __init__(self): ##Constructor
        super(AppFrame, self).__init__(None, title="My Python App") # Initializes parent constructor, set window title
        self.SetSize((960, 540)) # Set window size
        self.Centre() # Centers on screen
        self.panel = AppPanel(self) # Create an AppPanel object
        #self.create_menu() # Runs create_menu function
        #wx.Frame(None, title="My PythonApp", style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
    
    #def create_menu(self): # Menues are created here
        #menu_bar = wx.MenuBar()
        #file_menu = wx.Menu()
        #open_folder_menu_item = file_menu.Append(wx.ID_ANY, "Open...", "Open PDF files for editing")
        
        #menu_bar.Append(file_menu, "&File")
        #self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item) # Bind functions to open_folder_menu_item to on_open_folder
        #self.SetMenuBar(menu_bar)
    
    

class AppPanel(wx.Panel): # AppPanel inherits from wx.Panel
    index = 0
    def __init__(self, parent): ##Constructor, inherits parent
        super().__init__(parent) #calls wx.Panel constructor (as in defining wx.Panel object)
        # Next: Sizers, layout and interface controllers
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.pdf_merge_list = []
        
        #self.list_ctrl = wx.ListCtrl = wx.ListCtrl(self, size=(750, 300), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl = wx.ListCtrl(self, size=(750, 300), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        
        self.list_ctrl.InsertColumn(0, "Title", width=250)
        self.list_ctrl.InsertColumn(1, "Author", width=200)
        self.list_ctrl.InsertColumn(2, "Size", width=70)
        self.list_ctrl.InsertColumn(3, "Path", width=200)
        
        addpdf_btn = wx.Button(self, label="Add...")
        addpdf_btn.Bind(wx.EVT_BUTTON, self.on_add_files)
        
        clearlist_btn = wx.Button(self, label="Clear list")
        clearlist_btn.Bind(wx.EVT_BUTTON, self.on_clear_list)
        
        merge_btn = wx.Button(self, label="Merge PDF")
        merge_btn.Bind(wx.EVT_BUTTON, self.on_merge)
        
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.LEFT, 5)
        main_sizer.Add(right_sizer, 0, wx.ALL | wx.RIGHT, 5)
        right_sizer.Add(addpdf_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(clearlist_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(merge_btn, 0, wx.ALL | wx.CENTER, 5)
        
        self.SetSizer(main_sizer)
    
    def on_add_files(self, event): # func runs from menu
        title = "Select PDF files"
        dlg = wx.FileDialog(self, title, wildcard="PDF files (*.pdf)|*.pdf", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) # determine open dialog rules
        if dlg.ShowModal() == wx.ID_OK:
            self.add_file_listing(dlg.GetPaths()) # Get files open
        dlg.Destroy()
    
    def on_clear_list(self, event):
        self.list_ctrl.DeleteAllItems()
        self.pdf_merge_list.clear()
        self.index = 0
    
    def on_merge(self, event):
        if not self.pdf_merge_list:
            print("There is no files to merge, try adding some")
        else:
            pdf_writer = PyPDF4.PdfFileWriter()
    
            for path in self.pdf_merge_list:
                pdf_reader = PyPDF4.PdfFileReader(path)
                for page in range(pdf_reader.getNumPages()):
                    # Add each page to the writer object
                    pdf_writer.addPage(pdf_reader.getPage(page))
    
            # Write out the merged PDF
            with open("test.pdf", 'wb') as out:
                pdf_writer.write(out)
    
    def add_file_listing(self, files_path):
        #for pdf_path in files_path:
            #print(pdf_path)
            #pdf_reader = PyPDF4.PdfFileReader(pdf_path)
            #print((pdf_reader.getDocumentInfo()).title)
        
        #self.current_files_path = files_path
        #self.list_ctrl.DeleteAllItems()
        
        
        
        #pdf_objects = []
        #self.pdf_merge_list.clear() # Clear list of pdfs to merge
        for pdf_path in files_path:
            pdf = PyPDF4.PdfFileReader(pdf_path)
            if (os.path.getsize(pdf_path)) > (1048576): # If file is bigger than 1 MB, format str with size for MB
                xsz = os.path.getsize(pdf_path) / (1024*1024.0)
                pdf_size = f"{round(xsz,1)} MB"
            else: # else format it for KB
                xsz = os.path.getsize(pdf_path) / (1024)
                pdf_size = f"{int(xsz)} KB"
            
            # Insert pdf data into the table:
            self.list_ctrl.InsertItem(self.index, str((pdf.getDocumentInfo()).title))
            self.list_ctrl.SetItem(self.index, 1, str((pdf.getDocumentInfo()).author))
            self.list_ctrl.SetItem(self.index, 2, str(pdf_size))
            self.list_ctrl.SetItem(self.index, 3, str(pdf_path))
            #pdf_objects.append(pdf)
            #self.row_obj_dict[index] = pdf
            self.pdf_merge_list.append(pdf_path) # Add pdf to list of pdfs to merge
            self.index += 1
        