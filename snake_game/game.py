"""
Snake Game Implementation using PyGame
Controls: Arrow keys to move, Close window to quit
"""

# Import required libraries
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class c(object):
    """Represents individual segments of the snake and food items"""
    
    # Class variables for grid configuration
    rows = 20      # Number of grid rows
    w = 500        # Window width/height in pixels

    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        """
        Initialize a c object
        :param start: Starting (x,y) grid position
        :param dirnx: Initial x-direction (default: 1)
        :param dirny: Initial y-direction (default: 0)
        :param color: RGB color tuple (default: red)
        """
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        """Update c position based on direction"""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + dirnx, self.pos[1] + dirny)

    def draw(self, surface, eyes=False):
        """Draw c on game surface with optional eyes"""
        dis = self.w // self.rows  # Calculate grid cell size
        
        # Calculate pixel coordinates
        i, j = self.pos
        pygame.draw.rect(surface, self.color, 
                        (i*dis+1, j*dis+1, dis-2, dis-2))
        
        # Draw eyes on snake head
        if eyes:
            centre = dis // 2
            radius = 3
            # Eye positions
            circleMiddle = (i*dis + centre - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class Snake(object):
    """Main snake class handling movement and growth"""
    
    body = []      # List of c objects
    turns = {}     # Track turning points
    
    def __init__(self, color, pos):
        """Initialize snake with starting position and color"""
        self.color = color
        self.head = c(pos)  # Create head c
        self.body.append(self.head)
        self.dirnx = 0  # Initial direction: stationary
        self.dirny = 1  # Initial direction: down

    def move(self):
        """Handle movement and direction changes"""
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Handle direction changes
        if keys[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Move each cube in body
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                # Apply turn at this position
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)  # Remove completed turn
            else:
                # Handle screen wrapping
               if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
               elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
               elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
               elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
               else: c.move(c.dirnx,c.dirny)


    def reset(self, pos):
        """Reset snake to initial state"""
        self.head = c(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addc(self):
        """Add new c to snake body when eating food"""
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Determine position for new c based on tail direction
        if dx == 1 and dy == 0:
            self.body.append(c((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(c((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(c((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(c((tail.pos[0], tail.pos[1]+1)))

        # Set direction for new c
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        """Draw entire snake on surface"""
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # Draw eyes on head
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    """Draw grid lines on game surface"""
    sizeBtwn = w // rows  # Spacing between lines
    
    # Draw vertical and horizontal lines
    x = 0
    y = 0
    for _ in range(rows):
        x += sizeBtwn
        y += sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))


def redrawWindow(surface):
    """Refresh game display"""
    surface.fill((0,0,0))  # Clear screen with black
    s.draw(surface)        # Draw snake
    snack.draw(surface)    # Draw food
    drawGrid(width, rows, surface)  # Draw grid
    pygame.display.update()  # Update display


def randomSnack(rows, item):
    """Generate random food position avoiding snake body"""
    positions = item.body  # Get all snake positions
    
    # Find empty position
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Check if position is occupied
        if any(z.pos == (x,y) for z in positions):
            continue
        else:
            break
    return (x,y)


def message_box(subject, content):
    """Display game over message box"""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    """Main game loop"""
    global width, rows, s, snack
    width = 500       # Window size
    rows = 20         # Grid resolution
    
    # Initialize game window
    win = pygame.display.set_mode((width, width))
    s = Snake((255,0,0), (10,10))  # Red snake starting at center
    snack = c(randomSnack(rows, s), color=(0,255,0))  # Green food
    
    clock = pygame.time.Clock()  # Game speed control
    
    while True:
        pygame.time.delay(50)   # Short delay
        clock.tick(10)          # 10 FPS
        
        s.move()  # Handle movement
        
        # Check food collision
        if s.body[0].pos == snack.pos:
            s.addc()  # Grow snake
            snack = c(randomSnack(rows, s), color=(0,255,0))  # New food
        
        # Check self-collision
        for x in range(len(s.body)):
            if s.body[x].pos in [c.pos for c in s.body[x+1:]]:
                print("Score:", len(s.body))
                message_box('Game Over!', f'Score: {len(s.body)}\nPlay again...')
                s.reset((10,10))  # Reset snake
                break
        
        redrawWindow(win)  # Update display


if __name__ == "__main__":
    main() 