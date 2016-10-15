# AI-Search-Algorithms

Developed a two-player board game where the user can simulate battles by applying either Greedy Best-First Search, Minimax or Alpha-Beta pruning algorithms as two players.

On each turn, a player can make one of two moves:  
**Raid** – You can take over any unoccupied square that is adjacent to one of your current pieces (horizontally or vertically, but not diagonally). You place a new piece in the taken over square. Also, any enemy pieces adjacent to your new piece (horizontally or vertically, but not diagonally) are conquered and replaced by your own pieces. You can Raid a square even if there are no enemy pieces adjacent to it to be conquered. Once you have made this move, your turn is over.

**Sneak** – You can take any unoccupied square on the board that is not next to your existing pieces. This will create a new piece on the board. Unlike Raid which is an aggressive move, Sneak is a covert operation, so it won’t conquer any enemy pieces. It simply allows one to place a piece at an unoccupied square that is not reachable by Raid. 

Notice that a space that can be Raided cannot be Sneaked (your squirrel warriors are always more aggressive when near home territory). Once you have done a Sneak, your turn is complete.
