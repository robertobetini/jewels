# Jewels

## What is it?

This is ~or will be~ my match 3 game, which I'm still developing and I hope i won't be giving up so soon.
It is obviously inspired by PopCap game series Bejeweled, but I kind of wanted to add some different mechanics, like free jewel swapping, limited move count and some kind of progression (still trying to understang how to mix all those things up).

### Why python and pygame?

I like python and I didn't want to use a complex game dev environment, such as Godot (gdscript is a python-like language though) or Unity.
And by complex I mean something that do lot of more things besides text editing.

## How do I run it?

You can run it with python on a virtual environment with pygame  installed

1. Install [Python 3.13](https://www.python.org/downloads/)
2. Fork and/or clone this repo via HTTPS
```shell
git clone https://github.com/robertobetini/jewels
```
or via SSH
```shell
git clone git@github.com:robertobetini/jewels.git
```
3. Create a python virtual environment
```shell
python -m venv .venv
```
or
```shell
python3 -m venv .venv
```
4. Install package dependencies from `requirements.txt`
```shell
pip install -r requirements.txt
```
or
```shell
python -m pip install -r requirements.txt
```
5. Run main script
```shell
python main.py
```

## How do I play it?

The core mechanic of the game is to match 3 or more subsequent jewels on a row or column. 

![](/doc/match.gif)

You can even do a match including jewels on a row AND a column

> TODO: insert match on both a row and a column gifs here

You can free swap any jewel with any of its neighors, which means that you can swap even if that move doesn't makes a match, but you also have limited movements, so think carefully.

There's also a progress gauge for each jewel type, but it's not fully function right now

## TODO

- [ ] Create a better game name
- [x] Create a board with gem swap
- [x] Create a progress/score window
- [x] Create animation for swapping jewels
- [x] Create animation for jewel match
- [ ] Improve jewel match animation translating jewels to respective progress bar
- [ ] Create some music
- [ ] Create some sound effects
- [ ] Create custom visual assets
- [x] Add limited movements
- [ ] Create game config file
- [x] Create a simple game event engine
- [ ] Create a log system to catch erros and unexpected behaviour
- [x] Adjust visual elements size to the window
- [x] Dynamically Centralize visual elements
- [ ] Better control of threads spawned by the game
- [x] Title scene
- [x] Game over scene
- [x] Pause scene

## Credits

* Sztek for their [match 3 gems assets](https://sztek.itch.io/match-3-gems-pixel-art) in this early development stage
