import pygame
from random import randint
from typing import Optional, Tuple, List

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 20
GRID_COLS = SCREEN_WIDTH // CELL_SIZE
GRID_ROWS = SCREEN_HEIGHT // CELL_SIZE

DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)

COLOR_BACKGROUND = (0, 0, 0)
COLOR_BORDER = (93, 216, 228)
COLOR_APPLE = (255, 0, 0)
COLOR_SNAKE = (0, 255, 0)

GAME_SPEED = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameEntity:

    def __init__(self, position: Optional[Tuple[int, int]] = None,
                 color: Optional[Tuple[int, int, int]] = None) -> None:
        self.position = position or (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.color = color or (255, 255, 255)

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def draw_cell(self, surface: pygame.Surface, position: Tuple[int, int],
                  color: Optional[Tuple[int, int, int]] = None) -> None:
        rect = pygame.Rect(position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, color or self.color, rect)
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1)


class Apple(GameEntity):

    def __init__(self) -> None:
        super().__init__(color=COLOR_APPLE)
        self.randomize_position()

    def randomize_position(self) -> None:
        self.position = (randint(0, GRID_COLS - 1) * CELL_SIZE,
                         randint(0, GRID_ROWS - 1) * CELL_SIZE)

    def draw(self, surface: pygame.Surface) -> None:
        self.draw_cell(surface, self.position)


class Snake(GameEntity):

    def __init__(self) -> None:
        super().__init__(position=(GRID_COLS // 2 * CELL_SIZE, GRID_ROWS // 2 * CELL_SIZE),
                         color=COLOR_SNAKE)
        self.length: int = 1
        self.body_positions: List[Tuple[int, int]] = [self.position]
        self.direction: Tuple[int, int] = DIRECTION_RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self, new_direction: Tuple[int, int]) -> None:
        if new_direction != (self.direction[0] * -1, self.direction[1] * -1):
            self.next_direction = new_direction

    def move(self) -> None:
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.body_positions[0]
        x, y = self.direction
        new_head = ((head_x + x * CELL_SIZE) % SCREEN_WIDTH,
                    (head_y + y * CELL_SIZE) % SCREEN_HEIGHT)

        if len(self.body_positions) > 2 and new_head in self.body_positions[2:]:
            self.reset()
        else:
            self.body_positions.insert(0, new_head)
            if len(self.body_positions) > self.length:
                self.body_positions.pop()

    def draw(self, surface: pygame.Surface) -> None:
        for position in self.body_positions[:-1]:
            self.draw_cell(surface, position)

        head_position = self.body_positions[0]
        self.draw_cell(surface, head_position, COLOR_SNAKE)

    def get_head_position(self) -> Tuple[int, int]:
        return self.body_positions[0]

    def reset(self) -> None:
        self.length = 1
        self.body_positions = [self.position]
        self.direction = DIRECTION_RIGHT
        self.next_direction = None


def handle_keys(snake: Snake) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(DIRECTION_UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DIRECTION_DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(DIRECTION_LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(DIRECTION_RIGHT)


def main() -> None:
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(GAME_SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(COLOR_BACKGROUND)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
