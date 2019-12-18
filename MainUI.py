from tkinter import *
import XMLParser
from FileExplorer import *
from LoadingScreen import *
from RunAudiveris import *
import LeastSquaresError

def main():
   root = Tk()
   root.withdraw()
   fileexplorer = FileExplorer(root)
   root.update()
   # ld = LoadingScreen(root, 'optical music recognition')
   audiveris = RunAudiveris(fileexplorer.get_inputfilepath(),fileexplorer.get_outputfilepath())
   # ld.end()
   audiveris.makexml()
   filename = fileexplorer.get_inputfilepath()[fileexplorer.get_inputfilepath().rfind('/'):fileexplorer.get_inputfilepath().rfind('.')]
   xmlfilepath = fileexplorer.get_outputfilepath() + filename + '/' + filename + '.xml'
   notes_durations = XMLParser.parseXML(xmlfilepath)
   LeastSquaresError.readAudio(notes_durations)


if __name__ == '__main__':
   main()
