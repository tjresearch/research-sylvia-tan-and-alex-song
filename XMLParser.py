import xml.etree.ElementTree as ET
import re

def parseXML(inputfilepath):
   tree = ET.parse(open(inputfilepath))

   root = tree.getroot()
   # print(ET.tostring(root, 'utf8').decode('utf8'))
   # different for score time-wise and score part-wise
   # first support basic implementation of one part read through measures
   # rest pitches are negative integers (-1)
   default_tempo = 120
   notes = []
   pitch_table = get_table()
   # for scoring part-wise, returns of list of tuples of (note duration in seconds, pitches in Hz)
   tempo = default_tempo

   divisions = None
   # key_signature = None
   time_signature = None
   for measure in root.findall('part/measure'):
      # measures have attributes {number} and children {attributes, note}
      measure_attrib = measure.find('attributes')
      # attributes have children {divisions, key {fifths}, time{beats, beat-type}}
      if measure_attrib != None:
         # divisions is divisions per quarter note
         if measure_attrib.find('divisions') != None:
            divisions = int(measure_attrib.find('divisions').text)
         if measure_attrib.find('time') != None:
            time = measure_attrib.find('time')
            time_signature = (int(time.find('beats').text), int(time.find('beat-type').text))
         # if measure_attrib.get('key') != None:
         # key_signature = get_key_sig(int(measure_attrib.find('key').get('fifths').text), measure_attrib.find('key'.get('mode')).text)
      # apply time_signature settings on each note
      for note in measure.findall('note'):
         # note has attributes {attack and release} and children {chord (not using right now), pitch, rest, duration, tie}
         pitch = None
         value = None
         if note is None:
            pass
         elif note.find('rest') != None:
            pitch = -1
            value = 'rest'
         else:
            pitch_element = note.find('pitch')
            value = pitch_element.find('step').text
            alter = 0
            if pitch_element.find('alter') is not None:
               alter = int(pitch_element.find('alter').text)
            pitch = get_pitch(value, alter, int(pitch_element.find('octave').text), pitch_table)

         duration = get_duration(int(note.find('duration').text), divisions, tempo, time_signature)
         notes.append((pitch, duration))
   return notes

def get_duration(duration, divisions, tempo, timesig):
   return duration/divisions/tempo * 60

def get_pitch(step, alter, octave_value, pitch_table):
   note_value = pitch_table[0].index(step) + alter
   return pitch_table[octave_value][note_value]

def get_table():
   pitch_table = []
   octave_notes = []
   with open('/Users/alexandersong/PycharmProjects/Astong/note_frequencies.txt') as file:
      lines = file.readlines()
      octave_notes = [note.strip() for note in re.split(r'\t+', lines.pop(0))]
      pitch_table.append(octave_notes)
      for octave in lines:
         freq = [note.strip() for note in octave.split('\t')]
         freq.pop(0)
         pitch_table.append(freq)
   return pitch_table

"""
function not necessary right now because alter element of each pitch takes care of time signature, could be useful in error later because keysig is common mistake
def get_key_sig(num, mode):
   sharps_order = [('F', 'F#'), ('C', 'C#'), ('G', 'G#'), ('D', 'D#'), ('A', 'A#'), ('E', 'E#'), ('B', 'B#')]
   flats_order = [('B', 'Bb'), ('E', 'Eb'), ('A', 'Ab'), ('D', 'Db'), ('G', 'Gb'), ('C', 'Cb'), ('F', 'Fb')]
   accidental_dict = {}
   if num > 0:
      for i in range(num):
         accidental_dict[sharps_order[i][0]] = sharps_order[i][1]
   if num < 0:
      for i in range(-num):
         accidental_dict[flats_order[i][0]] = flats_order[i][1]
   return accidental_dict

def main():
   parseXML('/Users/alexandersong/Documents/Senior Year/CS Research/Audiveris Test Files/Winter_Goal_Test_2.xml')
"""
if __name__ == '__main__':
   main()
