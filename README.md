# Ethyca Code Test -- Open Source Engineer

## User Story
As a keen noughts and crosses (/tix-tac-toe) player (and aspiring champion), I need a web service that allows me to play noughts and crosses against a computer via a REST API. The API must allow me to create a new game, make the next move in a game, and list all games previously played.

### Noughts and Crosses (Tic-tac-toe)
Tic-tac-toe (American English), noughts and crosses (Commonwealth English and British English) is a game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a diagonal, horizontal, or vertical row is the winner. ~It is a solved game with a forced draw assuming best play from both players.~

An example game series can be represented as:
```
# A blank board
[
    [".", ".", "."],
    [".", ".", "."],
    [".", ".", "."],
]

# First move
[
    [".", ".", "."],
    [".", "X", "."],
    [".", ".", "."],
]

# Second move
[
    [".", ".", "."],
    [".", "X", "."],
    [".", ".", "O"],
]

# Third move
[
    [".", ".", "X"],
    [".", "X", "."],
    ["O", ".", "O"],
]

...and so forth
```

## Your Task
Use Python (any flavour) to Develop a REST API that:
- Allows me to create a new game of Noughts and Crosses, and returns the game ID.
- Allows me to make the next move by specifying the co-ordinates I wish to move on e.g. `{"x": 1, "y": 1}` would denote a move to the middle square by the requesting player, and returns the new state of the board _after_ the computer has made its move in turn.
- Allows me to view all moves in a game, choronologically ordered.
- Allows me to view all games I have played, chronologically ordered.

### Stretch goals
- Allow me to authenticate with this service, so only I can view my game history.
- Build a simple UI for this service.
- Deploy the service.
- Expand the game-grid to size N*N, allowing for longer and more fulfulling games.
- Surprise us! Use your inherent style and panache to sprinkle that extra bit of gee-whizz atop your solution.

## Notes
- Please work independently without code review by others. State any assumptions you made or questions you had along the way. When complete, note how much time you spent from beginning to end.
- It's our intention that you spend between 3 and 4 hours on this task.
- This challenge is designed to (mostly) reflect a real world scenario, so is deliberately vague on detail. Feel free to reach out and ask questions as needed.
- There is no 100% correct solution, be creative! We are just as interested in your approach to problem solving as we are in your actual solution.


## Delivery
- Once completed, please create a README file descibing:
  - How to run your project (or where it is hosted),
  - How much time you spent building the project,
  - Any assumptions you made,
  - Any trade-offs you made,
  - Any stretch goals you attempted,
  - Anything else you want us to know about,
  - Any feedback you have on this technical challenge -- we care deeply about our hiring process here at Ethyca, and about the engineers who go through it (that's you!) -- we wholeheartedly promise any feedback will be met with a warm thankyou,
- The assignment can be published and shared with us via any code sharing platform such as Github, Gitlab, or sent as a .zip file.
