# ----| IMPORTS |----

import pygame # Library used for graphics
import json # To read from the JSON file
import time # For eeping
import math # Wonder what this is for...
import sys # Used to exit the app


# ----| PARAMETERS |----
with open("data/settings.json", "r") as file: # Load settings from JSON file
    data = json.load(file)
    screenwidth = data["scr_width"]

# ----| PYGAME SETUP |----

# Initialize Pygame
pygame.init()
# Set up display
width = screenwidth
height = width * 1.5 # 2:3 aspect ratio
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Calculator Game")


# ----| DEFINE CLASSES |----

class Button:
    """
    This class provides us with a Button template and some methods to do many things
    like drawing it or checking input which would take ages instead.
    Example usage:
    example_button_instance = Button(300, 300, 100, 100, (0, 255, 0), "Click me")
    example_button_instance.draw(screen) #draw button on screen
    if example_button_instance.on_click() == True:
        doSomething()

    """
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def on_click(self, events):
        # This somehow works.
        # We have been graced by Allah.
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN) and (self.rect.collidepoint(event.pos)):
                return True
            if (event == pygame.MOUSEBUTTONUP):
                return True # Don't ask.


# ----| DEFINE FUNCTIONS |----

def draw_rect(x, y, width, height, color):
    """
    (int) x, y : position of upmost left corner
    (int) width, height : width and height from upmost left corner
    (int, int, int) color : you know
    """
    # Define rectangle properties
    rect_x, rect_y = x, y
    rect_width, rect_height = width, height
    rect_color = color
    # Draw the rectangle
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

def draw_calculator():
    """
    Draws a naked calculator (without actual buttons).
    Call once per frame (at beginning), or when resetting the calculator.
    """
    # Base and screen
    draw_rect(x = width*0.2, y = width*0.2, width = width*0.5, height = width*0.8, color = (100, 100, 100))
    draw_rect(x = width*0.225, y = width*0.24, width = width*0.45, height = width*0.25, color = (127, 127, 127))
    # First row
    draw_rect(x = width*0.385, y = width*0.52, width = width*0.13, height = width*0.10, color = (127, 127, 127))
    draw_rect(x = width*0.545, y = width*0.52, width = width*0.13, height = width*0.10, color = (127, 127, 127))
    draw_rect(x = width*0.225, y = width*0.52, width = width*0.13, height = width*0.10, color = (127, 127, 127))
    # Second row
    draw_rect(x = width*0.225, y = width*0.65, width = width*0.13, height = width*0.10, color = (127, 127, 127))
    draw_rect(x = width*0.385, y = width*0.65, width = width*0.13, height = width*0.10, color = (127, 127, 127))
    draw_rect(x = width*0.545, y = width*0.65, width = width*0.13, height = width*0.10, color = (127, 127, 127))

def talk(text): # Maybe update this for the text to look better
    while True:

        events = pygame.event.get()

        draw_rect(width*0.05, width*1.2, width*0.9, width*0.25, (255, 255, 255))
    
        font = pygame.font.Font(None, round(width*0.06))
        text_surface = font.render(text, True, (0,0,0))
        text_rect = pygame.Rect(width*0.05 + width*0.005, width*1.2 + width*0.005, width*0.9 - width * 0.01, width*0.25 - width * 0.01)
        screen.blit(text_surface, text_rect)

        button1 = Button(width*0.545, width*0.52, width*0.13, width*0.10, (0,255,0), "->")
        button1.draw(screen)
        if button1.on_click(events):
            break
    
        pygame.display.flip()

def play_level(n):
    """
    Will create a new game loop for the selected level
    (parameter n for levelnumber)
    """
    with open("data/levels.json", "r") as file:
        data = json.load(file)  # Load JSON data from the file

        # Grab values from JSON data and assign to vars
        item = data[n] # Grab value from level number
        moves = item["moves"]
        initial = item["initial"]
        ops = item["buttons"]
        goal = item["goal"]

        button_count = len(ops)
        while True: # NEW GAME LOOP
            screen.fill((50, 50, 50))  # Fill with dark gray
            draw_calculator()
            events = pygame.event.get()

            quit_button = Button(x = width*0.545, y = width*0.65, width = width*0.13, height = width*0.10, color = (255, 10, 10), text = "X")
            quit_button.draw(screen)
            if quit_button.on_click(events):
                return n
            

            button_list = [Button(width*0.225, width*0.52, width*0.13, width*0.10, (255,255,255), ""),
                          Button(width*0.385, width*0.52, width*0.13, width*0.10, (255,255,255), ""),
                          Button(width*0.225, width*0.65, width*0.13, width*0.10, (255,255,255), ""), 
                          Button(width*0.385, width*0.65, width*0.13, width*0.10, (255,255,255), "")]
            
            for x in range(button_count):
                op = ops[x]
                # Button text
                # Yes we can make this nicer with lists and indices. But... uhh...
                text = ""
                if op[0] == "add":
                    text += "+"
                if op[0] == "sub":
                    text += "-"
                if op[0] == "mul":
                    text += "x"
                if op[0] == "div":
                    text += "/"
                if op[0] == "pow":
                    text += "^"
                if op[0] == "sin":
                    text += "sin"
                if op[0] == "cos":
                    text += "cos"
                text += str(op[1])

                button = button_list[x]
                button.text = text
                button.draw(screen)
                if button.on_click(events):
                    if op[0] == "add":
                        initial += op[1]
                    if op[0] == "sub":
                        initial -= op[1]
                    if op[0] == "mul":
                        initial *= op[1]
                    if op[0] == "div":
                        initial /= op[1]
                    if op[0] == "pow":
                        initial **= op[1]
                    if op[0] == "sin":
                        initial = round(math.sin(initial / 180*math.pi), 3)
                    if op[0] == "cos":
                        initial = round(math.cos(initial / 180*math.pi), 3)

                    moves -= 1

            # Should we turn this into a function? yes. Is it worth it right now? no.
            # Number
            font = pygame.font.Font(None, round(width*0.13))
            text_surface = font.render(str(initial).zfill(4), True, (0,0,0))
            text_rect = pygame.Rect(width*0.45, width*0.39, width*0.3, width*0.1)
            screen.blit(text_surface, text_rect)
            # Goal
            font = pygame.font.Font(None, round(width*0.06))
            text_surface = font.render("goal: "+str(goal).zfill(3)+" |", True, (0,0,0))
            text_rect = pygame.Rect(width*0.23, width*0.25, width*0.15, width*0.085)
            screen.blit(text_surface, text_rect)
            # Moves
            font = pygame.font.Font(None, round(width*0.06))
            text_surface = font.render("moves: "+str(moves).zfill(2), True, (0,0,0))
            text_rect = pygame.Rect(width*0.45, width*0.25, width*0.15, width*0.085)
            screen.blit(text_surface, text_rect)

            if initial == goal:
                
                pygame.display.flip()
                talk("Congratulations!")
                return n + 1 # Tell loop to go to next level
                
            elif moves <= 0:
                pygame.display.flip()
                talk("Nuh huh (try again)")
                return n # Tell loop to STAY THE FRICK HERE

            pygame.display.flip()


# ----| MAIN GAME LOOP |----

running = True
while running: # In the future remove this loop. we already have game loops inside levels.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # Clear the screen
    screen.fill((50, 50, 50))  # Fill with dark gray

    # Things to do once per frame
    draw_calculator()
    talk("Hello and wecome to the Calculator Game")
    talk("Reach the goal with the provided functions.")
    talk("Here's an wasy one. (I hope)")
    x = 0
    while True:
        x = play_level(x)
        if x == 1:
            break
        else:
            talk("That was a good one though.")
    talk("Now for something a little more complete.")
    talk("Remember. Don't run out of moves!")
    x = 1
    while x < 7:
        x = play_level(x)
    talk("Congratulations you completed the game!")
    talk("Click the arrow to restart.") 

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

def doSomething():
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((50, 50, 50))
     
    doSomething()

    pygame.display.flip()


pygame.quit()
sys.exit()
