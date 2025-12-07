import pygame
import random
import sys

# Инициализация констант
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 20

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None):
        """Инициализирует игровой объект.

        Args:
            position (tuple): Начальная позиция объекта (x, y)
        """
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position
        self.body_color = None

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки
        """
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки
        """
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__()
        self.body_color = GREEN
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении.

        Returns:
            tuple: Координаты удаленного сегмента (для затирания следа)
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        old_tail = None
        if len(self.positions) >= self.length:
            old_tail = self.positions[-1]

        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.positions.pop()

        return old_tail

    def draw(self, surface):
        """Отрисовывает змейку на поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки
        """
        for i, (x, y) in enumerate(self.positions):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            if i == 0:
                pygame.draw.rect(surface, BLUE, rect)
            else:
                pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Returns:
            tuple: Координаты головы (x, y)
        """
        return self.positions[0]

    def grow(self):
        """Увеличивает длину змейки на 1 сегмент."""
        self.length += 1


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой.

    Args:
        snake (Snake): Объект змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)

        snake.update_direction()

        old_tail = snake.move()

        if old_tail:
            rect = pygame.Rect(old_tail, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, rect)

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        screen.fill(BLACK)

        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (30, 30, 30), (0, y), (SCREEN_WIDTH, y))

        apple.draw(screen)
        snake.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Счет: {snake.length - 1}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()