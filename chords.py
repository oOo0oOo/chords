#########################################################
#
# Music Helper Functions
# Oliver Dressler, 2013
#
#########################################################

import random
import math

# Get all the music theory (parameters)
from theory import *

def quick_song(chord_list, pause = True):
    bar_inp = raw_input('Around which bar do you want to play? E.g. 5 or 4-8\n')
    try:
        bar = int(bar_inp)
        bounds = False
    except ValueError:
        bar_inp = bar_inp.replace(' ', '')
        bounds = [int(b) for b in bar_inp.split('-')]

    for chord_str in chord_list:
        if bounds:
            bar = random.randrange(bounds[0], bounds[1]+1)

        print quick_tab(chord_str, bar)
        if pause:
            raw_input('Press enter for next chord...')

def quick_tab(chord_str, bar, convert = True):
    tones, use_b = find_tones(chord_str)
    tabs = create_tabs(tones, position = bar)
    if convert:
        ret = ['Tabs for {} ({}), located approx at bar {}:\n\n'.format(chord_str, convert_chord(tones, use_b), bar)]
        for tab in tabs:
            ret.append(convert_tab(tab) + '\n\n')
        return ''.join(ret)
    else:
        return tabs

def find_tone(tone_str):
    '''returns tone value (integer) and b (or #) used'''
    tone_str = tone_str.lower()
    #Find base tone
    if tone_str in sharp_map:
        return sharp_map.index(tone_str), False
    
    elif tone_str in b_map:
        return b_map.index(tone_str), True

def find_tones(chord_str):
    '''
        Returns a list with all the tones in the chord, and use_b.
        Examples for valid chord_str:
        A , A m , H m b5 7, C sus , F dim 11, D aug #6 9 b11
    '''
    chord_str = chord_str.lower()
    parts = chord_str.split(' ')
    chord = []
    
    base, use_b = find_tone(parts[0])
    
    chord.append(base)
    
    if len(parts) == 1:
        #add major terz & quint to base
        chord.append((base + 4) % 12)
        chord.append((base + 7) % 12)
        
    else:
        
        added_5 = False
        if parts[1] in ('m', 'dim', 'dim.'):
            chord.append((base + 3) % 12)
            if parts[1] in ('dim', 'dim.'):
                chord.append(((base + 6) % 12))
                added_5 = True
            pos = 2
            
        elif parts[1] == 'aug':
            chord.append((base + 4) % 12)
            chord.append((base + 8) % 12)
            pos = 2
            added_5 = True
            
        elif parts[1] in ('sus', 'sus4'):
            chord.append((base + 5) % 12)
            pos = 2
            
        else:
            chord.append((base + 4) % 12)
            pos = 1
        
        #addition per note: (add_per note is a global dict of half-tones to add for a given intervall)
        add = add_per_note
        if len(parts) > pos:
            for i in range(pos, len(parts)):
                sel = parts[i]
                if sel[0] in ('b', '#'):
                    note = int(sel[1:])
                    if sel[0] == 'b':
                        tone = (base + add[note] - 1)%12
                    elif sel[0] == '#':
                        tone = (base + add[note] + 1)%12
                        
                    if note == 5:
                        added_5 = True
                    
                    chord.append(tone)
                            
                elif sel[0] == '/':
                    #add note as bass tone (beginning of list)
                    note = sel[1:]
                    if note in sharp_map:
                        chord = [sharp_map.index(note)] + chord
                    elif note in b_map:
                        chord = [b_map.index(note)] + chord
                    else:
                        try:
                            chord = [int(note)] + chord
                        except ValueError:
                            pass
                        
                else:
                    try:
                        note = int(sel)
                        tone = (base + add[note]) % 12
                        chord.append(tone)
                        if note == 5:
                            added_5 = True
                    except ValueError:
                        print 'Use '
                        print 'value error', sel
        
        if not added_5:
            chord.append((base + 7) % 12)
    
    def uniquify(seq, idfun=None):
        #order preserving uniquify
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result
    
    chord = uniquify(chord)
    return chord, use_b

def convert_chord(chord, use_b = False):
    if use_b:
        conv_table = b_map
    else:
        conv_table = sharp_map
        
    chord_str = ''
    for tone in chord:
        chord_str += conv_table[tone] + ' '
    
    return chord_str

def create_tabs(chord, position = 1):
    '''
        Create a tab from a chord. Returns three tab suggestions.
        Position is the suggested optimal position.
    '''

    min_pos = position - 3
    max_pos = position + 4
    if min_pos < 0:
        min_pos = 0
    if max_pos > 20:
        max_pos = 20

    # for each tone: get all positions on the guitar board
    pos = {}
    for tone in chord:
        pos[tone] = []
        for i in range(len(guitar_tones)):
            string = guitar_tones[i]
            for bar in [0] + range(min_pos, max_pos):
                if ((string + bar) % 12) == tone:
                    pos[tone].append((i, bar))
        pos[tone] = list(set(pos[tone]))

    tabs = []
    for i in range(200):
        tab = []
        strings = []

        # Set each requested tone
        for tone, presses in pos.items():
            for i in range(10):
                press = random.choice(presses)
                if press[0] not in strings:
                    tab.append(press)
                    strings.append(press[0])
                    break


        if len(tab) == len(chord):
            # Duplicate base tone once if possible
            for i in range(10):
                press = random.choice(pos[chord[0]])
                if press[0] not in strings:
                    strings.append(press[0])
                    tab.append(press)
                    break
            
            # Check if tab has holes (not played strings between others)
            strings = sorted(strings)
            found = False
            for ind in range(1,len(strings)):
                if strings[ind-1] + 1 != strings[ind]:
                    found =True
                    break

            if not found:
                tab = tuple(sorted(tab))
                bars = [t[1] for t in tab if t[1] != 0]
                
                # favour baret chords
                if len(bars) == len(tab):
                    m = min(bars)
                    bars = [b for b in bars if b != m]
                    bars += [m]

                if len(bars) > 1:
                    stdev = calculate_stdev(bars)
                else:
                    stdev = 0
                tabs.append(tuple([stdev, tab]))

    tabs = list(sorted(set(tabs)))[:3]
    tabs = [t[1] for t in tabs]
    return tabs

def create_tab_OLD(chord):
    '''
        Creates a tab configuration on a 6-string guitar.
    '''
    # Maximal mean of all bars pressed (excluding empty strings)
    max_mean = 5

    #trim chord if more than 6 tones
    if len(chord) > 6:
        num_strings = 6
    else:
        num_strings = len(chord)
    
    #select start string; chord will be played on 4 adjacent strings
    #first three strings are tested, lowest bar wins
    cur_lowest = [100, 100]
    strings_used = 7-num_strings
    if strings_used > 3:
        strings_used = 3
        
    for i in range(strings_used):
        bar = chord[0]
        bar -= guitar_tones[i]
        if bar < 0:
            bar += 12
            
        if bar < cur_lowest[1]:
            cur_lowest = [i, bar]
    
    num_strings = num_strings + cur_lowest[0]
    
    #choose random combinations for other tones, select best combination
    best_tab = [100, []]
    for i in range(150):
        tab = []
        tab.append(cur_lowest)
        
        chord_left = chord[1:]
        next_string = cur_lowest[0]+1
        while len(chord_left) > 0 and next_string <= num_strings and next_string < 6:
            tone = random.choice(chord_left)
            chord_left.remove(tone)
            bar = tone - guitar_tones[next_string]
            if bar < 0:
                bar += 12
            
            tab.append([next_string, bar])
            next_string += 1
        
        #Extract list of all PRESSED bars from tab (not 0)
        bars = [bar for i, bar in tab if bar is not 0]
        
        #Calculate mean, spread and standard deviation
        if len(bars) > 1:
            stdev = calculate_stdev(bars)
            mean = sum(bars)/len(bars)
            if mean < max_mean and stdev < best_tab[0]:
                best_tab = [stdev, tab]
            
    return best_tab[1]

    
def convert_tab(tab):
    ''' 
        Creates string like this from tab:

        e   |---|---|---|---|---|
        b   |---|-x-|---|---|---| c#
        g   |---|-x-|---|---|---| a
        d   |---|-x-|---|---|---| e
        a x |---|---|---|---|---| a
        E   |---|---|---|---|---|
              1              .  
    '''
    
    tab_list = []
    #create lookup dict
    tab_map = {}
    for string, bar in tab:
        tab_map[string] = bar
    
    lowest_bar = 10000
    for i in tab_map.values():
        if i != 0 and i < lowest_bar:
            lowest_bar = i
            
    highest_bar = max(tab_map.values())
    num_bars = highest_bar - lowest_bar + 1
    lowest = True
    
    while num_bars < 5:
        if lowest and lowest_bar > 1:
            lowest_bar -= 1
        elif not lowest:
            highest_bar += 1
            
        lowest = not lowest
        num_bars = highest_bar - lowest_bar + 1
        
    #Go through strings in reverse direction
    for string in reversed(range(6)):
        tab_list.append(guitar_strings[string])
        
        try:
            bar = tab_map[string]
            if bar == 0:
                bar_pos = -1
            else:
                bar_pos = bar - lowest_bar
        except KeyError:
            bar_pos = -2
            
        if bar_pos == -1:
            tab_list.append(' x |')
        else:
            tab_list.append('   |')
        
        for i in range(num_bars):
            if i == bar_pos and bar_pos != -2:
                tab_list.append('-x-|')
            else:
                tab_list.append('---|')
        
        #Write the note played behind the line
        if bar_pos != -2:
            tone = (guitar_tones[string] + tab_map[string])%12
            tone = sharp_map[tone]
            tab_list.append(' ' + tone)
        
        tab_list.append('\n')
        
    #add lowest string
    tab_list.append('      ' + str(lowest_bar) + ' ' * (2-len(str(lowest_bar))))
    
    marks = {5: '.  ', 7: '.  ', 9: '.  ', 12: '.. ',
             15: '.  '}
    
    #add marks on guitar
    for i in range(lowest_bar+1, highest_bar+1):
        try:
            add_str = marks[i]
        except KeyError:
            add_str = '   '
        tab_list.append(' ' + add_str)

    return ''.join(tab_list)

def calculate_stdev(q):
    '''
        From: http://www.daniweb.com/software-development/python/
        threads/438922/finding-the-standard-deviation-in-python
    '''
    avg = float(sum(q))/len(q)
    dev = []
    for x in q:
        dev.append(x - avg)
    sqr = []
    for x in dev:
        sqr.append(x * x)
    standard_dev = math.sqrt(sum(sqr)/(len(sqr)-1))
    return standard_dev

def convert_chords_to_midi(chord_list, filename):
    '''Requires pyknon to create the midi...'''
    from pyknon.music import NoteSeq
    from pyknon.genmidi import Midi

    chord_prog = []
    
    midi = Midi(1, tempo=90)
    
    for chord in chord_list:
        chord = chord.upper()
        chord = chord.replace('B', 'BB')
        chord = chord.replace('H', 'B')
        chord_prog.append(NoteSeq(chord))
    
    midi.seq_chords(chord_prog, 0, 0)
    midi.write(filename)

def create_progression(num_chords = 4, ends_in_I = True, spicyness = 2):
    '''!!! UNTESTED !!!'''
    def random_progression(num_chords):
        #random start chord
        prog = [random.choice(major_progressions.keys())]
        last = 0
        while len(prog) < num_chords:
            prog.append(random.choice(major_progressions[prog[last]]))
            last += 1
        return prog
    
    num = 0
    while num < 1000:
        num += 1
        prog = random_progression(num_chords)    
        if not (ends_in_I and prog[len(prog)-1] != 'I'):
            if prog.count('I') <= 2:
                #spice up the progression
                for c_id in range(len(prog)):
                    for i in [0] * random.randrange(0, spicyness + 1):
                        try:
                            add = random.choice(major_additions[prog[c_id]])
                            prog[c_id] += ' ' + add
                        except KeyError:
                            pass
                return prog
            
def random_chord(num_tones = 4):
    tones = []
    for i in range(num_tones):
        tones.append(random.choice(range(12)))
    
    return tones

def cast_chord(chord, key):
    '''
    !!! UNTESTED !!!
    Casts a relative chord (e.g III m 7) in a key (number of I),
    key can be either an integer or a string (e.g. Eb)'''
    
    if type(key) == str:
        tone, use_b = find_tone(key)
    elif type(key) == int:
        tone = key
        use_b = False
    
    if use_b:
        conv_table = b_map
    else:
        conv_table = sharp_map
    
    relative_order = ['VII', 'VI', 'IV', 'V', 'III', 'II', 'I']
    for literal in relative_order:
        value = relative_map[literal]
        actual_tone = (tone + value)%12
        found = False
        while not found:
            ind = chord.find(literal)
            if ind == -1:
                found = True
            else:
                #check if sign is followed by b or #
                length = len(literal)
                end = ind + length
                try:
                    after = chord[ind + length]
                    if after == '#':
                        actual_tone += 1
                        end += 1
                    elif after == 'b':
                        actual_tone -= 1
                        end += 1
                except Exception, e:
                    pass
                    
                chord = chord[:ind] + conv_table[actual_tone] + chord[end:]
    
    return chord