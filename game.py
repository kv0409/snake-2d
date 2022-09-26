# Snake class
class Snake:
    def __init__(self, boundary=(20, 20)):
        self.head, self.body, self.direction = None, None, None
        self.spawn()
        self.bounds = boundary

    def spawn(self):
        self.head = [0, 0]
        self.body = [[0, 0]]
        self.direction = "right"

    def move(self):
        if self.direction == "right":
            self.head[0] += 1
        elif self.direction == "left":
            self.head[0] -= 1
        elif self.direction == "up":
            self.head[1] -= 1
        elif self.direction == "down":
            self.head[1] += 1

        self.body.insert(0, list(self.head))
        self.body.pop()

    def change_direction(self, direction):
        if direction == "right" and self.direction != "left":
            self.direction = "right"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"

    def eat(self):
        self.body.insert(0, list(self.head))

    def check_collision(self):
        if self.head in self.body[3:]:  # The snake can't hit itself in the first 3 segments
            print("Collision with body")
            return True
        elif self.head[0] not in range(self.bounds[0]) or self.head[1] not in range(self.bounds[1]):
            print("Collision with wall")
            return True
        else:
            return False

    def get_head(self):
        return self.head

    def get_body(self):
        return self.body

    def get_direction(self):
        return self.direction


# Food class
class Food:
    def __init__(self, boundary=(20, 20)):
        self.position = [0, 0]
        self.bounds = boundary

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def spawn(self, snake):
        while True:
            self.position = [random.randrange(1, self.bounds[0]), random.randrange(1, self.bounds[1])]
            if self.position not in snake.get_body():
                break


# Game class
class Game:
    def __init__(self, boundary=(20, 20)):
        self.state = "game"
        self.snake = Snake(boundary)
        self.food = Food(boundary)
        self.food.spawn(self.snake)
        self.score = 0

    def get_snake(self):
        return self.snake

    def get_food(self):
        return self.food

    def get_score(self):
        return self.score

    def set_snake(self, snake):
        self.snake = snake

    def set_food(self, food):
        self.food = food

    def set_score(self, score):
        self.score = score

    def check_food_collision(self):
        if self.snake.get_head() == self.food.get_position():
            return True
        else:
            return False

    def check_game_over(self):
        if self.snake.check_collision():
            return True
        else:
            return False

    def update_score(self):
        self.score += 1

    def reset(self):
        self.snake.spawn()
        self.food.spawn(self.snake)
        self.score = 0
        self.state = "game"

    def get_game_state(self):
        return self.state

    def set_game_state(self, state):
        self.state = state

    def update(self):
        if self.check_game_over():
            self.state = "game_over"
        elif self.state == "game":
            self.snake.move()
            if self.check_food_collision():
                self.snake.eat()
                self.food.spawn(self.snake)
                self.update_score()


# Main class
import pygame
import random


class GameView:
    def __init__(self, boundary=(20, 20), cell_size=20):
        pygame.init()
        self.boundary = boundary
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.boundary[0] * self.cell_size, self.boundary[1] * self.cell_size))
        self.game = Game(self.boundary)
        self.clock = pygame.time.Clock()
        self.fps = 10

    def draw_grid(self):
        for x in range(0, self.boundary[0] * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.boundary[1] * self.cell_size))
        for y in range(0, self.boundary[1] * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.boundary[0] * self.cell_size, y))

    def draw_snake(self):
        for pos in self.game.get_snake().get_body():
            x = pos[0] * self.cell_size
            y = pos[1] * self.cell_size
            snake_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 255, 0), snake_rect)
            # Setting the snake head
            if pos == self.game.get_snake().get_head():
                inner_rect = pygame.Rect(x + 4, y + 4, self.cell_size - 8, self.cell_size - 8)
                pygame.draw.rect(self.screen, (0, 200, 0), inner_rect)

    def draw_food(self):
        x = self.game.get_food().get_position()[0] * self.cell_size
        y = self.game.get_food().get_position()[1] * self.cell_size
        food_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (255, 0, 0), food_rect)

    def draw_score(self):
        font = pygame.font.Font("freesansbold.ttf", 16)
        score_text = font.render("Score: " + str(self.game.get_score()), True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topleft = (self.boundary[0] * self.cell_size - 120, 10)
        self.screen.blit(score_text, score_rect)

    def draw_game_over(self):
        font = pygame.font.Font("freesansbold.ttf", 48)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.midtop = (self.boundary[0] * self.cell_size / 2, self.boundary[1] * self.cell_size / 2)
        self.screen.blit(game_over_text, game_over_rect)

    def draw_restart(self):
        font = pygame.font.Font("freesansbold.ttf", 16)
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect()
        restart_rect.midtop = (self.boundary[0] * self.cell_size / 2, self.boundary[1] * self.cell_size / 2 + 40)
        self.screen.blit(restart_text, restart_rect)

    def draw_pause(self):
        font = pygame.font.Font("freesansbold.ttf", 16)
        pause_text = font.render("Press P to pause", True, (255, 255, 255))
        pause_rect = pause_text.get_rect()
        pause_rect.midtop = (self.boundary[0] * self.cell_size / 2, self.boundary[1] * self.cell_size / 2 + 80)
        self.screen.blit(pause_text, pause_rect)

    def draw_resume(self):
        font = pygame.font.Font("freesansbold.ttf", 16)
        resume_text = font.render("Press P to resume", True, (255, 255, 255))
        resume_rect = resume_text.get_rect()
        resume_rect.midtop = (self.boundary[0] * self.cell_size / 2, self.boundary[1] * self.cell_size / 2 + 80)
        self.screen.blit(resume_text, resume_rect)

    def draw_exit(self):
        font = pygame.font.Font("freesansbold.ttf", 16)
        exit_text = font.render("Press ESC to exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect()
        exit_rect.midtop = (self.boundary[0] * self.cell_size / 2, self.boundary[1] * self.cell_size / 2 + 120)
        self.screen.blit(exit_text, exit_rect)

    def draw_pause_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_game_over()
        self.draw_restart()
        self.draw_pause()
        self.draw_exit()
        pygame.display.flip()

    def draw_game_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        self.draw_score()
        pygame.display.flip()

    def draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_game_over()
        self.draw_restart()
        self.draw_exit()
        pygame.display.flip()

    def draw(self):
        if self.game.get_game_state() == "pause":
            self.draw_pause_screen()
        elif self.game.get_game_state() == "game":
            self.draw_game_screen()
        elif self.game.get_game_state() == "game_over":
            self.draw_game_over_screen()

    def update(self):
        self.game.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.set_game_state("exit")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.set_game_state("exit")
                elif event.key == pygame.K_UP:
                    self.game.get_snake().change_direction("up")
                elif event.key == pygame.K_DOWN:
                    self.game.get_snake().change_direction("down")
                elif event.key == pygame.K_LEFT:
                    self.game.get_snake().change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    self.game.get_snake().change_direction("right")
                elif event.key == pygame.K_r:
                    self.game.reset()
                elif event.key == pygame.K_p:
                    if self.game.get_game_state() == "pause":
                        self.game.set_game_state("game")
                    elif self.game.get_game_state() == "game":
                        self.game.set_game_state("pause")

    def run(self):
        while self.game.get_game_state() != "exit":
            if self.game.get_game_state() == "game":
                self.update()
            self.draw()
            self.handle_events()
            # Gratually increase the speed of the game based on the score
            self.clock.tick(5 + int(self.game.get_score() / 5))
        pygame.quit()


if __name__ == "__main__":
    game_view = GameView((20, 20), 20)
    game_view.run()
