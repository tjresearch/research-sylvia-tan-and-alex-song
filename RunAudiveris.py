import subprocess
from pathlib import Path
class RunAudiveris:
   inputfilepath = None
   outputfilepath = str(Path.home()) + '/audiveris/'

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

   def makexml(self):
      # needs your working directory of audiveris
      print(subprocess.check_output('gradle run -PcmdLineArgs=\"-batch,-export,-output,' + self.outputfilepath + ',--,' + self.inputfilepath + '\"', shell = True, cwd = str(Path.home()) + '/audiveris/'))



