'''
Created on 7 Nov 2012

@author: AlienBaby
'''
import sys
import pygame
import math
from pygame.locals import *
pygame.init()
    
font=pygame.font.SysFont([],25)
#Surface.blit(source, dest, area=None, special_flags = 0): return Rect

#tunable constants
TICKS_TO_STOP=19.0 #19
MOUSE_DAMPING=10.0 #10
LOW_ENERGY_FACTOR=4.0 #4



class UIBadge(object):
    def __init__(self):
        self.cx=0 #anchor X
        self.vx=0 #velocity X
        self.xf=0 #friction X
        self.vy=0 #   ~"~  as Y
        self.cy=0 #   ~"~  as Y
        self.yf=0 #   ~"~  as Y
        self.surface=None
        self.parent=None
        
    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")

    def get_shape(self):
        pass
    
    def tick(self):
        #erase
        erase_rects=self.erase()
        #apply physics
        self.tick_physics()
        #render
        render_rects=self.render()
        return erase_rects+render_rects

    def tick_physics(self):
        #if I have a parent, let them decide for me
        if hasattr(self,"parent"):
            if self.parent:
                #ask the parent where they would like me to be
                self.cx,self.cy=self.parent.get_child_position(self)
                return
        
        #apply velocity
        self.cx+=self.vx
        self.cy+=self.vy
        #degrade velocities
        if int(self.vy*LOW_ENERGY_FACTOR)!=0:
            self.vy-=self.yf
        else:
            self.vy=0
        if int(self.vx*LOW_ENERGY_FACTOR)!=0:
            self.vx-=self.xf
        else:
            self.vx=0
    
    def impulse_move(self,delta):
        self.vx=delta[0]
        self.xf=self.vx/TICKS_TO_STOP
        self.vy=delta[1]
        self.yf=self.vy/TICKS_TO_STOP
        
    def set_parent(self,new_parent):
        if new_parent!=self.parent:
            if self.parent:
                self.parent.remove_child(self)
            self.parent=new_parent
            self.parent.add_child(self)
            
    def add_child(self,child):
        if child not in self.children:
            self.children.append(child)
            child.set_parent(self)

    def remove_child(self,child):
        del(self.children[self.children.index(child)])

    def get_child_position(self,child):
        if (not child) or (len(self.children)==0):
            raise Exception("No child to find, or I have no children.")
        else:
            try:
                child_position=self.children.index(child)
            except IndexError:
                raise Exception("Child is not amongst my children.")
            #Stories arrange their children like a clock around them
            x=self.cx+math.sin( (math.pi/len(self.children))*child_position )*180.0
            y=self.cy+math.cos( (math.pi/len(self.children))*child_position )*190.0
            return x,y
            
class EntityBadge(UIBadge):
    """data: name"""
    def __init__(self,data):
        UIBadge.__init__(self)
        self.data=data
        
        self.radius=40
        self.border_color=(0,255,255)
        self.border_width=0 #/ solid fill
        self.shape_style='circle'
        
        self.rendered_text={}
        self.rendered_text['name']=font.render(self.data['name'], True, (255,0,0))
        
    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
                
        background_rect=pygame.draw.circle(self.surface, self.border_color, (int(self.cx),int(self.cy)), self.radius, self.border_width)
        text_rect=self.surface.blit(self.rendered_text['name'], (self.cx-self.radius/2.0,self.cy-self.radius/2.0))
        return [background_rect,text_rect]
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx),int(self.cy)), self.radius, self.border_width)
        return [dirty_rect]

        
class StoryBadge(UIBadge):
    def __init__(self,data):
        """data:  name,headline"""
        UIBadge.__init__(self)
        self.data=data
        
        self.width_x=240
        self.width_y=300
        self.border_color=(255,255,255)
        self.border_width=0 #/ solid fill
        self.shape_style='rectangle'
        
        self.rendered_text={}
        self.rendered_text['headline']=font.render(self.data['headline'], True, (255,0,0))

        self.children=[]
        
    def get_shape(self):
        return Rect(self.cx-self.width_x/2.0,self.cy-self.width_y/2.0,self.width_x,self.width_y)
    
    def render(self):
        #render all children
        dirty_child_rects=[]
        for child in self.children:
            dirty_child_rects+=child.render()
        
        background_rect=pygame.draw.rect(self.surface, self.border_color, self.get_shape(), self.border_width)
        text_rect=self.surface.blit(self.rendered_text['headline'], (self.cx-self.width_x/2.0,self.cy-self.width_y/2.0))
        return dirty_child_rects+[background_rect,text_rect]
    
    def erase(self):
        dirty_rect=pygame.draw.rect(self.surface, 0, Rect(self.cx-self.width_x/2.0,self.cy-self.width_y/2.0,self.width_x,self.width_y), self.border_width)
        return [dirty_rect]
    

class View(object):
    def __init__(self):
        self.window = pygame.display.set_mode((750, 750))
        pygame.display.set_caption('Nonews ui prototype')
        self.surface=pygame.display.get_surface()
        self.focus=None
        self.named_nodes={}
    
    def focus_node(self,node):
        self.focus=node
    
    def add_badge(self,node):
        self.named_nodes[node.data['name']]=node
        node.surface=self.surface
        
    def remove_badge(self,node):
        del(self.named_nodes[node.data['name']])
        
    def render(self):
        #tick
        dirty_rects=[]
        nodes=self.named_nodes.values()
        for node in nodes:
            dirty_rects+=node.erase()
        for node in nodes:
            node.tick_physics()
        for node in nodes:
            dirty_rects+=node.render()

        #draw all
        pygame.display.update(dirty_rects)
        
        #timing
        pygame.time.delay(1000/50)
              
if __name__=='__main__':

    view=View()

    E1=EntityBadge({'name':'Bob1'})
    E2=EntityBadge({'name':'Bob2'})
    E3=EntityBadge({'name':'Bob3'})
    E4=EntityBadge({'name':'Bob4'})
    S=StoryBadge({'name':'Story1','headline':'Some Story Headline'})
    S.add_child(E1)
    S.add_child(E2)
    S.add_child(E3)
    S.add_child(E4)
    view.add_badge(E1)
    view.add_badge(E2)
    view.add_badge(E3)
    view.add_badge(E4)
    view.add_badge(S)
    
    while 1:
        for event in pygame.event.get():
            if event.type in [QUIT]:
                sys.exit()
            elif event.type==KEYDOWN:
                eb=EntityBadge({'name':'bobbs'})
                S.add_child(eb)
                view.add_badge(eb)
            elif event.type==MOUSEBUTTONDOWN:
                mouse_down_x=event.pos[0]
                mouse_down_y=event.pos[1]
            elif event.type==MOUSEBUTTONUP:
                mouse_up_x=event.pos[0]
                mouse_up_y=event.pos[1]
                delta_x=(mouse_up_x-mouse_down_x)/MOUSE_DAMPING
                delta_y=(mouse_up_y-mouse_down_y)/MOUSE_DAMPING
                S.impulse_move((delta_x,delta_y))
        view.render()
