# Mtrix - Tetris clone in Python


Hello there!

Mtrix is a Tetris clone. It is implemented using:
 * pygame
 * blinker
 * Python2.7

## Screens

![mtrix_init_screen](https://ikacikax.files.wordpress.com/2018/02/mtrix_initial_screen1.png)
![mtrix_gameplay_screen](https://ikacikax.files.wordpress.com/2018/02/mtrix_gameplay1.png)
![mtrix_paused_screen](https://ikacikax.files.wordpress.com/2018/02/mtrix_paused1.png)
![mtrix_gameover_screen](https://ikacikax.files.wordpress.com/2018/02/mtrix_game_over1.png)


## Installation

To install Mtrix just clone this git repository and run `pip install -r requirements.txt`.

After pygame and blinker packages are installed you are ready to play!

## Run the game

After installinga all you have to do is run `mtrix.py` by typing `python mtrix.py`.

## Folder structure

Game logic and media are separated in few folders. Here is a brief description of what is contained in them:
 * `game` - holds all Python scripts that are managing game logic and configuration,
 * `media` - holds media files (icon file at the moment),
 * `utils` - holds `Vect2D` class and Blinker's events.


## Future ideas

Main purpose of this pet project was to practice Python programming and getting to know pygame framework.

However, the initial idea was to create multiplayer version with client/server architecture.
During the implementation period it was obvious that creating multiplayer version would be time consuming and would
involve more learning and practice in other domains (e.g. game network programming).

This is why why project will remain in current state for a certain period of time.

Hope you like it and learn something from this code. **Happy playing!!!**
