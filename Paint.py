import curses
import json
import os
from TIDE import Game, Sprite

class PaintApp(Game):
    def __init__(self):
        super().__init__()
        self.cursor = Sprite("▒▒", 10, 10, color_pair=2)  # Start y=1 so we have room for instructions
        self.grid = {}  # (x, y) → color_pair
        self.current_color = 1
        self.mode = "paint"  # or "typing-save", "typing-load"
        self.typed_text = ""

    def setup(self):
        self.add(self.cursor)

    def update(self):
        if self.mode == "paint":
            self.paint_mode()
        elif self.mode.startswith("typing"):
            if self.key == 10:  # Enter key
                filename = self.typed_text.strip()
                if filename:
                    if self.mode == "typing-save":
                        self.save_canvas(filename + ".json")
                    elif self.mode == "typing-load":
                        self.load_canvas(filename + ".json")
                self.typed_text = ""
                self.mode = "paint"
            elif self.key in (curses.KEY_BACKSPACE, 127, 8):
                self.typed_text = self.typed_text[:-1]
            elif self.key and 32 <= self.key <= 126:
                self.typed_text += chr(self.key)

    def paint_mode(self):
        if self.key == curses.KEY_UP:
            self.cursor.y = max(1, self.cursor.y - 1)  # Stay below instructions
        elif self.key == curses.KEY_DOWN:
            self.cursor.y = min(curses.LINES - 1, self.cursor.y + 1)
        elif self.key == curses.KEY_LEFT:
            self.cursor.x = max(0, self.cursor.x - 2)
        elif self.key == curses.KEY_RIGHT:
            self.cursor.x = min(curses.COLS - 2, self.cursor.x + 2)
        elif self.key == ord(" "):  # Paint
            self.grid[(self.cursor.x, self.cursor.y)] = self.current_color
            self.grid[(self.cursor.x + 1, self.cursor.y)] = self.current_color
        elif self.key == ord("e"):  # Erase
            self.grid.pop((self.cursor.x, self.cursor.y), None)
            self.grid.pop((self.cursor.x + 1, self.cursor.y), None)
        elif self.key == ord("c"):  # Clear
            self.grid.clear()
        elif self.key == ord("s"):  # Save
            self.mode = "typing-save"
            self.typed_text = ""
        elif self.key == ord("l"):  # Load
            self.mode = "typing-load"
            self.typed_text = ""
        elif self.key in [ord(str(n)) for n in range(1, 6)]:
            self.current_color = int(chr(self.key))
        elif self.key == ord("q"):
            self.running = False

    def draw(self, screen):
        screen.clear()

        # --- Draw Instructions ---
        instructions = (
            "[ARROWS] Move  [SPACE] Paint  [E] Erase  [C] Clear  "
            "[1–5] Color  [S] Save  \n[L] Load  [Q] Quit"
        )
        screen.addstr(0, 0, instructions[:curses.COLS - 1])

        # --- Draw Painted Grid ---
        for (x, y), color in self.grid.items():
            try:
                screen.attron(curses.color_pair(color))
                screen.addstr(y, x, "█")
                screen.attroff(curses.color_pair(color))
            except curses.error:
                pass

        # --- Draw Cursor ---
        self.cursor.draw(screen)

        # --- Draw Input Prompt ---
        if self.mode.startswith("typing"):
            prompt = f"{'Save' if self.mode == 'typing-save' else 'Load'} file: {self.typed_text}"
            screen.addstr(curses.LINES - 1, 0, prompt[:curses.COLS - 1])

    def save_canvas(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump({f"{x},{y}": c for (x, y), c in self.grid.items()}, f)
        except Exception as e:
            print(f"Error saving: {e}")

    def load_canvas(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    self.grid = {
                        tuple(map(int, key.split(","))): value for key, value in data.items()
                    }
            except Exception as e:
                print(f"Error loading: {e}")

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    game = PaintApp()
    game.stdscr = stdscr
    game.setup()

    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)

    while game.running:
        game.key = stdscr.getch()
        game.update()
        game.draw(stdscr)
        stdscr.refresh()
        curses.napms(30)

if __name__ == "__main__":
    curses.wrapper(main)
