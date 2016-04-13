# lighbot-solver
LUMO is a simple search and rules-based AI that writes code to solve levels in the game Lightbot

### About
Lightbot is a game for teaching kids how to program. Players write short programs to make the robot touch all the checkpoints and reach its goal. Players are rewarded additional points for *shorter* programs.

Example of Lightbot game:

![Alt Text](https://github.com/nicholaslocascio/lightbot-solver/raw/master/lightbot_run.gif)

### Technical Approach
LUMO searches the space of possible programs for a suitable path that reaches the goal, then it attempts to compress path with various recursion, functional composition, or iteration techniques.

### Limitations
For very large maps, the naiive searching technique becomes exponentially slow, as finding the best path for the robot to take to touch all its checkpoints is essentially the Travelling Salesperson problem, which is NP.
