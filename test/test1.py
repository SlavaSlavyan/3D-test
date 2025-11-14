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
            rotate: list
        ):
            
            self.name = name
            self.points = []
            for i in range(len(points)):
                self.points.append(points[i])
            self.polygons = polygons
            self.position = position
            self.rotate = rotate
            #print(f"{self.name}\n{self.points}\n{self.polygons}\n{self.position}")

class Display:
    
    def __init__(self,m):
        
        self.Screen = turtle.Screen()
        self.Screen.setup(1200,800)
        turtle.bgcolor(0,0,0)
        turtle.pencolor(1,1,1)
        turtle.hideturtle()
        turtle.tracer(0)
        turtle.pensize(1)
    
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

        rotate_matrix_x = numpy.array([
            [1,0,0],
            [0,math.cos(obj.rotate[0]),-math.sin(obj.rotate[0])],
            [0,math.sin(obj.rotate[0]),math.cos(obj.rotate[0])]
        ])

        rotate_matrix_y = numpy.array([
            [math.cos(obj.rotate[1]),0,math.sin(obj.rotate[1])],
            [0,1,0],
            [-math.sin(obj.rotate[1]),0,math.cos(obj.rotate[1])]
        ])

        rotate_matrix_z = numpy.array([
            [math.cos(obj.rotate[2]),-math.sin(obj.rotate[2]),0],
            [math.sin(obj.rotate[2]),math.cos(obj.rotate[2]),0],
            [0,0,1]
        ])

        rotate_matrix = rotate_matrix_x * rotate_matrix_y * rotate_matrix_z
        
        #print(f"{obj.name}\n{obj.points}\n{obj.polygons}\n{obj.position}")
        
        polygons = []
        
        for polygon in obj.polygons:

            new_polygon = []
            
            for point_id in polygon:

                new_polygon.append(numpy.array(obj.points[point_id].copy()))
                new_polygon[-1] = rotate_matrix_x @ new_polygon[-1]
                new_polygon[-1] = rotate_matrix_y @ new_polygon[-1]
                new_polygon[-1] = rotate_matrix_z @ new_polygon[-1]
                new_polygon[-1] = new_polygon[-1] + obj.position
                new_polygon[-1] = numpy.append(new_polygon[-1],1)
            
            #print(new_polygon)
            
            A = new_polygon[-1][:3] - new_polygon[0][:3]
            B = new_polygon[1][:3] - new_polygon[0][:3]

            normal = numpy.cross(A,B)
            normal = normal/numpy.linalg.norm(normal)

            to_cam = new_polygon[0][:3] + new_polygon[1][:3] + new_polygon[2][:3] / 3
            to_cam = to_cam/numpy.linalg.norm(to_cam)

            if numpy.dot(normal,to_cam) < 0:
                
                polygons.append(new_polygon)

        #print(polygons[0][-1][:3],polygons[0][0][:3])
        #print(numpy.cross(polygons[0][-1][:3],polygons[0][0][:3]))

        #p = 10
        #ac = polygons[p][-1][:3] - polygons[p][0][:3]
        #ab = polygons[p][1][:3] - polygons[p][0][:3]
        #n = numpy.cross(ab,ac)

        #c = -polygons[p][0][:3] + polygons[p][1][:3] + polygons[p][2][:3] / 3
        #c = c/numpy.linalg.norm(c)

        #print(numpy.dot(n,c) > 0)

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

        
        
        #turtle.teleport(
        #    projection_polygons[p][0][0]*self.width/2,
        #    projection_polygons[p][0][1]*self.height/2
        #)

        #turtle.pencolor("red")
        #turtle.circle(5)
        #turtle.pencolor("white")

        #turtle.teleport(
        #    projection_polygons[p][1][0]*self.width/2,
        #    projection_polygons[p][1][1]*self.height/2
        #)

        #turtle.pencolor("green")
        #turtle.circle(5)
        #turtle.pencolor("white")

        #turtle.teleport(
        #    projection_polygons[p][2][0]*self.width/2,
        #    projection_polygons[p][2][1]*self.height/2
        #)

        #turtle.pencolor("blue")
        #turtle.circle(5)
        #turtle.pencolor("white")
            
class Main:
    
    def __init__(self):
        
        self.config = {
            "FOV":90,
            "FAR":64,
            "NEAR":0.1
        }
        
        self.Objects = Objects()
        self.Display = Display(self)
        
    def main(self):
        
        self.Objects.list.append(self.Objects.Create(
            "TestCube",
            [
                [ 1.0, 1.0, 1.0],
                [-1.0, 1.0, 1.0],
                [ 1.0,-1.0, 1.0],
                [ 1.0, 1.0,-1.0],
                [ 1.0,-1.0,-1.0],
                [-1.0, 1.0,-1.0],
                [-1.0,-1.0, 1.0],
                [-1.0,-1.0,-1.0]
            ],
            [
                [0,2,6],
                [0,6,1],
                [0,4,2],
                [0,3,4],
                [0,5,3],
                [0,1,5],
                [7,2,4],
                [7,6,2],
                [7,1,6],
                [7,5,1],
                [7,4,3],
                [7,3,5]
            ],
            [5,0,5],
            [math.radians(0),math.radians(0),0]
        ))
        
        self.Objects.list.append(self.Objects.Create(
            "TestCube",
            [
                [ 1.0, 1.0, 1.0],
                [-1.0, 1.0, 1.0],
                [ 1.0,-1.0, 1.0],
                [ 1.0, 1.0,-1.0],
                [ 1.0,-1.0,-1.0],
                [-1.0, 1.0,-1.0],
                [-1.0,-1.0, 1.0],
                [-1.0,-1.0,-1.0]
            ],
            [
                [0,2,6],
                [0,6,1],
                [0,4,2],
                [0,3,4],
                [0,5,3],
                [0,1,5],
                [7,2,4],
                [7,6,2],
                [7,1,6],
                [7,5,1],
                [7,4,3],
                [7,3,5]
            ],
            [-5,0,5],
            [math.radians(0),math.radians(0),0]
        ))

        theta = 0

        while True:
            
            start = time.time()
            
            self.Display.main(self)
            #exit()

            self.Objects.list[0].rotate[0] = math.radians(theta)
            #self.Objects.list[0].rotate[1] = math.radians(theta)
            #self.Objects.list[0].rotate[2] = math.radians(theta)

            self.Objects.list[1].position[2] = 3+math.sin(theta/10)
            #self.Objects.list[0].position[0] = math.cos(theta/15)*20

            theta += 1
            
            end = time.time()
            
            
            if end - start < 1/60:
                time.sleep(1/60 - (end - start))
    
M = Main()
M.main()