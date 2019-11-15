from RunAudiveris import *
from FileExplorer import *
def main():
   fileexplorer = FileExplorer()
   audiveris = RunAudiveris(fileexplorer.get_inputfilepath(),fileexplorer.get_outputfilepath())
   #print(audiveris.makemxl())

if __name__ == '__main__':
   main()