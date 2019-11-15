from tkinter import *
from tkinter import filedialog
class FileExplorer:
   inputfilepath = None
   outputfilepath = None

   def __init__(self):
      root = Tk()
      self.inputfilepath = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = [("PDF files", '*.pdf'), ("Jpeg files", '*.jpeg'), ('all files', '*.*')])

      temp = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = [('PDF files', '*.pdf'), ("all files", "*.*")])
      index = temp.rfind('/')
      self.outputfilepath = temp[0:index]

   def get_inputfilepath(self):
      return self.inputfilepath

   def set_inputfilepath(self, ifp):
      self.inputfilepath = ifp

   def get_outputfilepath(self):
      return self.outputfilepath

   def set_outputfilepath(self, ofp):
      self.outputfilepath = ofp
