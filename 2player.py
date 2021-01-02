# pacman game in PyGame
# can be played 1 or 2 players
# can change the game board by left and right clicking
# when the game starts a BFsearch is made to find the reachable food spots
# each time a ghost gets to a junction it choses the direction (not backwards) that brings it closer to pacman
# each ghost has a slightly different target (eg left right above below pacman)
######################
#controls
######################
#arrow keys for player 1
#wasd for player 2
#enter to add/remove player 2
#-/+ or o/p to add/remove lives from player 1/2
#space to begin 
######################
import pygame
import sys
import random
import numpy as np
import queue
def main():
    width= 930# size of popup in pixels
    rows= 31  #number of rows
    gridpoints=[[GRIDPOINT(i,j,rows,True) for j in range(rows+1)]for i in range(rows+1)]
    Presetlevel(gridpoints,Preset1)
    sam=PACMAN(15,23,(250,250,0),width,rows)
    sam2=PACMAN(15,23,(0,250,250),width,rows)
    ghosts=AddGhost(width,rows)
    pygame.init() 
    myfont = pygame.font.SysFont('comicsansms',99)
    screen = pygame.display.set_mode((width,width))
    coopplay=False
    while True:
        coopplay=Customising(gridpoints,screen,width,rows,sam,sam2,ghosts,myfont,coopplay)
        Playing(gridpoints,screen,width,rows,sam,sam2,ghosts,myfont,coopplay)
        ResetPositions(sam,sam2,ghosts)
def Customising(gridpoints,screen,width,rows,sam,sam2,ghosts,myfont,coopplay):
    customising=True
    while customising:
        for columns in gridpoints:
            for node in columns:
                node.pacmanshere=False
        sam.Pacmanshere(gridpoints)
        if coopplay:
            sam2.Pacmanshere(gridpoints)
        for ghost in ghosts:
            ghost.Ghosthere(gridpoints)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]: # LEFT
                x,y = pygame.mouse.get_pos()
                i=x//(width//rows)
                j=y//(width//rows)
                if not gridpoints[i][j].pacmanshere and not gridpoints[i][j].ghosthome and not gridpoints[i][j].edge:
                        gridpoints[i][j].border=True
                        gridpoints[i][j].nonborder=False
                        
            if pygame.mouse.get_pressed()[2]: # RIGHT
                x,y = pygame.mouse.get_pos()
                i=x//(width//rows)
                j=y//(width//rows)
                if not gridpoints[i][j].pacmanshere and not gridpoints[i][j].ghosthome and not gridpoints[i][j].edge:
                    gridpoints[i][j].border=False
                    gridpoints[i][j].nonborder=True  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    customising=False
                elif event.key == pygame.K_UP :
                    sam.yposition = (sam.yposition-2) % (rows-2)+1
                elif event.key == pygame.K_DOWN :
                    sam.yposition = (sam.yposition) % (rows-2)+1 
                elif event.key == pygame.K_LEFT :
                     sam.xposition = (sam.xposition-2) % (rows-2)+1
                elif event.key == pygame.K_RIGHT :
                     sam.xposition = (sam.xposition) % (rows-2)+1
                elif event.key == pygame.K_EQUALS and sam.lives<3:
                     sam.lives+=1
                elif event.key == pygame.K_MINUS and sam.lives>1:
                     sam.lives-=1

                elif event.key == pygame.K_w :
                    sam2.yposition = (sam2.yposition-2) % (rows-2)+1
                elif event.key == pygame.K_s:
                    sam2.yposition = (sam2.yposition) % (rows-2)+1 
                elif event.key == pygame.K_a:
                     sam2.xposition = (sam2.xposition-2) % (rows-2)+1
                elif event.key == pygame.K_d:
                     sam2.xposition = (sam2.xposition) % (rows-2)+1
                elif event.key == pygame.K_p and sam2.lives<3:
                     sam2.lives+=1
                elif event.key == pygame.K_o and sam2.lives>1:
                     sam2.lives-=1
                elif event.key == pygame.K_RETURN:
                    coopplay= not coopplay 
                elif event.key == pygame.K_1:
                    Presetlevel(gridpoints,Preset1)
                    sam.xposition=sam.xstartpos
                    sam.yposition=sam.ystartpos 
                    sam2.xposition=sam2.xstartpos
                    sam2.yposition=sam2.ystartpos
                elif event.key == pygame.K_2:
                    Presetlevel(gridpoints,Preset2)
                    sam.xposition=sam.xstartpos
                    sam.yposition=sam.ystartpos 
                    sam2.xposition=sam2.xstartpos
                    sam2.yposition=sam2.ystartpos
                elif event.key == pygame.K_3:
                    Presetlevel(gridpoints,PresetBlank)
                    sam.xposition=sam.xstartpos
                    sam.yposition=sam.ystartpos 
                    sam2.xposition=sam2.xstartpos
                    sam2.yposition=sam2.ystartpos
                
        Drawboard(gridpoints,screen,width,rows,sam,sam2,ghosts,coopplay)
    return coopplay
def Playing(gridpoints,screen,width,rows,sam,sam2,ghosts,myfont,coopplay):
    for col in gridpoints:
        for grid in col:
            if grid.pacmanshere:
                grid.nonborder=True
                grid.border=False
    sam.Pixel(width,rows)
    sam.totallives=sam.lives
    sam2.Pixel(width,rows)
    sam2.totallives=sam2.lives
    foodpoints1=bfsfood(gridpoints, (sam.prevxpos,sam.prevypos))
    foodpoints2=bfsfood(gridpoints, (sam2.prevxpos,sam2.prevypos))
    if coopplay:
        aset=set()
        foodpoints=aset.union(foodpoints1,foodpoints2) 
    else:
        foodpoints=foodpoints1 
    foods=AddFood(foodpoints,rows,width)
    for ghost in ghosts:
        ghost.Pixel(width,rows)
    alive=True 
    foodleft=True
    clock = pygame.time.Clock()
    Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
    countdown=3
    while countdown>0:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        image = myfont.render(str(countdown),True,(250,0,0))
        rect = image.get_rect(center = (width/2 ,width/2))# midtop = (width//rows*15.5 ,width//rows*13 ) )     
        Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
        screen.blit(image , rect)
        pygame.display.update()        
        clock.tick(1.5) 
        countdown-=1
    while alive and foodleft:
        Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP  :
                    sam.clickeddirection=(0,-1)
                elif event.key == pygame.K_DOWN :
                   sam.clickeddirection=(0,1)
                elif event.key == pygame.K_LEFT :
                    sam.clickeddirection=(-1,0)
                elif event.key == pygame.K_RIGHT:
                    sam.clickeddirection=(1,0)
                
                elif event.key == pygame.K_w :
                    sam2.clickeddirection=(0,-1)
                elif  event.key == pygame.K_s:
                   sam2.clickeddirection=(0,1)
                elif  event.key == pygame.K_a:
                    sam2.clickeddirection=(-1,0)
                elif  event.key == pygame.K_d:
                    sam2.clickeddirection=(1,0)
                elif event.key == pygame.K_h:
                    for ghost in ghosts:
                        ghost.retreat=True
        sam.Move(gridpoints,width,rows)
        sam2.Move(gridpoints,width,rows)
        for ghost in ghosts:
            ghost.Move(gridpoints,width,rows,sam,sam2,ghosts,coopplay)
        if  sam.CheckDead(ghosts,width,rows,screen):
            sam.xposition=sam.xstartpos
            sam.yposition=sam.ystartpos 
            sam.Pixel(width,rows)
            sam2.xposition=sam2.xstartpos
            sam2.yposition=sam2.ystartpos 
            sam2.Pixel(width,rows)
            for ghost in ghosts:
                ghost.xposition=ghost.xstartpos
                ghost.yposition=ghost.ystartpos
                ghost.Pixel(width,rows)
            sam.lives-=1
            if sam.lives==0:
                Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
                while alive:
                    image = myfont.render("Game Over",True,(250,0,0))
                    rect = image.get_rect(center = (width/2 ,width/2) )     
                    screen.blit(image , rect)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                alive=False
            if alive:
                Countdown(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,myfont,clock,coopplay)
        if  coopplay and sam2.CheckDead(ghosts,width,rows,screen) :   
            sam.xposition=sam.xstartpos
            sam.yposition=sam.ystartpos 
            sam.Pixel(width,rows)
            sam2.xposition=sam2.xstartpos
            sam2.yposition=sam2.ystartpos 
            sam2.Pixel(width,rows)
            for ghost in ghosts:
                ghost.xposition=ghost.xstartpos
                ghost.yposition=ghost.ystartpos
                ghost.Pixel(width,rows)
            sam2.lives-=1
            if sam2.lives==0:
                Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
                while alive:
                    image = myfont.render("Game Over",True,(250,0,0))
                    rect = image.get_rect(center = (width/2 ,width/2) )     
                    screen.blit(image , rect)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                alive=False

                        
            if alive:
                Countdown(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,myfont,clock,coopplay)    
        
        
        if sam.CheckFoodGone(foods,width,rows):
            Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
            while foodleft:
                image = myfont.render("Winner",True,(250,0,0))
                rect = image.get_rect(center = (width/2 ,width/2) )     
                screen.blit(image , rect)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                foodleft=False 
                  
        if coopplay and sam2.CheckFoodGone(foods,width,rows): #foods2 for own food
            
            Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
            while foodleft:
                image = myfont.render("Winner",True,(250,0,0))
                rect = image.get_rect(center = (width/2 ,width/2) )     
                screen.blit(image , rect)
                pygame.display.update()
                foodleft=False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                foodleft=False        
        clock.tick(40 )     
def ResetPositions(sam,sam2,ghosts):
    sam.xposition=sam.xstartpos
    sam.yposition=sam.ystartpos 
    sam2.xposition=sam2.xstartpos
    sam2.yposition=sam2.ystartpos
    for ghost in ghosts:
        ghost.xposition=ghost.xstartpos
        ghost.yposition=ghost.ystartpos
    sam.lives=3
    sam2.lives=3        
def Countdown(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,myfont,clock,coopplay):
    countdown=3
    while countdown>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        image = myfont.render(str(countdown),True,(250,0,0))
        rect = image.get_rect(center = (width/2 ,width/2) ) #midtop = (width//rows*15.5 ,width//rows*13) )     
        Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay)
        screen.blit(image , rect)
        pygame.display.update()        
        clock.tick(1.5) 
        countdown-=1             
class GRIDPOINT():
    def __init__(self,i,j,rows,extra):
        self.xposition=i
        self.yposition=j
        self.border=False
        self.nonborder=True
        self.pacmanshere=False
        self.colour=(0,0,255)
        self.ghosthome=False
        self.edge=False

       # if i==0 or i==rows-1 or j==0 or j==rows-1:
        #    self.edge=True
         #   self.border=True
          #  self.nonborder=False

    def Addtoborder(self,preset):
        #sets to border if in the set 'preset'
        if (self.xposition,self.yposition) in preset :
            self.border=True
            self.nonborder=False
        else:
            self.nonborder=True
            self.border=False
class PACMAN():
    def __init__(self,i,j,color,width,rows):
        self.color=color
        self.xposition=i
        self.yposition=j
        self.xstartpos=i
        self.ystartpos=j
        speed=7
        while not width//rows% speed ==0:
          speed-=1
        self.speed=speed #non int can go thru walls
        self.direction=(1,0)
        self.clickeddirection=(1,0)
        self.image=pygame.image.load('Games/pacman/pacman.png')
        self.image=pygame.transform.scale(self.image, (width//rows, width//rows)) 
        self.lives=3
    
    def Pacmanshere(self,gridpoints):
        gridpoints[self.xposition][self.yposition].pacmanshere=True
    def Move(self, gridpoints,width,rows):
        if self.xposition % (width//rows)==0 and self.yposition % (width//rows)==0:
            #if on node
            self.nextxpos=self.xposition // (width//rows)
            self.nextypos=self.yposition // (width//rows)
            if not self.nextxpos==self.prevxpos and not self.nextypos==self.prevxpos:
                self.prevprevprevxpos=self.prevprevxpos
                self.prevprevprevypos=self.prevprevypos
                self.prevprevxpos=self.prevxpos
                self.prevprevypos=self.prevypos
            self.prevxpos=self.xposition // (width//rows)
            self.prevypos=self.yposition // (width//rows)
            
            if gridpoints[(self.nextxpos + self.clickeddirection[0])%rows][(self.nextypos + self.clickeddirection[1])%rows].nonborder and not gridpoints[(self.nextxpos + self.clickeddirection[0])%rows][(self.nextypos + self.clickeddirection[1])%rows].ghosthome:
                self.direction=self.clickeddirection
                self.nextxpos =(self.nextxpos + self.direction[0])
                self.nextypos =(self.nextypos + self.direction[1])
            elif gridpoints[(self.nextxpos + self.direction[0])%rows][(self.nextypos + self.direction[1])%rows].nonborder and not gridpoints[(self.nextxpos + self.direction[0])%rows][(self.nextypos + self.direction[1])%rows].ghosthome:
                self.nextxpos =(self.nextxpos + self.direction[0])
                self.nextypos =(self.nextypos + self.direction[1])
        self.direction=((self.nextxpos-self.prevxpos) ,  (self.nextypos- self.prevypos))
        self.xposition =(self.xposition + self.speed*self.direction[0])%width
        self.yposition = (self.yposition +self.speed*self.direction[1])%width

    def Pixel(self,width,rows):
        self.xstartpos= self.xposition
        self.ystartpos= self.yposition
        self.prevxpos=self.xposition
        self.prevypos=self.yposition
        self.prevprevxpos=self.xposition
        self.prevprevypos=self.yposition
        self.prevprevprevxpos=self.xposition
        self.prevprevprevypos=self.yposition 
        self.nextxpos=self.xposition
        self.nextypos=self.yposition
        self.xposition=(width//rows)*self.xposition
        self.yposition=(width//rows)*self.yposition
        
    def CheckDead(self,ghosts,width,rows,screen):
        self.rect=pygame.Rect(self.xposition, self.yposition, width//rows,width//rows )
        for ghost in ghosts:
            if ghost.Collision(self.rect,width,rows,screen):
                return True
        return False
    def CheckFoodGone(self,foods,width,rows):
        self.rect=pygame.Rect(self.xposition, self.yposition, width//rows,width//rows )
        for food in foods:
            if food.Collision(self.rect,width,rows) and not food.eaten:
                food.eaten=True
        for food in foods:
            if not food.eaten:
                return False
        return True
class Ghost():
    def __init__(self,xpos,ypos,color,speed,goal,destination,width,rows):
        self.color=color
        self.xstartpos=xpos
        self.ystartpos=ypos
        self.xposition=xpos
        self.yposition=ypos
        while not width//rows% speed ==0:
            speed-=1
        self.speed=speed
        self.direction=(0,0)
        self.goal=goal
        self.image=pygame.image.load(destination)
        self.image=pygame.transform.scale(self.image, (width//rows, width//rows)) 
    def Ghosthere(self,gridpoints):
        gridpoints[self.xposition][self.yposition].pacmanshere=True
    def Collision(self,playerrect,width,rows,screen):
        self.rect=pygame.Rect(self.xposition+width//rows/4, self.yposition+width//rows/4, width//rows/2,width//rows/2 )
        return self.rect.colliderect(playerrect)
    
    def Pixel(self,width,rows):
        self.xstartpos= self.xposition
        self.ystartpos= self.yposition
        self.prevxpos=self.xposition
        self.prevypos=self.yposition
        self.nextxpos=self.xposition
        self.nextypos=self.yposition
        self.xposition=(width//rows)*self.xposition
        self.yposition=(width//rows)*self.yposition
        self.retreat=False
        self.ishome=False
    
    def Move(self, gridpoints,width,rows,sam,sam2,ghosts,coopplay):
        if self.xposition % (width//rows)==0 and self.yposition % (width//rows)==0:
            #if on node
            self.prevxpos=self.xposition // (width//rows)
            self.prevypos=self.yposition // (width//rows)
            if gridpoints[self.prevxpos][self.prevypos].ghosthome:
                self.retreat=False #if home randomly moves about until finding ghost home
                directionchoice=[(self.prevxpos+1,self.prevypos),(self.prevxpos-1,self.prevypos),(self.prevxpos,self.prevypos+1),(self.prevxpos,self.prevypos-1)]
                if (self.prevxpos-self.direction[0],self.prevypos-self.direction[1]) in directionchoice:
                    directionchoice.remove((self.prevxpos-self.direction[0],self.prevypos-self.direction[1]))
                self.clickeddirection=(self.prevxpos-self.direction[0],self.prevypos-self.direction[1])
                distance=100000
                while directionchoice:
                    random.shuffle(directionchoice)
                    popped=directionchoice.pop()
                    if  gridpoints[popped[0]][popped[1]].nonborder:#poppeddist<distance and
                        #distance=poppeddist
                        self.clickeddirection=popped
                        if not gridpoints[popped[0]][popped[1]].ghosthome:
                            break
            
            elif self.retreat:
                directionchoice=[(self.prevxpos+1,self.prevypos),(self.prevxpos-1,self.prevypos),(self.prevxpos,self.prevypos+1),(self.prevxpos,self.prevypos-1)]
                if (self.prevxpos-self.direction[0],self.prevypos-self.direction[1]) in directionchoice:
                    directionchoice.remove((self.prevxpos-self.direction[0],self.prevypos-self.direction[1]))
                self.clickeddirection=(self.prevxpos-self.direction[0],self.prevypos-self.direction[1])
                distance=100000
                while directionchoice:
                    popped=directionchoice.pop()
                    poppeddist=(popped[0]-15)*(popped[0]-15)+(popped[1]-14)*(popped[1]-14)
                    if poppeddist<distance and gridpoints[popped[0]][popped[1]].nonborder==True:
                        distance=poppeddist
                        self.clickeddirection=popped
            else:
                directionchoice=[(self.prevxpos+1,self.prevypos),(self.prevxpos-1,self.prevypos),(self.prevxpos,self.prevypos+1),(self.prevxpos,self.prevypos-1)]
                if (self.prevxpos-self.direction[0],self.prevypos-self.direction[1]) in directionchoice:
                    directionchoice.remove((self.prevxpos-self.direction[0],self.prevypos-self.direction[1]))
                self.clickeddirection=(self.prevxpos-self.direction[0],self.prevypos-self.direction[1])
                distance=100000
                while directionchoice:
                    popped=directionchoice.pop()
                    
                    poppeddist1=(popped[0]-sam.nextxpos-self.goal[0])*(popped[0]-sam.nextxpos-self.goal[0])+(popped[1]-sam.nextypos-self.goal[1])*(popped[1]-sam.nextypos-self.goal[1])
                    if coopplay:
                        poppeddist2=(popped[0]-sam2.nextxpos-self.goal[0])*(popped[0]-sam2.nextxpos-self.goal[0])+(popped[1]-sam2.nextypos-self.goal[1])*(popped[1]-sam2.nextypos-self.goal[1])
                    else:
                        poppeddist2=100000
                    poppeddist=min(poppeddist1,poppeddist2)
                    if poppeddist<distance and gridpoints[popped[0]][popped[1]].nonborder:
                        distance=poppeddist
                        self.clickeddirection=popped
            self.nextxpos=self.clickeddirection[0]
            self.nextypos=self.clickeddirection[1]        
        self.direction=((self.nextxpos-self.prevxpos) ,  (self.nextypos- self.prevypos))
        self.xposition =(self.xposition + self.speed*self.direction[0])%width
        self.yposition = (self.yposition +self.speed*self.direction[1])%width
        self.rect=pygame.Rect(self.xposition, self.yposition, width//rows,width//rows )
        #if random.randint(0,2000)==0:
         #   self.retreat=True
class Food():
    def __init__(self,i,j):
        self.xposition=i
        self.yposition=j
        self.color=(250,150,250)
        self.eaten=False
    def Collision(self,playerrect,width,rows):
        self.rect=pygame.Rect(self.xposition+width//rows/3, self.yposition+width//rows/3, width//rows/3,width//rows/3 )
        if self.rect.colliderect(playerrect):
            return True
        return False
def bfsfood(gridpoints, start):
    ###applies a BFS to find all food accessable by PacMan
    queue = [start]
    visited = set()
    rows= len(gridpoints)-1
    while queue:
        # Gets the first path in the queue
        vertex = queue.pop(0)
        # Gets the last node in the path
        # We check if the current node is already in the visited nodes set in order not to recheck it
        if vertex not in visited:
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            graph_to_search=[]
            if gridpoints[(vertex[0]+1)%rows][vertex[1]].nonborder and not gridpoints[(vertex[0]+1)%rows][vertex[1]].ghosthome:
                graph_to_search.append(((vertex[0]+1)%rows,vertex[1]))
            if gridpoints[(vertex[0]-1)%rows][vertex[1]].nonborder and not gridpoints[(vertex[0]-1)%rows][vertex[1]].ghosthome:
                graph_to_search.append(((vertex[0]-1)%rows,vertex[1]))
            if gridpoints[vertex[0]][(vertex[1]+1)%rows].nonborder and not gridpoints[vertex[0]][(vertex[1]+1)%rows].ghosthome :
                graph_to_search.append((vertex[0],(vertex[1]+1)%rows))
            if gridpoints[vertex[0]][(vertex[1]-1)%rows].nonborder and not gridpoints[vertex[0]][(vertex[1]-1)%rows].ghosthome :
                graph_to_search.append((vertex[0],(vertex[1]-1)%rows))
            for current_neighbour in graph_to_search:
                queue.append(current_neighbour)
            # Mark the vertex as visited
            visited.add(vertex)
    return visited
def Presetlevel(gridpoints,Preset):
    preset=Preset()
    for i in range (len(gridpoints)):
        for j in range (len(gridpoints)):
            gridpoints[i][j].Addtoborder(preset)
    for node in Ghosthome():
        gridpoints[node[0]][node[1]].ghosthome=True
        gridpoints[node[0]][node[1]].nonborder=True
        gridpoints[node[0]][node[1]].border=False      
def Drawboard(gridpoints,screen,width,rows,sam,sam2,ghosts,coopplay):
    screen.fill((0,0,0))
    for column in gridpoints:
        for node in column:
            if node.border:
                pygame.draw.rect(screen, (0,0,250), (width//rows*node.xposition, width//rows*node.yposition, width//rows,width//rows ) )
            elif node.ghosthome:
                pygame.draw.rect(screen, (100,250,250), (width//rows*node.xposition, width//rows*node.yposition, width//rows,width//rows ) )
    for i in range(rows+1):
        gridsize=width//rows
        pygame.draw.line(screen,(0,250,0),(0,i*gridsize) , (width,i*gridsize))
    for j in range(rows+1):
        pygame.draw.line(screen,(0,250,0),(j*gridsize,0) , (j*gridsize,width))
    pygame.draw.rect(screen, sam.color, (width//rows*sam.xposition, width//rows*sam.yposition, width//rows,width//rows ) )
    if coopplay:
        pygame.draw.rect(screen, sam2.color, (width//rows*sam2.xposition, width//rows*sam2.yposition, width//rows,width//rows ) )
    livesdrawn=0
    for i in range(3):
        pygame.draw.circle(screen, (0), (width//rows*(14+i)+width//rows/2, width//rows*(14)+width//rows/2), width//rows/2-1)
        if livesdrawn<sam.lives:
            pygame.draw.circle(screen, sam.color, (width//rows*(14+i)+width//rows/2, width//rows*(14)+width//rows/2), width//rows/2-4)
            livesdrawn+=1
    livesdrawn=0
    if coopplay:
        for i in range(3):
            pygame.draw.circle(screen, (0), (width//rows*(14+i)+width//rows/2, width//rows*(15)+width//rows/2), width//rows/2-1)
            if livesdrawn<sam2.lives:
                pygame.draw.circle(screen, sam2.color, (width//rows*(14+i)+width//rows/2, width//rows*(15)+width//rows/2), width//rows/2-4)
                livesdrawn+=1    
    pygame.display.update()
def Drawgame(gridpoints,screen,width,rows,sam,sam2,ghosts,foods,coopplay):
    screen.fill((0,0,0))
    for ghost in ghosts:
        pygame.draw.rect(screen, ghost.color, (ghost.xposition, ghost.yposition, width//rows,width/rows ) )
        #pacrect=pygame.Rect(ghost.xposition, ghost.yposition, width//rows,width/rows )
        #screen.blit(ghost.image,pacrect)
    for column in gridpoints:
        for node in column:
            if node.border:
                pygame.draw.rect(screen, (0,0,250), (width//rows*node.xposition, width//rows*node.yposition, width//rows,width//rows ) )
            elif node.ghosthome:
                 pygame.draw.rect(screen, (100,250,250), (width//rows*node.xposition, width//rows*node.yposition, width//rows,width//rows ) )
    #pygame.draw.rect(screen, sam.color, (sam.xposition, sam.yposition, width//rows,width//rows ) )
    pygame.draw.circle(screen, sam.color, (sam.xposition+width//rows/2, sam.yposition+width//rows/2), width//rows/2)
    if coopplay:
        pygame.draw.circle(screen, sam2.color, (sam2.xposition+width//rows/2, sam2.yposition+width//rows/2), width//rows/2)
    for food in foods: 
        if not food.eaten:
           # pygame.draw.rect(screen, food.color, (food.xposition+width//rows/3, food.yposition+width//rows/3, width//rows/3,width//rows/3 ) )
            pygame.draw.circle(screen, food.color, (food.xposition+width//rows/2, food.yposition+width//rows/2), width//rows/6 )
    
    totaldrawn=0
    livesdrawn=0
    for i in range(3):
        if totaldrawn<sam.totallives:
            totaldrawn+=1
            pygame.draw.circle(screen, (0), (width//rows*(14+i)+width//rows/2, width//rows*(14)+width//rows/2), width//rows/2-1)
    for i in range(3):
        if livesdrawn<sam.lives:
            pygame.draw.circle(screen, sam.color, (width//rows*(14+i)+width//rows/2, width//rows*(14)+width//rows/2), width//rows/2-4)
            livesdrawn+=1
    totaldrawn=0
    if coopplay:
        livesdrawn=0
        for i in range(3):
            if totaldrawn<sam2.totallives:
                totaldrawn+=1
                pygame.draw.circle(screen, (0), (width//rows*(14+i)+width//rows/2, width//rows*(15)+width//rows/2), width//rows/2-1)
        for i in range(3):
            if livesdrawn<sam2.lives:
                pygame.draw.circle(screen, sam2.color, (width//rows*(14+i)+width//rows/2, width//rows*(15)+width//rows/2), width//rows/2-4)
                livesdrawn+=1
            

    
    
    pygame.display.update()
def AddGhost(width,rows):
    ghosts=set()
    ghosts.add(Ghost(14,14,(200,100,100),5,(0,0),'Games/pacman/ghost1.png',width,rows)) #red
    ghosts.add(Ghost(16,14,(100,200,100),5,(3,0),'Games/pacman/ghost2.png',width,rows)) # green 
    ghosts.add(Ghost(14,15,(200,100,200),5,(-3,0),'Games/pacman/ghost3.png',width,rows  )) #pink
    ghosts.add(Ghost(15,14,(100,100,200),5,(0,3),'Games/pacman/ghost6.png',width,rows ))#purple
    ghosts.add(Ghost(15,14,(100,200,200),5,(0,-3),'Games/pacman/ghost6.png',width,rows ))#blue
    return ghosts
def AddFood(foodpoints,rows,width):# pathfinding 
    foods=set()
    for food in foodpoints:
        foods.add(Food(width//rows*food[0],width//rows*food[1]))
    return foods
def Preset1():
    #set of borders
   return {(0, 15),(30, 15),(15, 21), (26, 21), (15, 30), (26, 30), (27, 4), (8, 0), (19, 0), (30, 0), (27, 13), (30, 9), (19, 9), (8, 9), (0, 5), (30, 18), (8, 18), (19, 18), (11, 14), (0, 23), (10, 27), (25, 25), (4, 2), (22, 10), (3, 6), (22, 19), (3, 15), (22, 28), (14, 24), (3, 24), (15, 7), (26, 7), (18, 3), (15, 16), (26, 16), (18, 12), (15, 25), (18, 21), (7, 30), (18, 30), (29, 27), (30, 4), (8, 4), (19, 4), (0, 0), (11, 0), (30, 13), (0, 9), (11, 9), (25, 11), (10, 22), (14, 1), (14, 10), (3, 10), (14, 19), (3, 19), (14, 28), (3, 28), (26, 2), (15, 2), (26, 11), (18, 7), (18, 16), (29, 13), (29, 22), (21, 18), (21, 27), (11, 4), (25, 6), (25, 15), (2, 13), (25, 24), (22, 0), (22, 9), (22, 18), (22, 27), (15, 6), (17, 25), (26, 6), (18, 2), (28, 25), (9, 30), (29, 8), (29, 17), (6, 15), (21, 13), (29, 26), (6, 24), (21, 22), (10, 3), (25, 10), (10, 21), (2, 17), (25, 19), (10, 30), (25, 28), (22, 4), (3, 
    0), (14, 0), (22, 13), (14, 9), (3, 9), (14, 18), (3, 18), (5, 27), (9, 25), (29, 3), (29, 12), (6, 10), (21, 8), (29, 21), (6, 19), (21, 17), (29, 30), (6, 28), (21, 26), (2, 12), (2, 30), (22, 8), (24, 27), (14, 4), (3, 4), (17, 6), (28, 15), (17, 15), (9, 11), (17, 24), (5, 22), (28, 24), (29, 7), (21, 3), (29, 16), (21, 12), (29, 25), (6, 23), (21, 21), (21, 30), (10, 2), (25, 0), (25, 9), (2, 16), (24, 13), (13, 13), (24, 22), (16, 18), (1, 
    29), (16, 27), (28, 10), (9, 6), (17, 19), (5, 17), (28, 19), (9, 15), (9, 24), (29, 2), (6, 0), (29, 11), (6, 9), (21, 7), (6, 18), (21, 16), (12, 25), (2, 11), (4, 30), (1, 15), (24, 17), (16, 13), (1, 24), (16, 22), (5, 3), (5, 12), (17, 14), (9, 10), (5, 21), (9, 19), (5, 30), (9, 28), (29, 6), (6, 4), (21, 2), (6, 13), (24, 3), (1, 10), (24, 12), (13, 12), (16, 8), (1, 19), (24, 21), (13, 30), (24, 30), (1, 28), (16, 26), (17, 0), (28, 0), (28, 9), (5, 7), (28, 18), (5, 16), (5, 25), (27, 22), (19, 27), (30, 27), (8, 27), (20, 10), (12, 6), (12, 15), (20, 28), (4, 11), (12, 24), (13, 7), (1, 5), (24, 7), (16, 3), (24, 16), (13, 16), (16, 12), (1, 23), (24, 25), 
    (16, 21), (16, 30), (5, 2), (9, 0), (5, 11), (9, 9), (27, 17), (19, 13), (8, 13), (30, 22), (8, 22), (19, 22), (0, 18), (11, 18), (0, 27), (11, 27), (12, 10), (4, 6), (12, 19), (4, 15), (12, 28), (23, 28), (1, 0), (24, 2), (1, 9), (24, 11), (16, 7), (1, 18), (16, 16), (15, 20), (5, 6), (18, 25), (27, 3), (27, 12), (30, 8), (8, 8), (27, 21), (0, 4), (30, 17), (8, 17), (27, 30), (0, 13), (11, 13), (30, 26), (8, 26), (0, 22), (11, 22), (20, 0), (20, 9), (12, 14), (4, 10), (4, 19), (4, 28), (1, 4), (24, 6), (16, 2), (1, 13), (26, 15), (15, 24), (27, 7), (30, 3), (8, 3), (19, 3), (27, 16), (30, 12), (8, 12), (19, 12), (0, 8), (27, 25), (30, 21), (8, 21), (19, 21), (0, 17), (8, 30), (19, 30), (30, 30), (0, 26), (20, 4), (12, 0), (23, 0), (12, 9), (22, 22), (14, 27), (3, 27), (15, 1), (15, 10), (26, 10), (18, 6), (15, 19), (26, 19), (18, 15), (15, 28), (26, 28), (18, 24), (27, 2), (27, 11), (30, 7), (19, 7), (8, 7), (0, 3), (11, 3), (30, 16), (8, 16), (19, 16), (0, 12), (11, 12), (19, 25), (30, 25), (0, 21), (11, 21), (11, 30), (12, 4), (25, 23), (4, 0), (4, 9), (22, 17), (3, 13), (22, 26), (14, 13), (14, 22), (3, 
    22), (18, 10), (18, 19), (7, 28), (18, 28), (27, 6), (8, 2), (19, 2), (30, 2), (30, 11), (8, 11), (0, 7), (11, 7), (0, 16), (11, 16), (25, 18), (2, 25), (25, 27), (22, 3), (22, 12), (14, 8), (22, 21), (3, 17), (22, 30), (14, 
    26), (15, 0), (26, 0), (15, 9), (26, 9), (15, 18), (26, 18), (18, 14), (29, 20), (29, 29), (6, 27), (30, 6), (19, 6), (21, 25), (0, 2), (11, 2), (25, 4), (25, 13), (25, 22), (22, 7), (14, 3), (3, 3), (22, 16), (3, 12), (22, 25), (14, 12), (14, 21), (3, 21), (3, 30), (14, 30), (15, 4), (26, 4), (7, 0), (18, 0), (26, 13), (18, 9), (18, 18), (29, 15), (21, 11), (29, 24), (6, 22), (10, 10), (25, 17), (2, 15), (10, 28), (2, 24), (22, 2), (22, 11), (14, 7), (3, 7), (14, 16), (3, 16), (14, 25), (3, 25), (17, 18), (18, 4), (29, 1), (26, 12), (29, 10), (21, 6), (29, 19), (6, 17), (21, 15), (29, 28), (21, 24), (25, 3), (2, 10), (25, 12), (2, 19), (25, 21), (22, 6), (13, 25), (14, 2), (3, 2), (3, 11), (28, 13), (17, 13), (9, 18), (9, 27), (29, 5), (6, 3), (6, 12), (21, 10), (29, 23), (6, 21), (21, 19), (6, 30), (21, 28), (10, 0), (10, 9), (25, 7), (25, 16), (1, 27), (14, 6), (16, 25), (9, 4), (28, 
    17), (5, 15), (9, 13), (5, 24), (9, 22), (29, 0), (29, 9), (6, 7), (29, 18), (6, 16), (6, 25), (20, 27), (10, 4), (2, 0), (25, 2), (2, 9), (13, 6), (2, 18), (24, 15), (13, 15), (1, 22), (13, 24), (24, 24), (16, 20), (5, 10), 
    (28, 12), (17, 12), (9, 8), (5, 19), (9, 17), (17, 30), (28, 30), (5, 28), (9, 26), (6, 2), (29, 4), (21, 0), (6, 11), (21, 9), (20, 22), (12, 18), (12, 27), (23, 27), (1, 8), (24, 10), (16, 6), (13, 19), (1, 17), (24, 19), (1, 26), (24, 28), (16, 24), (17, 7), (9, 3), (28, 16), (17, 16), (9, 12), (5, 23), (9, 21), (6, 6), (8, 25), (21, 4), (0, 30), (12, 13), (12, 22), (4, 18), (4, 27), (1, 3), (16, 1), (1, 12), (13, 14), (16, 10), (1, 21), (24, 
    23), (16, 19), (1, 30), (16, 28), (5, 0), (5, 9), (28, 11), (9, 7), (5, 18), (9, 16), (27, 15), (27, 24), (30, 20), (30, 29), (0, 25), (11, 25), (20, 3), (20, 21), (4, 4), (20, 30), (4, 13), (4, 22), (13, 0), (24, 0), (1, 7), (24, 9), (13, 18), (1, 16), (24, 18), (1, 25), (15, 27), (26, 27), (5, 4), (9, 2), (5, 13), (27, 10), (8, 6), (27, 19), (8, 15), (19, 15), (0, 11), (27, 28), (19, 24), (30, 24), (8, 24), (0, 20), (0, 29), (12, 3), 
    (12, 12), (12, 21), (4, 17), (12, 30), (23, 30), (1, 2), (24, 4), (16, 0), (1, 11), (16, 9), (1, 20), (15, 22), (26, 22), (18, 27), (7, 27), (30, 1), (30, 10), (19, 10), (8, 10), (0, 6), (11, 6), (19, 19), (30, 19), (8, 19), 
    (11, 15), (30, 28), (8, 28), (19, 28), (0, 24), (11, 24), (20, 2), (12, 7), (4, 3), (12, 16), (4, 12), (4, 21), (1, 6), (16, 4), (15, 8), (26, 17), (18, 13), (15, 26), (18, 22), (27, 0), (27, 9), (30, 5), (27, 18), (0, 1), (19, 14), (27, 27), (0, 10), (11, 10), (30, 23), (0, 19), (11, 19), (0, 28), (11, 28), (12, 2), (25, 30), (4, 7), (4, 16), (22, 15), (22, 24), (1, 1), (14, 20), (15, 3), (26, 3)}
def Preset2():
    return {(26, 21), (15, 30), (26, 30), (7, 26), (18, 26), (8, 0), (19, 0), (30, 0), (8, 9), (19, 9), (30, 9), (0, 5), (11, 5), (8, 18), (30, 18), (0, 14), (0, 23), (10, 27), (25, 25), (22, 10), (3, 6), (22, 19), (3, 15), (3, 24), (14, 24), (15, 7), (26, 7), (7, 3), (18, 3), (15, 16), (26, 16), (7, 12), (18, 12), (26, 25), (7, 21), (7, 30), (18, 30), (29, 27), (8, 4), (19, 4), (30, 4), (0, 0), (11, 0), (30, 13), (0, 9), (11, 9), (25, 11), (10, 22), (25, 20), (10, 31), (2, 27), (25, 29), (22, 5), 
    (3, 1), (14, 1), (22, 14), (14, 10), (14, 19), (14, 28), (26, 11), (26, 20), (18, 16), (21, 18), (6, 29), (29, 31), (21, 27), (11, 4), (10, 8), (25, 6), (2, 13), (25, 15), (10, 26), (2, 22), (25, 24), (22, 0), (2, 31), (22, 9), (22, 18), (3, 14), (15, 6), (17, 25), (26, 6), (9, 30), (6, 15), (21, 13), (6, 24), (29, 26), (21, 22), (21, 31), (25, 1), (10, 12), (2, 8), (25, 10), (10, 21), (2, 17), (25, 19), (10, 30), (2, 26), (22, 4), (3, 0), (14, 0), (22, 13), (14, 9), (14, 18), (26, 1), (17, 20), (28, 20), (5, 27), (28, 29), (9, 25), (29, 3), (6, 10), (21, 8), (6, 19), (21, 26), (2, 3), (10, 16), (2, 12), (25, 14), (10, 25), (2, 21), (2, 30), (22, 8), (13, 27), (24, 27), (14, 4), (17, 6), (28, 6), (17, 15), (28, 15), (5, 22), (17, 24), (28, 24), (5, 31), (9, 29), (21, 3), (6, 14), (21, 12), (21, 21), (21, 30), (25, 0), (2, 7), (25, 9), (2, 16), (13, 13), (13, 22), (24, 22), (16, 18), (13, 31), (24, 31), (16, 27), (17, 1), (28, 1), (28, 10), (9, 6), (17, 19), (28, 19), (9, 15), (5, 26), (17, 28), (9, 24), (6, 0), (6, 9), (21, 7), (6, 18), (21, 16), (20, 29), (31, 29), (12, 25), (23, 25), (2, 11), (4, 30), (16, 13), (13, 26), (24, 26), (16, 22), (16, 31), (5, 3), (9, 1), (5, 12), (17, 14), (28, 14), (9, 10), (5, 21), (28, 23), (9, 19), (5, 30), (6, 4), (20, 15), (31, 15), (20, 24), (31, 24), (12, 20), (23, 20), (23, 29), (4, 25), (24, 3), (13, 12), (24, 12), (16, 8), (24, 21), (13, 30), (24, 30), (16, 26), (17, 0), (28, 0), (5, 7), (28, 9), (9, 5), (5, 16), (28, 18), (9, 14), (5, 25), (27, 31), (30, 27), (20, 1), (31, 1), (20, 10), (31, 10), (12, 6), (20, 19), (31, 19), (12, 15), (31, 28), (4, 11), (12, 24), (23, 24), (4, 20), (4, 29), (24, 7), (16, 3), (13, 16), (24, 16), (16, 12), (24, 25), (16, 30), (28, 4), (9, 0), (5, 11), (9, 9), (8, 13), (19, 22), (30, 22), (0, 18), (8, 31), (19, 31), (30, 31), (0, 27), (31, 5), (12, 1), (23, 1), (20, 14), (31, 14), (12, 10), (20, 23), (4, 6), (31, 23), (12, 19), (23, 19), (4, 15), (12, 28), (4, 24), (24, 11), (16, 7), (16, 16), (26, 29), (5, 6), (7, 25), (18, 25), (8, 8), (19, 8), (30, 8), (0, 4), (30, 17), (27, 30), (0, 13), (30, 26), (0, 22), (11, 22), (20, 0), (31, 0), (0, 31), (11, 31), (20, 9), (31, 9), (12, 5), (20, 18), (4, 1), (31, 18), (12, 14), (4, 10), (4, 19), (1, 4), (24, 6), (26, 15), (26, 24), (7, 20), 
    (18, 20), (7, 29), (27, 7), (8, 3), (19, 3), (27, 16), (30, 3), (8, 12), (30, 12), (0, 8), (11, 8), (30, 21), (0, 17), (8, 30), (19, 30), (30, 30), (0, 26), (31, 4), (12, 0), (23, 0), (20, 13), (31, 13), (12, 9), (23, 18), (4, 14), (22, 31), (14, 27), (15, 1), (15, 10), (26, 10), (18, 6), (26, 19), (18, 15), (7, 24), (18, 24), (8, 7), (30, 7), (11, 3), (0, 3), (8, 16), (30, 16), (0, 12), (30, 25), (0, 21), (11, 30), (12, 4), (23, 4), (4, 0), (4, 9), (14, 13), (14, 22), (3, 31), (14, 31), (7, 1), (18, 1), (26, 14), (18, 10), (15, 23), (7, 19), (18, 19), (18, 28), (27, 6), (30, 2), (30, 11), (0, 7), (0, 16), (25, 18), (10, 29), (25, 27), (22, 3), (22, 12), (14, 8), (22, 30), (14, 26), (15, 0), (26, 0), (15, 9), (26, 9), (18, 5), (26, 18), (18, 14), (27, 1), (6, 27), (19, 6), (21, 25), (30, 6), (0, 2), (25, 4), 
    (10, 15), (10, 24), (2, 20), (25, 22), (2, 29), (25, 31), (22, 7), (14, 3), (22, 16), (14, 12), (3, 30), (14, 30), (15, 4), (26, 4), (7, 0), (18, 0), (18, 9), (18, 
    18), (6, 22), (6, 31), (21, 29), (10, 1), (10, 10), (2, 6), (10, 19), (2, 15), (2, 24), (25, 26), (3, 7), (14, 7), (3, 16), (14, 16), (14, 25), (17, 18), (17, 27), 
    (28, 27), (7, 4), (9, 23), (18, 4), (21, 6), (21, 15), (6, 26), (21, 24), (2, 1), (25, 3), (10, 14), (2, 10), (25, 12), (10, 23), (2, 19), (25, 21), (22, 6), (13, 25), (17, 13), (28, 13), (5, 20), (17, 22), (28, 22), (9, 18), (5, 29), (17, 31), (28, 31), (9, 27), (6, 3), (21, 1), (6, 12), (21, 10), (6, 21), (21, 19), (6, 30), 
    (10, 0), (10, 9), (25, 7), (10, 18), (2, 14), (25, 16), (2, 23), (22, 1), (13, 20), (24, 20), (1, 27), (24, 29), (14, 6), (16, 25), (28, 8), (9, 4), (5, 15), (28, 17), (9, 13), (5, 24), (17, 26), (28, 26), (9, 22), (9, 31), (6, 7), (21, 5), (6, 16), (21, 14), (6, 25), (21, 23), (20, 27), (31, 27), (2, 0), (10, 13), (2, 9), (13, 6), (2, 18), (13, 15), (24, 15), (13, 24), (24, 24), (16, 20), (1, 31), (5, 1), (28, 3), (5, 10), (17, 12), (28, 12), (9, 8), (5, 19), (28, 21), (17, 30), (28, 30), (9, 26), (29, 4), (21, 0), (6, 11), (21, 9), (6, 20), (20, 22), (31, 22), (12, 18), (20, 31), (31, 31), (12, 27), (23, 27), (2, 4), (13, 1), (24, 1), (24, 10), (16, 6), (13, 19), (24, 19), (1, 26), (13, 28), (16, 24), (28, 7), (9, 3), (5, 14), (17, 16), (28, 16), (9, 12), (9, 21), (27, 29), (6, 6), (21, 4), (0, 30), (20, 8), (31, 8), (31, 17), (12, 13), (20, 26), (31, 26), (12, 22), (23, 22), (4, 18), (12, 31), (23, 31), (4, 27), (1, 3), (16, 1), (13, 14), (24, 14), (16, 10), (16, 19), (16, 28), (5, 0), (5, 9), (28, 11), (9, 7), (5, 18), (9, 16), (27, 15), (27, 24), (6, 1), (30, 20), (8, 29), (30, 29), (0, 25), (31, 3), (20, 12), (31, 12), (12, 
    8), (20, 21), (4, 4), (31, 21), (20, 30), (31, 30), (12, 26), (23, 26), (4, 22), (13, 0), (24, 0), (4, 31), (24, 9), (13, 18), (24, 18), (26, 27), (5, 4), (8, 6), (8, 15), (30, 15), (0, 11), (30, 24), (0, 20), (0, 29), (31, 7), (12, 3), (23, 3), (20, 16), (31, 16), (12, 12), (23, 12), (20, 25), (31, 25), (23, 21), (12, 30), (23, 30), (4, 26), (24, 4), (16, 0), (16, 9), (15, 22), (26, 22), (7, 18), (15, 31), (26, 31), (7, 27), (18, 27), (8, 1), (19, 1), (27, 14), (30, 1), (8, 10), (19, 10), (30, 10), (0, 6), (11, 6), (8, 19), (30, 19), (0, 15), (30, 28), (0, 24), (31, 2), (31, 11), (31, 20), (4, 3), (12, 16), (4, 12), (4, 21), (22, 29), (16, 4), (15, 8), (18, 13), (26, 26), (7, 22), (18, 22), (27, 0), (7, 31), (18, 31), (8, 5), (19, 5), (30, 5), (0, 1), (11, 1), (8, 14), (30, 14), (0, 10), (11, 10), (30, 23), 
    (0, 19), (0, 28), (31, 6), (25, 30), (4, 7), (4, 16), (22, 15), (14, 20), (3, 29), (15, 3), (26, 3), (26, 12), (18, 8)}
def PresetBlank():
    return {(15, 21), (26, 21), (7, 17), (18, 17), (15, 30), (26, 30), (7, 26), (18, 26), (27, 4), (8, 0), (19, 0), (27, 13), (30, 0), (8, 9), (19, 9), (30, 9), (0, 5), (11, 5), (8, 18), (19, 18), (30, 18), (0, 14), (11, 14), (0, 23), (11, 23), (10, 27), (25, 25), (4, 2), (22, 10), (3, 6), (22, 19), (3, 15), (22, 28), (3, 24), (14, 24), 
    (15, 7), (26, 7), (7, 3), (18, 3), (15, 16), (26, 16), (7, 12), (18, 12), (15, 25), (26, 25), (7, 21), (18, 21), (7, 30), (18, 30), (27, 8), (29, 27), (8, 4), (19, 
    4), (30, 4), (0, 0), (11, 0), (30, 13), (0, 9), (11, 9), (25, 11), (10, 22), (25, 20), (2, 27), (25, 29), (22, 5), (3, 1), (14, 1), (22, 14), (14, 10), (3, 10), (22, 23), (3, 19), (14, 19), (3, 28), (14, 28), (15, 2), (26, 2), (15, 11), (26, 11), (7, 7), (18, 7), (26, 20), (7, 16), (18, 16), (29, 13), (29, 22), (21, 18), (6, 29), (21, 27), (11, 4), (10, 8), (25, 6), (10, 17), (2, 13), (25, 15), (10, 26), (2, 22), (25, 24), (22, 0), (22, 9), (3, 5), (14, 5), (22, 18), (3, 14), (22, 27), (3, 23), (14, 23), (15, 6), (17, 25), (26, 6), (7, 2), (18, 2), (28, 25), (7, 11), (9, 30), (18, 11), (29, 8), (6, 15), (29, 17), (21, 13), (6, 24), (29, 26), (21, 22), (10, 3), (25, 1), (10, 12), (2, 8), (25, 10), (10, 21), (2, 17), (25, 19), (10, 30), (2, 26), (25, 28), (22, 4), (3, 0), (14, 0), (22, 13), (3, 9), (14, 9), (3, 18), (14, 18), (26, 1), (17, 20), (28, 20), (5, 27), (17, 29), (28, 29), (9, 25), (29, 3), (6, 10), (29, 12), (21, 8), (6, 19), (29, 21), (21, 17), (6, 28), (29, 30), (21, 26), (10, 7), (2, 3), (25, 5), (10, 16), (2, 12), (25, 14), (10, 25), (2, 21), (2, 30), (22, 8), (13, 27), (24, 27), (3, 4), (14, 4), (17, 6), (28, 6), (17, 15), (28, 15), (9, 11), (5, 22), (17, 24), (28, 24), (9, 20), (9, 29), (6, 5), (29, 7), (21, 3), (6, 14), (29, 16), (21, 12), (6, 23), (29, 25), (21, 21), (21, 30), (10, 2), (25, 0), (10, 11), (2, 7), (25, 9), (2, 16), (13, 13), (24, 13), (13, 22), (24, 22), (16, 18), (1, 29), (16, 27), (17, 1), (28, 1), (5, 8), (17, 10), (28, 10), (9, 6), (5, 17), (17, 19), (28, 19), (9, 15), (5, 26), (17, 28), (28, 28), (9, 24), (6, 0), (29, 2), (6, 9), (29, 11), (21, 7), (6, 18), (21, 16), (20, 20), (20, 29), (10, 6), (12, 25), (23, 25), (2, 2), (2, 11), (4, 30), (13, 8), (24, 8), (1, 15), (13, 17), (24, 17), (16, 13), (1, 24), (13, 26), (24, 26), (16, 22), (5, 3), (17, 5), (28, 5), (9, 1), (5, 12), (17, 14), (28, 14), (9, 10), (5, 21), (17, 23), (28, 23), (9, 19), (5, 30), (9, 28), (6, 4), (29, 6), (21, 2), (6, 13), (20, 15), (20, 24), (12, 20), (23, 20), (12, 29), (23, 29), (4, 25), (13, 3), (24, 3), (1, 10), (13, 12), (24, 12), (16, 8), (1, 19), (13, 21), (24, 21), (16, 17), (1, 28), (13, 30), (24, 30), (16, 26), (17, 0), (28, 0), (5, 7), (17, 9), (28, 9), (9, 5), (5, 16), (28, 18), (9, 14), (5, 25), (27, 22), (8, 27), (19, 27), (30, 27), 
    (20, 1), (20, 10), (12, 6), (23, 6), (20, 19), (12, 15), (23, 15), (20, 28), (4, 11), (12, 24), (23, 24), (4, 20), (4, 29), (1, 5), (13, 7), (24, 7), (16, 3), (1, 14), (13, 16), (24, 16), (16, 12), (1, 23), (24, 25), (16, 21), (16, 30), (5, 2), (17, 4), (28, 4), (9, 0), (5, 11), (9, 9), (27, 17), (8, 13), (19, 13), (27, 26), (8, 22), (19, 22), (30, 22), (0, 18), (11, 18), (0, 27), (11, 27), (20, 5), (12, 1), (23, 1), (20, 14), (12, 10), (23, 10), (20, 23), (4, 6), (12, 19), (23, 19), (4, 15), (12, 28), (23, 28), (4, 24), (1, 0), (13, 2), (24, 2), (1, 9), (13, 11), (24, 11), (16, 7), (1, 18), (16, 16), (15, 20), (15, 29), (26, 29), (5, 6), (7, 25), 
    (18, 25), (18, 8), (27, 3), (27, 12), (8, 8), (19, 8), (27, 21), (0, 4), (30, 8), (8, 17), (19, 17), (27, 30), (0, 13), (11, 13), (8, 26), (19, 26), (30, 17), (0, 22), (11, 22), (30, 26), (20, 0), (20, 9), (12, 5), (23, 5), (20, 18), (4, 1), (12, 14), (23, 14), (4, 10), (12, 23), (23, 23), (4, 19), (4, 28), (1, 4), (24, 6), (16, 2), (1, 13), (26, 15), (15, 24), (26, 24), (7, 20), (18, 20), (7, 29), (18, 29), (27, 7), (8, 3), (19, 3), (27, 16), (30, 3), (8, 12), (19, 12), (27, 25), (0, 8), (11, 8), (8, 21), (19, 21), (30, 12), (0, 17), (11, 17), (8, 30), (19, 30), (30, 21), (0, 26), (11, 26), (30, 30), (20, 4), (12, 0), (23, 0), (20, 13), (12, 9), (23, 9), (4, 5), (23, 18), (4, 14), (22, 22), (3, 27), (14, 27), (15, 1), (15, 10), (26, 10), (7, 6), (18, 6), (15, 19), (26, 19), (7, 15), (18, 15), (15, 28), (26, 
    28), (7, 24), (18, 24), (27, 2), (27, 11), (8, 7), (19, 7), (27, 20), (0, 3), (11, 3), (8, 16), (19, 16), (30, 7), (0, 12), (11, 12), (19, 25), (30, 16), (30, 25), 
    (0, 21), (11, 21), (11, 30), (12, 4), (23, 4), (25, 23), (4, 0), (4, 9), (22, 17), (3, 13), (14, 13), (22, 26), (3, 22), (14, 22), (15, 5), (26, 5), (7, 1), (18, 1), (26, 14), (7, 10), (18, 10), (15, 23), (26, 23), (7, 19), (18, 19), (7, 28), (18, 28), (27, 6), (8, 2), (19, 2), (30, 2), (8, 11), (19, 11), (30, 11), (0, 7), (11, 7), (0, 16), (11, 16), (10, 20), (25, 18), (10, 29), (2, 25), (25, 27), (22, 3), (22, 12), (3, 8), (14, 8), (22, 21), (3, 17), (14, 17), (22, 30), (3, 26), (14, 26), (15, 0), (26, 0), (15, 9), (26, 9), (7, 5), (18, 5), (15, 18), (26, 18), (7, 14), (18, 14), (7, 23), (18, 23), (27, 1), (29, 20), (6, 27), (29, 29), (19, 6), (21, 25), (30, 6), (0, 2), (11, 2), (25, 4), (10, 15), (25, 13), (10, 24), (2, 20), (25, 22), (2, 29), (22, 7), (3, 3), (14, 3), (22, 16), (3, 12), (14, 12), (22, 25), (3, 21), (14, 21), (3, 30), (14, 30), (15, 4), (26, 4), (7, 0), (18, 0), (15, 13), (26, 13), (7, 9), (18, 9), (18, 18), (29, 15), (21, 11), (6, 22), (29, 24), (21, 20), (21, 29), (10, 1), (10, 10), (2, 6), (25, 8), (10, 19), (2, 15), (25, 17), (10, 28), (2, 24), (25, 26), (22, 2), (22, 11), (3, 7), (14, 7), (22, 20), (3, 16), (14, 16), (3, 25), (14, 25), (17, 18), (17, 27), (28, 27), (7, 4), (9, 23), (18, 4), (29, 1), (26, 12), (6, 8), (29, 10), (21, 6), (6, 17), (29, 19), (21, 15), (6, 26), (29, 28), (21, 24), (10, 5), (2, 1), (25, 3), (10, 14), (2, 10), (25, 12), (10, 23), (2, 19), (25, 21), (2, 28), (22, 6), (13, 25), (3, 2), (14, 2), (3, 11), (14, 11), (17, 13), (28, 13), (5, 20), (17, 22), (28, 22), (9, 18), (5, 29), (9, 27), (6, 3), (29, 5), (21, 1), (6, 12), (29, 14), (21, 10), (6, 21), (29, 23), (21, 19), (6, 30), (21, 28), (10, 0), (10, 9), (2, 5), (25, 7), (10, 18), (2, 14), (25, 16), (2, 23), (22, 1), (13, 20), (24, 20), (1, 27), (13, 29), (14, 6), (16, 25), (24, 29), (17, 8), (28, 8), (9, 4), (5, 15), (17, 17), (28, 17), (9, 13), (5, 24), (17, 26), (28, 26), (9, 22), (29, 0), (6, 7), (29, 9), (21, 5), (6, 16), (29, 18), (21, 14), (6, 25), (21, 23), (20, 27), (10, 4), (2, 0), (25, 2), (10, 13), (2, 9), (13, 6), (2, 18), (13, 15), (24, 15), (16, 11), (1, 22), (13, 24), (24, 24), 
    (16, 20), (16, 29), (5, 1), (17, 3), (28, 3), (5, 10), (17, 12), (28, 12), (9, 8), (5, 19), (17, 21), (28, 21), (9, 17), (5, 28), (17, 30), (28, 30), (9, 26), (6, 2), (29, 4), (21, 0), (6, 11), (21, 9), (6, 20), (20, 22), (12, 18), (12, 27), (23, 27), (2, 4), (4, 23), (13, 1), (24, 1), (1, 8), (13, 10), (24, 10), (16, 6), (1, 
    17), (13, 19), (24, 19), (1, 26), (13, 28), (24, 28), (16, 24), (5, 5), (17, 7), (28, 7), (9, 3), (5, 14), (17, 16), (28, 16), (9, 12), (5, 23), (9, 21), (27, 29), 
    (6, 6), (8, 25), (21, 4), (0, 30), (20, 8), (20, 17), (12, 13), (23, 13), (20, 26), (12, 22), (23, 22), (4, 18), (4, 27), (1, 3), (13, 5), (24, 5), (16, 1), (1, 12), (13, 14), (24, 14), (16, 10), (1, 21), (13, 23), (24, 23), (16, 19), (1, 30), (16, 28), (5, 0), (17, 2), (28, 2), (5, 9), (17, 11), (28, 11), (9, 7), (5, 18), (9, 16), (27, 15), (27, 24), (6, 1), (8, 20), (19, 20), (30, 20), (8, 29), (19, 29), (30, 29), (0, 25), (11, 25), (20, 3), (20, 12), (12, 8), (23, 8), (20, 21), (4, 4), (12, 17), (23, 17), (20, 30), (4, 13), (12, 26), (23, 26), (4, 22), (13, 0), (24, 0), (1, 7), (13, 9), (24, 9), (16, 5), (1, 16), (13, 18), (24, 18), (1, 25), (16, 23), (15, 27), (26, 27), (5, 4), (9, 2), (5, 13), (27, 10), (8, 6), (27, 19), (8, 15), (19, 15), (27, 28), (0, 11), (11, 11), (8, 24), (19, 24), (30, 15), (0, 20), (11, 20), (30, 24), (0, 29), (11, 29), (20, 7), (12, 3), (23, 3), (20, 16), (12, 12), (23, 12), (20, 25), (4, 8), (12, 21), (23, 21), (4, 17), (12, 30), (23, 30), (4, 26), (1, 2), (13, 4), (24, 4), (16, 0), (1, 11), (16, 9), (1, 20), (15, 22), (26, 22), (7, 18), (7, 27), (18, 27), (27, 5), (8, 1), (19, 1), (27, 14), (30, 1), (8, 10), (19, 10), (27, 23), (0, 6), (11, 6), (8, 19), (19, 19), (30, 10), (0, 15), (11, 15), (8, 28), (19, 28), (30, 19), (0, 24), (11, 24), (30, 28), (20, 2), (20, 11), (12, 7), (23, 7), (4, 3), (12, 16), (23, 16), (4, 12), (4, 21), (22, 29), (1, 6), (16, 4), (15, 8), (26, 8), (15, 17), (26, 17), (7, 13), (18, 13), (15, 26), (26, 26), (7, 22), (18, 22), (27, 0), (27, 9), (30, 5), (8, 5), (19, 5), (27, 18), (0, 1), (11, 1), (8, 14), (19, 14), (27, 27), (0, 10), (11, 10), (8, 23), (19, 
    23), (30, 14), (0, 19), (11, 19), (30, 23), (0, 28), (11, 28), (20, 6), (12, 2), (23, 2), (12, 11), (23, 11), (25, 30), (4, 7), (4, 16), (22, 15), (22, 24), (1, 1), (3, 20), (14, 20), (3, 29), (14, 29), (15, 3), (26, 3), (15, 12), (7, 8)}
def Ghosthome():
    return  {(14,14),(15,14),(16,14),(14,15),(15,15),(16,15)}
main()