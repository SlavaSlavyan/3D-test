import pygame
import numpy

class Display:
    
    def __init__(self,m):
        pass
    
    def main(self,m):
        
        self.projection_matrix = self.create_projection_matrix(m)
        
        m.Disp.Screen.fill((0,0,0))
        
        for object in m.Scenes.Game.Objects.list:
            self.projection(m,object)
        
    def projection(self,m,object):
        
        pass

    def create_projection_matrix(self,m) -> list:
        
        hw = m.Disp.height/m.Disp.width
        f = m.config['FOV']
        zf = m.config['FAR']
        zn = m.config['NEAR']
        
        matrix = numpy.zeros(4,4)
        
        matrix[0][0] = hw * (1 / numpy.tan(f/2))
        matrix[1][1] = 1 / numpy.tan(f/2)
        matrix[2][2] = zf/(zf-zn)
        matrix[2][3] = (-zf*zn)/(zf-zn)
        matrix[3][2] = 1
        
        return matrix