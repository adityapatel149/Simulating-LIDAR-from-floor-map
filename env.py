import math
import pygame

class buildEnvironment:
    def __init__(self, MapImage):
        pygame.init()
        self.pointCloud = []
        self.maph, self.mapw = (MapImage.get_height(),  MapImage.get_width())
        self.MapWindowName = 'RRT Path Planning'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(MapImage, (0,0))

        # Colors
        self.black = (0, 0, 0)
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
    
    # get point from angle,distance data
    def AD2pos(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]
        return (int(x), int(y))
    
    # convert raw sensor data to cartesian coordinates to show on map and store in pointcloud list
    def dataStorage(self, data):
        if data:
            for element in data:
                point = self.AD2pos(element[0], element[1], element[2])
                if point not in self.pointCloud:
                    self.pointCloud.append(point)

    def show_sensorData(self):
        self.infomap = self.map.copy()
        for point in self.pointCloud:
            self.infomap.set_at((int(point[0]), int(point[1])), self.red)
