import cmd 
import chords as ch

class ChordsCLI(cmd.Cmd):
    '''A CLI where a simple read-print loop would do. Gotta love concious over-engineering...'''
    def preloop(self):
        self.chord_tones = []
        self.key = 0
        self.chord_progression = []
        self.relative_progression = []
        self.tone_progression = []
        
        text = 'Music Helper Command Line Interface'
        print text
        
    def do_exit(self, line):
        '''Exit this command line tool.'''
        return True
    
    def do_chord(self, line):
        try:
            chord, use_b = ch.find_tones(line)
            print ch.convert_chord(chord, use_b)   
        except Exception, e:
            print e

    def do_tab(self, line):
        try:
            print ch.quick_tab(line)
        except Exception, e:
            print e


cli = ChordsCLI()
cli.cmdloop()