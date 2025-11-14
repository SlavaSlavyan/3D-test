import numpy

class Objects:
    
    def __init__(self):
        self.list = []
        self.last_id = 0
        
    class NewObject:
        
        def __init__(self, 
                     name: str,
                     id: int,
                     points: list,
                     polygons: list,
                     position: list,
                     rotation: list):
            
            self.name = name
            self.id = id
            self.polygons = polygons
            
            for polygon in self.polygons:
                
                for point in range(3):
                    
                    polygon[point] = numpy.array(points[polygon[point]])
            
            self.position = position
            self.rotation = rotation
    
    def create_new_object(self, 
                          name: str,
                          points: list,
                          polygons: list,
                          position: list,
                          rotation: list):
        
        self.list.append(self.NewObject(name,self.last_id,points,polygons,position,rotation))
        self.last_id += 1