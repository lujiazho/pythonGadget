# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
from point import Point
from finger import Finger
import cv2
import mediapipe as mp 
import time 
import hand_landmarks_module as hlm

CONNECTIONS = [(5, 9), (10, 11), (5, 6), (15, 16), (13, 17), (18, 19), (1, 2), (6, 7), (0, 17), (3, 4), (9, 10), (0, 5), (2, 3), (14, 15), (11, 12), (19, 20), (0, 1), (9, 13), (17, 18), (13, 14), (7, 8)]
FINGERS = [(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),(13,14),(14,15),(15,16),(17,18),(18,19),(19,20)]
FINGERS_set = set(FINGERS)
pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

# points = [Point((255,0,0),20,200) for _ in range(21)]
fingers = [Finger((255,0,0),0,0) for _ in range(len(FINGERS))]
 
# paddleB = Paddle(WHITE, 10, 100)
# paddleB.rect.x = 670
# paddleB.rect.y = 200
cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0
detector = hlm.handDetector()
 
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
fingers_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
# all_sprites_list.add(paddleB)
# for point in points:
#     all_sprites_list.add(point)
for finger in fingers:
    fingers_list.add(finger)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 
    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    success, img = cap.read()
    # img1 = detector.findHands(img)
    lmList = detector.findPosition(img)
    if lmList:
        # for idx, x, y in lmList:
        #     points[idx].change(size[0]-x, y)
        for i, (n1, n2) in enumerate(FINGERS):
            fingers[i].change(size[0]-lmList[n1][1], lmList[n1][2], size[0]-lmList[n2][1], lmList[n2][2])

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    print(f"fps: {fps}")

    # if keys[pygame.K_UP]:
    #     paddleB.moveUp(5)
    # if keys[pygame.K_DOWN]:
    #     paddleB.moveDown(5)    
 
    # --- Game logic should go here
    all_sprites_list.update()
    if lmList:
        fingers_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=690:
        scoreA+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    #Detect collisions between the ball and the paddles
    # if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
    if pygame.sprite.collide_mask(ball, paddleA):
        ball.bounce()
    # for point in points:
    #     if pygame.sprite.collide_mask(ball, point):
    #         ball.bounce()
    if lmList:
        for finger in fingers:
            if pygame.sprite.collide_mask(ball, finger):
                ball.bounce()
                break
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    if lmList:
        for idx, x, y in lmList:
            pygame.draw.rect(screen, (0,0,255), [size[0]-x, y, 7, 7])
        # for n1, n2 in CONNECTIONS:
        #     if (n1, n2) not in FINGERS_set:
        #         x1, y1, x2, y2 = lmList[n1][1], lmList[n1][2], lmList[n2][1], lmList[n2][2], 
        #         pygame.draw.line(screen, WHITE, [size[0]-x1, y1], [size[0]-x2, y2], 3) # bgr
        fingers_list.draw(screen) 
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
    
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(180)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()