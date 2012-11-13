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

ebs=[]

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
                
    def render(self):
        """Should draw itself to self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        raise Exception("render not implemented")
    
    def find_children(self):
        """Should return a list of badges representing this nodes children"""

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
        print "I AM %s do I have a parent?" % str(self)
        if hasattr(self,"parent"):
            if self.parent:
                print "Yes I do! my parent is %s" % str(self.parent)
                #ask the parent where they would like me to be
                self.cx,self.cy=self.parent.get_child_position(self)
                return
        print "Nope :(, lets do some physics"
        #apply velocity
        print "\tcurrent position and vel_deltas are %f/%f %f/%f" % (self.cx,self.vx,self.cy,self.vy)
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
        child_index=self.children.index(child)
        child.parent=None
        self.children=self.children[0:child_index]+self.children[child_index+1:]
        
    def remove_children(self):
        print "removing children from %s" % str(self)
        for child in self.children:
            print "\tremoving: %s" % str(child)
            child.parent=None
        self.children=[]
            
    def get_child_position(self,child):
        if (not child) or (len(self.children)==0):
            raise Exception("No child to find, or I have no children.")
        else:
            try:
                child_position=self.children.index(child)
            except IndexError:
                raise Exception("Child is not amongst my children.")
            #Stories arrange their children like a clock around them
            x=self.cx+math.sin( ((2*math.pi)/len(self.children))*child_position )*180.0
            y=self.cy+math.cos( ((2*math.pi)/len(self.children))*child_position )*190.0
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
        #if i am the focus draw myself  twice as big as normal
        if self.is_focus:      
            background_rect=pygame.draw.circle(self.surface, self.border_color, (int(self.cx),int(self.cy)), self.radius, self.border_width)
            text_rect=self.surface.blit(self.rendered_text['name'], (self.cx-self.radius/2.0,self.cy-self.radius/2.0))
        else:
            background_rect=pygame.draw.circle(self.surface, self.border_color, (int(self.cx),int(self.cy)), int(self.radius/2.0), self.border_width)
            text_rect=self.surface.blit(self.rendered_text['name'], (self.cx-self.radius/2.0,self.cy-self.radius/2.0))

        return [background_rect,text_rect]
    
    def erase(self):
        """Should erase itself from self.surface and return a list of dirty rectangles"""
        if self.is_focus:
            dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx),int(self.cy)), self.radius, self.border_width)
        else:
            dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx/2.0),int(self.cy/2.0)), int(self.radius/2.0), self.border_width)
        return [dirty_rect]

    def find_children(self):
        for child in ebs:
            child.set_parent(self)
        
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

    def find_children(self):
        for child in ebs:
            child.set_parent(self)
            
class View(object):
    def __init__(self):
        self.window = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption('Nonews ui prototype')
        self.surface=pygame.display.get_surface()
        self.focus=None
        self.focus_change=False
        self.named_nodes={}
        self.nodes_to_add_in_tick=[]
        
    def focus_node(self,node):
        if self.focus:
            self.focus.remove_children()
            self.focus.is_focus=False
        self.focus=node    
        self.focus.is_focus=True
        
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
        self.focus_do()
        
        #bring in new nodes
        for node in self.nodes_to_add_in_tick:
            self.named_nodes[node.data['name']]=node
        self.nodes_to_add_in_tick=[]
        
        for node in nodes:
            node.tick_physics()
        for node in nodes:
            dirty_rects+=node.render()

        #draw all
        pygame.display.update(dirty_rects)
        
        #timing
        pygame.time.delay(1000/2)
              
if __name__=='__main__':

    view=View()

    S=StoryBadge({'name':'Story1','headline':'Some Story Headline'})
    view.add_badge(S)
    view.focus_node(S)
    ebs.append(S)
    while 1:
        for event in pygame.event.get():
            if event.type in [QUIT]:
                print 'QUIT'
                sys.exit()
            elif event.type==KEYDOWN:
                print 'KEYDOWN'
                new_eb=EntityBadge({'name':'bob%d' % len(ebs)})
                ebs.append(new_eb)
                S.add_child(new_eb)
                view.add_badge(ebs[-1])
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
                S.impulse_move((delta_x,delta_y))
            elif event.type==MOUSEBUTTONDOWN and event.button==2:
                print 'DOWN BUTTON 2'
                view.focus_node(ebs[2])
        view.render()
