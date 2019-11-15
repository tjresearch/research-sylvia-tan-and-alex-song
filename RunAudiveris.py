import subprocess
class RunAudiveris:
   inputfilepath = None
   outputfilepath = None

   def __init__(self, ifp, ofp):
      self.inputfilepath = ifp
      self.outputfilepath = ofp

   def get_inputfilepath(self):
      return self.inputfilepath

   def set_inputfilepath(self, ifp):
      self.inputfilepath = ifp

   def get_outputfilepath(self):
      return self.outputfilepath

   def set_outputfilepath(self, ofp):
      self.outputfilepath = ofp

   def makemxl(self):
      print('gradle run -PcmdLineArgs=\"-batch,-export,-output,' + self.inputfilepath + ',--,' + self.outputfilepath + '\"')
      # needs your working directory of audiveris
      return subprocess.check_output('gradle run -PcmdLineArgs=\"-batch,-export,-output,' + self.inputfilepath + ',--,' + self.outputfilepath + '\"', shell = True, cwd = '/Users/alexandersong/audiveris')



