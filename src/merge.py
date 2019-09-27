# merge.py

def on_merge(self):
    pdf_writer = parent.PyPDF4.PdfFileWriter()

    for path in parent.pdf_merge_list:
        pdf_reader = parent.PyPDF4.PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open("test.pdf", 'wb') as out:
        pdf_writer.write(out)