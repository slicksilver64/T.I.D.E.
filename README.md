# Remember to install dependencie
<br>
<br>
Install `curses` (already included on most MacOS and Unix-based systems):
<p>
<p>

```bash
pip install curses
````

> On Windows, run:
>
> ```bash
> pip install windows-curses
> ```

---
## Included functions
<br>
<br>
<br>

### `Sprite`
Represents a game object displayed as a character on screen.
- `char`: the character to draw
- `x`, `y`: screen position
- `color_pair`: the color scheme to use
- `move(dx, dy)`: changes position
- `draw(screen)`: renders the sprite to the screen
  
```python
player = Sprite('@', 10, 5, color_pair=1, name="Player")
```

### `Game`
Handles the game loop and manages sprites.
- `add(sprite)`: adds a sprite to the game
- `setup()`: override to initialize your game objects
- `update()`: override to define logic each frame
- `draw(screen)`: handles rendering
- `type(prompt)`: prompts the user to type text interactively at the bottom of the screen

### `run_engine(game_class, fps=30)`
Runs your custom game class with the defined frame rate.

---

## Colors

Use `curses.init_pair()` to define colors:

```python
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Player
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)   # Enemy
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN) # Background
```

Set a background color:

```python
self.background_color_pair = 3
```
