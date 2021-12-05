import pygame
BLACK = (0, 0, 0)
 
class Point(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([7, 7])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        # pygame.draw.circle(self.image, color, (5,5), 5) # bgr, circle might be slower
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.rect = self.image.get_rect(center=(width, height))

    def change(self, x, y):
        self.rect.x = x
        self.rect.y = y