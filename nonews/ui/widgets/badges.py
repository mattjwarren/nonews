'''
Created on 7 Nov 2012

@author: AlienBaby
'''
import math

import pygame
pygame.init()
    
font_big=pygame.font.SysFont([],20)
font_small=pygame.font.SysFont([],12)

#tunable constants
TICKS_TO_STOP=19.0 #19
MOUSE_DAMPING=10.0 #10
LOW_ENERGY_FACTOR=2.0 #4

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
        self.is_focus=False
        self.children=[]
        self.component_positions={}
             
    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        raise Exception("erase not implemented")
    
    def find_children(self):
        """Should return a list of badges representing this nodes children"""
        raise Exception("find_children not implemented")

    def layout_components(self):
        """set values in self.component_positions"""
        raise Exception("layout_components not implemented")
        
    def get_child_position(self,child):
        """Given a child, tell it where to draw itself"""
        raise Exception("get_child_position not implemented")

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
                #update internal positional references
                self.layout_components()
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

        #update internal positional references
        self.layout_components()
    
    def impulse_move(self,delta):
        self.vx=delta[0]
        self.xf=self.vx/TICKS_TO_STOP
        self.vy=delta[1]
        self.yf=self.vy/TICKS_TO_STOP
        
    def set_parent(self,new_parent):
        if (new_parent!=self.parent) and (new_parent!=self):
            if self.parent:
                self.parent.remove_child(self)
            self.parent=new_parent
            self.parent.add_child(self)
            
    def add_child(self,child):
        if (child not in self.children) and (child!=self):
            self.children.append(child)
            child.set_parent(self)

    def remove_child(self,child):
        if child and (not child.is_focus) and (not child==self):
            try:
                child_index=self.children.index(child)
            except:
                raise Exception("No Child to remove / Child to remove not found amongst my children / Child is myself.")
            child.parent=None
            self.children=self.children[0:child_index]+self.children[child_index+1:]
        
    def remove_children(self):
        for child in self.children:
            child.parent=None
        self.children=[]

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
        self.rendered_text['large_name']=font_big.render(self.data['name'], True, (255,0,0))
        self.rendered_text['small_name']=font_small.render(self.data['name'], True, (255,0,0))
        
        self.component_positions={}
        
    def layout_components(self):
        if self.is_focus:
            self.component_positions['shape_center']=(int(self.cx),int(self.cy))
            self.component_positions['shape_radius']=int(self.radius)
            self.component_positions['name']=(self.cx-self.radius/2.0,self.cy-self.radius/2.0)
            self.component_positions['rendered_text_name']=self.rendered_text['large_name']
        else:
            self.component_positions['shape_center']=(int(self.cx),int(self.cy))
            self.component_positions['shape_radius']=int(self.radius/2.0)
            self.component_positions['name']=(self.cx-self.radius/3.0,self.cy-self.radius/3.0)
            self.component_positions['rendered_text_name']=self.rendered_text['small_name']

    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
        background_rect=pygame.draw.circle(self.surface, self.border_color, self.component_positions['shape_center'], self.component_positions['shape_radius'], self.border_width)
        text_rect=self.surface.blit(self.component_positions['rendered_text_name'], self.component_positions['name'])

        return [background_rect,text_rect]
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        if self.is_focus:
            dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx),int(self.cy)), self.radius, self.border_width)
        else:
            dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx),int(self.cy)), int(self.radius/2.0), self.border_width)
        return [dirty_rect]

    def find_children(self,list_of_children=None):
        if not list_of_children:
            pass
        else:
            for child in list_of_children:
                child.set_parent(self)
            
    def get_child_position(self,child):
        if (not child) or (len(self.children)==0):
            raise Exception("No child to find, or I have no children.")
        else:
            try:
                child_position=self.children.index(child)
            except IndexError:
                raise Exception("Child is not amongst my children.")
            # arrange children like a clock
            x=self.cx+math.sin( ((2*math.pi)/len(self.children))*child_position )*180.0
            y=self.cy+math.cos( ((2*math.pi)/len(self.children))*child_position )*190.0
            return x,y
        
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
        self.rendered_text['headline']=font_big.render(self.data['headline'], True, (255,0,0))

        self.component_positions={}
        
    def layout_components(self):
        if self.is_focus:
            self.component_positions['headline']=(self.cx-self.width_x/2.0,self.cy-self.width_y/2.0)
            self.component_positions['shape']=pygame.Rect(self.cx-self.width_x/2.0,self.cy-self.width_y/2.0,self.width_x,self.width_y)
        else:
            self.component_positions['headline']=(self.cx-self.width_x/4.0,self.cy-self.width_y/4.0)
            self.component_positions['shape']=pygame.Rect(self.cx-self.width_x/4.0,self.cy-(self.width_y/4.0),self.width_x/2.0,self.width_y/2.0)
            
    def render(self):        
        background_rect=pygame.draw.rect(self.surface, self.border_color, self.component_positions['shape'], self.border_width)
        text_rect=self.surface.blit(self.rendered_text['headline'], self.component_positions['headline'])
        return [background_rect,text_rect]
            
    def erase(self):
        dirty_rect=pygame.draw.rect(self.surface, 0, self.component_positions['shape'], self.border_width)
        return [dirty_rect]

    def find_children(self,list_of_children=None):
        if not list_of_children:
            pass
        else:
            for child in list_of_children:
                child.set_parent(self)

    def get_child_position(self,child):
        if (not child) or (len(self.children)==0):
            raise Exception("No child to find, or I have no children.")
        else:
            try:
                child_position=self.children.index(child)
            except IndexError:
                raise Exception("Child is not amongst my children.")
            # arrange children like a clock
            x=self.cx+math.sin( ((2*math.pi)/len(self.children))*child_position )*180.0
            y=self.cy+math.cos( ((2*math.pi)/len(self.children))*child_position )*190.0
            return x,y
            
