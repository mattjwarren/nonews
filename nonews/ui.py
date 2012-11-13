'''
Created on 7 Nov 2012

@author: AlienBaby
'''
import sys
import pygame
from pygame.locals import *
pygame.init()
    
font=pygame.font.SysFont([],25)
#Surface.blit(source, dest, area=None, special_flags = 0): return Rect

#tunable constants
TICKS_TO_STOP=19.0 #19
MOUSE_DAMPING=10.0 #10
LOW_ENERGY_FACTOR=4.0 #4



class UIBadge(object):
    def __init__(self,surface):
        self.cx=0 #anchor X
        self.vx=0 #velocity X
        self.xf=0 #friction X
        self.vy=0 #   ~"~  as Y
        self.cy=0 #   ~"~  as Y
        self.yf=0 #   ~"~  as Y
        self.surface=surface
        
    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")

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
                self.cx,self.cy=self.parent.get_child_position(child=self)
                return

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
        
    def set_parent(self,parent):
        parent.add_child(self)
        self.parent=parent

class PersonBadge(UIBadge):
    """data: name"""
    def __init__(self,data,surface):
        UIBadge.__init__(self,surface)
        self.data=data
        
        self.radius=30
        self.border_color=(255,255,255)
        self.border_width=0 #/ solid fill
        self.shape_style='circle'
        
        self.rendered_text={}
        self.rendered_text['name']=font.render(self.data['name'], True, (255,0,0))

    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
                
        background_rect=pygame.draw.circle(self.surface, self.border_color, (int(self.cx),int(self.cy)), self.radius, self.border_width)
        text_rect=self.surface.blit(self.rendered_text['name'], (self.cx,self.cy))
        return [background_rect,text_rect]
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx),int(self.cy)), self.radius, self.width)
        return [dirty_rect]

        
class StoryBadge(UIBadge):
    def __init__(self,data,surface):
        """data:  headline"""
        UIBadge.__init__(self,surface)
        self.data=data
        
        self.width_x=75
        self.width_y=60
        self.border_color=(255,255,255)
        self.border_width=0 #/ solid fill
        self.shape_style='rectangle'
        
        self.rendered_text={}
        self.rendered_text['headline']=font.render(self.data['headline'], True, (255,0,0))

        self.children=[]
        
    def get_child_position(self,child=None):
        if (not child) or (len(self.children)==0):
            raise Exception("No child to get position for")
        else:
            #Stories arrange their children like a clock around them, every 11.25 degrees
            pass

    def render(self):
        #render all children
        dirty_child_rects=[]
        for child in self.children:
            dirty_child_rects+=child.render()
        
        background_rect=pygame.draw.rect(self.surface, self.border_color, Rect(self.cx-self.width_x/2.0,self.cy-self.width_y/2.0,self.width_x,self.width_y), self.border_width)
        text_rect=self.surface.blit(self.rendered_text['headline'], (self.cx,self.cy))
        return dirty_child_rects+[background_rect,text_rect]
    
    def erase(self):
        dirty_rect=pygame.draw.rect(self.surface, 0, Rect(self.cx-self.width_x/2.0,self.cy-self.width_y/2.0,self.width_x,self.width_y), self.border_width)
        return [dirty_rect]
    
    def move(self):
        #erase
        erase_rects=self.erase()
        
        #add velocities
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
        
        #render
        render_rects=self.render()

        return erase_rects+render_rects
    
    def accelerate(self,delta):
        self.vx=delta[0]
        self.xf=self.vx/TICKS_TO_STOP
        self.vy=delta[1]
        self.yf=self.vy/TICKS_TO_STOP

    def add_child(self,child):
        self.children.append(child)
        child.set_parent(self)

if __name__=='__main__':

    window = pygame.display.set_mode((750, 750))
    pygame.display.set_caption('Nonews ui prototype')

    display_surface = pygame.display.get_surface()


    pb=PersonBadge({'name':'Bob'},display_surface)
    dirty_rect=pb.render()

    while 1:
        dirty_rects=[]
        for event in pygame.event.get():
            if event.type in (QUIT,KEYDOWN):
                sys.exit()
            elif event.type==MOUSEBUTTONDOWN:
                mouse_down_x=event.pos[0]
                mouse_down_y=event.pos[1]
            elif event.type==MOUSEBUTTONUP:
                mouse_up_x=event.pos[0]
                mouse_up_y=event.pos[1]
                delta_x=(mouse_up_x-mouse_down_x)/MOUSE_DAMPING
                delta_y=(mouse_up_y-mouse_down_y)/MOUSE_DAMPING
                pb.accelerate((delta_x,delta_y))

        #move all
        dirty_rects=pb.move()
        #draw all
        pygame.display.update(dirty_rects)
        
        #timing
        pygame.time.delay(1000/50)
        
