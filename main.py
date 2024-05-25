import pygame
import sys

# 게임 보드 크기
BOARD_SIZE = 15

# Pygame 초기화
pygame.init()

# 창 크기 설정
WINDOW_SIZE = 600
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))


def draw_board(board):
    # Draw grid lines
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (i * 40 + 20, 0), (i * 40 + 20, WINDOW_SIZE), 1)
        pygame.draw.line(screen, (0, 0, 0), (0, i * 40 + 20), (WINDOW_SIZE, i * 40 + 20), 1)

    # Draw stones
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == 1:
                pygame.draw.circle(screen, (25, 25, 25), (x * 40 + 20, y * 40 + 20), 18)
            elif board[x][y] == 2:
                pygame.draw.circle(screen, (230, 230, 230), (x * 40 + 20, y * 40 + 20), 18)


def draw_end_screen(winner):
    """Draw the end screen with the winner and the options to play again or quit"""
    text = font.render(f"Player {winner} wins!", True, (0, 0, 0))
    screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 3))

    play_again_text = font.render("Play again", True, (0, 0, 0))
    quit_text = font.render("Quit", True, (0, 0, 0))

    pygame.draw.rect(screen, (0, 255, 0), (WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2, 200, 50))
    pygame.draw.rect(screen, (255, 0, 0), (WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 60, 200, 50))

    screen.blit(play_again_text, (WINDOW_SIZE // 2 - play_again_text.get_width() // 2, WINDOW_SIZE // 2 + 15))
    screen.blit(quit_text, (WINDOW_SIZE // 2 - quit_text.get_width() // 2, WINDOW_SIZE // 2 + 75))


font = pygame.font.Font(None, 36)


def handle_end_screen_click(pos):
    """Handle a mouse click on the end screen"""
    x, y = pos
    if WINDOW_SIZE // 2 - 100 <= x <= WINDOW_SIZE // 2 + 100:
        if WINDOW_SIZE // 2 <= y <= WINDOW_SIZE // 2 + 50:
            return "play again"
        elif WINDOW_SIZE // 2 + 60 <= y <= WINDOW_SIZE // 2 + 110:
            return "quit"


class Game:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.player = 1
        self.winner = 0

    def place_stone(self, x, y):
        if self.board[x][y] == 0 and self.winner == 0:
            self.board[x][y] = self.player
            return True
        return False

    def update_game_status(self, x, y):
        if self.check_game_over(x, y):
            self.winner = self.player
        else:
            self.player = 3 - self.player

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x //= 40
            y //= 40
            if self.place_stone(x, y):
                self.update_game_status(x, y)

    def draw(self):
        screen.fill((165, 133, 69))
        draw_board(self.board)
        if self.winner != 0:
            draw_end_screen(self.winner)
        pygame.display.flip()

    def check_game_over(self, x, y):
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            if self.is_five_in_a_row(x, y, dx, dy):
                return True
        return False

    def is_five_in_a_row(self, x, y, dx, dy):
        for i in range(-4, 1):
            if all(0 <= x + j * dx < BOARD_SIZE and 0 <= y + j * dy < BOARD_SIZE
                   and self.board[x + j * dx][y + j * dy] == self.board[x][y] for j in range(i, i + 5)):
                return True
        return False

    def reset(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.player = 1
        self.winner = 0


# 게임 루프
game = Game()
while True:
    for event in pygame.event.get():
        if game.winner == 0:
            game.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = handle_end_screen_click(event.pos)
                if action == "play again":
                    game.reset()
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
    game.draw()
