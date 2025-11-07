import numpy
import turtle
import math
import copy
import time

class Objects:
    
    def __init__(self):
        self.list = []
        
    class Create:
        
        def __init__(
            self,
            name: str,
            points: list,
            polygons: list,
            position: list,
        ):
            
            self.name = name
            self.points = []
            for i in range(len(points)):
                self.points.append(points[i])
            self.polygons = polygons
            self.position = position
            #print(f"{self.name}\n{self.points}\n{self.polygons}\n{self.position}")

class Display:
    
    def __init__(self,m):
        
        self.Screen = turtle.Screen()
        self.Screen.setup(1200,800)
        turtle.bgcolor(0,0,0)
        turtle.pencolor(1,1,1)
        turtle.hideturtle()
        turtle.tracer(0)
        turtle.pensize(2)
    
    def main(self,m):
        
        self.width = self.Screen.window_width()
        self.height = self.Screen.window_height()
        
        turtle.clear()

        for obj in m.Objects.list:
            self.projection(m,copy.deepcopy(obj))
        
        turtle.update()
    
    def projection(self,m,obj):
        
        projection_matrix = numpy.array([
            [1/math.tan(m.config["FOV"]/2)*(self.height/self.width),0,0,0],
            [0,1/math.tan(m.config["FOV"]/2),0,0],
            [0,0,m.config["FAR"]/(m.config["FAR"]-m.config["NEAR"]),1],
            [0,0,-m.config["FAR"]*m.config["NEAR"]/(m.config["FAR"]-m.config["NEAR"]),0]
        ])
        
        #print(f"{obj.name}\n{obj.points}\n{obj.polygons}\n{obj.position}")
        
        polygons = []
        
        for polygon in obj.polygons:
            polygons.append([])
            
            for point_id in polygon:
                polygons[-1].append(numpy.array(obj.points[point_id].copy()) + obj.position)
                polygons[-1][-1] = numpy.append(polygons[-1][-1],1)
                
        projection_polygons = []
            
        for polygon in polygons:

            projection_polygons.append([])
            
            for point in range(3):
                
                polygon[point] = projection_matrix @ polygon[point]

                polygon[point] = polygon[point] / polygon[point][3]
                
                projection_polygons[-1].append([
                    polygon[point][0] / polygon[point][2],
                    polygon[point][1] / polygon[point][2]
                ])
        
        for polygon in projection_polygons:

            for point in range(3):
                
                turtle.teleport(
                    polygon[point-1][0]*self.width/2,
                    polygon[point-1][1]*self.height/2
                )
                
                turtle.goto(
                    polygon[point][0]*self.width/2,
                    polygon[point][1]*self.height/2
                )
            
class Main:
    
    def __init__(self):
        
        self.config = {
            "FOV":90,
            "FAR":100,
            "NEAR":0.01
        }
        
        self.Objects = Objects()
        self.Display = Display(self)
        
    def main(self):
        
        self.Objects.list.append(self.Objects.Create(
            "TestCube",
            [
                [-1.0, 1.0, 1.0],
                [-1.0,-1.0, 1.0],
                [ 1.0,-1.0, 1.0],
                [ 1.0, 1.0, 1.0],
                [-1.0, 1.0,-1.0],
                [-1.0,-1.0,-1.0],
                [ 1.0,-1.0,-1.0],
                [ 1.0, 1.0,-1.0]
            ],
            [
                [3,1,0],
                [3,2,1],
                [3,6,2],
                [3,7,6],
                [3,0,4],
                [3,4,7],
                [5,1,0],
                [5,0,4],
                [5,1,2],
                [5,2,6],
                [5,4,7],
                [5,7,6]
            ],
            [0,0,2]
        ))
        
        theta = 0
        
        while True:
            
            self.Display.main(self)
            #exit()
            
            self.Objects.list[0].position[0] = math.sin(theta)*5
            self.Objects.list[0].position[1] = math.cos(theta*2.5)*2
            self.Objects.list[0].position[2] = 5+math.cos(theta*3.7)
            
            theta += 0.01
            time.sleep(0.01)
    
M = Main()
M.main()