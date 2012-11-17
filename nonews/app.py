'''
Created on 15 Nov 2012

@author: GB108544
'''
import random
import sys


import pygame
from pygame.locals          import *
pygame.init()

from ui.views.simple_view   import View
from ui.widgets.badges      import StoryBadge, EntityBadge
from ui.widgets.badges      import MOUSE_DAMPING
from db.simple_connections  import sqlite3_connection

db=sqlite3_connection("test.db")


view=View(display_mode=(960,540),display_name="nonews UI Prototype")

S=StoryBadge(name='Story1',headline='Some Headline',data={})
view.add_node(S)
view.focus_node(S)

while True:
    for event in pygame.event.get():
        if event.type in [QUIT]:
            print 'QUIT'
            sys.exit()
        elif event.type==KEYDOWN and event.unicode==u' ':
            print 'KEYDOWN [space]'
            new_eb=EntityBadge(name='bob%d' % len(view.named_nodes.values()),
                               data={})
            view.add_node(new_eb)
        elif event.type==KEYDOWN and event.unicode==u'd':
            print 'KEYDOWN [d]'
            if view.nodes:
                view.remove_node(view.nodes[-1])
        elif event.type==MOUSEBUTTONDOWN and event.button==1:
            print 'DOWN BUTTON 1'
            mouse_down_x=event.pos[0]
            mouse_down_y=event.pos[1]
        elif event.type==MOUSEBUTTONUP and event.button==1:
            print 'UP BUTTON 1'
            mouse_up_x=event.pos[0]
            mouse_up_y=event.pos[1]
            delta_x=(mouse_up_x-mouse_down_x)/MOUSE_DAMPING
            delta_y=(mouse_up_y-mouse_down_y)/MOUSE_DAMPING
            view.focus.impulse_move((delta_x,delta_y))
        elif event.type==MOUSEBUTTONDOWN and event.button==2:
            print 'DOWN BUTTON 2'
            view.focus_node(random.choice(view.nodes))
    view.render()