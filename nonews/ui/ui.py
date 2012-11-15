'''
Created on 7 Nov 2012

@author: AlienBaby
'''

import pygame
pygame.init()
        
class View(object):
    def __init__(self):
        self.window = pygame.display.set_mode((960, 540))
        pygame.display.set_caption('Nonews ui prototype')
        self.surface=pygame.display.get_surface()
        self.focus=None
        self.focus_change=False
        self.named_nodes={}
        self.nodes_to_add_in_tick=[]
        self.focus_erase_rect=[]
        self.focus_pos=(0,0)
        
    def focus_node(self,node):
        if self.focus:
            self.focus_erase_rect=self.focus.erase()
            self.focus.remove_children()
            self.focus.is_focus=False
            self.focus_pos=(self.focus.cx,self.focus.cy)
        self.focus=node
        self.focus.cx,self.focus.cy=self.focus_pos
        self.focus.is_focus=True
        self.focus_change=True
        
    def focus_do(self):
        self.focus.find_children()
        
        
    def add_badge(self,node):
        self.nodes_to_add_in_tick.append(node)
        node.surface=self.surface
        
    def remove_badge(self,node):
        del(self.named_nodes[node.data['name']])
        
    def render(self):
        #tick
        dirty_rects=[]
        nodes=self.named_nodes.values()
        for node in nodes:
            dirty_rects+=node.erase()
            
        #make focus change
        if self.focus_change:
            self.focus_do()
            self.focus_change=False
        
        #bring in new nodes
        for node in self.nodes_to_add_in_tick:
            self.named_nodes[node.data['name']]=node
        self.nodes_to_add_in_tick=[]
        nodes=self.named_nodes.values()
        
        #physics the things
        for node in nodes:
            node.tick_physics()
            
        #render the stuff
        for node in nodes:
            dirty_rects+=node.render()

        #draw all
        pygame.display.update(dirty_rects+self.focus_erase_rect)
        self.focus_erase_rect=[]
        
        #timing
        pygame.time.delay(1000/50)
              
