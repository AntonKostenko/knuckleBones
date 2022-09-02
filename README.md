# Knuckle Bones
A clone of the mini-game "Knuckle Bones" from the game "Cult of the Lamb." 
Made in Python using the Arcade engine.

## Getting Started

* Clone the repo
* Configure your venv
* `$ pip install -r requirements.txt`
* Run `main()`

## How to play

* Place a dice in any column on your board using the mouse. The dice value is added to your column score.
* Your total score is calculated by adding all of your column scores together.
* When dice of the same value are placed in the same column, the dice value is multiplied.
* Destroy your opponents dice by matching yours to theirs in the same column.
* The game ends when either board fills up. The winner is the player with the highest score.
* Press the "R" key to start a new game.

![Screen Shot 2022-08-26 at 3 53 01 PM](https://user-images.githubusercontent.com/29261200/187005343-8deece7f-35bd-4c79-a3ad-6c3c58b792ae.png)

## Roadmap

### Sounds/Effects
* Background Music
* Dice roll sound
* Win sound
* Lose sound (if vs AI)

### Opponent AI
* Player vs hard AI
* AI vs AI

### Outside the game loop
* Other color themes
