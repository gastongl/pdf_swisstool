# mergeui.py

import wx
import PyPDF4
import os
import merge

class MergePanel(wx.Panel):
    def __init__(self, parent): ##Constructor, inherits parent
        super().__init__(parent) #calls wx.Panel constructor (as in defining wx.Panel object)
        self.mergeobj = merge.MergeObject # Object that contains pdf merging functions
        self.index = 0 # Global index tracker
        self.totalpages = 0
        self.finalsize = 0 # Final (merged) pdf size
        self.items_list = [] # List that contains tuples, where PDF files data is stored
        
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        ### List control ###
        #self.list_ctrl = wx.ListCtrl = wx.ListCtrl(self, size=(750, 300), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl = wx.ListCtrl(self, size=(750, 300), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        
        self.list_ctrl.InsertColumn(0, "Title", width=220)
        self.list_ctrl.InsertColumn(1, "Author", width=180)
        self.list_ctrl.InsertColumn(2, "Size", width=70)
        self.list_ctrl.InsertColumn(3, "Pages", width=50)
        self.list_ctrl.InsertColumn(4, "Path", width=200)
        
        
        ### Buttons ###
        addpdf_btn = wx.Button(self, label="Add...")
        addpdf_btn.Bind(wx.EVT_BUTTON, self.on_add_files)
        
        moveitemup_btn = wx.Button(self, label="↑")
        moveitemup_btn.Bind(wx.EVT_BUTTON, self.on_move_item_up)
        
        moveitemdown_btn = wx.Button(self, label="↓")
        moveitemdown_btn.Bind(wx.EVT_BUTTON, self.on_move_item_down)
        
        rempdf_btn = wx.Button(self, label="Remove")
        rempdf_btn.Bind(wx.EVT_BUTTON, self.on_rem_file)
        
        clearlist_btn = wx.Button(self, label="Clear list")
        clearlist_btn.Bind(wx.EVT_BUTTON, self.on_clear_list)
        
        merge_btn = wx.Button(self, label="Merge PDF")
        merge_btn.Bind(wx.EVT_BUTTON, self.on_merge)
        
        
        ### Labels ###
        self.finalsize_lbl = wx.StaticText(self, label="Final PDF size: 0 KB")
        self.totalpages_lbl = wx.StaticText(self, label="0 pages")
        
        
        # Adds widgets to sizers
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.LEFT, 5)
        main_sizer.Add(right_sizer, 0, wx.ALL | wx.RIGHT, 5)
        
        right_sizer.Add(addpdf_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(moveitemup_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(moveitemdown_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(rempdf_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(clearlist_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(merge_btn, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(self.finalsize_lbl, 0, wx.ALL | wx.CENTER, 5)
        right_sizer.Add(self.totalpages_lbl, 0, wx.ALL | wx.CENTER, 5)
        
        self.SetSizer(main_sizer)
    
    def on_add_files(self, event): # Handles add files event
        #title = "Select PDF files"
        #dlg = wx.FileDialog(self, title, wildcard="PDF files (*.pdf)|*.pdf", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) # determine open dialog rules
        #if dlg.ShowModal() == wx.ID_OK: self.add_file_listing(dlg.GetPaths()) # Get files open
        #dlg.Destroy() # Destroy dialog window
        with wx.FileDialog(self, "Open PDF files", wildcard="PDF files (*.pdf)|*.pdf", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL: return     # the user changed their mind
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPaths()
            try:
                self.add_file_listing(pathname)
            except IOError:
                wx.LogError("An error has ocurred while trying to open the files.")
    
    def on_rem_file(self, event): # Handles remove event
        if (self.list_ctrl.GetFocusedItem()) == -1: print ("There is no objects selected to remove") #If there is not items selected, don't remove
        else:
            del self.items_list[self.list_ctrl.GetFocusedItem()] #Delete the item from items_list
            self.update_file_listing() #Call update file listing, and pass new position of the item for tracking (keep it selected)
    
    def on_move_item_up(self, event): # Handles move up event
        if (self.list_ctrl.GetFocusedItem()) == -1: print ("There is no objects selected to move") #If there is not items selected, don't move
        else:
            selected_item_pos = self.list_ctrl.GetFocusedItem() # Get position of selected item
            if selected_item_pos == 0: print ("Can't move up") # If it's the first item (aka at the top of the list), don't move
            else:
                moving_item = self.items_list[selected_item_pos] #Put item in temporal tuple
                del self.items_list[selected_item_pos] #Delete the item from items_list
                self.items_list.insert(selected_item_pos-1,moving_item) #Put again the item that was stored in moving_item, but one position up
                self.update_file_listing(selected_item_pos-1) #Call update file listing, and pass new position of the item for tracking (keep it selected)

    def on_move_item_down(self, event): # Handles move down event
        if (self.list_ctrl.GetFocusedItem()) == -1: print ("There is no objects selected to move") #If there is not items selected, don't move
        else:
            selected_item_pos = self.list_ctrl.GetFocusedItem() # Get position of selected item
            if selected_item_pos == (self.list_ctrl.GetItemCount())-1: print ("Can't move down") # If it's on the bottom, don't move
            else:
                moving_item = self.items_list[selected_item_pos] #Put item in temporal tuple
                del self.items_list[selected_item_pos] #Delete the item from items_list
                self.items_list.insert(selected_item_pos+1,moving_item) #Put again the item that was stored in moving_item, but one position down
                self.update_file_listing(selected_item_pos+1) #Call update file listing, and pass new position of the item for tracking (keep it selected)
    
    def on_clear_list(self, event): # Handles Clear list event
        #print(f"{self.list_ctrl.GetItemCount()}")
        if self.items_list: # If there are items on the list, remove them all and reinitialize objects
            self.list_ctrl.DeleteAllItems()
            self.items_list.clear()
            self.index = 0
            self.mergeobj.clearlist()
            self.finalsize = 0
            self.finalsize_lbl.SetLabel(f"Final PDF size: {self.calculate_pdf_size(self.finalsize)}")
            self.totalpages_lbl.SetLabel(f"0 pages")
            self.totalpages = 0
        else: print("There is no files in list, not clearing list")
    
    def on_merge(self, event): # Handles merge event
        if not self.items_list: print("There is no files to merge, try adding some") # If there are not elements on the list, don't merge
        else:
            self.mergeobj.clearlist() # Clear list of mergeobj
            for x in self.items_list: # Add the path of all the pdfs to merge to the pdf_merge_list of mergeobj
                self.mergeobj.pdf_merge_list.append(x[4])
            mergedpdf = self.mergeobj.merge_pdf() # Call merge_pdf function and merge pdfs
            with wx.FileDialog(self, "Save merged PDF file", wildcard="PDF file (*.pdf)|*.pdf", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL: return     # the user changed their mind

                # save the current contents in the file
                pathname = fileDialog.GetPath()
                try:
                    with open(pathname, 'wb') as out:
                        mergedpdf.write(out)
                except IOError:
                    wx.LogError(f"Cannot save current data in file {pathname}.")
            
    
    def update_file_listing(self, selection=-1): # Update list control after moving up or down items
        self.list_ctrl.DeleteAllItems() # Deletes all items from the list
        index_temp = 0 # Creates a temporal index for tracking items
        self.finalsize = 0 # Set finalsize of the merged (final) pdf to zero, as it is going to be calculated again.
        self.totalpages = 0
        for x in self.items_list: # Goes through all the data in items_list and adds it to the list
            self.list_ctrl.InsertItem(index_temp, x[0])
            self.list_ctrl.SetItem(index_temp, 1, x[1])
            self.list_ctrl.SetItem(index_temp, 2, x[2])
            self.list_ctrl.SetItem(index_temp, 3, x[3])
            self.list_ctrl.SetItem(index_temp, 4, x[4])
            self.finalsize += (os.path.getsize(x[4])) # Check size of each pdf and adds it to finalsize var
            pdf = PyPDF4.PdfFileReader(x[4]) # Read the pdf file
            self.totalpages += pdf.getNumPages() # Check number of pages and adds it to the totalpages var
            index_temp += 1
        self.index = index_temp # Finally set the global index tracker to the same value as the temporal one
        self.totalpages_lbl.SetLabel(f"{self.totalpages} pages")
        self.finalsize_lbl.SetLabel(f"Final PDF size: {self.calculate_pdf_size(self.finalsize)}") # Updates final pdf size
        
        #The following instructions make it so the item moved can be moved again without having to select it again
        #(!WARNING!: Make sure that when remove individual items this doesn't break
        if selection != -1:
            self.list_ctrl.Select(selection)
            self.list_ctrl.Focus(selection)
    
    def add_file_listing(self, files_path): # Add files to the list
        for pdf_path in files_path: #Checks all the files that the user opened
            if self.index >= 10: # When index reaches 10 stop loop, don't add more files
                print ("Can't add more than 10 files")
                break
            else:
                pdf = PyPDF4.PdfFileReader(pdf_path) #Read the pdf file from path and puts into var
                
                self.finalsize += os.path.getsize(pdf_path) # Adds the size to var that contains merged (total) pdf size
                pdf_size = self.calculate_pdf_size(os.path.getsize(pdf_path)) # Calculates size of the pdf to store info in items_list
                pdf_pages = pdf.getNumPages() # Calculates the number of pages of the pdf to store info in items_list
                
                # Insert pdf data as strings into items_list:
                self.items_list.append((str((pdf.getDocumentInfo()).title), # Insert title data
                                    str((pdf.getDocumentInfo()).author), # Insert author data
                                    str(pdf_size), # Insert size data
                                    str(pdf.getNumPages()), # Insert number of pages
                                    str(pdf_path))) # Insert path of the file
                
                # The next instructions refresh the with the data of the pdf:
                self.list_ctrl.InsertItem(self.index, str((pdf.getDocumentInfo()).title))
                self.list_ctrl.SetItem(self.index, 1, str((pdf.getDocumentInfo()).author))
                self.list_ctrl.SetItem(self.index, 2, str(pdf_size))
                self.list_ctrl.SetItem(self.index, 3, str(pdf_pages))
                self.list_ctrl.SetItem(self.index, 4, str(pdf_path))
                
                self.finalsize_lbl.SetLabel(f"Final PDF size: {self.calculate_pdf_size(self.finalsize)}") # Update label with final size of the pdf
                
                self.totalpages += pdf_pages # Adds the value of pdf_pages to totalpages var
                self.totalpages_lbl.SetLabel(f"{self.totalpages} pages") # Update label with total pages
                
                self.index += 1
    
    def calculate_pdf_size(self, xsz): # Function that takes an integer and returns a string with size
        if (xsz) > (1048576): # If file is bigger than 1 MB, format str with size for MB
            xsz = xsz / (1024*1024.0)
            pdf_size = f"{round(xsz,1)} MB"
        else: # else format it for KB
            xsz = xsz / (1024)
            pdf_size = f"{int(xsz)} KB"
        return pdf_size