import turtle
import math
import numpy
import threading

Screen = turtle.Screen()
Screen.setup(1200,800)
turtle.bgcolor(0,0,0)
turtle.pencolor(1,1,1)
turtle.hideturtle()
turtle.tracer(0)

FOV = 90
FAR = 9999
NEAR = 0.01

class Block:

    def __init__(self):
        
        self.points = [
            numpy.array(
                [[-1,-1,0,1],[1,-1,0,1],[1,1,0,1]]
            )
        ]

        for i in range(len(self.points)):
            self.points[i] += [0,0,1,0]
        
        print(*self.points)
        
Block0 = Block()

def display():
    
    projection_matrix = numpy.array([
        [1/math.tan(FOV/2)*(height/width),0,0,0],
        [0,1/math.tan(FOV/2),0,0],
        [0,0,FAR/(FAR-NEAR),1],
        [0,0,-FAR*NEAR/(FAR-NEAR),0]
    ])
    new_array = []
    for i in range(3):
        arr = projection_matrix*Block0.points[0][i]
        arr = numpy.sum(arr, axis=0)

        arr = arr/arr[3]
        #print(arr)
        new_array.append([arr[0]/arr[2],arr[1]/arr[2]])
    
    for i in range(3):
        turtle.teleport(new_array[i-1][0]*width/2,new_array[i-1][1]*height/2)
        turtle.goto(new_array[i][0]*width/2,new_array[i][1]*height/2)

def PI():

    global Block0

    while True:
        try:
            exec(input(">"))
        except:
            print('[ERROR]')

thread = threading.Thread(target=PI)
thread.start()

while True:

    height = Screen.window_height()
    width = Screen.window_height()

    turtle.clear()

    display()

    turtle.update()