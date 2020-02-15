""" Google Spreadsheet To Png converter
"""

import os
import urllib.parse
import urllib.request
import io

import PyPDF2
from wand.image import Image


class SheetToPng:
    """ Convert sheet to png Class.
    """

    def __init__(self, sheet_url: str):
        self.sheet_url = sheet_url
    
    def cell_to_pdf(self, start: int, end: int):
        params = {
                "format": "pdf",
                "gid": 0,
                "range": f"{start}:{end}",
                "size": 1,
                "portrait": "false",
                "vertical_alignment": "MIDDLE",
                "horizontal_alignment":"CENTER",
                "scale": 4
                }

        url = self.sheet_url + "/export?" + urllib.parse.urlencode(params) 
        pdf = urllib.request.urlopen(url)

        stream = io.BytesIO()
        stream.write(pdf.read())
        stream.seek(0)

        return stream

    def sheet_to_png(self, start: int, end: int, filename: str=None):

        pdf = self.cell_to_pdf(start, end)

        reader = PyPDF2.PdfFileReader(pdf)
        writer = PyPDF2.PdfFileWriter()

        writer.addPage(reader.getPage(0))

        pdf_stream = io.BytesIO()
        writer.write(pdf_stream)
        pdf_stream.seek(0)

        img = Image(file=pdf_stream, resolution=100)
        img.convert("png")

        self.stream = io.BytesIO()
        img.trim()
        img.format="png"
        img.save(file=self.stream)
        self.stream.seek(0)

        return self.stream

    def save(self, filename: str):
        with open(filename, "wb") as f:
            self.stream.seek(0)
            f.write(self.stream.read())

if __name__ == "__main__":
    o = os.getenv("SHEET_URL")
    s = SheetToPng(o)
    s.sheet_to_png("A1", "C8")
    s.save("sheet.png")
