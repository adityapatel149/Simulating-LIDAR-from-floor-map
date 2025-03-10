import dis
import pygame
import math 
import numpy as np

def add_uncertainty(distance, angle, sigma):
    mean = np.array([distance, angle])
    cov = np.diag(sigma ** 2)
    distance, angle = np.random.multivariate_normal(mean, cov)
    distance = max(distance, 0)
    angle = max(angle, 0)
    return [distance, angle]


class LaserSensor:
    def __init__(self, range, map, uncertainty):
        self.range = range
        self.map = map
        self.speed = 4 #rounds per second
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0,0)
        self.W, self.H = pygame.display.get_surface().get_size()
        self.sensedObstacles = []

    def distance(self, obstaclePosition):
        px = (obstaclePosition[0] - self.position[0])**2
        py = (obstaclePosition[1] - self.position[1])**2
        return math.sqrt(px+py)

    def sense_obstacles(self):
        data = []
        x1, y1 = self.position

        # for all angles between 0 to 2pi, 60 angles
        for angle in np.linspace(0,2*math.pi, 60, False):
            # calculate end of line segment from position at distance = range
            x2, y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            # sampling
            for i in range(0, 100):
                # calculate a point on line segment using interpolation formula
                u = i/100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))

                # if calculated point within the window
                if 0 < x < self.W and 0 < y < self.H:
                    color = self.map.get_at((x,y))
                    if ((color[0],color[1],color[2]) == (0,0,0)):
                        distance = self.distance((x,y))
                        output = add_uncertainty(distance, angle, self.sigma)
                        output.append(self.position)

                        data.append(output)
                        break; # break loop if obstacle encountered. no need to check other points on line segment
        if len(data)>0:
            return data
        else:
            return False



