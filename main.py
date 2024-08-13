# Main.py
# Bubble Screen Saver program

from enum import Enum
from abc import ABC, abstractmethod
import pygame
import sys
import random

class IComponent(ABC):

    # Component type
    class IC(Enum):
        Noc = 0
        Bubble = 1
    
    class XYDir(Enum):
        Idle = 0
        Positive = 1
        Negative = -1

    __m_compType = IC.Noc
    __m_xDirSign = XYDir.Idle
    __m_yDirSign = XYDir.Idle

    #Constructor
    def __init__(self, compType):
        self.__m_compType = compType

    def getCompType(self):
        return self.__m_compType

    def setXDirSign(self, xDir):
        self.__m_xDirSign = xDir

    def setYDirSign(self, yDir):
        self.__m_yDirSign = yDir

    def getXYDirSign(self):
        return (self.__m_xDirSign, self.__m_yDirSign)

    def display(self):
        print("IComponent:", self.__m_compType)

    @abstractmethod
    def getPosition(self):
        pass
    
    @abstractmethod
    def setPosition(self, pos):
        pass

    @abstractmethod
    def setScale(self, scaleFactor):
        pass

class Bubble(IComponent, pygame.sprite.Sprite):
    
    #Constructor
    def __init__(self, compType, pos=None):
        IComponent.__init__(self, compType)
        pygame.sprite.Sprite.__init__(self)
        
        # load texture NOTE: image member variable is necessary for Sprite class
        self.image = pygame.image.load("Resources/bubble.png")
        self.rect = self.image.get_rect()

        if pos != None:
            self.rect.topleft = (pos.x, pos.y)
        
        # Setting up random speed of the component
        self._m_speed = random.choice([0.5, 1, 1.5])

    def setPosition(self, posTuple):
        self.rect.topleft = posTuple

    def getPosition(self):
        return self.rect.topleft
    
    def setScale(self, scaleFactor):
        width = int(self.image.get_width() * scaleFactor)
        height = int(self.image.get_height() * scaleFactor)
        self.image = pygame.transform.scale(self.image, (width, height))
    
    def getSpeed(self):
        return self._m_speed

    def update(self):
        # Position update based on Direction
        xdir, ydir = self.getXYDirSign()
        xpos, ypos = self.rect.topleft
        if xdir == IComponent.XYDir.Positive:
            xpos += self._m_speed
        elif xdir == IComponent.XYDir.Negative:
            xpos -= self._m_speed

        if ydir == IComponent.XYDir.Positive:
            ypos += self._m_speed
        elif ydir == IComponent.XYDir.Negative:
            ypos -= self._m_speed
        
        # Update the position of the sprite
        self.setPosition((xpos, ypos))

class Entity:

    #Constructor
    def __init__(self):
        self.__m_spriteComponents = pygame.sprite.Group()

    def addComponent(self, componentObject):
        self.__m_spriteComponents.add(componentObject)
    
    def render(self, window):
        # Check the bounds and set direction accordingly
        for sprite in self.__m_spriteComponents:
            xpos, ypos = sprite.getPosition()
            xLim, yLim = window.get_size()

            # Direction setting
            if xpos <= -120:
                sprite.setXDirSign(IComponent.XYDir.Positive)
            elif xpos >= xLim:
                sprite.setXDirSign(IComponent.XYDir.Negative)
            
            if ypos <= -120:
                sprite.setYDirSign(IComponent.XYDir.Positive)
            elif ypos >= yLim:
                sprite.setYDirSign(IComponent.XYDir.Negative)

            sprite.update()

        self.__m_spriteComponents.draw(window)

# Main Entry Point
if __name__ == "__main__":
    print("[Console log] Bubble Screen Saver")

    windowWidth = 800
    windowHeight = 600

    # Initialize pygame and game window window
    pygame.init()
    window = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Bubble Screen Saver")

    xLim, yLim = window.get_size()

    # Create Entity
    entity = Entity()

    # Creating first Bubble sprite with random position
    for _ in range(1):
        randomPos = pygame.math.Vector2(random.randint(-10, xLim * 0.9), random.randint(-10, yLim * 0.9))
        bubbleComponent = Bubble(IComponent.IC.Bubble, randomPos)
        bubbleComponent.setXDirSign(random.choice([IComponent.XYDir.Positive, IComponent.XYDir.Negative]))
        bubbleComponent.setYDirSign(random.choice([IComponent.XYDir.Positive, IComponent.XYDir.Negative]))
        bubbleComponent.setScale(random.uniform(0.2, 0.6))
        entity.addComponent(bubbleComponent)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse button up event
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    # Add a new bubble component aka sprite
                    randomPos = pygame.math.Vector2(random.randint(-10, xLim * 0.9), random.randint(-10, yLim * 0.9))
                    bubbleComponent = Bubble(IComponent.IC.Bubble, randomPos)
                    bubbleComponent.setXDirSign(random.choice([IComponent.XYDir.Positive, IComponent.XYDir.Negative]))
                    bubbleComponent.setYDirSign(random.choice([IComponent.XYDir.Positive, IComponent.XYDir.Negative]))
                    bubbleComponent.setScale(random.uniform(0.2, 0.6))

                    # Add sprite to the entity
                    entity.addComponent(bubbleComponent)

            # Mouse motion event
            if event.type == pygame.MOUSEMOTION:
                pass

        # Clear the screen with white for now
        window.fill((255, 255, 255))

        # Draw the entities
        entity.render(window)

        # Flip the display
        pygame.display.flip()

        pygame.time.Clock().tick(144)

# Quit Pygame
pygame.quit()

sys.exit()