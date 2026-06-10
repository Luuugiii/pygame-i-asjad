#!/usr/bin/env python3
import random
from tkinter import *

WIDTH = 500
HEIGHT = 500
SPACE_SIZE = 20

BACKGROUND = "#000000"

FOOD_TYPES = ["normal", "bonus", "poison"]

SNAKE_COLOR = "#FFFF00"

score = 0
high_score = 0
lives = 3

direction = "down"
paused = False

game_started = False
on_start_screen = True

selected_speed = 200
SPEED = 200


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        self.grow = 0

        for _ in range(2):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            sq = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake"
            )
            self.squares.append(sq)


class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        self.type = random.choices(
            FOOD_TYPES,
            weights=[70, 20, 10]
        )[0]

        color = {
            "normal": "red",
            "bonus": "gold",
            "poison": "purple"
        }[self.type]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=color,
            tag="food"
        )


def show_start_screen():
    canvas.delete(ALL)

    canvas.create_text(WIDTH/2, 70,
                       text="SNAKE GAME",
                       fill="yellow",
                       font=("consolas", 28, "bold"))

    canvas.create_text(WIDTH/2, 130,
                       text="Vali raskusaste (vajuta 1–4)",
                       fill="white",
                       font=("consolas", 14))

    canvas.create_text(WIDTH/2, 160,
                       text="1 Easy | 2 Normal | 3 Hard | 4 Extreme",
                       fill="gray",
                       font=("consolas", 10))

    canvas.create_text(WIDTH/2, 220,
                       text="TOIDUD",
                       fill="white",
                       font=("consolas", 14))

    canvas.create_text(WIDTH/2, 250,
                       text="RED = +1 punkt",
                       fill="red",
                       font=("consolas", 11))

    canvas.create_text(WIDTH/2, 275,
                       text="GOLD = +3 punkt",
                       fill="gold",
                       font=("consolas", 11))

    canvas.create_text(WIDTH/2, 300,
                       text="PURPLE = -1 elu",
                       fill="purple",
                       font=("consolas", 11))

    canvas.create_text(WIDTH/2, 370,
                       text="ENTER = START",
                       fill="white",
                       font=("consolas", 13))


def change_direction(new_dir):
    global direction

    opposite = {
        "left": "right",
        "right": "left",
        "up": "down",
        "down": "up"
    }

    if new_dir != opposite.get(direction):
        direction = new_dir

def set_speed(event):
    global selected_speed

    if not on_start_screen:
        return

    if event.char == "1":
        selected_speed = 300
    elif event.char == "2":
        selected_speed = 200
    elif event.char == "3":
        selected_speed = 120
    elif event.char == "4":
        selected_speed = 80

    show_start_screen()


def start_game(event=None):
    global game_started, on_start_screen, snake, food, score, lives, SPEED

    game_started = True
    on_start_screen = False

    score = 0
    lives = 3
    SPEED = selected_speed

    canvas.delete(ALL)

    snake = Snake()
    food = Food()

    window.after(SPEED, next_turn, snake, food)


def toggle_pause(event=None):
    global paused
    paused = not paused


# =========================
# RESET ROUND
# =========================
def reset_round():
    canvas.delete("snake")
    canvas.delete("food")


def next_turn(snake, food):
    global score, lives, high_score, SPEED

    if not game_started:
        return

    if paused:
        window.after(100, next_turn, snake, food)
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    sq = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, sq)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        if food.type == "normal":
            score += 1
            snake.grow += 1

        elif food.type == "bonus":
            score += 3
            snake.grow += 1

        elif food.type == "poison":
            lives -= 1

        if score > high_score:
            high_score = score

        canvas.delete("food")
        food = Food()

    else:
        if snake.grow > 0:
            snake.grow -= 1
        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

    out_of_bounds = (
        x < 0 or x >= WIDTH or
        y < 0 or y >= HEIGHT
    )

    self_collision = any(
        x == part[0] and y == part[1]
        for part in snake.coordinates[1:]
    )

    if out_of_bounds or self_collision:
        lives -= 1

        if lives <= 0:
            game_over()
            return
        else:
            reset_round()
            snake = Snake()
            food = Food()
            window.after(SPEED, next_turn, snake, food)
            return

    window.after(SPEED, next_turn, snake, food)


def game_over():
    canvas.delete(ALL)

    canvas.create_text(WIDTH/2, HEIGHT/3,
                       text="GAME OVER",
                       fill="red",
                       font=("consolas", 30))

    canvas.create_text(WIDTH/2, HEIGHT/2,
                       text=f"Score: {score}  High: {high_score}",
                       fill="white",
                       font=("consolas", 14))


window = Tk()
window.title("Snake Game")

canvas = Canvas(window,
                width=WIDTH,
                height=HEIGHT,
                bg=BACKGROUND)
canvas.pack()

label = Label(window,
              text="Arrows + ENTER",
              font=("consolas", 12))
label.pack()


window.bind("<Left>", lambda e: change_direction("left"))
window.bind("<Right>", lambda e: change_direction("right"))
window.bind("<Up>", lambda e: change_direction("up"))
window.bind("<Down>", lambda e: change_direction("down"))

window.bind("<p>", toggle_pause)
window.bind("<Key>", set_speed)
window.bind("<Return>", start_game)


show_start_screen()

window.mainloop()
