from TIDE import Game, Sprite, run_engine


class CoolGame(Game):
    def __init__(self):
        super().__init__()
        self.player = None
        self.npc = None
        self.message = ""

    def setup(self):
        name = self.type("Enter your name: ")
        self.player = Sprite('  ', 10, 5, color_pair=1, name=name)
        self.add(self.player)

        self.npc = Sprite('#', 20, 10, color_pair=2, name="NPC")
        self.add(self.npc)

        self.background_color_pair = 10

    def update(self):
        if not self.player:
            return

        if self.key == ord('w'):
            self.player.move(0, -1)
        elif self.key == ord('s'):
            self.player.move(0, 1)
        elif self.key == ord('a'):
            self.player.move(-1, 0)
        elif self.key == ord('d'):
            self.player.move(1, 0)
        elif self.key == ord('e'):
            if self.npc and self.player.x == self.npc.x and self.player.y == self.npc.y:
                self.message = self.type("Talk to NPC: ")
            else:
                self.message = "No one to talk to."

    def draw(self, screen):
        super().draw(screen)
        if self.player:
            screen.addstr(0, 0, f"{self.player.name} the Adventurer")
        else:
            screen.addstr(0, 0, "Unnamed Adventurer")
        screen.addstr(1, 0, "[WASD to move, E to interact, Q to quit]")
        if self.message:
            screen.addstr(3, 0, f"🗨️ {self.message}")


if __name__ == "__main__":
    run_engine(CoolGame)
