# Parameters for chords.py

sharp_map = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'h']
b_map = ['c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab', 'a', 'b', 'h']

#add per note (intervall)
add_per_note = {5: 7, 6: 9, 7: 10, 9: 14, 11: 17, 13: 21}

#Relative tones
relative_map = {'I': 0, 'II': 2, 'III': 4, 'IV': 5, 'V': 7, 'VI': 9, 'VII': 11}

guitar_strings = ['E', 'a', 'd', 'g', 'b', 'e']
guitar_tones = [4, 9, 2, 7, 11, 4]

#Major progressions from
#http://mugglinw.ipower.com/chordtab_maps/images/genmap.gif
major_progressions = {
    'III #7 b5': ['VI'], 'VI': ['II m'], 'I# dim b7': ['II m'], 
    'IV# #7 b5': ['VII'], 'VII': ['III m'], 'II# dim b7': ['III m'], 
    'II m': ['V', 'III m', 'IV #7', 'IIb 7', 'I /V'], 
    'IV #7': ['I'], 'IIb 7': ['I'], 'III m': ['I', 'IV', 'VI m'],
    'V m': ['I 7', 'I 9', 'I b9'], 'I 7': ['IV'], 'I 9': ['IV'],
    'I b9': ['IV'],'III #7 b5': ['IV'],'I #6': ['II', 'V /II'], 
    'V /II': ['II'], 'II': ['V'], 'IV# #7 b5': ['V'],
    'VIb': ['VIIb'], 'VIIb': ['I'], 'V': ['III m', 'VI m', 'I'],
    'IV': ['V', 'I', 'I /V', 'II m'], 'VI m': ['IV', 'II m'],
    'I /V': ['V'], 'IV /I': ['I'], 'V /I': ['I'],
    'I': ['IV /I', 'V /I'], 'VIb 7': ['I /V'], 'VIIb 9': ['I /V'], 
    'IV# #7 b5': ['I /V'],'I dim /IIIb': ['II m'],
    'VII #7 b5': ['III'], 'III': ['VI m'], 'V# dim 7': ['VI m'],
    'VI #7 b5': ['II'], 'VI dim b7 b5': ['II']
     }

major_additions = {
    'II m': ['#7', '#9'], 'III m': ['#7'], 'IV': ['m', '6', '#7'],
    'V': ['sus', '7', '9', '11', '13'], 'VI m': ['#7', '#9'],
    'II m': ['#7', '#9'], 'I': ['sus', '9', '#9', '#7', '6']
    }

for chord in ['VI', 'VII', 'II', 'III']:
    major_additions[chord] = ['7', '9', 'b9']
