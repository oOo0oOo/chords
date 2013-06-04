import chords as ch

ipanema = ['F #7', 'G 7', 'G m 7', 'F# 7', 'F #7', 'F# 9']

creep = ['G', 'H', 'C', 'C m', 'G', 'H', 'C', 'C m']

nothing_else_matters = [
'E m', 'D', 'C',
'E m', 'D', 'C',
'E m', 'D', 'C',
'G', 'H', 'E m', 

'C', 'A', 'D', 
'C', 'A', 'D',
'C', 'A', 'D',

'C'
]

funeral = [
'G', 'D', 'A', 'H m',
'G', 'D', 'A', 'H m',

'A', 'D', 'G',
'A', 'D', 'G',

'G', 'D', 'A', 'H m',
'G', 'D', 'A', 'H m',

'A', 'D', 'G',
'A', 'D', 'G'
]

print ch.quick_tab('D aug #6 9 b11', 1)

print ch.quick_song(funeral)