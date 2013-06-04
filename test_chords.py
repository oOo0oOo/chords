#########################################################
#
# Tests for chords.py
#
#########################################################

import chords as ch
import unittest, random

class TestFindTones(unittest.TestCase):
    def test_simple(self):
        test_chords = [
                       #Simple chords
                       ('C', ['c', 'e', 'g']),
                       ('C 7', ['c', 'e', 'g', 'a#']),
                       ('C b5', ['c', 'e', 'f#']),
                       ('C m 7', ['c', 'd#', 'g', 'a#']),
                       ('E m', ['e', 'g', 'h']),
                       ('D dim', ['d', 'f', 'g#']),
                       ('F 7', ['f', 'a', 'c', 'eb']),
                       
                       #Complicated
                       ('c /e', ['e', 'c', 'g']),
                       ('e m 7 b5', ['e', 'g', 'a#', 'd']),
                       ('g m #7', ['g', 'a#', 'd', 'f#']),
                       ('g# m #7', ['g#', 'h', 'd#', 'g']),
                       ('a 6', ['a', 'c#', 'e', 'f#']),
                       
                       #Aug / sus
                       ('c aug b7', ['c', 'e', 'g#', 'a']),
                       ('d# aug', ['d#', 'g', 'h']),
                       ('f sus4', ['f', 'a#', 'c']),
                       ('d sus4', ['d', 'g', 'a'])
                       ]
        
        for chord, exp_tones in test_chords:
            tones, u = ch.find_tones(chord)
            
            exp = []
            for t in exp_tones:
                tone, u = ch.find_tone(t)
                exp.append(tone)
            
            self.assertEqual(set(tones), set(exp), '{0}, {1}'.format(tones, exp))
            
if __name__ == '__main__':
    unittest.main()