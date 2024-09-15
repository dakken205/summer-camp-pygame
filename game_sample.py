import sys
import pygame

# スクリーンのサイズ
SCREEN_SIZE = (560, 560)
# オセロのボードの1つのマスのサイズ
CELL_SIZE = (70, 70)

# 画像を取り込む
EMPTY_IMAGE = pygame.image.load("./images/empty.png")
BLACK_IMAGE = pygame.image.load("./images/black.png")
WHITE_IMAGE = pygame.image.load("./images/white.png")

# 画像をマスのサイズに合わせる
EMPTY = pygame.transform.scale(EMPTY_IMAGE, CELL_SIZE)
BLACK = pygame.transform.scale(BLACK_IMAGE, CELL_SIZE)
WHITE = pygame.transform.scale(WHITE_IMAGE, CELL_SIZE)

# 現在選択しているマスを表すレイヤ
GOLD = pygame.Surface(CELL_SIZE, pygame.SRCALPHA)
GOLD.fill((255, 215, 0, 60))


def main():
    pygame.init()
    # スクリーン
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("othello game")

    # オセロのボード
    board = [["EMPTY" for _ in range(8)] for _ in range(8)]
    board[3][3] = "WHITE"
    board[4][4] = "WHITE"
    board[3][4] = "BLACK"
    board[4][3] = "BLACK"
    # 現在操作できるプレイヤー
    player = "BLACK"
    # 現在選択されているマス
    selected = (0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                (x, y) = selected
                if key[pygame.K_RIGHT]:
                    selected = (
                        min(7, x + 1),
                        y,
                    )
                if key[pygame.K_LEFT]:
                    selected = (
                        max(0, x - 1),
                        y,
                    )
                if key[pygame.K_UP]:
                    selected = (
                        x,
                        max(0, y - 1),
                    )
                if key[pygame.K_DOWN]:
                    selected = (
                        x,
                        min(7, y + 1),
                    )
                if key[pygame.K_RETURN]:
                    if flip(board, player, selected):
                        if player == "BLACK":
                            player = "WHITE"
                        else:
                            player = "BLACK"
            draw(screen, board, selected)
            pygame.display.update()

    pygame.quit()
    sys.exit()


# 描画する関数
def draw(screen, board, selected):
    for x in range(8):
        for y in range(8):
            cell = board[x][y]
            position = (
                x * CELL_SIZE[0],
                y * CELL_SIZE[1],
            )
            if cell == "BLACK":
                screen.blit(BLACK, position)
            elif cell == "WHITE":
                screen.blit(WHITE, position)
            else:
                screen.blit(EMPTY, position)

            if (x, y) == selected:
                screen.blit(GOLD, position)


# 駒を置いてひっくり返す関数
def flip(board, player, selected):
    (x, y) = selected
    flag = False
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                now_x = x + dx
                now_y = y + dy
                while 0 <= now_x < 8 and 0 <= now_y < 8:
                    if board[now_x][now_y] != player and board[now_x][now_y] != "EMPTY":
                        now_x += dx
                        now_y += dy
                    else:
                        break
                if 0 <= now_x < 8 and 0 <= now_y < 8:
                    if board[now_x][now_y] == player:
                        now_x -= dx
                        now_y -= dy
                        while (now_x, now_y) != (x, y):
                            flag = True
                            board[now_x][now_y] = player
                            now_x -= dx
                            now_y -= dy
    if flag:
        board[x][y] = player
    return flag


if __name__ == "__main__":
    main()
