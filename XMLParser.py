import xml.etree.ElementTree as ET

def parseXML(inputfilepath):
   tree = ET.parse(open(inputfilepath))

   root = tree.getroot()

   # different for score time-wise and score part-wise
   # first support basic implementation of one part read through measures
   # rest pitches are negative integers (-1)
   default_tempo = 90
   notes = []

   # for scoring part-wise, returns of list of tuples of (note duration in seconds, pitches in Hz)
   tempo = default_tempo
   for part in root.iter('part'):
      # part has attributes {id}
      divisions = None
      # key_signature = None
      time_signature = None
      for measure in part.findall('measure'):
         # measures have attributes {number} and children {attributes, note}
         measure_attrib = measure.get('attributes')
         # attributes have children {divisions, key {fifths}, time{beats, beat-type}}
         if measure_attrib != None:
            # divisions is divisions per quarter note
            if measure_attrib.get('divisions') != None:
               divisions = int(measure_attrib.get('divisions').text)
            if measure_attrib.get('time') != None:
               time_signature = (int(measure_attrib.get('beats').text), int(measure_attrib.get('divisions').text))
            # if measure_attrib.get('key') != None:
               # key_signature = get_key_sig(int(measure_attrib.find('key').get('fifths').text), measure_attrib.find('key'.get('mode')).text)
         # apply time_signature settings on each note
         for note in measure.findall('note'):
            # note has attributes {attack and release} and children {chord (not using right now), pitch, rest, duration, tie}
            pitch = None
            value = None
            if note.get('rest') != None:
               pitch = -1
               value = 'rest'
            else:
               pitch_element = note.get('pitch')
               value = pitch_element.get('step').text + pitch_element.get('alter').text
               pitch = get_pitch(pitch_element.get('step').text, int(pitch_element.get('alter').text), int(pitch_element.get('octave').text))

            duration = get_duration(note.get('duration'), divisions, tempo, time_signature)
            notes.append(pitch, duration)

def get_duration(duration, divisions, tempo, timesig):
   return duration/divisions/tempo * 60

def get_pitch(step, alter, octave_value):
   pitch_table = []
   octave_notes = []
   with open('/Users/alexandersong/PycharmProjects/Astong/note_frequencies.txt') as file:
      lines = file.readlines()
      octave_notes = [note.strip() for note in lines.pop(0).split(' ')]
      for octave in lines:
         freq = [note.strip() for note in octave.split(' ')]
         pitch_table.append(freq)
   return pitch_table[octave_value][octave_notes.index(step) + alter]

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
"""
def main():
   parseXML('/Users/alexandersong/PycharmProjects/Astong/ten_notes.musicxml')

if __name__ == '__main__':
   main()