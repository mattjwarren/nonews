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
class person_badge(object):
    
    def __init__(self,data,surface):
        self.data=data
        self.cx=325
        self.vx=0
        self.vy=0
        self.cy=325
        self.radius=50
        self.surface=surface
        self.border_color=(255,255,255)
        self.width=0
        self.rendered_text={}
        self.rendered_text['name']=font.render(self.data['name'], True, (255,0,0))

    def render(self):
        circle_rect=pygame.draw.circle(self.surface, self.border_color, (int(self.cx),int(self.cy)), self.radius, self.width)
        text_rect=self.surface.blit(self.rendered_text['name'], (self.cx,self.cy))
        return [circle_rect,text_rect]
    
    def erase(self):
        dirty_rect=pygame.draw.circle(self.surface, 0, (int(self.cx),int(self.cy)), self.radius, self.width)
        return [dirty_rect]
    
    def move(self):
        #erase
        erase_rects=self.erase()
        
        #add velocities
        self.cx+=self.vx
        self.cy+=self.vy
        #degrade velocities
        if int(self.vy*4)!=0:
            self.vy-=self.yf
        else:
            self.vy=0
        if int(self.vx*4)!=0:
            self.vx-=self.xf
        else:
            self.vx=0
        
        #render
        render_rects=self.render()

        return erase_rects+render_rects
    
    def accelerate(self,delta):
        self.vx=delta[0]
        self.xf=self.vx/19.0 #19 ticks to stop
        self.vy=delta[1]
        self.yf=self.vy/19.0
        
if __name__=='__main__':

    window = pygame.display.set_mode((750, 750))
    pygame.display.set_caption('Nonews ui prototype')

    display_surface = pygame.display.get_surface()


    pb=person_badge({'name':'Bob'},display_surface)
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
                delta_x=(mouse_up_x-mouse_down_x)/10.0
                delta_y=(mouse_up_y-mouse_down_y)/10.0
                pb.accelerate((delta_x,delta_y))

        #move all
        dirty_rects=pb.move()
        #draw all
        pygame.display.update(dirty_rects)
        
        #timing
        pygame.time.delay(1000/50)
        
