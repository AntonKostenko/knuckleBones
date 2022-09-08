# Knuckle Bones
A clone of the mini-game "Knuckle Bones" from the game "Cult of the Lamb." 
Made in Python using the Arcade engine.

## Getting Started

* Clone the repo
* Configure your venv
* `$ pip install -r requirements.txt`
* Run `main()`

## How to play

* By default, the game will start with Player 1 as a Human, and Player 2 as an Easy CPU.
  * Change this in the Settings screen. 
* Place a dice in any column on your board using the mouse. The dice value is added to your column score.
* Your total score is calculated by adding all of your column scores together.
* When dice of the same value are placed in the same column, the dice value is multiplied.
* Destroy your opponents dice by matching yours to theirs in the same column.
* The game ends when either board fills up. The winner is the player with the highest score.
* Press the "R" key to start a new game.
* Press the "M" key while in game to go to the main menu.

![Screen Shot 2022-09-08 at 2 18 42 PM](https://user-images.githubusercontent.com/29261200/189230123-23107d6e-49c9-4017-ae46-f1c892dd7768.png)


## Roadmap

### Sounds/Effects
* Background Music
* Dice roll sound
* Win sound
* Lose sound (if vs AI)

### Outside the game loop
* Other color themes/Prettier UI
