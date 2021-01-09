# Blocky
CSC148 project where I developed parts of a game.

## COPYRIGHT
#### Work I developed:
player.py \
goal.py \
block.py \
_block_to_squares method in blocky.py 

#### Starter code:
The starter code (everything not listed above) is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

## INSTRUCTIONS
First, you need the latest version of Python.
1. Download ZIP 
2. Change settings to your desire
3. Run game.py

#### Changing the settings:
Blocky is a game that you can play by yourself or with 2 players, or watch 2 computers play against each other. To decide what game to play, go to game.py and uncomment the line that corresponds to the type of the game you would like to play. Lines 139-142 will look like this: \
    `# game = create_sample_game()` \
    `# game = create_auto_game()` \
    `# game = create_two_player_game()` \
    `# game = create_solitaire_game()`
    
To change the settings of each game, go to the methods that are called above and change the parameters inside the initialized Game object. The first parameter `max_depth` determines how many layers of squares you can see in the game; you can choose `max_depth` to be between 2 and 5. Do not change the second parameter `num_human` and the third parameter `num_random`. The last parameter `smart_players` can be changed; an empty list indicates no smart computers and adding a positive int element to the list indicates adding a smart computer of that difficulty level. Note: it's better to not change the size of the lists of the last parameter, but change the value instead.

**Terms to know:**\
Sample game: a game to be played by yourself against a random computer and a smart computer. 

Auto game: a game with 2 random computers playing against each other.

Two player game: a game to be played with 2 players. 

Solitaire game: a game to be played by yourself against a smart computer.
