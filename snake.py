"""
1Logician Snake
Copyright (c) 2026 Jonathan Boyd / 1Logician

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

1Logician Snake (Beginner-Friendly)
-----------------------------------

A minimal Snake game designed for learning.

## What this project teaches
- The classic game loop: input → update → draw
- Sprite sheets (loading, slicing, scaling)
- Collision detection (cars, platforms, goal slots)
- Scoring, lives, start screen, and game over screen
- Procedural spawning and **level-based difficulty scaling**

Controls:
- Arrow keys: Move
- Space: Pause / Resume
- R: Reset
"""

from __future__ import annotations

import random
import sys
from typing import List, Tuple

import pygame

# -----------------------------
# Configuration (easy to tweak)
# -----------------------------

BLOCK_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 10  # game speed (frames/steps per second)

BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (255, 255, 255)
FOOD_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

WINDOW_TITLE = "1Logician Snake"


GridPos = Tuple[int, int]


class SnakeGame:
    """A simple snake game with wrap-around edges."""

    def __init__(self) -> None:
        pygame.init()

        # Window setup
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()

        # Font created once (not every frame)
        self.font = pygame.font.Font(None, 36)

        self.reset_game()

    # -----------------------------
    # Game state / setup
    # -----------------------------

    def reset_game(self) -> None:
        """Reset the game to its starting state."""
        self.snake: List[GridPos] = [(200, 200), (220, 200), (240, 200)]
        self.direction: str = "RIGHT"
        self.score: int = 0
        self.paused: bool = False
        self.food: GridPos = self.generate_food()

    def generate_food(self) -> GridPos:
        """
        Place food on a random grid cell that is not inside the snake.
        """
        while True:
            x = (random.randint(0, SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = (random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            pos = (x, y)
            if pos not in self.snake:
                return pos

    # -----------------------------
    # Input + update logic
    # -----------------------------

    def handle_events(self) -> None:
        """Handle window events and keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                # Quality-of-life keys
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                # Movement keys (prevent instant reversal)
                elif event.key == pygame.K_UP and self.direction != "DOWN":
                    self.direction = "UP"
                elif event.key == pygame.K_DOWN and self.direction != "UP":
                    self.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.direction = "RIGHT"

    def get_next_head(self, head: GridPos) -> GridPos:
        """Compute the snake's next head position based on direction + wrap-around."""
        x, y = head

        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        # Wrap around screen edges
        if x < 0:
            x = SCREEN_WIDTH - BLOCK_SIZE
        elif x >= SCREEN_WIDTH:
            x = 0

        if y < 0:
            y = SCREEN_HEIGHT - BLOCK_SIZE
        elif y >= SCREEN_HEIGHT:
            y = 0

        return (x, y)

    def update(self) -> None:
        """Advance the game by one step."""
        self.handle_events()

        if self.paused:
            return

        head = self.snake[-1]
        new_head = self.get_next_head(head)

        # Collision with self -> reset (keeps it beginner-simple)
        if new_head in self.snake:
            self.reset_game()
            return

        # Move snake forward
        self.snake.append(new_head)

        # Eat food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            # Remove tail so length stays the same unless we ate food
            self.snake.pop(0)

    # -----------------------------
    # Drawing / rendering
    # -----------------------------

    def draw(self) -> None:
        """Render everything."""
        self.display.fill(BACKGROUND_COLOR)

        # Draw snake
        for x, y in self.snake:
            pygame.draw.rect(self.display, SNAKE_COLOR, (x, y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw food
        fx, fy = self.food
        pygame.draw.rect(self.display, FOOD_COLOR, (fx, fy, BLOCK_SIZE, BLOCK_SIZE))

        # Draw score
        score_surface = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.display.blit(score_surface, (10, 10))

        # Pause overlay
        if self.paused:
            pause_surface = self.font.render("PAUSED - Press SPACE to continue", True, TEXT_COLOR)
            rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display.blit(pause_surface, rect)

        pygame.display.update()

    # -----------------------------
    # Main loop / exit
    # -----------------------------

    def run(self) -> None:
        """Run the main game loop."""
        while True:
            self.update()
            self.draw()
            self.clock.tick(FPS)

    @staticmethod
    def quit() -> None:
        """Clean exit."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    SnakeGame().run()
