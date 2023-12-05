import pygame
import random
import os

pygame.init()
pygame.font.init()

Width, Height = 900, 900
Win = pygame.display.set_mode((Width, Height))
croix = pygame.transform.scale(pygame.image.load(os.path.join("assets", "1200px-Red_x.svg.png")),
                               (Width // 3, Height // 3))
rond = pygame.transform.scale(pygame.image.load(os.path.join("assets", "254px-Letter_o.svg.png")),
                              (Width // 3, Height // 3))
bckg = (173, 216, 230)
Clock = pygame.time.Clock()

AI = +1
human = -1

fps = 120


def create_board():
    return [[0 for _ in range(3)] for _ in range(3)]


def empty_cells(board):
    empty_cells = []
    for y, row in enumerate(board):
        for x, case in enumerate(row):
            if case == 0:
                empty_cells.append([x, y])
    return empty_cells


def check_game(board, player):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return player
        if board[0][i] == board[1][i] == board[2][i] == player:
            return player

    if board[0][0] == board[1][1] == board[2][2] == player:
        return player
    if board[0][2] == board[1][1] == board[2][0] == player:
        return player

    if len(empty_cells(board)) == 0:
        return "tie"

    return None


def valid_locations(board, x, y, player):
    return [x, y] in empty_cells(board)


def set_location(board, x, y, player):
    if valid_locations(board, x, y, player):
        board[y][x] = player
        return True
    return False


def draw_board(Win):
    for i in range(1, 3):
        pygame.draw.line(Win, (255, 255, 255), (Width * (i / 3), 0), (Width * (i / 3), Height), 1)
        pygame.draw.line(Win, (233, 233, 233), (0, Width * (i / 3)), (Width, Width * (i / 3)), 1)


def draw_pieces(Win, board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == -1:
                Win.blit(croix, (x * (Width // 3), y * (Width // 3)))
            elif board[y][x] == 1:
                Win.blit(rond, (x * (Width // 3), y * (Width // 3)))


def reset(board):
    for x, row in enumerate(board):
        for y in range(len(row)):
            board[y][x] = 0


def main():
    def ai_move(board):
        if len(empty_cells(board)) > 0:
            best_score = float('-inf')
            best_move = None

            for move in empty_cells(board):
                x, y = move
                board[y][x] = AI
                score = minimax(board, 0, False)
                board[y][x] = 0

                if score > best_score:
                    best_score = score
                    best_move = move

            return best_move

    def minimax(board, depth, is_maximizing):
        scores = {'-1': -1, '1': 1, 'tie': 0}

        winner = check_game(board, human)
        if winner is not None:
            return scores[str(winner)]

        if is_maximizing:
            max_eval = float('-inf')
            for move in empty_cells(board):
                x, y = move
                board[y][x] = AI
                eval = minimax(board, depth + 1, False)
                board[y][x] = 0
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in empty_cells(board):
                x, y = move
                board[y][x] = human
                eval = minimax(board, depth + 1, True)
                board[y][x] = 0
                min_eval = min(min_eval, eval)
            return min_eval

    run = True
    game_over = False
    game_board = create_board()
    current_turn = random.choice([human, AI])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    reset(game_board)

            if current_turn == human:
                pass
            elif current_turn == AI and not game_over:
                ai_x, ai_y = ai_move(game_board)
                set_location(game_board, ai_x, ai_y, AI)
                if check_game(game_board, AI):
                    print("AI wins")
                    game_over = True
                current_turn = human

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_turn == human:
                    pos = pygame.mouse.get_pos()
                    x, y = pos[0] // (Width // 3), pos[1] // (Height // 3)
                    if set_location(game_board, x, y, human):
                        if check_game(game_board, human):
                            print("Human wins")
                            game_over = True
                        current_turn = AI

        Win.fill(bckg)
        draw_board(Win)
        draw_pieces(Win, game_board)
        pygame.display.update()
        Clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()