# Import a library of functions called 'pygame'
import pygame
import numpy as np
from math import pi, sin, cos, tan

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Point3D:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
class Line3D():

    def __init__(self, start, end):
        self.start = start
        self.end = end

def loadOBJ(filename):
    
    vertices = []
    indices = []
    lines = []

    f = open(filename, "r")
    for line in f:
        t = str.split(line)
        if not t:
            continue
        if t[0] == "v":
            vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
            
        if t[0] == "f":
            for i in range(1,len(t) - 1):
                index1 = int(str.split(t[i],"/")[0])
                index2 = int(str.split(t[i+1],"/")[0])
                indices.append((index1,index2))
            
    f.close()

    #Add faces as lines
    for index_pair in indices:
        index1 = index_pair[0]
        index2 = index_pair[1]
        lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
        
    #Find duplicates
    duplicates = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]
            
            # Case 1 -> Starts match
            if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
                if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
                    duplicates.append(j)
            # Case 2 -> Start matches end
            if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
                if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
                    duplicates.append(j)
                    
    duplicates = list(set(duplicates))
    duplicates.sort()
    duplicates = duplicates[::-1]

    #Remove duplicates
    for j in range(len(duplicates)):
        del lines[duplicates[j]]

    return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    
    return tire


DISPLAY_HEIGHT = 512
DISPLAY_WIDTH = 512

# Global variables for camera position and properties
CAMERA_LOCATION = np.array([0.0, 0.0, 10.0])
CAMERA_YROTATE = np.deg2rad(180)
NEAR_FIELD = 1.0
FAR_FIELD = 1000
XFOV = np.deg2rad(100)
YFOV = np.deg2rad(100)


# Implement world-to-camera and camera-to-projection matrices
# Will return all steps in single matrix 
def buildProjectionMatrix():	

    translateMatrix = np.array([[1, 0, 0, -CAMERA_LOCATION[0]],
                                [0, 1, 0, -CAMERA_LOCATION[1]],
                                [0, 0, 1, -CAMERA_LOCATION[2]],
                                [0, 0, 0,  1]]) 
    
    rotateMatrix = np.array([   [np.cos(CAMERA_YROTATE), 0, -np.sin(CAMERA_YROTATE), 0],
                                [0, 1, 0, 0],
                                [np.sin(CAMERA_YROTATE), 0, np.cos(CAMERA_YROTATE), 0],
                                [0, 0, 0, 1]
                            ])
    
    zoomx = 1 / np.tan(XFOV / 2)
    zoomy = 1 / np.tan(YFOV / 2)
    z3 = (FAR_FIELD + NEAR_FIELD) / (FAR_FIELD - NEAR_FIELD)
    z4 = (-2 * NEAR_FIELD * FAR_FIELD) / (FAR_FIELD - NEAR_FIELD)

    projectionMatrix = np.array([
        [zoomx, 0, 0, 0],
        [0, zoomy, 0, 0],
        [0, 0, z3, z4],
        [0, 0, 1, 0]
    ])

    worldToCameraMatrix = np.linalg.multi_dot([projectionMatrix, rotateMatrix, translateMatrix])
    return worldToCameraMatrix



def clipTest(pt1,pt2):

    # Homogenous coords
    w1, x1, y1, z1 = pt1[3, 0], pt1[0, 0], pt1[1, 0], pt1[2, 0]
    w2, x2, y2, z2 = pt2[3, 0], pt2[0, 0], pt2[1, 0], pt2[2, 0]

    # Clip tests
    if (z1 < NEAR_FIELD and z2 < NEAR_FIELD) or (z1 > FAR_FIELD and z2 > FAR_FIELD):
        return False
    if (x1 < -w1 and x2 < -w2) or (x1 > w1 and x2 > w2) or (y1 < -w1 and y2 < -w2) or (y1 > w1 and y2 > w2):
        return False

    # Passed tests
    return True




def toScreen(pt):
    
    # Prevent division by zero
    def safe_divide(numerator, denominator, default=0.0):
        return numerator / denominator if denominator else default

    x_hd = safe_divide(pt.item(0), pt.item(3))
    y_hd = safe_divide(pt.item(1), pt.item(3))
    
    normalizedXY = np.array([[x_hd], [y_hd], [1]])
    viewportTransMatrix = np.array([[DISPLAY_WIDTH/2, 0, DISPLAY_WIDTH/2],
                                    [0, -DISPLAY_HEIGHT/2, DISPLAY_HEIGHT/2],
                                    [0, 0, 1]]) 

    screenMatrix = viewportTransMatrix @ normalizedXY

    x_screen = screenMatrix.item(0)
    y_screen = screenMatrix.item(1)

    return Point(x_screen, y_screen)



# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [DISPLAY_WIDTH, DISPLAY_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
linelist = loadHouse()

#Loop until the user clicks the close button.
while not done:
 
    # This limits the while loop to a max of 100 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(100)

    # Clear the screen and set the screen background
    screen.fill(BLACK)

    #Controller Code#
    #####################################################################

    movement_speed = 0.25  # Units per key press
    rotation_angle = np.deg2rad(2)  # Rotate 2 degrees per key press

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True


    # Calculate the camera's forward and right vectors based on the current rotation
    forward = np.array([
        np.sin(CAMERA_YROTATE),
        0,
        np.cos(CAMERA_YROTATE)
    ])
    right = np.array([
        np.cos(CAMERA_YROTATE),
        0,
        -np.sin(CAMERA_YROTATE)
    ])
    

    pressed = pygame.key.get_pressed()

    # Apply movement
    if pressed[pygame.K_w]:  # Move Forward
        CAMERA_LOCATION += forward * movement_speed
    if pressed[pygame.K_s]:  # Move Backward
        CAMERA_LOCATION -= forward * movement_speed
    if pressed[pygame.K_a]:  # Move Left
        CAMERA_LOCATION -= right * movement_speed
    if pressed[pygame.K_d]:  # Move Right
        CAMERA_LOCATION += right * movement_speed
    if pressed[pygame.K_e]:  # Rotate Left
        CAMERA_YROTATE += rotation_angle
    if pressed[pygame.K_q]:  # Rotate Right
        CAMERA_YROTATE -= rotation_angle
    if pressed[pygame.K_r]:  # Move Up
        CAMERA_LOCATION[1] += movement_speed
    if pressed[pygame.K_f]:  # Move Down
        CAMERA_LOCATION[1] -= movement_speed

    # Reset to home position
    if pressed[pygame.K_h]:  # Return to Home Position
        CAMERA_LOCATION = np.array([0.0, 0.0, 10.0])
        CAMERA_YROTATE = np.deg2rad(180)
        


    #Viewer Code#
    #####################################################################

    project = buildProjectionMatrix()

    for s in linelist:
        
        pt1_w = np.matrix([[s.start.x],[s.start.y],[s.start.z],[1]])
        pt2_w = np.matrix([[s.end.x],[s.end.y],[s.end.z],[1]])
        
        pt1_c = project*pt1_w
        pt2_c = project*pt2_w
        
        if clipTest(pt1_c,pt2_c):
            pt1_s = toScreen(pt1_c)
            pt2_s = toScreen(pt2_c)
            pygame.draw.line(screen, BLUE, (pt1_s.x, pt1_s.y), (pt2_s.x, pt2_s.y))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
