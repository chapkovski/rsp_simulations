# RSP simulations

The code is intended to imitate human-bot interactions. 

There are two classes of players within each game (`human` and `bot`).
The former can be replaced by oTree player later. For porting you'll
need to substitute `game` class with oTree `player` class and associate
`human` and `bot` object with it.

The code structure now is three-tier.
There is a `Move` object which is simply a modular ariphmetic object 
with a fixed base (by default 3, but easily extendable to any base).
It supports comparison (==, > or <), so 
```python
Move(1) == Move(4) # True
Move(2) > Move(7) # True 
```
and basic ariphmetic and conversion from/to `int`:
```python
Move(1) +=2  # = Move(0) or Rock
Move(0) + 2 # = Move(0)
Move(2) - Move(1) # = Move (1)
```
`Move` class also has a built-in function `.move_random` that returns
a random choice from its base.

Then there is a base class `Player` which has `history` property 
returning history of moves, and `result_history` property returning history of outputs
 (0 for loss, 1 for tie, 2 for win)
 
 and there are two child classes of `Player`: `Bot` and `Human` 
 where the logic of move making is defined. This example uses 
 fictitious play logic to check for optimal strategy of a human, 
 but it can be replaced by any other logic later on as an add-on.
   
and the last one is a `Game` class that simply creates two players,  
a bot and a human and let them play with each other for `n` rounds defined in a class instance creation:
```python
game = Game(90)
game.run_game()
```
 will create a new game with 90 rounds, and let them play.
 
 

