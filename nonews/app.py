'''
Created on 15 Nov 2012

@author: GB108544
'''
import random
import sys

import pygame
from pygame.locals import *
pygame.init()

from ui.ui import View
from ui.ui_widgets.badges import StoryBadge, EntityBadge
from ui.ui_widgets.badges import MOUSE_DAMPING


view=View()
ebs=[]

S=StoryBadge({'name':'Story1','headline':'Some Headline'})
view.add_badge(S)
view.focus_node(S)
ebs.append(S)
while True:
    for event in pygame.event.get():
        if event.type in [QUIT]:
            print 'QUIT'
            sys.exit()
        elif event.type==KEYDOWN and event.unicode==u' ':
            print 'KEYDOWN [space]'
            new_eb=EntityBadge({'name':'bob%d' % len(ebs)})
            ebs.append(new_eb)
            S.add_child(new_eb)
            view.add_badge(ebs[-1])
        elif event.type==KEYDOWN and event.unicode==u'd':
            print 'KEYDOWN [d]'
            S.remove_child(ebs[-1])
            view.remove_badge(ebs[-1])
            del(ebs[-1])
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
            view.focus_node(random.choice(ebs))
    view.render()