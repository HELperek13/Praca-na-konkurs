"""
game.py - Glowna logika gry Turtle Snake
"""

import turtle
import random
import json
import os
import time


def load_config():
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "window": {"width": 600, "height": 600, "title": "Turtle Snake", "bg_color": "#1a2e1a"},
            "grid": {"cell_size": 20, "cols": 28, "rows": 28},
            "snake": {"start_length": 3, "initial_speed": 150, "speed_increment": 5, "min_speed": 60},
            "scoring": {"leaf_points": 10, "speed_bonus_threshold": 5},
            "colors": {
                "head": "#4dff91", "body": "#b8492d", "body_dark": "#1a8040",
                "leaf": "#ff6b35", "leaf_stem": "#8BC34A", "border": "#2d4a2d",
                "text": "#ffffff", "score_color": "#4dff91", "game_over_color": "#ff4444"
            }
        }


class TurtleSnakeGame:
    def __init__(self):
        self.cfg = load_config()
        self.w    = self.cfg["window"]
        self.g    = self.cfg["grid"]
        self.s_cfg = self.cfg["snake"]
        self.sc   = self.cfg["scoring"]
        self.col  = self.cfg["colors"]

        self.cell  = self.g["cell_size"]
        self.cols  = self.g["cols"]
        self.rows  = self.g["rows"]

        self.grid_w = self.cols * self.cell
        self.grid_h = self.rows * self.cell
        self.x_off  = -self.grid_w // 2
        self.y_off  = -self.grid_h // 2

        self.high_score = self._load_high_score()
        self._setup_window()
        self._setup_turtles()
        self.state = "start"
        self._init_game_state()

    # setup ----------------------------------------------------------------

    def _setup_window(self):
        self.screen = turtle.Screen()
        self.screen.setup(self.w["width"] + 20, self.w["height"] + 80)
        self.screen.title(self.w["title"])
        self.screen.bgcolor(self.w["bg_color"])
        self.screen.tracer(0)
        self.screen.listen()
        self.screen.onkeypress(lambda: self._change_dir("Up"),    "Up")
        self.screen.onkeypress(lambda: self._change_dir("Down"),  "Down")
        self.screen.onkeypress(lambda: self._change_dir("Left"),  "Left")
        self.screen.onkeypress(lambda: self._change_dir("Right"), "Right")
        self.screen.onkeypress(lambda: self._change_dir("Up"),    "w")
        self.screen.onkeypress(lambda: self._change_dir("Down"),  "s")
        self.screen.onkeypress(lambda: self._change_dir("Left"),  "a")
        self.screen.onkeypress(lambda: self._change_dir("Right"), "d")
        self.screen.onkeypress(lambda: self._change_dir("Up"),    "W")
        self.screen.onkeypress(lambda: self._change_dir("Down"),  "S")
        self.screen.onkeypress(lambda: self._change_dir("Left"),  "A")
        self.screen.onkeypress(lambda: self._change_dir("Right"), "D")
        self.screen.onkeypress(self._on_pause,   "p")
        self.screen.onkeypress(self._on_pause,   "P")
        self.screen.onkeypress(self._on_restart, "r")
        self.screen.onkeypress(self._on_restart, "R")
        self.screen.onkeypress(self._on_quit,    "Escape")

    def _setup_turtles(self):
        def make_t():
            t = turtle.Turtle()
            t.hideturtle(); t.speed(0); t.penup()
            return t
        self.board_t = make_t()
        self.snake_t = make_t()
        self.leaf_t  = make_t()
        self.hud_t   = make_t()

    # high score -----------------------------------------------------------

    def _hs_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")

    def _load_high_score(self):
        try:
            with open(self._hs_path()) as f:
                return json.load(f).get("high_score", 0)
        except Exception:
            return 0

    def _save_high_score(self):
        try:
            with open(self._hs_path(), "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception:
            pass

    # grid helpers ---------------------------------------------------------

    def _cell_center(self, col, row):
        return (self.x_off + col * self.cell + self.cell // 2,
                self.y_off + row * self.cell + self.cell // 2)

    def _random_free(self):
        occupied = set(self.snake)
        while True:
            c = random.randint(0, self.cols - 1)
            r = random.randint(0, self.rows - 1)
            if (c, r) not in occupied:
                return c, r

    # state ----------------------------------------------------------------

    def _init_game_state(self):
        mc, mr = self.cols // 2, self.rows // 2
        n = self.s_cfg["start_length"]
        self.snake     = [(mc - i, mr) for i in range(n)]
        self.direction = "Right"
        self.next_dir  = "Right"
        self.score     = 0
        self.speed     = self.s_cfg["initial_speed"]
        self.leaf      = self._random_free()

    # input ----------------------------------------------------------------

    def _change_dir(self, d):
        if self.state != "playing":
            return
        opp = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if d != opp.get(self.direction):
            self.next_dir = d

    def _on_pause(self):
        if   self.state == "playing": self.state = "paused"
        elif self.state == "paused":  self.state = "playing"

    def _on_restart(self):
        self._init_game_state()
        self.state = "playing"

    def _on_quit(self):
        self.state = "quit"

    # step -----------------------------------------------------------------

    def _step(self):
        self.direction = self.next_dir
        hc, hr = self.snake[0]
        dc, dr = {"Up":(0,1),"Down":(0,-1),"Left":(-1,0),"Right":(1,0)}[self.direction]
        nc, nr = hc + dc, hr + dr

        if nc < 0 or nc >= self.cols or nr < 0 or nr >= self.rows:
            self._do_game_over(); return
        if (nc, nr) in self.snake[:-1]:
            self._do_game_over(); return

        self.snake.insert(0, (nc, nr))
        if (nc, nr) == self.leaf:
            self.score += self.sc["leaf_points"]
            if self.score > self.high_score:
                self.high_score = self.score
            eaten = self.score // self.sc["leaf_points"]
            if eaten % self.sc["speed_bonus_threshold"] == 0:
                self.speed = max(self.s_cfg["min_speed"],
                                 self.speed - self.s_cfg["speed_increment"])
            self.leaf = self._random_free()
        else:
            self.snake.pop()

    def _do_game_over(self):
        self.state = "gameover"
        self._save_high_score()

    # drawing --------------------------------------------------------------

    def _draw_rect(self, t, x, y, w, h, fill, pen, psize=1):
        t.fillcolor(fill); t.pencolor(pen); t.pensize(psize)
        t.goto(x, y); t.pendown(); t.begin_fill()
        t.goto(x+w, y); t.goto(x+w, y+h); t.goto(x, y+h); t.goto(x, y)
        t.end_fill(); t.penup()

    def _draw_board(self):
        t = self.board_t; t.clear()
        self._draw_rect(t, self.x_off, self.y_off,
                        self.grid_w, self.grid_h, "#0d1f0d", self.col["border"], 2)
        t.pencolor("#182818"); t.pensize(1)
        for c in range(0, self.cols+1, 4):
            x = self.x_off + c*self.cell
            t.goto(x, self.y_off); t.pendown()
            t.goto(x, self.y_off+self.grid_h); t.penup()
        for r in range(0, self.rows+1, 4):
            y = self.y_off + r*self.cell
            t.goto(self.x_off, y); t.pendown()
            t.goto(self.x_off+self.grid_w, y); t.penup()

    def _draw_leaf(self):
        t = self.leaf_t; t.clear()
        c, r = self.leaf
        cx, cy = self._cell_center(c, r)
        sz = self.cell // 2 - 2
        t.pencolor(self.col["leaf_stem"]); t.pensize(2)
        t.goto(cx, cy-sz); t.pendown(); t.goto(cx, cy+sz//2); t.penup()
        t.fillcolor(self.col["leaf"]); t.pencolor("#cc4400"); t.pensize(1)
        t.goto(cx, cy); t.pendown(); t.begin_fill()
        t.circle(sz, steps=10); t.end_fill(); t.penup()
        t.pencolor("#ff9966"); t.pensize(1)
        t.goto(cx, cy); t.pendown(); t.goto(cx+sz-2, cy+sz//2); t.penup()

    def _draw_snake(self):
        t = self.snake_t; t.clear()
        sz = self.cell - 3
        for i, (c, r) in enumerate(self.snake):
            cx, cy = self._cell_center(c, r)
            bx, by = cx - sz//2, cy - sz//2
            if i == 0:
                t.fillcolor(self.col["head"]); t.pencolor("#00cc55"); t.pensize(2)
            else:
                fc = self.col["body"] if i%2==0 else self.col["body_dark"]
                t.fillcolor(fc); t.pencolor("#155a30"); t.pensize(1)
            t.goto(bx, by); t.pendown(); t.begin_fill()
            for _ in range(4):
                t.forward(sz); t.left(90)
            t.end_fill(); t.penup()
            if i == 0:
                er = max(2, self.cell//8)
                eyes = {
                    "Right": [(sz*2//3, sz//4),      (sz*2//3, sz*3//4-er)],
                    "Left":  [(sz//4-er, sz//4),      (sz//4-er, sz*3//4-er)],
                    "Up":    [(sz//4,    sz*2//3),     (sz*3//4-er, sz*2//3)],
                    "Down":  [(sz//4,    sz//4-er),    (sz*3//4-er, sz//4-er)],
                }
                t.fillcolor("white"); t.pencolor("black"); t.pensize(1)
                for ox, oy in eyes.get(self.direction, []):
                    t.goto(bx+ox, by+oy); t.pendown(); t.begin_fill()
                    t.circle(er); t.end_fill(); t.penup()

    def _draw_hud(self):
        t = self.hud_t; t.clear()
        hy = self.y_off + self.grid_h + 5
        self._draw_rect(t, self.x_off, hy, self.grid_w, 36, "#0d1f0d", "#2d4a2d")
        t.pencolor(self.col["score_color"])
        t.goto(self.x_off+10, hy+10)
        t.write("WYNIK: %d" % self.score, font=("Courier", 13, "bold"))
        t.pencolor("#aaffcc")
        t.goto(self.x_off + self.grid_w//2 - 55, hy+10)
        t.write("REKORD: %d" % self.high_score, font=("Courier", 13, "normal"))
        t.pencolor("#88bbaa")
        t.goto(self.x_off + self.grid_w - 100, hy+10)
        t.write("DL:%d" % len(self.snake), font=("Courier", 13, "normal"))

    def _draw_start_overlay(self):
        t = self.hud_t; t.clear()
        # Tlo
        self._draw_rect(t, -170, -100, 340, 230, "#091409", "#2d6a2d", 2)
        t.pencolor("#4dff91")
        t.goto(-108, 85); t.write("TURTLE SNAKE", font=("Courier", 18, "bold"))
        t.pencolor("#aaffcc")
        t.goto(-140, 45); t.write("Sterowanie: strzalki lub WASD", font=("Courier", 10, "normal"))
        t.pencolor("#88bbaa")
        t.goto(-125, 15); t.write("[P] Pauza    [Esc] Wyjscie", font=("Courier", 10, "normal"))
        t.goto(-125, -15); t.write("[R] Start / Restart", font=("Courier", 10, "normal"))
        t.pencolor("#ffff66")
        t.goto(-130, -55); t.write("Nacisnij [R] aby zagrac!", font=("Courier", 13, "bold"))
        t.pencolor("#ff6b35")
        t.goto(-95, -85); t.write("Jedz liscie, nie sciany!", font=("Courier", 10, "normal"))

    def _draw_gameover_overlay(self):
        t = self.hud_t; t.clear()
        self._draw_hud()
        self._draw_rect(t, -160, -100, 320, 190, "#0a0a0a", "#ff4444", 2)
        t.pencolor(self.col["game_over_color"])
        t.goto(-115, 55); t.write("KONIEC GRY!", font=("Courier", 20, "bold"))
        t.pencolor("#ffffff")
        t.goto(-140, 15); t.write("Wynik: %d" % self.score, font=("Courier", 13, "normal"))
        t.pencolor("#aaffcc")
        t.goto(-140, -20); t.write("Rekord: %d" % self.high_score, font=("Courier", 13, "normal"))
        t.pencolor("#ffff66")
        t.goto(-130, -65); t.write("[R] Zagraj ponownie", font=("Courier", 13, "bold"))

    def _draw_pause_overlay(self):
        t = self.hud_t; t.clear()
        self._draw_hud()
        self._draw_rect(t, -120, -40, 240, 90, "#0a1a0a", "#2d6a2d", 2)
        t.pencolor("#ffff66")
        t.goto(-75, 15); t.write("PAUZA", font=("Courier", 20, "bold"))
        t.pencolor("#aaffcc")
        t.goto(-85, -25); t.write("[P] Kontynuuj", font=("Courier", 12, "normal"))

    # main loop ------------------------------------------------------------

    def run(self):
        self._draw_board()
        self._draw_leaf()
        self._draw_snake()
        self._draw_start_overlay()
        self.screen.update()

        last_step = time.time()

        while self.state != "quit":
            try:
                self.screen.update()
            except Exception:
                break

            now = time.time()

            if self.state == "start":
                time.sleep(0.016)
                continue

            if self.state == "paused":
                self._draw_pause_overlay()
                self.screen.update()
                time.sleep(0.05)
                continue

            if self.state == "gameover":
                self._draw_gameover_overlay()
                self.screen.update()
                time.sleep(0.05)
                continue

            # playing
            elapsed_ms = (now - last_step) * 1000
            if elapsed_ms >= self.speed:
                self._step()
                last_step = now
                self._draw_board()
                self._draw_leaf()
                self._draw_snake()
                self._draw_hud()
                self.screen.update()
            else:
                time.sleep(0.005)

        try:
            turtle.done()
        except Exception:
            pass
