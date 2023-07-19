# chesspy &#9817;

A chess program written in Python without the use of any external chess libraries, including a primitive functional AI. The primary purpose of this project is to present a fun challenge rather than to develop a highly advanced chess bot. This README gives a brief overview of how the AI works and the structure of the project.

For more information and regular updates on the development of this project, please visit my [website/blog](https://hanafi.dev/2023/07/10/writing-a-chess-ai-from-scratch-in-python-part-1/).

## Examples

*to be added*

## Compilation

To start the game, run `Main.py`.

## Usage

Customize the game settings in `Main.py`. Set `WHITE` and `BLACK` to either `PLAYER` or `AI`, change the `SIZE` of the window if you wish, and then run the `Main.py` file.

To change the depth of the AI, you can set the `depth` parameter in the respective `self.ai_turn()` function in the `Controller.game_loop()` function found in `Controller.py`.

To use the baseline random move AI (which, as you may have guessed, chooses a legal move at random), set the desired `self.COLOR_AI` to `RandomAI(COLOR)` instead of `AI(COLOR)` in  `Controller.__init__()`.

***

## AI

The AI is extremely primitive so far, and I intend to expand on it later. 

### Scoring Algorithm

First, we need a way for the AI to determine 'good' positions and 'bad' positions. Thus, we need to discern between aspects that are important versus those that aren't, or set the priorities of the pieces. 

To calculate the value of a player's pieces, we use the standard chess piece valuation:
<table>
    <tr>
        <th>Piece</th>
        <td>Pawn</td>
        <td>Knight</td>
        <td>Bishop</td>
        <td>Rook</td>
        <td>Queen</td>
    </tr>
    <tr>
        <th>Value</th>
        <td>1</td>
        <td>3</td>
        <td>3</td>
        <td>5</td>
        <td>9</td>
    </tr>
</table>

Controlling the center is also an important concept in chess, so for each piece a player has in the central four squares they get +2, and for the surounding twelve squares they get +1.

### Minimax Algorithm

At `depth=1`, the AI gets all possible legal moves in the position. For each move, it clones the board, plays the move, and then 'scores' the position. After finding the move that leads it to the best position, it plays that move. 

At `depth=2`, it still clones the board for each possible legal move, but then clones the board again for each response the opponent can play. After scoring those positions, it scores each legal move it has by the best response an opponent can come up with (the opponent response with the *minimum* board score i.e. bad for the AI), and then picks the best legal move (the *maximum* AI legal move score).

This is then recursively applied to depths of $k$ moves, gaining more insight as $k$ is increased. This method of scoring positions is called the minimax algorithm, and works extremely well but unfortunately becomes extremely slow at higher depths. This means that optimizations are needed.

### Alpha-beta Pruning

This is an optimization used to improve the efficiency of the minimax algorithm in decision-making problems. It works by keeping track of two values, `alpha` and `beta`, that represent the minimum and maximum scores that the AI is assured of getting, assuming that their opponent play optimally. 

As the algorithm explores the possible moves, it uses these values to prune branches that cannot possibly affect the final score. By eliminating these branches, the algorithm can greatly reduce the number of nodes that it needs to explore, resulting in a significant speedup. In other words, it is a way to eliminate moves that will never be used in the final decision, allowing the AI to pick the optimal move in less time and with less computational power.


## Implementation

### Board

The `Board` class is made up of the actual board array which holds the pieces on the board, as well as data like whose turn it is. It includes auxiliary methods to create a piece (and update relevant data structures), initialize a board to the starting position, check if a square contains a piece (and if so, can retrieve it), as well as drawing the board using Pygame.

The color scheme and various indicators take inspiration from Chess.com's default layout.

### Piece

The `Piece` class holds each piece's color, location, and image to be displayed by the board. It includes basic methods that allow generic movement and capturing.

Each type of piece inherits this basic class and has its own `get_legal_moves()` method. This method returns an array of all legal moves the piece can move to on that turn.

> Note: In previous versions, each piece had a `can_move_to_square()` method that would return `True` if a piece could move to the specified square on that particular turn. Then, to find a piece's legal moves (e.g. to know which squares to highlight when a piece is selected), we would iterate over the entire board and check if the piece could go to each square. Now, we generate the list of legal moves and simply check if the desired square is in the array.

### Controller

The `Controller` class is how the `Main` file interacts with the game. It contains a board, and methods that start and manage the game loop.