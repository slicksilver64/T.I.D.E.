import curses
import time


class Sprite:
    def __init__(self, char, x=0, y=0, color_pair=1, name=""):
        self.char = char
        self.x = x
        self.y = y
        self.color_pair = color_pair
        self.name = name

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        try:
            screen.attron(curses.color_pair(self.color_pair))
            screen.addstr(self.y, self.x, self.char)
            screen.attroff(curses.color_pair(self.color_pair))
        except curses.error:
            pass


class Game:
    def __init__(self):
        self.sprites = []
        self.key = None
        self.running = True
        self.mode = "game"
        self.typed_text = ""
        self.stdscr = None
        self.background_color_pair = 0  # No bg by default

    def add(self, sprite):
        self.sprites.append(sprite)

    def setup(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        # Fill screen background if specified
        if self.background_color_pair != 0:
            height, width = screen.getmaxyx()
            try:
                screen.attron(curses.color_pair(self.background_color_pair))
                for y in range(height):
                    screen.addstr(y, 0, ' ' * (width - 1))
                screen.attroff(curses.color_pair(self.background_color_pair))
            except curses.error:
                pass

        # Draw all sprites
        for sprite in self.sprites:
            sprite.draw(screen)

    def type(self, prompt: str) -> str:
        self.mode = "typing"
        self.typed_text = ""

        curses.curs_set(1)
        self.stdscr.nodelay(False)
        self.stdscr.timeout(-1)

        while True:
            self.stdscr.clear()
            self.draw(self.stdscr)
            height, width = self.stdscr.getmaxyx()
            display_prompt = prompt + self.typed_text
            if len(display_prompt) > width - 1:
                display_prompt = display_prompt[-(width - 1):]
            self.stdscr.addstr(height - 1, 0, display_prompt)
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key in (10, 13):  # Enter
                result = self.typed_text
                break
            elif key in (8, 127, curses.KEY_BACKSPACE):
                self.typed_text = self.typed_text[:-1]
            elif 32 <= key <= 126:
                self.typed_text += chr(key)

        self.mode = "game"
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(int(1000 / 30))

        return result


def run_engine(game_class, fps=30):
    def _main(stdscr):
        game = game_class()
        game.stdscr = stdscr

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        # Define color pairs (fg, bg)
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_BLACK)  # Black background
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # white on black
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Player
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)     # NPC
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)   # Background

        stdscr.nodelay(True)
        stdscr.timeout(int(1000 / fps))

        game.setup()

        while game.running:
            game.key = stdscr.getch()

            if game.mode == "typing":
                pass
            else:
                if game.key == ord('q'):
                    break
                game.update()

            game.draw(stdscr)
            stdscr.refresh()
            time.sleep(1 / fps)

    curses.wrapper(_main)
