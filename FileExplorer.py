from tkinter import filedialog
class FileExplorer:
   inputfilepath = None
   outputfilepath = None
   root = None
   def __init__(self, r):
      root = r
      self.inputfilepath = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = [("PDF files", '*.pdf'), ("Jpeg files", '*.jpeg'), ('ALL files', '*.*')])
      self.outputfilepath = filedialog.asksaveasfilename(initialdir = "/",title = "Select file")


   def get_inputfilepath(self):
      return self.inputfilepath

   def set_inputfilepath(self, ifp):
      self.inputfilepath = ifp

   def get_outputfilepath(self):
      return self.outputfilepath

   def set_outputfilepath(self, ofp):
      self.outputfilepath = ofp
