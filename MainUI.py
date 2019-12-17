from RunAudiveris import *
from FileExplorer import *
def main():
   root = Tk()
   fileexplorer = FileExplorer(root)
   audiveris = RunAudiveris(fileexplorer.get_inputfilepath(),fileexplorer.get_outputfilepath())
   audiveris.makexml()
   filename = fileexplorer.get_inputfilepath()[fileexplorer.get_inputfilepath().rfind('/'):fileexplorer.get_inputfilepath().rfind('.')]
   xmlfilepath = fileexplorer.get_outputfilepath() + filename + '/' + filename + '.xml'
   notes_durations = XMLParser.parseXML(xmlfilepath)

if __name__ == '__main__':
   main()
