import pygame
from pygame.locals import *

from theory import *
import chords
import time

def render_lines(string):
    lines = string.splitlines()
    x = 180
    y = 120
    for line in lines:
        text = tab_font.render(line, True, (20, 20, 150))
        textRect = text.get_rect()
        textRect.left = x
        textRect.centery = y
        screen.blit(text, textRect)
        y += 24


def display(transpose):
        text = std_font.render(transpose, True, (20, 20, 150))
        textRect = text.get_rect()
        textRect.left = 50
        textRect.centery = 50
        screen.blit(text, textRect)


def create_msg(tones):
	regular = ', '.join([ sharp_map[t].title() for t in tones ])
	sax = ', '.join([ b_map[ (t+9) % 12 ].title() for t in tones ])

	return 'Regular:  {}       Sax:  {}'.format(regular, sax)


pygame.init()
screen = pygame.display.set_mode( (600,700) )
pygame.display.set_caption('Live Transposer')

std_font = pygame.font.Font(None, 40)
tab_font = pygame.font.Font(None, 30)

done = False
tones = []

cur_tabs = ''
cur_tones = []

while not done:
    screen.fill( (159, 182, 205) )

    display( create_msg(tones) )

    # Make tabs
    if len(tones) > 2 and cur_tones != tones:
	    tabs = chords.create_tabs(tones, position = 3)
	    ret = [ chords.convert_tab(tab) + '\n\n' for tab in tabs]
	    cur_tabs = ''.join(ret)
	    cur_tones = tones

    render_lines(cur_tabs)

    pygame.display.update()

    pygame.event.pump()
    keys = pygame.key.get_pressed()

    if keys[K_ESCAPE]:
        done = True

    tones = [pygame_key_map.index(k)%12 for k, v in enumerate(keys) if v and k in pygame_key_map]
    # stones = set(tones)
    time.sleep(0.01)