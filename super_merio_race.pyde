# Name                          Type         Purpose                                        Restrictions
# p1x,p1y,p2x,p2y               Int          X and Y val of players                         xval: 0-800, yval: 0-900
# whatlevel                     Int          sets what level                                -2 to 3      
# l1p                           List/Array   Array of all the platforms in the level        N/A
# p1scorestop,p2scorestop       Boolean      If the players score should continue to lower  True, False
# whoname                       Int          sets who's turn it is to enter their name      1,2
# p1right,p1left,p1up           Boolean      If the player is moving left/right/up          True, False
# poweruplist                   List         List of all the powerup names                  N/A
# p1timescore,p2timescore       Int          The player's score                             < 10000
# winsound,powerupsound,etc     minim        All the sounds                                 N/A
# p1/p2 counterincr             Int          Limits the player's jump                       18 >
# inmenu                        String       Sets which part of the game                    ingame, start, highscores, howtoplay
# p1/p2 spawnx/y                Int          Sets the spawn of the players                  N/A
# bonusclicked                  Int          Turns on the bonus level                       1,2,3
# p1/p2loop                     Int          For playersonplatform runs it only once        1,2
# p1/p2name                     String       Names of players                               9 characters
# whowins                       Int          Determines which player has the highest score  1,2 





import random
def setup():
    global l1p, l1pfills
    global p1x,p1y,p2x,p2y, p1right, p1left, p1up, p2up, p2left, p2right, p1counter, p1jump, p2counter, p2jump, powerupcounter
    global playerlw
    global leftborder, rightborder
    global p1speed, p1speed, p1JumpIncr, p2speed, p2speed, p2JumpIncr
    global p1counterincr, p2counterincr
    global inmenu, howfill, highfill, playfill, p1scorestop, p1timescore, whatlevel, p2scorestop, p2timescore, p1gravity, p2gravity, lasttime, playersonplatform, p1loop, p2loop
    global howtoimg, p1keys, p2keys, p1name, p2name, whoname
    global backgroundfillred, backgroundfillgreen, backgroundfillblue, sunx, moon1x, moon2x, backgroundmusic, powerupsound, coinsound, powerupnumber, poweruplist, deathsound, winsound, timedifference, whowins, scorelist
    global player1spawnx, player1spawny, player2spawnx, player2spawny, bonusclicked, bonuscounter1, bonuscounter2
                        
    #music files
    add_library("minim")
    minim=Minim(this)
    powerupsound = minim.loadFile("powerup.mp3")
    backgroundmusic = minim.loadFile("music.mp3")
    deathsound = minim.loadFile("death.mp3")
    winsound = minim.loadFile("win.mp3")
    coinsound = minim.loadFile("coin.mp3")
    backgroundmusic.loop()
    
    size(800,1000)
    p1x = 50
    p1y = 900
    p2x = 700
    p2y = 900
    playerlw = 50
    rightborder = 800
    leftborder = 0
    p1speed = 5
    p1JumpIncr = 10
    p2speed = 5
    p2JumpIncr = 10 
    p1counterincr = 18
    p2counterincr = 18
    player1spawnx = p1x
    player1spawny = p1y
    player2spawnx = p2x
    player2spawny = p2y
    p1timescore = 10000
    p2timescore = 10000
    p1scorestop = False
    p2scorestop = False
    whatlevel = 1
    playersonplatform = 0
    bonusclicked = 0
    bonuscounter1 = 0
    bonuscounter2 = 0
    p1loop = 0
    p2loop = 0
    p1name = ""
    p2name = ""
    whoname = 1
    moon1x = -90
    moon2x = -55
    sunx = -75
    backgroundfillred = 30
    backgroundfillgreen = 144
    backgroundfillblue = 255  
    powerupnumber = 0
    poweruplist = ["Speedup!", "Jump Boost!", "Score Boost!", "Opponent's Confused!"]
    timedifference = 0
    whowins = 0
    scorelist = []
    
    p1keys = ["w","a","d"]
    p2keys = [UP, LEFT, RIGHT]
    howtoimg = loadImage("howtoimage.JPG")
    p1jump = False
    p2jump = False
    p1counter = 0
    p2counter = 0
    powerupcounter = 0
    inmenu = "start"
    playfill = 255
    howfill = 255
    highfill = 255
    soopersize = 100
    
    l1p = [        
        (0,0,950,1000,50),
        (0,350,850,100,25),
        (0,100,750,100,25),
        (0,600,750,100,25),
        (1,680,600,100,25),
        (1,20,600,100,25),
        [2,350,600,100,25],
        (0,200,450,100,25),
        (0,500,450,100,25),
        (0,50,380,100,25),
        (0,650,380,100,25),
        (1,550,310,100,25),
        (1,150,310,100,25),
        [0,50,240,100,25],
        [0,650,240,100,25],
        (0,475,180,100,25),
        (0,225,180,100,25),
        (3,325,100,150,25),
            ]     
        
    p1up = False
    p1left = False
    p1right = False
    p2up = False
    p2left = False
    p2right = False
    
# function that reads a text file. Each line contains a top score and name seperated by a comma.
# The function then adds the name and score to a list.        
def get_scores(scorelist):
    with open("highscores.txt", "r") as a:
        for line in a:
            score, name = line.split(",")
            score = int(score)    
            scorelist.append((score, name.replace('\n', '')))
    return scorelist

# function that takes the list returned from get_scores and compares it to the player's score.
# If the player's score is higher, it adds it to the list
# Next it writes the list to the text file
def writetofile(scorelist, playerscore, playername):
        for i in range (5):
            if playerscore > scorelist[i][0]:
                scorelist.insert(i,(playerscore,playername))
                break
        with open("highscores.txt", 'w') as c:
            for i in range(5):
                c.write('{},{}\n'.format(*scorelist[i]))
                
# Chooses a random number between 1 and 4 to decide which powerup the player gets.
# 1 = Speed Boost (x1.5 speed)
# 2 = Jump Boost  (x1.4 jump time)
# 3 = Score Boost (+500 Score)
# 4 = Confuse (Switch the opposite player's left and right keys)
def powerupDecider(playerspeed, playercounterincr, opponentspeed, opponentjump, playerscore):
    randomPowerup = random.randint(1,4)
    if randomPowerup == 1:
        playerspeed *= 1.5                              
    if randomPowerup == 2:
        playercounterincr *= 1.4                
    if randomPowerup == 3:
        playerscore += 500                
    if randomPowerup == 4:
        opponentspeed *= -1
            
    return (playerspeed, playercounterincr, opponentspeed, opponentjump, playerscore, randomPowerup) 

#resets stats when next level    
def reset(playerspeed, playerJumpIncr, playerloop, playerx, playery, playercounterincr, spawnx, spawny):
    playerspeed = 5
    playerJumpIncr = 10
    playerloop = 0
    playerx = spawnx
    playery = spawny
    playercounterincr = 18
    return (playerspeed, playerJumpIncr, playerloop, playerx, playery, playercounterincr) 

# Function is called when both players reach the pink (end) platform.
# Changes the level value and platforms.
def levelselect(whatlevel):
    global p1scorestop, p2scorestop, scorelist, p1timescore, whowins, l1p, inmenu, scorelist
    if whatlevel >= 0 :
        whatlevel += 1
    if whatlevel == 2:
            l1p = [        
                (0,0,950,1000,50),
                (0,675,850,100,25),
                (0,25,850,100,25),
                (1,575,800,100,25),
                (1,125,800,100,25),
                (0,50,750,100,25),
                (0,650,750,100,25),
                [2,350,700,100,25],
                (0,200,540,100,25),
                (0,500,540,100,25),
                (1,320,850,150,25),
                (1,50,500,100,25),
                (1,650,500,100,25),
                (0,500,400,100,25),
                (0,200,400,100,25),
                (1,350,460,100,25),
                [0,350,300,100,25],
                (3,325,100,150,25),
                (0,100,200,100,25),
                (0,600,200,100,25),
                (1,500,250,100,25),
                (1,200,250,100,25)                                            
                ]
    elif whatlevel == 3:
            l1p = [ 
                (0,0,950,1000,50),
                (0,350,850,100,25),
                (1,250,800,50,25),
                (0,150,750,50,25),
                (1,50,700,50,25),
                (0,730,750,50,25),
                (0,550,650,50,25),
                (1,430,600,70,25),
                (0,340,570,50,25),
                (1,250,520,50,25),
                [2,170,450,50,25],
                (0,50,450,100,25),
                (0,650,350,100,25),
                (0,50,250,100,25),
                (0,650,150,100,25),
                (3,325,50,150,25),
                (1,200,300,400,25),
                (0,0,950,1000,50),
                (0,0,950,1000,50),
                (0,0,950,1000,50),
                (0,0,950,1000,50),
                (0,0,950,1000,50),
                (0,0,950,1000,50),
                (0,0,950,1000,50),
                (0,0,950,1000,50),                       
                ]
    #When all 3 levels have been completed, the read/write to file functions are called for both players        
    elif whatlevel == 4:
            p1scorestop = True
            p2scorestop = True
            l1p = [(0,1000,1000,5,5)]
            scorelist = get_scores(scorelist)
            writetofile(scorelist, p2timescore, p2name)
            scorelist = get_scores(scorelist)
            writetofile(scorelist, p1timescore, p1name)
            if p1timescore > p2timescore:
                whowins = 1
            else:
                whowins = 2
    elif whatlevel == -1:
        l1p = [
                [0,-50,80,400,25],
                [0,450,80,400,25],
                [1,205,370,370,25],
                [0,400,350,4,4],
                [0,100,400,50,25],
                [0,650,400,50,25],
                [1,0,500,200,25],
                [1,600,500,200,25],
                [0,600,600,50,25],
                [0,150,600,50,25],
                [0,0,900,1000,150],
                [0,50,600,150,25],
                [0,600,600,150,25],
                [1,200,630,400,25],
                [3,350,870,100,25],
                [1,200,630,25,270],
                [1,575,630,25,270],
                [1,225,870,100,25],
                [1,475,870,100,25],                    
                    ] 
        
    elif whatlevel == -2:
        l1p = [        
                (0,0,950,1000,50),
                (1,0,850,350,25),
                (1,450,850,350,25),
                (0,350,850,100,25),
                (0,250,700,100,25),
                (1,0,700,250,25),
                (1,350,700,550,25),
                (0,150,550,100,25),
                (1,0,550,150,25),
                (1,250,550,650,25),
                (0,50,400,100,25),
                (1,0,400,50,25),
                (1,150,400,750,25),
                (0,150,250,100,25),
                (1,0,250,150,25),
                (1,250,250,650,25),
                (3,325,100,100,25),
                (0,0,100,325,25),
                (0,425,100,375,25)
                    ]
                
    return(l1p, whatlevel, whowins)

#gravity for p1 and p2
def playerygravity (playergravity, playerjumpincr, playery):
    if playergravity:
        if playery < 900:
            playery += playerjumpincr
    return (playery)

#player 1/2 horizontal movement
def playerxmovement(playerx, playerspeed, playerleft, playerright):
    if playerleft == True:
        playerx -= playerspeed
    if playerright == True:
        playerx += playerspeed
    return (playerx)

#scroll between sides            
def sidetoside (playerx):
    if playerx >= rightborder + playerlw -1:
        playerx = 0
        
    if playerx <= leftborder - playerlw:
        playerx = rightborder - playerlw
        
    return (playerx)

# p1counterincr limits how high the player can jump, p1JumpIncr is how much the y cooridinate changes depending on how long as playerjump is True                                                                                 
def playerymovement(playerup, playerjump, playercounter, playercounterincr, playergravity, playery, playerJumpIncr):
    if playerup == True:
        playerjump = True
        if playerjump:
            if playercounter <= playercounterincr:
                playercounter += 1
                playergravity = False
                playery -= playerJumpIncr
            else:
                playerjump = False 
    return (playerjump, playercounter, playergravity, playery, playerJumpIncr)

#changes the colour of the text when the mouse if hovering over it
def colourchange(range1y, range2x):
    if (100 <= mouseX <= 100 + range2x) and (range1y <= mouseY <= range1y + 50):
        colourfill = (color(255,223,0))
    else:
        colourfill = 255
        
    return (colourfill)

def bonuslevel(bonusclicked):
    global p1x,p1y,p2x,p2y, p1speed, p1speed, p1JumpIncr, p2speed, p2speed, p2JumpInc, p1loop, p2loop, p1counterincr, p2counterincr, p2JumpIncr
    whatlevel = 1
    if bonusclicked == 1:
        whatlevel = -1            
    if bonusclicked == 2:
        whatlevel = 0      
    if bonusclicked == 3:
        whatlevel = -2
    
    return (whatlevel)

def draw():
    global l1p, l1pfills
    global p1x,p1y,p2x,p2y, p1right, p1left, p1up, p2up, p2left, p2right, p1counter, p1jump, p2counter, p2jump, powerupcounter
    global playerlw
    global leftborder, rightborder
    global p1speed, p1speed, p1JumpIncr, p2speed, p2speed, p2JumpIncr
    global p1counterincr, p2counterincr
    global inmenu, howfill, highfill, playfill, p1scorestop, p1timescore, whatlevel, p2scorestop, p2timescore, p1gravity, p2gravity, lasttime, playersonplatform, p1loop, p2loop, scorelist
    global howtoimg, p1name, p2name, whoname
    global backgroundfillred, backgroundfillgreen, backgroundfillblue, sunx, moon1x, moon2x, backgroundmusic, powerupsound, powerupnumber, poweruplist, deathsound, timedifference, whowins
    global player1spawnx, player1spawny, player2spawnx, player2spawny, bonusclicked
    if inmenu == "start":
        background(0)
        textSize(100)
        fill(color(0,100,255))
        text("Sooper Merio",50,100)
        text("Race",250,200)
        textSize(50)
        fill(playfill)
        text("Play Game",100,400)
        fill(highfill)
        text("Highscores",100,500)
        fill(howfill)
        text("How to Play",100,600)
        
        #secret level hint    
        if (181 <= mouseX <= 207) and (54 <= mouseY <= 92):
            fill (255,0,0)
            ellipse(195, 75, 20, 30)
            textSize(30)
            
        #shows the player they found the secret level
        if bonusclicked == 1 or bonusclicked == 3:
            fill (255,0,0)
            textSize(30)
            text ("BONUS ACTIVATED", 500,500)
            
        if bonusclicked == 2:
            textSize(28)
            text ("BONUS DEACTIVATED", 500,500)
            
        #calls the function to change the colour
        playfill = colourchange(350, 250)
        highfill = colourchange(450, 300)
        howfill = colourchange(550, 320)
        
        if whoname == 1:                                                    
            fill(200,0,0)
            textSize(40)
            p1name = "".join([i for i in p1name if i not in "123456789"])
            text("player "+str(whoname)+" enter your name: "+p1name,10,800)
        if whoname == 2:
            fill(200,0,0)
            textSize(40)
            p2name = "".join([i for i in p2name if i not in "123456789"])
            text("player "+str(whoname)+" enter your name: "+p2name,10,800)
    
    if len(p1name) >= 9 or len(p2name) >= 9:
                text("MAX 9 CHARACTERS",200,900)            
                
     #find the difference between when the player clicks play game for the animation of the sun since millis() starts when the program starts       
    if inmenu != "ingame":
        timedifference = millis()
        
    if inmenu == "ingame":
        if bonusclicked == 1 or bonusclicked == 3:
            whatlevel = bonuslevel(bonusclicked) 
            l1p, _, _ = levelselect(whatlevel)
        background(backgroundfillred, backgroundfillgreen, backgroundfillblue)
        
        #in milliseconds to slowly turn the number whole, once whole it reaches the second colour 
        transitionmath = (((millis()-timedifference)%34000)/34000.0)
        #this causes the colour to revert back to the original colour
        if transitionmath >= 0.5:
            transitionmath = (1 - (((millis()-timedifference)%34000)/34000.0))
        
        #slowly changes the colour where 1/1 = second colour and 0/1 = first colour https://forum.processing.org/two/discussion/20861/change-between-colors-over-time
        backgroundfillblue = lerpColor(255, 0, (transitionmath))
        backgroundfillred = lerpColor(30,0, (transitionmath))
        backgroundfillgreen = lerpColor(144,0, (transitionmath))
                                    
        #creation of the sun  
        fill (255,255,0)
        ellipse (sunx,100,150,150) 
        #moon creation, noStroke to avoid any outlines  
        noStroke()  
        fill (240,230,140)
        ellipse (moon1x, 100,150,150)
        #gives the illusion of the moon's crescent shape
        fill (backgroundfillred, backgroundfillgreen, backgroundfillblue)
        ellipse (moon2x, 100, 115, 140) 
          
        #animation for the sun        
        if sunx <= rightborder + 150:
            sunx += 1
            
        if moon2x <= rightborder + 150:
            moon2x += 1
            moon1x += 1
        
        if sunx == rightborder + 150:
            moon1x = -90
            moon2x = -55
            
        if moon2x == rightborder + 150:
            sunx = -75  
            
        #to make everything else have an outline    
        stroke(0)
        #create players
        fill(100)
        rect(p1x,p1y,playerlw,playerlw)
        fill(200)
        rect(p2x,p2y,playerlw,playerlw)
                                
        #Platforms creation; 0 = neutral platorm, 1 = kill platform, 2 = powerup platform 3 = ending platform
        l1pfills = [color(1,142,14),color(255,0,0), color(138,43,226), color(255,105,180)]
            
        #platform creation
        for i in range(len(l1p)):
            fill(l1pfills[l1p[i][0]])
            rect(l1p[i][1],l1p[i][2],l1p[i][3],l1p[i][4])
            
        #this displays both player's name and score in the top right corner
        if whatlevel > 0:            
            textSize(30)
            fill(100)
            text(p1name,5,50)
            text(p1timescore,150,50)
            fill(200)
            text(p2name,5,80)
            text(p2timescore,150,80)
        
        #This makes it so your player falls down when it's not on a boundary/ platform
        p1gravity = True
        p2gravity = True        

        #This starts the timer's countdown and can be paused by switching it to True
        if p1scorestop == False:
            p1timescore -= 1
        if p2scorestop == False:
            p2timescore -= 1
            
        #Initiates the events that occur when landing on a special platform such as teleporting back to spawn
        def landingPlatform(playerx, playery, startingx, startingy, playernumber, playergravity, playercounter):
            global p1speed, p1speed, p1JumpIncr, p2speed, p2speed, p2JumpIncr, powerupcounter
            global p1counterincr, p2counterincr, p1timescore, p2timescore, powerupsound, powerupnumber
            #Bad Platform
            playergravity = False
            playercounter = 0
            #teleport player back to spawn if they land on a red platform
            if l1p[i][0] == 1:
                playery = startingy
                playerx = startingx
            #Powerup Platform
            if l1p[i][0] == 2:
                #sets the platform back to neutral
                powerupsound.loop(0)
                l1p[i][0] = 0
                if playernumber == 1:
                    p1speed, p1counterincr, p2speed, p2JumpIncr, p1timescore, powerupnumber = powerupDecider(p1speed, p1counterincr, p2speed, p2JumpIncr, p1timescore)
                else:
                    p2speed, p2counterincr, p1speed, p1JumpIncr, p2timescore, powerupnumber = powerupDecider(p2speed, p2counterincr, p1speed, p1JumpIncr, p2timescore)
                                                                                                                                                                        
            return (playerx, playery, powerupnumber, playergravity, playercounter)
        
        #displays the text according to the powerup received
        powerup = landingPlatform (p1x, p1y, 100, 900, 1,  p1gravity, p1counter)[2]
        #no powerup = 0
        if powerup > 0:
            textSize(31)
            fill(0,255,0)
            #-1 because lists start at 0
            text(poweruplist[powerup-1], 450,50)   
                                          
    #This the boundary detection used by both players    
        #player 1
        for i in range(len(l1p)):
            if ((p1y + 50) == l1p[i][2]) and not( (p1x < l1p[i][1] and  p1x+50 < l1p[i][1]) or (p1x > l1p[i][1]+l1p[i][3] and p1x+50 > l1p[i][1]+l1p[i][3]) ):
                p1x,p1y,_, p1gravity, p1counter = landingPlatform (p1x, p1y, player1spawnx, player1spawny, 1, p1gravity, p1counter)
                if l1p[i][0] == 1:
                    deathsound.loop(0)
                if l1p[i][0] == 3:
                    #shifts the player to the middle when landing on the pink platform
                    p1x = 375
                    #placed in this kind of statement so it runs once, adds 1 to players on platform
                    if p1loop == 0:
                        playersonplatform += 1
                        p1loop = 1
                    #stops the player's score and forbid the player from moving
                    p1scorestop = True
                    p1speed = 0
                    p1JumpIncr = 0                                
        # #player 2
        for i in range(len(l1p)):
            if ((p2y + playerlw) == l1p[i][2]) and not( (p2x < l1p[i][1] and  p2x+playerlw < l1p[i][1]) or (p2x > l1p[i][1]+l1p[i][3] and p2x+playerlw > l1p[i][1]+l1p[i][3])  ):
                p2x,p2y,_,p2gravity,p2counter = landingPlatform (p2x, p2y, player2spawnx, player2spawny, 2, p2gravity, p2counter)               
                if l1p[i][0] == 1:
                    deathsound.loop(0)
                if l1p[i][0] == 3:
                    #shifts the player to the middle when landing on the pink platform
                    p2x = 375
                    #placed in this kind of statement so it runs once, adds 1 to players on platform
                    if p2loop == 0:
                        playersonplatform += 1
                        p2loop = 1
                    #stops the player's score and forbid the player from moving
                    p2scorestop = True
                    p2speed = 0
                    p2JumpIncr = 0 
                       
        #only activated when both players are on the platform
        if playersonplatform == 2:
            winsound.play(0)
            l1p, whatlevel, _ = levelselect(whatlevel)
            #calls the function reset to set the stats below to deafult
            p1speed, p1JumpIncr, p1loop, p1x, p1y, p1counterincr = reset(p1speed, p1JumpIncr, p1loop, p1x, p1y, p1counterincr, player1spawnx, player1spawny)
            p2speed, p2JumpIncr, p2loop, p2x, p2y, p2counterincr = reset(p2speed, p2JumpIncr, p2loop, p2x, p2y, p2counterincr, player2spawnx, player2spawny)
            powerupnumber = 0
            playersonplatform = 0
            if whatlevel == 4:
                inmenu = "endscreen"
            if whatlevel != 4:
                p1scorestop = False
                p2scorestop = False
            if whatlevel < 0:
                backgroundmusic.pause()
                setup()
                        
        #MOVEMENT OF PLAYERS     
        
        #calling function that allows the player to jump and limits it    
        p1jump, p1counter, p1gravity, p1y, p1JumpIncr = playerymovement(p1up, p1jump, p1counter, p1counterincr, p1gravity, p1y, p1JumpIncr)
        p2jump, p2counter, p2gravity, p2y, p2JumpIncr = playerymovement(p2up, p2jump, p2counter, p2counterincr, p2gravity, p2y, p2JumpIncr)  

        #calling function that allows player to move left and right          
        p1x = playerxmovement (p1x, p1speed, p1left, p1right)
        p2x = playerxmovement (p2x, p2speed, p2left, p2right)
        
        #calling function that enables the player to fall down when not touching a boundary
        p1y = playerygravity (p1gravity, p1JumpIncr, p1y)
        p2y = playerygravity (p2gravity, p2JumpIncr, p2y)
        
        #calling function that allows player to appear on the other side if they move to the right/left border                
        p1x = sidetoside(p1x)
        p2x = sidetoside(p2x) 
     
    #loads the how to play menu
    if inmenu == "howtoplay":
        image(howtoimg, 0, 0, 800, 1000)
        fill(color(0, 255, 0))
        rect(580, 20, 200, 200)
        fill(255, 0, 0)
        textSize(50)
        text("Return", 600, 120)
          
   #loads when all the levels are completed, displays the score and such      
    if inmenu == "endscreen":
        background(0)
        textSize(35)
        fill (34,139,34)
        if p1timescore > p2timescore:
            text(p1name+" won! With "+str(p1timescore)+" points",100,400)
        else:
            text(p2name+" won! With "+str(p2timescore)+" points",100,400)
        fill(color(0, 255, 0))
        rect(580, 20, 200, 200)
        fill(255, 0, 0)
        textSize(50)
        text("Return", 600, 120)
     
     #displays the highscore from the scorelist off the file "highscores.txt"   
    if inmenu == "highscores":        
        background(0)
        fill(color(0,255,0))
        rect(580,780,200,200)
        textSize(100)
        fill(255)
        text("TOP 5 SCORES",50,100)
        textSize(50)
        text("Return",600,900)
        scorelist = get_scores(scorelist)
        for i in range(5):
            text(str(i+1) + ".",100,(i*100)+300)
            text(scorelist[i][0],200,(i*100)+300)
            text("(" + scorelist[i][1] + ")",400,(i*100)+300)
            
        #secrets for the second bonus level    
        if (123 <= mouseX <= 170) and (35 <= mouseY <= 90):
            fill (255,0,0)
            ellipse (150,60,50,65)    
            
        if bonusclicked == 3:
            textSize(30)
            text ("BONUS ACTIVATED", 500,200)
        if bonusclicked == 2:
            textSize(25)
            text ("BONUS DEACTIVATED", 500,200)
            

def keyPressed():
    global p1x,p1y,p2x,p2y
    global p1keys, p2keys, p1right, p1left, p1up, p2up, p2left, p2right, p1gravity, p2gravity, p1name, p2name, whoname
    if inmenu == "ingame":
    #This moves the player's by returning a boolean to the functions above to allow the player to move
        if (key == p1keys[0]) and (p1gravity == False):
            p1up = True
        if (key == p1keys[1]):
            p1left = True
        if (key == p1keys[2]):
            p1right = True
            
        if key == CODED:
            if (keyCode == p2keys[0]) and (p2gravity == False):
                p2up = True
            if (keyCode == p2keys[1]):
                p2left = True
            if (keyCode == p2keys[2]):
                p2right = True
    
    #this is to switch from player 1 to player 2 for typing their name                    
    if key == ENTER and inmenu == "start" and len(p1name) <= 9 and len(p2name) <= 9:
        whoname += 1
                    
    if whoname == 1:
        if key != ENTER:
            #converts whatever you type into string and adds it to a variable with your name
            p1name = p1name + str(key)
        if key == '\b':
            #removes the last letter you typed
            p1name = p1name[:-2]
    if whoname == 2:
        if key != ENTER:
                p2name = p2name + str(key) 
        if key == '\b':
                p2name = p2name[:-2]   
                
                
def keyReleased():
    global p1x,p1y,p2x,p2y
    global p1keys, p2keys, p1right, p1left, p1up, p2up, p2right, p2left, lastUpPressed, l1p
    #This forces the player to fall down if the key is released
    if (key == p1keys[0]):
        p1up = False
    if (key == p1keys[1]):
        p1left = False
    if (key == p1keys[2]):
        p1right = False
                 
    if key == CODED:
        if (keyCode == p2keys[0]):
            p2up = False
        if (keyCode == p2keys[1]):
            p2left = False
        if (keyCode == p2keys[2]):
            p2right = False

def mousePressed():
    global inmenu, whoname, whatlevel, p1speed, p1JumpIncr, p1loop, p1x, p1y, p1counterincr, p2speed, p2JumpIncr, p2loop, p2x, p2y, p2counterincr
    global player1spawnx, player1spawny, player2spawnx, player2spawny, bonusclicked, bonuscounter1, bonuscounter2
    #mouse range for things such as returning to menu and navigating through the menu
    if inmenu == "start":
        if (100 <= mouseX <= 100 + 250) and (350 <= mouseY <= 350 + 50):
            if whoname == 3:
                coinsound.loop(0)
                inmenu = "ingame"
            else:
                print("ENTER YOUR NAMES FIRST")
                
        if (100 <= mouseX <= 100 + 300) and (450 <= mouseY <= 450 + 50):
                coinsound.loop(0)
                inmenu = "highscores"
                
        if (100 <= mouseX <= 100 + 320) and (550 <= mouseY <= 550 + 50):
            inmenu = "howtoplay"            
            coinsound.loop(0)
            
        if (181 <= mouseX <= 207) and (54 <= mouseY <= 92):
            #changes player's x and y cooridinate for specific bonus map
            if bonuscounter1 == 0:
                bonusclicked = 1
                bonuscounter1 = 1
                p1y = 0
                p2y = 0
                player1spawny = 10
                player2spawny = 10 
             #triggered by player clicking same spot again, resets the whole game to bring back the first level  
            else:
                setup()
                backgroundmusic.pause()
                bonusclicked = 2
                bonuscounter1 = 0 
            
    if inmenu == "highscores":         
        if (580 <= mouseX <= 580 + 200) and (780 <= mouseY <= 780 + 200):
                inmenu = "start"
                
        if (123 <= mouseX <= 170) and (35 <= mouseY <= 90):
            #activates the second bonus level
            if bonuscounter2 == 0:
                bonusclicked = 3
                bonuscounter2 = 1        
            #triggered by player clicking same spot again, resets the whole game to bring back the first level  
            else:
                setup()
                backgroundmusic.pause()
                bonusclicked = 2
                bonuscounter2 = 0    
            
    if inmenu == "endscreen":
        if (580 <= mouseX <= 580 + 200) and (20 <= mouseY <= 20 + 200):
            backgroundmusic.pause()
            setup()
            
    if inmenu == "howtoplay":
        if (580 <= mouseX <= 580 + 200) and (20 <= mouseY <= 20 + 200):
            inmenu = "start"