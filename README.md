# Checkers Game

This Python-based Checkers game is implemented using a combination of algorithms and techniques designed for board game logic and artificial intelligence. The main highlights are:

## Implementation Details
- **Minimax Algorithm with Alpha-Beta Pruning**:
  - The AI player is powered by the Minimax algorithm, which evaluates all possible moves to choose the best one based on a scoring function. Alpha-beta pruning is used to optimize performance by eliminating branches of the search tree that won't affect the final decision.
  - **Heuristic Evaluation**: The evaluation function assigns scores based on the number of pieces, kings, and strategic positions, ensuring the AI makes intelligent moves.

- **Simulated Moves and Capture Logic**:
  - Moves are simulated on a duplicate board to calculate their outcomes without altering the original board state.
  - Capturing mechanics follow traditional Checkers rules, including multi-jump sequences and piece promotion to kings.

- **King Promotion Rules**:
  - Pieces are promoted to kings upon reaching the opponent's back row, enabling them to move both forward and backward.

- **GUI with Tkinter**:
  - The game's graphical interface is built using Python's Tkinter library. It provides an interactive board where players can click to make moves and view possible actions.
  - Highlights valid moves to assist players during gameplay.


## Project Structure:

`checkers.py` (The main Python script or code of the game)

`README.md` (The descriptive file about this game which is this file)

img folder (Contains the images for describting the game on this file)

## Features of the Game: 

1. **Human User plays against AI player**: 

The GUI of the game provides an interactive gameplay environment which user
can play against the AI. Additionally, the pieces of the human users are
represented as red colour and the pieces of the AI are shown as White colour.
Therefore, the user can interact with the board by clicking on red pieces and
moving to the available places, and then the AI responds with its moves.

2. **AI Difficulty Levels which is adjustable by the user**: 

As showing in the below image, there is a slider to adjust the difficulty of the game. By changing the
slider, then the depth of the minimax algorithm will change.
The following figure shows the slider which is for adjusting the level of difficulty:

<img src="img/difficulity.png" alt="difficulity" width="480" height="auto">


3. **King Mechanics**:

Pieces are promoted to kings upon reaching the opponent's end. The following figure represents how the piece will become the king:

<img src="img/king.png" alt="King" width="480" height="auto">

4. **Capture Rules**:

Normal pieces can capture kings. Then, that normal pieces will become a King pieces. The image below shows this feature: 


<img src="img/capture.png" alt="capture rule" width="480" height="auto">


## How To Play the Game

1. **Move Pieces**: Click on your red pieces to highlight possible moves and select the destination. As showing ont he following figure, when you click on the the red pieces then the available places will highlight.

<img src="img/moves.png" alt="moves rule" width="480" height="auto">

2. **Win the Game**: Capture all the opponent's pieces or block their possible moves.

3. **Adjust Difficulty**: Use the slider to set AI difficulty before starting.


## Requirements
- Python 3.x
- Tkinter (built into most Python distributions)


## How to Run 
1. Clone the repository
   ``` bash
   git clone https://github.com/your-username/checkers-game.git
2. Navigate to the project directory:
   ``` bash
   cd checkers-game
 3. Run the Game:
    ``` bash
    python checkers.py 
