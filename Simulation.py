import random
import time
import threading
import pygame
import sys

# Default values of signal timers
defaultGreen = {0: 15, 1: 15, 2: 15, 3: 15}
defaultRed = 120  # Red signal duration
defaultYellow = 5  # Yellow signal duration

signals = []
noOfSignals = 4  # Total number of signals
currentGreen = 0  # Indicates which signal is green currently
nextGreen = (currentGreen + 1) % noOfSignals  # Indicates which signal will turn green next
currentYellow = 0  # Indicates whether yellow signal is on or off

# Average speeds of vehicles
speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5, 'ambulance': 1.8, 'firetruck': 1.8}

# Coordinates of vehicles' start positions
x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

# Vehicle storage and types
vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0}, 'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}
emergency_vehicleTypes = {0: 'ambulance', 1: 'firetruck'}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# The 'stops' line is commented out because it is not currently used in the code:
# stops = {'right': [580, 580, 580], 'down': [320, 320, 320], 'left': [810, 810, 810], 'up': [545, 545, 545]}

# Gap between vehicles
stoppingGap = 15  # Stopping gap
movingGap = 15  # Moving gap

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0  # Indicates if the vehicle has crossed the stop line
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1

        # Determine the file extension based on vehicle class
        file_extension = "jpg" if vehicleClass in emergency_vehicleTypes.values() else "png"
        path = f"img/{direction}/{vehicleClass}.{file_extension}"
        self.image = pygame.image.load(path)

        # If more than 1 vehicle in the lane and the vehicle before it has not crossed the stop line
        if len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0:
            if direction == 'right':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].image.get_rect().width - stoppingGap
            elif direction == 'left':
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].image.get_rect().width + stoppingGap
            elif direction == 'down':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].image.get_rect().height - stoppingGap
            elif direction == 'up':
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Set new starting and stopping coordinate
        if direction == 'right':
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] -= temp
        elif direction == 'left':
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif direction == 'down':
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif direction == 'up':
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.direction == 'right':
            if self.crossed == 0 and self.x + self.image.get_rect().width > stopLines[self.direction]:
                self.crossed = 1  # Mark the vehicle as crossed the stop line
            if (self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (currentGreen == 0 and currentYellow == 0)) and (self.index == 0 or self.x + self.image.get_rect().width < (vehicles[self.direction][self.lane][self.index - 1].x - movingGap)):
                self.x += self.speed  # Move the vehicle
        elif self.direction == 'down':
            if self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]:
                self.crossed = 1
            if (self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (currentGreen == 1 and currentYellow == 0)) and (self.index == 0 or self.y + self.image.get_rect().height < (vehicles[self.direction][self.lane][self.index - 1].y - movingGap)):
                self.y += self.speed
        elif self.direction == 'left':
            if self.crossed == 0 and self.x < stopLines[self.direction]:
                self.crossed = 1
            if (self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][self.index - 1].image.get_rect().width + movingGap)):
                self.x -= self.speed
        elif self.direction == 'up':
            if self.crossed == 0 and self.y < stopLines[self.direction]:
                self.crossed = 1
            if (self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][self.index - 1].image.get_rect().height + movingGap)):
                self.y -= self.speed

def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(ts1.red + ts1.yellow + ts1.green + ts2.red + ts2.yellow + ts2.green, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(ts1.red + ts1.yellow + ts1.green + ts2.red + ts2.yellow + ts2.green + ts3.red + ts3.yellow + ts3.green, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()


def repeat():
    global currentGreen, currentYellow, nextGreen
    while(signals[currentGreen].green > 0):
        updateValues()
        time.sleep(1)

    currentYellow = 1

    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]

    while(signals[currentGreen].yellow > 0):
        updateValues()
        time.sleep(1)

    currentYellow = 0

    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen
    nextGreen = (currentGreen + 1) % noOfSignals
    signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green

    repeat()

def updateValues():
    for i in range(noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Constants for vehicle generation
SPAWN_INTERVAL = 90  # Spawn interval in seconds (1.5 minutes)
last_emergency_spawn_time = time.time()
last_spawn_time = time.time()

def generateVehicles():
    global last_emergency_spawn_time, last_spawn_time

    while True:
        # Determine time difference since last emergency vehicle spawn
        current_emergency_time = time.time()
        time_emergency_diff = current_emergency_time - last_emergency_spawn_time
        
        # Determine time difference since last regular vehicle spawn
        current_time = time.time()
        time_diff = current_time - last_spawn_time
        
        # Regular vehicle spawn
        vehicle_type = random.randint(0, 3)
        lane_number = random.randint(1, 2)
        direction_number = random.randint(0, 3)
        
        # Check if it's time to spawn an emergency vehicle
        if time_emergency_diff >= SPAWN_INTERVAL:
            # Spawn an emergency vehicle
            emergency_vehicle_type = random.randint(0, 1)  # Choose between ambulance and firetruck
            direction_number = random.randint(0, 3)
            Vehicle(lane_number, emergency_vehicleTypes[emergency_vehicle_type], direction_number, directionNumbers[direction_number])
            
            #Add the emergency detection code here and heat situation intiation
            


            
            # Update last emergency spawn time
            last_emergency_spawn_time = current_emergency_time
        
        # Check if it's time to spawn a regular vehicle
        if time_diff >= (SPAWN_INTERVAL - 85):
            Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
            last_spawn_time = current_time
        
        time.sleep(1)



class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, args=())
    thread1.daemon = True
    thread1.start()

    black = (0, 0, 0)
    white = (255, 255, 255)
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)
    background = pygame.image.load('img/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")
    redSignal = pygame.image.load('img/signals/red.png')
    yellowSignal = pygame.image.load('img/signals/yellow.png')
    greenSignal = pygame.image.load('img/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))
        # Loop through all signals
        for i in range(noOfSignals):
            # Check if the current signal is the green signal
            if i == currentGreen:
                # If the yellow signal is active, display the yellow signal timer
                if currentYellow == 1:
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    # Otherwise, display the green signal timer
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                # For all other signals, display the red signal timer
                signals[i].signalText = signals[i].red
                screen.blit(redSignal, signalCoods[i])

        # Initialize an empty list to hold signal text surfaces
        signalTexts = ["", "", "", ""]

        # Loop through all signals again to render the signal timer text
        for i in range(noOfSignals):
            # Render the signal timer text with a white font on a black background
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            # Display the rendered signal timer text at the corresponding coordinates
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # Loop through all vehicles in the simulation
        for vehicle in simulation:
            # Display the vehicle image at its current position
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            # Move the vehicle according to its direction and speed
            vehicle.move()

        # Update the display to reflect the changes
        pygame.display.update()


Main()
