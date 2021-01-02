# pacman game in PyGame
# can be played 1 or 2 players
# can change the game board by left and right clicking
# when the game starts a BFsearch is made to find the reachable food spots
# each time a ghost gets to a junction it choses the direction (not backwards) that brings it closer to pacman
# each ghost has a slightly different target (eg left right above below pacman)
######################
#controls
#arrow keys for player 1
#wasd for player 2
#enter to add/remove player 2
#-/+ or o/p to add/remove lives from player 1/2
#space to begin 
######################
#I originally attempted to use A* algorithm on the ghost to find shortest route however this method is much easier to implement and creates a much harder game
