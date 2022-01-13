import pygame
import math
import random
import time
from os import*



#Defining some variables needed..

width = 1300
height = 800
FPS = 60
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#===============================================
#WINDOW DISPLAY:
pygame.init()       #pygame function that innitiates the window
pygame.mixer.init()     #iniates sounds functions/outputs
screen = pygame.display.set_mode((width,height))    #creating & setting window size
pygame.display.set_caption("Covid-19")  #window caption
clock = pygame.time.Clock()     #setting the appropriate speed for the game to run... not tooo fast
scorenum = 0
highest_score_list = []         #Iniating empty score list to be used later on..

#===============================================
#FILE INFORMATION:
img_dir = path.dirname(__file__)        #Locating the fil within the computer data-storage so when we need to pull the sounds/pictures we just combine this variable with the image/sound...
#===============================================
#===============all the images:===============
player_img = path.join(img_dir,"stest.png")     #locating Player image
bullet_img = path.join(img_dir,"bullet.png")    #locating Bullet image
zombie_img = path.join(img_dir,"ztest.png") #locating Zombie image


background_img = pygame.image.load(path.join(img_dir,"background.png")).convert()   #locating Background image and converting it as a image rather than pixel for pixel. A function that speeds up game process and shortens computer power as well as speeds up computing process
background_rect = background_img.get_rect()         #gets the boundries of the backgorund image
background_rectx = background_rect.centerx  #setting the x position of the background image         
background_recty = background_rect.centery  #setting the y postion of the back gorund position      (0,0) being the top left 
#===============================================
#=================MUSIC=========================

#Locating the musing and loading them and calling for them to play later on when needed.

bulletsound = pygame.mixer.Sound('bulletsound.wav')     #--Bullet sound
gameoversound = pygame.mixer.Sound('TestedPositive.wav')    #--TestedPositive sound
pygame.mixer.music.load('BackgroundMusic.mp3')          #Main sound.


#===============================================
#=================OBJECTS=================


class Player(pygame.sprite.Sprite):
    """This is the base for all players"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #making sure that the module knows that this is a Sprite/Object

        self.image_orig = pygame.image.load(player_img).convert()       #converting the images to an image rather pixels to run fast and smoothly
        self.image_orig.set_colorkey(BLACK)     #setting the background of the image o be transparent so when the image is imported no black colors is imported

        self.image = self.image_orig        #setting new variable for the image its needed so when the image is rotated it wouldn't be distorted
        
        self.rect = self.image.get_rect()   #getting the boundries of the image
        self.rectx = self.rect.centerx  #setting the x & y positions of the image
        self.recty = self.rect.centery


        #placing the player
        self.rect.centerx = (width // 2 )           #   Spawnning the player in the middle of the screen when starting
        self.rect.centery = (height // 2)


    def rotate(self):       # this function is for when the player image rotates following the cursuer
    
        self.mouse_x, self.mouse_y  = pygame.mouse.get_pos()  #finds the mouse coordts
        rel_x = self.mouse_x - self.rect.centerx
        rel_y =  self.mouse_y+2 - self.rect.centery # getting the vectors from mouse to player

        
        self.angle = math.degrees((-1*math.atan2(rel_y, rel_x)))    #the angle arctTan in radians i think but converted to degrees
        self.angle = (self.angle) % 360         # this here is needed after long testing i discoverred that the player image can be rotated > 360.. therefore '%' operator to if the angle became 361 deg, the angle will result in just 1 deg
        #===VV=[Need to rotate the actual image as wel as centering the hitBox]
        self.image = pygame.transform.rotate(self.image_orig, self.angle)   #the picture being rotated and reput
        old_center = self.rect.center       #getting the OLDEST hitbox center of the image
        self.rect = self.image.get_rect()   #getting the hitbox for the rotated image
        self.rect.center = old_center       #placing the OLDEST hitbox Image center on the new center
        self.image_orig.set_colorkey(BLACK)
    
    def shoot(self):            #this function is when the player shoots
        self.x, self.y = self.rect.center
        bullet = Bullet(self.x, self.y , self.angle)        #creates the bullet and taking the players position
        all_sprites.add(bullet)     #adding the bullet to a list so when later we can detect if the bullets hits anything
        bullets.add(bullet)

    

    def update(self):       #the object(player) update function is needed 
        self.rotate()       #call for rotate function

        self.speedx = 0
        self.speedy = 0
        
        keystate = pygame.key.get_pressed()     #seeing if any keys been pressed

#These now are for the A-W-S-D movments and relocating the player on the screen
        #{=====================================================
        if keystate[pygame.K_a]:            
            self.speedx = -3
        if keystate[pygame.K_a] and keystate[pygame.K_LSHIFT]:
            self.speedx = -6
        #-------------
        if keystate[pygame.K_d]:
            self.speedx = 3
        if keystate[pygame.K_d] and keystate[pygame.K_LSHIFT]:
            self.speedx = 6
        self.rect.x += self.speedx
        #-------------------------------------------------------
        #-------------------------------------------------------
        if keystate[pygame.K_s]:
            self.speedy = 3
        if keystate[pygame.K_s] and keystate[pygame.K_LSHIFT]:
            self.speedy = 6
        #-------------
        if keystate[pygame.K_w]:
            self.speedy = -3
        if keystate[pygame.K_w] and keystate[pygame.K_LSHIFT]:
            self.speedy = -6
        self.rect.y += self.speedy
        #=====================================================}
        
        #BLOCKing the player FROM escaping the window boundries:
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left <-1:
            self.rect.left = -1
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top <-1:
            self.rect.top = -1





class Mob(pygame.sprite.Sprite):                #same comments that went for the player it goes here
    """This is the base for all mobs"""

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image_orig = pygame.image.load(zombie_img).convert()
        self.image_orig.set_colorkey(BLACK)

        self.image = self.image_orig
        self.rect = self.image.get_rect()


        #=============[spawns the zombies]=============
        self.spawns = [ (1,1),   (width//2,1),   (width,1),  (1,height//2),  (1,height), (width//2,height),  (width,height), (width,height//2)   ]
        
        self.rect.center = random.choice(self.spawns)   #selecting the spawn 

        #=============[Speed of zombies]=============
        self.speed = random.randrange(2,5)

    def rotate(self):


        rel_x = player.rect.centerx - self.rect.centerx
        rel_y =  player.rect.centery - self.rect.centery # getting the vectors from mouse to player

        
        self.angle = math.degrees((-1*math.atan2(rel_y, rel_x)))    #the angle arctTan in radians i think but converted to degrees
        #self.angle = (self.angle) % 360
        #===VV=[Need to rotate the actual image as wel as centering the hitBox]
        self.image = pygame.transform.rotate(self.image_orig, self.angle)   #the old picture being rotated and reput
        old_center = self.rect.center       #getting the OLDEST hitbox center of the image
        self.rect = self.image.get_rect()   #getting the hitbox for the rotated image
        self.rect.center = old_center       #placing the OLDEST hitbox Image center on the new center
        self.image_orig.set_colorkey(BLACK)

    def follow(self):

        # Find direction vector (dx, dy) between enemy and player.
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist+0.0001), dy / (dist+0.0001)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed


    def update(self):
        self.rotate()
        self.follow()

        #if self.rect.top>(-20) or self.rect.left<-20 or self.rect.right> (width+20) or self.rect.bottom> (height+20):
            #self.rect.center = random.choice(self.spawns)
            #self.speed = random.randrange(1,3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)


        self.image_orig = pygame.image.load(bullet_img).convert()

        self.image = pygame.transform.rotate(self.image_orig, angle)
        
        self.image_orig.set_colorkey(BLACK)

        self.image = self.image_orig
        self.rect = self.image.get_rect()

        #where will it spawn up in innit(x,y)
        self.rect.bottom = y
        self.rect.centerx = x

        #bullet speed:
        self.speed = 20

        #direction of the bullet angle dpendent:                    # this two lines are for the bullets trajectory from using the players position and angle:
        self.speedy = math.sin(math.radians(-angle)) * self.speed   # taking the cos of the player's angle ( where he looks) and adding on the distance multplied by the standard bullet's speed
        self.speedx = math.cos(math.radians(-angle)) * self.speed   # taking the sin of the player's angle ( where he looks) and adding on the distance multplied by the standard bullet's speed

    def update(self):

        self.rect.y += self.speedy                  # adding the x component of the player's angle * speed to change the distance of the bullete to persue the smae trajectory line
        self.rect.x += self.speedx                  # adding the y component of the player's angle * speed to change the distance of the bullete to persue the smae trajectory line

        #Bullets delete themselves if they escaped the windws boundries
        if self.rect.bottom-3 < 0 or self.rect.left-3 <0 or self.rect.right+3 > width or self.rect.top+3 >height :
            self.kill()

#===============================================
#===============================================
#===============================================
# Creating a button class because its just a lot easier to call for it for independent buttonss


class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.centerx = x-20
        self.cenery = y
        self.width = width
        self.height = height
        self.text = text

                #Draw function on the screen
    def draw(self,screen,outline=None):
        """Call this method to draw the button on the screen"""

        if outline:     # this to make the button have some black boarder -- Thought it was kinda cool
            pygame.draw.rect(screen, outline, (self.centerx-2,self.cenery-2,self.width+4,self.height+4),0) #py game functions for drawing objects, in this case rect == rectangle
            #                       Color           x-pos           y-pos       width           height
        pygame.draw.rect(screen, self.color, (self.centerx,self.cenery,self.width,self.height),0)
        
        #If i decided to have a text on the button then :
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.centerx + (self.width//2 - text.get_width()//2), self.cenery + (self.height//2 - text.get_height()//2))) #position of the text to be in the middle of the button

    def isOver(self, pos):      # if the mouse is on the button::
        
        self.color = buttoncolor

                
        if pos[0] > self.centerx and pos[0] < (self.centerx + self.width):      #|         This is if the mouse         |
            if pos[1] > self.cenery and pos[1] < self.cenery + self.height:     #|is withing the boundries of the button|

                self.color = (192, 192, 192)                                    # Then chage the button color to grey - i thought it was kinda
                                                                                # needed for user-friendly/interactiveness stuff...


                if event.type == pygame.MOUSEBUTTONDOWN:  # check for mouse keys         
                    if pygame.mouse.get_pressed()[0]:     #check for if the key ((LEFT CLICK .aka [0]  )) is pressed then execute true for isOver function
                        return True
                    
        return False


#===============================================
#===============================================
# Standard functions to call when needed:


def MainMenu():
    """Manu Screen"""

    screen.fill(BLACK) #Making the background black

    startbutton.draw(screen,GREY)   #drawing the butoons
    controlsbutton.draw(screen,GREY)
    creditbutton.draw(screen,GREY)
    quitbutton.draw(screen,GREY)

    font = pygame.font.SysFont('comicsans', 60, True)       # Creating The Main title in the main menu
    text = font.render("COVID-19 OVERLOAD", 1, (255,255,255))
    screen.blit(text, (420, 150))

def pause():
    """Pause Screen"""
   
    screen.fill(BLACK) #Making the background black

    continuebutton.draw(screen,GREY)   #drawing the butoons
    controlsbutton.draw(screen,GREY)
    creditbutton.draw(screen,GREY)
    quitbutton.draw(screen,GREY)
    gobackbutton.draw(screen,GREY)

def score():
    """Displaying the score"""

    font = pygame.font.SysFont('comicsans', 60)
    text = font.render(f"score: "+str(scorenum), 1, (0,0,0))
    screen.blit(text, (5, 2))

def scorep():      
    """Displaying the Current score in pause manu"""

    font = pygame.font.SysFont('comicsans', 40)
    text = font.render(f"Your Current Score: "+str(scorenum), 0, WHITE)
    screen.blit(text, (506, 650))

def creditbutton_menu():
    """Credit Screen"""


    screen.fill(BLACK)  #making the background black
    font = pygame.font.SysFont('comicsans', 60, False)
    text = font.render("This game was created by Taha Madi", 1, (255,255,255))
    screen.blit(text, (270, 150))

    font2 = pygame.font.SysFont('comicsans', 60, False)
    text2 = font2.render("Inspired by the COVID-19 pandemic & Bordem", 1, (255,255,255))
    screen.blit(text2, (160, 220))

    font3 = pygame.font.SysFont('comicsans', 60, False)
    text3 = font3.render("I hope You Enjoy it!.", 1, (255,255,255))
    screen.blit(text3, (440, 290))

    font3 = pygame.font.SysFont('comicsans', 40, True)
    text3 = font3.render("Wash your hands & STAY HOME!!", 1, (255,255,255))
    screen.blit(text3, (390, 400+70))

def controls():
    """Controlls screen that explains the controlls"""


    screen.fill(BLACK)

    font = pygame.font.SysFont('comicsans', 60, False)

    text6 = font.render("Don't let the infected get too close or", 0, (255,255,255))
    screen.blit(text6, (270, 150))
    text6 = font.render("you will die!", 0, (255,255,255))
    screen.blit(text6, (270, 200))


    text = font.render("Up: W      Down: S", 0, (255,255,255))
    screen.blit(text, (270, 270))
    text1 = font.render("Left: A     Right: D", 0, (255,255,255))
    screen.blit(text1, (270, 320))
    text2 = font.render("To Sprint:   Hold SHIFT", 0, (255,255,255))
    screen.blit(text2, (270, 370))
    text3 = font.render("To Aim:       Move The Mouse", 0, (255,255,255))
    screen.blit(text3, (270, 420))
    text4 = font.render("To Shoot:   Press Left Mouse Click", 0, (255,255,255))
    screen.blit(text4, (270, 470))
    text5 = font.render("To Pause:   Press 'P' ", 0, (255,255,255))
    screen.blit(text5, (270, 520))

def gameover():
    """Game Over Text when the player dies"""

    gameovertext.draw(screen)   #The black Strip
    font = pygame.font.SysFont('comicsans', 80, True)       # Creating The actual text 
    text = font.render("You Tested Positive", 1, (255,255,255))
    screen.blit(text, (370, 380))

def highesscore():
    """This function displays your highest score you've played"""

    if len(highest_score_list) != 0:    # if there's one or more scores in the list then:
        scorenum = max(highest_score_list)      #a python function that returns the highest value in a list; max()


    elif len(highest_score_list) == 0 :     # if there's no score in the list then:
        scorenum = 0

    font = pygame.font.SysFont('comicsans', 40)                #creates the actual text
    text = font.render(f"Your Highest Score: "+str(scorenum), 1, WHITE)
    screen.blit(text, (506, 600))
    


#===============================================
#===============================================
#===============================================

##Creating the standered BUTTONS/texts

buttoncolor = (255,255,255)     # Making the button colors standard/constant (WHITE)

startbutton = button( buttoncolor, 550 ,190+70 ,250,50, 'START')

continuebutton = button( buttoncolor, 550 ,190+70 ,250,50, 'CONTINUE')

controlsbutton = button( buttoncolor, 550 ,250+70,250,50, 'CONTROLS')

creditbutton = button( buttoncolor, 550 ,250+70+60  ,250,50, 'CREDITS')

quitbutton = button( buttoncolor, 550 ,310+70+60 ,250,50, 'QUIT')

gobackbutton = button( buttoncolor, 40 ,700 ,130,40, 'BACK')

gameovertext = button( BLACK, 20 ,350 ,width,100, 'GAME OVER')


#=============================================================================
#=============================================================================
#==============================  THE GAME LOOP  ==============================

#---------------------------|
running = True      #preSetting some
main = True             #statments/loops
game = False                #to control the flow for function calls or 
play = True                # the game environment 
credit = False
cotrol = False
#---------------------------
while running:
    
    # keep loop running at a constant speed
    clock.tick(FPS)



    if main:
        MainMenu()
        highesscore()

        if play:        #some conditions i made to make the music play as the intr in the main menu - its like a glitch that i had to come up wih to make this process work..
            pygame.mixer.music.play() # If the loops is -1 then the music will repeat indefinitely.
        play = False            #thats also was needed to make this "glitch"




        for event in pygame.event.get():    #checking for all the events
            pos = pygame.mouse.get_pos()        #getting the information about the mouse position

            if event.type == pygame.QUIT:       # if the [X] button on the window bar has been pressed
                running = False                 #shuts of the running loop
                pygame.quit()                   #shuts off the pygame window
                quit()                          # It kills the python terminal.

            if startbutton.isOver(pos):         #checking for if the mouse is over the start button
                pygame.mixer.music.fadeout(380)
                spawning = True
                game = True
                main = False

            if controlsbutton.isOver(pos):
                cotrol = True       # if its pressed then go to control screen    
                main = False   
                

            if creditbutton.isOver(pos):        #checking for if the nouse is over or if its pressed te credit butoon
                credit = True       # if its pressed then go to credit    
                main = False    


            if quitbutton.isOver(pos):      # checking for if the mouse is over the quit button
                running = False
                game = False
                pygame.quit()


        pygame.display.update()

    if cotrol:         #show the credit menu from the controls button
        controls()
        gobackbutton.draw(screen,GREY)
        for event in pygame.event.get():    #checking for all the events
            pos = pygame.mouse.get_pos()        #getting the information about the mouse position

            if event.type == pygame.QUIT:          #checking for the main window if its closed
                running = False
                pygame.quit()
                quit()

        if gobackbutton.isOver(pos):        #if the mouse is on the go back button and or if its pressed
            main = True
            cotrol = False                      #then get out of the credit menu and back to the main
        
        pygame.display.update() # update the window with in the creit menu




    if credit:          #show the credit menu from the credit button
        creditbutton_menu()
        gobackbutton.draw(screen,GREY)
        for event in pygame.event.get():    #checking for all the events
            pos = pygame.mouse.get_pos()        #getting the information about the mouse position

            if event.type == pygame.QUIT:          #checking for the main window if its closed
                running = False
                pygame.quit()
                quit()

        if gobackbutton.isOver(pos):        #if the mouse is on the go back button and or if its pressed
            main = True
            credit = False                      #then get out of the credit menu and back to the main
        
        pygame.display.update() # update the window with in the creit menu


    #The actual Game loop starts
    if game:

        if spawning:        #spawns the objects: Players & Mobs(Zombies)

            all_sprites = pygame.sprite.Group()     #creating a list that contains all the objects that has been created
            mobs = pygame.sprite.Group()            #creating a list that contains only the Mobs ( zombies) 
            bullets = pygame.sprite.Group()         #creating a list that contains only the Bullets 
            player = Player()                       #spawning a Player
            all_sprites.add(player)                 #adding the player to the all_sprite list

            for i in range(3):
                m = Mob()                      # Spawning a mob
                all_sprites.add(m)              # adding the mob to the all objects list
                mobs.add(m)                     #adding the same mob to the only mobs list

            spawning = False                    # turning off this loop so it wouldn't keep spawning too much of un wanted objects


        credit = False
        paused = False


        # Process input (events)
        for event in pygame.event.get():    #For loop to list for events happening in the window/computer


            if event.type == pygame.QUIT:       # check for closing the main window
                running = False


            elif event.type == pygame.KEYDOWN:  # check for keyboards pressed

                if event.key == pygame.K_p:     #if <p> button is pressed
                    paused = True
                    credit = False
                    control = False
                    play = True

                    if play:
                        pygame.mixer.music.play()   # playing the main background song



                    while paused:           #pauses the game through a while loop
                        pygame.display.update()
                        pause()             #opens up the pause manu
                        highesscore()       #displayes the highes score
                        credit = False
                        control = False

                        pygame.draw.rect(screen, BLACK, (15 ,700-2 ,140,40+4),0)
                        
                        clock.tick(30)
                        scorep()            #it displays the current score for you over the pause screen

                        #Prints Game is paused
                        font = pygame.font.SysFont('comicsans', 60)
                        text = font.render("Game is Paused", 1, (255,255,255))
                        screen.blit(text, (490, 180))

                        
                        for event in pygame.event.get():        # checks for all the events that happen with the computer: Window,Mouse, Keyboard
                            pos = pygame.mouse.get_pos()        #geting the information from the mouse position in (x,y) form

                            if event.type == pygame.QUIT:       # if the [X] button on the window bar has been pressed
                                running = False                 #shuts of the running loop
                                pygame.quit()                   #shuts off the pygame window
                                quit()                          # It kills the python

                            if continuebutton.isOver(pos):         #checking for if the mouse is over the coninue button
                                clock.tick(FPS)
                                pygame.mixer.music.fadeout(380)
                                paused = False
                                
                            if quitbutton.isOver(pos):         #checking for if the mouse is over the quit button
                                running = False
                                game = False
                                pygame.quit()


                            if controlsbutton.isOver(pos):         #checking for if the mouse is over the control button
                                control = True

                                while control:
                                    controls()
                                    gobackbutton.draw(screen,GREY)  #draws the back button on the controls screen from the pause menu

                                    for event in pygame.event.get():    #checking for all the events
                                            pos = pygame.mouse.get_pos()        #getting the information about the mouse position

                                            if event.type == pygame.QUIT:          #checking for the main window if its closed
                                                running = False
                                                pygame.quit()
                                                quit()
                                    if gobackbutton.isOver(pos):        #if the mouse is on the go back button and or if its pressed
                                        control = False                      #then get out of the controls menu and back to the main
                                    pygame.display.update()     #update the go back button

                                pygame.display.update()


                            if creditbutton.isOver(pos):          #checking for if the mouse is over the credit button
                                credit = True

                                while credit:          #show the credit menu from the credit button

                                    creditbutton_menu()
                                    gobackbutton.draw(screen,GREY)  #draws the back button on the credit screen from the pause menu
                                    for event in pygame.event.get():    #checking for all the events
                                            pos = pygame.mouse.get_pos()        #getting the information about the mouse position

                                            if event.type == pygame.QUIT:          #checking for the main window if its closed
                                                running = False
                                                pygame.quit()
                                                quit()
                                    if gobackbutton.isOver(pos):        #if the mouse is on the go back button and or if its pressed
                                        credit = False                      #then get out of the credit menu and back to the main
                                    pygame.display.update()     #update the go back button

                        pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # check for mouse pressed
                if pygame.mouse.get_pressed()[0]:     #check for <space> pressed
                    bulletsound.play()
                    player.shoot()
        

        

        #check to see if mob/zombies hit the player
        hits = pygame.sprite.spritecollide(player, mobs, False) #the False means if the first parameter hits the second paramter, it decides wether to delete the second paramter pbject. if False means no, If true means delete//this will give you a list
        
        
        if hits:            #This if statment that i would like to call a loop is mainly for when the player 
                            #dies these are the updates we will be seeing
            gameoversound.play()
            gameover()
            pygame.display.update()
            time.sleep(5)
            play = True     #for the music to play
            main = True     #The main menue comes on first then
            game = False     #The game loop will shut down
            highest_score = scorenum    #take the previous score and put it the highest - this may not be done.
            
            highest_score_list.append(highest_score)
            scorenum = 0            #reset the score



        #check to see if bullete hit the mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        
         #(group1, group2, dokill1, dokill2, collided = None) the true maes either spriteGrup get
        #deleted(nature of the function) - but it will cause the mobs to be deleted for ever
        #so... i have made them spawn again:

        for hit in hits:
            scorenum +=1       ##<<< for every kill the player gets +1 point
            m = Mob()           #Respawning the killed mobs
            all_sprites.add(m)  #adding them to the sprite list
            mobs.add(m)         


        #updating all objects(player,mobs,bullets)
        all_sprites.update()


        #DRAWING ALL THE OBJECTS
        screen.fill(BLACK)  #filling the background color black
        screen.blit(background_img, (0,0))          #and then placing the image on top
        all_sprites.draw(screen)        #drawing all the objects (player,Mob, Bullet..) onton the screen

        score()     # prints the current socre on top left screen


        #RENDERING the pictures AFTER EVERY loop
        pygame.display.flip()           #flipping all the picturs so they would print nicely and separtly - so they wouldn't look like windows XP when it lags  - i know perefect analogy
        


pygame.quit()           #once the user press quit button or the [X] on the window bar the game shuts off 
