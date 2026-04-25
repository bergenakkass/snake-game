import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 35)

clock = pygame.time.Clock()

def load_highscore():
    if not os.path.exists("highscore.txt"):
        return 0
    with open("highscore.txt", "r") as f:
        return int(f.read())

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    win.blit(img, (x, y))

def game():
    snake = [(100,50),(90,50),(80,50)]
    direction = "RIGHT"
    food = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))
    score = 0

    running = True
    while running:
        clock.tick(10 + score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                elif event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"

        head = snake[0]

        if direction == "LEFT":
            new_head = (head[0] - 10, head[1])
        elif direction == "RIGHT":
            new_head = (head[0] + 10, head[1])
        elif direction == "UP":
            new_head = (head[0], head[1] - 10)
        elif direction == "DOWN":
            new_head = (head[0], head[1] + 10)

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))
        else:
            snake.pop()

        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake[1:]):
            return score

        win.fill(BLACK)

        for block in snake:
            pygame.draw.rect(win, GREEN, (block[0], block[1], 10, 10))

        pygame.draw.rect(win, RED, (food[0], food[1], 10, 10))

        draw_text(f"Score: {score}", 10, 10)

        pygame.display.update()


def menu():
    while True:
        win.fill(BLACK)
        draw_text("SNAKE GAME", 220, 120)
        draw_text("Press SPACE to Start", 180, 180)
        draw_text("Press Q to Quit", 200, 220)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "start"
                if event.key == pygame.K_q:
                    return "quit"


def game_over(score):
    highscore = load_highscore()

    if score > highscore:
        save_highscore(score)
        highscore = score

    while True:
        win.fill(BLACK)
        draw_text(f"Game Over! Score: {score}", 180, 140)
        draw_text(f"High Score: {highscore}", 200, 180)
        draw_text("Press R to Restart", 190, 220)
        draw_text("Press Q to Quit", 200, 260)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "quit"


while True:
    action = menu()

    if action == "quit":
        break

    score = game()

    if score == "quit":
        break

    action = game_over(score)

    if action == "quit":
        break

pygame.quit()