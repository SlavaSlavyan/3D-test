import pygame
import sys

from src.display.Main import Display
from src.input.Main import UserInput
from data.scenes.Main import Scenes

class Main:
    
    def __init__(self):
        
        self.config = {"FOV":90,
                       "FAR":64,
                       "NEAR":0.1}
        
        pygame.init()
        
        self.Disp = Display(self)
        self.UI = UserInput(self)
        self.Scenes = Scenes(self)
    
    def main(self):
        
        self.UI.main(self)
        
        self.Disp.main(self)
    
    def stop(self):
        
        pygame.quit()
        sys.exit()