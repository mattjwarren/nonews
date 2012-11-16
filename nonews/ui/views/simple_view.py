'''
Created on 7 Nov 2012

@author: AlienBaby
'''
from argtools.validation import process_kwargs
import pygame
pygame.init()
        
class View(object):
    def __init__(self,**kwargs):
        process_kwargs(self,
                       #required
                       ["display_mode","display_name"],
                       #with defaults
                       None,
                       #keywords
                       kwargs)
        self.window = pygame.display.set_mode(self.display_mode)
        pygame.display.set_caption(self.display_name)
        self.surface=pygame.display.get_surface()
        self.focus=None
        self._focus_change=False
        self.named_nodes={}
        self.nodes=[]
        self._nodes_to_add_in_tick=[]
        self._nodes_to_remove_in_tick=[]
        self._focus_erase_rect=[]
        self.focus_pos=(0,0)
        
    def focus_node(self,node):
        if self.focus:
            self._focus_erase_rect=self.focus.erase()
            self.focus.remove_children()
            self.focus.is_focus=False
            self.focus_pos=(self.focus.cx,self.focus.cy)
        self.focus=node
        self.focus.cx,self.focus.cy=self.focus_pos
        self.focus.is_focus=True
        self._focus_change=True

    def add_node(self,node):
        if node not in self.nodes:
            self._nodes_to_add_in_tick.append(node)
            node.surface=self.surface
        else:
            raise Exception("Attempt to add a node that has already been added.")
        
    def remove_node(self,node):
        if node in self.nodes:
            if node!=self.focus:
                self._nodes_to_remove_in_tick.append(node)
        else:
            raise Exception("Node not found to remove.")
        

    def render(self):
        #tick
        dirty_rects=self._erase_nodes()
        
        #make focus change
        self._perform_focus_change()
        
        #take out removed nodes
        self._take_out_nodes()
        
        #bring in new nodes
        self._bring_in_new_nodes()
        
        #physics the things
        for node in self.nodes:
            node.tick_physics()
            
        #render the stuff
        for node in self.nodes:
            dirty_rects+=node.render()

        #draw all
        pygame.display.update(dirty_rects+self._focus_erase_rect)
        self._focus_erase_rect=[]
        
        #timing
        pygame.time.delay(1000/50)
        
    def _focus_do(self):
        print 'doing _focus_do'
        self.focus.find_children(list_of_children=self.nodes)
            
    def _erase_nodes(self):
        dirty_rects=[]
        for node in self.nodes:
            dirty_rects+=node.erase()
        return dirty_rects
    
    def _perform_focus_change(self):
        if self._focus_change:
            self._focus_do()
            self._focus_change=False
            
    def _bring_in_new_nodes(self):
        for node in self._nodes_to_add_in_tick:
            if node not in self.nodes:
                self.named_nodes[node.name]=node
                self.nodes.append(node)
                self.focus.add_child(node)
            else:
                raise Exception("Attempt to add a node that has already been added.")
        self._nodes_to_add_in_tick=[]
        
    def _take_out_nodes(self):
        for node in self._nodes_to_remove_in_tick:
            if node in self.nodes:
                del(self.named_nodes[node.name])
                node_index=self.nodes.index(node)
                self.nodes=self.nodes[0:node_index]+self.nodes[node_index+1:]
                self.focus.remove_child(node)
            else:
                raise Exception("Cannot remove node %s, node not found." % node)
        self._nodes_to_remove_in_tick=[]
        