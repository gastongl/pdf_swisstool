# merge.py

import PyPDF4

class MergeObject:
    #index = 0
    pdf_merge_list = []
    
    def merge_pdf():
        pdf_writer = PyPDF4.PdfFileWriter()
    
        for path in MergeObject.pdf_merge_list:
            pdf_reader = PyPDF4.PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))
    
        # Write out the merged PDF
        with open("C:\\pdftest\\test.pdf", 'wb') as out:
            pdf_writer.write(out)
    
    
    def clearlist():
        #MergeObject.index = 0
        MergeObject.pdf_merge_list.clear()