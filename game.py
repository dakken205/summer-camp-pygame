import sys
import pygame

# スクリーンのサイズ
SCREEN_SIZE = (560, 560)
# オセロのボードの1つのマスのサイズ
CELL_SIZE = (70, 70)

# ☆画像を取り込む☆

# ☆画像をマスのサイズに合わせる☆

# 現在選択しているマスを表すレイヤ
GOLD = pygame.Surface(CELL_SIZE, pygame.SRCALPHA)
GOLD.fill((255, 215, 0, 60))


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("othello game")

    # オセロのボード
    board = [["EMPTY" for _ in range(8)] for _ in range(8)]
    # ☆ボードの初期配置を定義する☆

    # 現在操作できるプレイヤー
    player = "BLACK"
    # 現在選択されているマス
    selected = (0, 0)

    while True:
        # 画面を描画する
        draw(screen, board, selected)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# 描画する関数
def draw(screen, board, selected):
    pass
    # ☆描画する関数を実装する☆


# 駒を置いてひっくり返す関数
# 現在選ばれているマスに置くことが可能なら，駒を置いてひっくり返してTrueを返す
# 現在選ばれているマスに置くことが不可能なら，何もせずFalseを返す
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
