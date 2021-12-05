import pygame
BLACK = (0,0,0)
 
class Finger(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([700, 500])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        self.color = color

        # Draw the paddle (a rectangle!)
        pygame.draw.line(self.image, self.color, [0, 0], [0, 0], 3)
        
        # # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect(center=(width, height))

    def change(self, x1, y1, x2, y2):
        self.image.fill(BLACK)
        pygame.draw.line(self.image, self.color, [x1, y1], [x2, y2], 3)
        self.rect.x = 0
        self.rect.y = 0