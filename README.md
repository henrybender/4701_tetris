# DEEP Q TETRIS

This project requires Pytorch, Pygame, Numpy, and Python3 installed.

Please see the report for a description of the game classes and the Deep Q Network implementation, training, and optimization.

To train a Deep Q Network to play Tetris, cd to the directory and run Python train.py in a terminal window. The number of epochs trained can be adjusted in the train file, but is set at a default of 2500, which takes about an hour to train.

After training completes, or if you use the pretrained 'trained_models/tetris' model, you can run python tetris.py to observe the AI clear hundreds of lines and pieces.
