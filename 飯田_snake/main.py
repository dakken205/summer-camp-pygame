import asyncio
import random

import pygame
from pygame import mixer

# %%
## 各種設定
mixer.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
w_black = (50, 50, 50)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (105, 105, 105)

# アイコンの読み込み
icon = pygame.image.load("./texture/icon.png")
# アイコンの設定
pygame.display.set_icon(icon)
snake_speed = 60
size_block = 10
enemy_num = 0
enemy_counter = 10
num_block_width = int(800 / size_block)
num_block_height = int(num_block_width * 0.75)
wall_thick = 1
stop = 1
# ver1.04 ユーザ画面表示
user_windth = num_block_width
user_height = int(user_windth * 0.15)
# 餌の表示回数
num_food = 8
item_expand = int(snake_speed / 15)
fps_counter = 0
blinking_fps = 15
# プレイヤーライフ
p1_life = 4

dis_width = size_block * num_block_width
dis_height = size_block * (num_block_height + user_height)
foodxy_point_dict = {}
enemy_number_direction_dict = {}
# 0:衝突時のfps, 1:点滅回数(無敵時間)
p1_hit_list = []

# p1,p2 item_list 0:アイテム獲得時のfps ,1:点滅回数, 2:アイテムの種類(ランダム)
p1_item_list = []

# attackの座標
attack_dict = {}


# 画像リサイズ関数(サイズブロック×アイテム拡大数)
def re_item_image(image_path):
    image_re = pygame.transform.scale(
        pygame.image.load(image_path),
        (size_block * item_expand, size_block * item_expand),
    )
    return image_re


# 画像リサイズ関数(アイテムdisplay)
def re_item_display_image(image_path):
    image_re = pygame.transform.scale(
        pygame.image.load(image_path),
        (120, 120),
    )
    return image_re


# 結果画面リサイズ関数
def re_result(image_path):
    image_re = pygame.transform.scale(
        pygame.image.load(image_path),
        (num_block_width * size_block, (num_block_height + user_height) * size_block),
    )
    return image_re


# ユーザwindowリサイズ関数
def re_user(image_path):
    image_re = pygame.transform.scale(
        pygame.image.load(image_path),
        (user_windth * size_block, user_height * size_block),
    )
    return image_re


# %%
# 画像の読み込み
food_image_re = pygame.transform.scale(
    pygame.image.load("./texture/point/red_grape.png"),
    (size_block * item_expand, size_block * item_expand),
)

snake_blue_normal_re = re_item_image("./texture/snake/blue_normal.png")
snake_blue_sad_re = re_item_image("./texture/snake/blue_sad.png")
wall_tate_l_image_re = re_item_image("./texture/wall/tate_l.png")
wall_tate_r_image_re = re_item_image("./texture/wall/tate_r.png")
wall_yoko_up_image_re = re_item_image("./texture/wall/yoko_up.png")
wall_yoko_down_image_re = re_item_image("./texture/wall/yoko_down.png")
wall_r_up_image_re = re_item_image("./texture/wall/r_up.png")
wall_r_down_image_re = re_item_image("./texture/wall/r_down.png")
wall_l_up_image_re = re_item_image("./texture/wall/l_up.png")
wall_l_down_image_re = re_item_image("./texture/wall/l_down.png")
enemy_yoko_image_re = re_item_image("./texture/enemy/enemy_yoko.png")
enemy_tate_image_re = re_item_image("./texture/enemy/enemy_tate.png")
life_image_re = re_item_image("./texture/point/life.png")
item_image_re = re_item_image("./texture/point/item_block.png")
up_re = re_item_image("./texture/point/11_up.png")
right_re = re_item_image("./texture/point/11_right.png")
left_re = re_item_image("./texture/point/11_left.png")
down_re = re_item_image("./texture/point/11_down.png")
result_re = re_result("./texture/result.png")


item_1_re = re_item_display_image("./texture/item/item_1.PNG")
item_2_re = re_item_display_image("./texture/item/item_2.png")
item_3_re = re_item_display_image("./texture/item/item_3.PNG")
item_4_re = re_item_display_image("./texture/item/item_4.PNG")
item_5_re = re_item_display_image("./texture/item/item_5.PNG")
item_6_re = re_item_display_image("./texture/item/item_6.PNG")
item_7_re = re_item_display_image("./texture/item/item_7.PNG")
item_8_re = re_item_display_image("./texture/item/item_8.PNG")
item_9_re = re_item_display_image("./texture/item/item_9.PNG")
item_10_re = re_item_display_image("./texture/item/item_10.PNG")
item_11_re = re_item_display_image("./texture/item/item_11.PNG")


attack_image_re = re_item_image("./texture/point/life.png")

item_value_dict = {
    item_1_re: (1, 12),
    item_2_re: (12, 23),
    item_3_re: (23, 28),
    item_4_re: (28, 39),
    item_5_re: (39, 50),
    item_6_re: (50, 61),
    item_7_re: (61, 72),
    item_8_re: (72, 77),
    item_9_re: (77, 82),
    item_10_re: (82, 90),
    item_11_re: (90, 101),
}

user_window_d = re_user("./texture/user_window/user_window.PNG")
user_window_up = re_user("./texture/user_window/user_window_up.PNG")
user_window_down = re_user("./texture/user_window/user_window_down.PNG")
user_window_enter = re_user("./texture/user_window/user_window_enter.PNG")
user_window_left = re_user("./texture/user_window/user_window_left.PNG")
user_window_right = re_user("./texture/user_window/user_window_right.PNG")

# サウンドの読み込み

food_eat_sound = pygame.mixer.Sound("./music/se/food_eat.ogg")
enemy_notice_sound = pygame.mixer.Sound("./music/se/enemy_notice.ogg")
enemy_hit = pygame.mixer.Sound("./music/se/enemy_hit.ogg")
item_eat = pygame.mixer.Sound("./music/se/enemy_hit.ogg")
roulette = pygame.mixer.Sound("./music/se/roulette.ogg")
item_great = pygame.mixer.Sound("./music/se/item_great.ogg")
item_bad = pygame.mixer.Sound("./music/se/item_bad.ogg")
item_good = pygame.mixer.Sound("./music/se/item_good.ogg")
item_happen = pygame.mixer.Sound("./music/se/item_happen.ogg")
beam = pygame.mixer.Sound("./music/se/beam.ogg")
life_up = pygame.mixer.Sound("./music/se/life_count.ogg")
game_over_under_200 = pygame.mixer.Sound("./music/se/game_over_under_200.ogg")
game_over_over_200 = pygame.mixer.Sound("./music/se/game_over_over_200.ogg")
get_item = pygame.mixer.Sound("./music/se/get_item.ogg")
money = pygame.mixer.Sound("./music/se/money.ogg")
del_enemy = pygame.mixer.Sound("./music/se/del_enemy.ogg")
place_change = pygame.mixer.Sound("./music/se/place_change.ogg")
food_add = pygame.mixer.Sound("./music/se/food_add.ogg")


# %%


# %%
# 効果音の再生
def play_sound(sound):
    sound.play()


# スコアの表示
def show_score(dis, score):
    text_value = pygame.font.SysFont("Gill Sans MT", 35).render(
        "Your Score", True, white
    )
    dis.blit(text_value, [0.5 * size_block, size_block * (num_block_height + 0.5)])
    text_your_hp = pygame.font.SysFont("Gill Sans MT", 35).render(
        "Your HP", True, white
    )
    dis.blit(text_your_hp, [15 * size_block, size_block * (num_block_height + 0.5)])
    point_value = pygame.font.SysFont("Gill Sans MT", 100).render(
        f"{score}", True, white
    )
    dis.blit(
        point_value,
        [size_block * 1, size_block * (num_block_height + user_height / 3)],
    )


# ライフの描写
def draw_life(dis, p1_life):
    for i in range(p1_life):
        dis.blit(
            life_image_re,
            [
                (i + 5.7) * (size_block - 3) * item_expand,
                size_block * (num_block_height + 6.7),
            ],
        )


# playerの描画
def draw_snake(dis, snake_head, p1_hit_list):
    if p1_hit_list == []:
        dis.blit(
            snake_blue_normal_re,
            (snake_head[0] * size_block, snake_head[1] * size_block),
        )
    elif p1_hit_list[1] in [7, 5, 3, 1]:
        dis.blit(
            snake_blue_sad_re, (snake_head[0] * size_block, snake_head[1] * size_block)
        )


# 餌,アイテムの描画
def draw_food_item(dis, foodxy_point_dict, font):
    for key in foodxy_point_dict:
        if foodxy_point_dict[key] == 0:
            dis.blit(item_image_re, (key[0] * size_block, key[1] * size_block))
        else:
            dis.blit(food_image_re, (key[0] * size_block, key[1] * size_block))
            point_value = font.render(str(foodxy_point_dict[key]), True, white)
            dis.blit(
                point_value,
                [
                    (key[0] + item_expand / 4) * size_block,
                    (key[1] + item_expand / 4) * size_block,
                ],
            )


# 敵の描画
def draw_enemy(dis):
    for i in enemy_number_direction_dict:
        if enemy_number_direction_dict[i][6] in [0, 1, 3, 5]:
            if enemy_number_direction_dict[i][2] == 0:
                dis.blit(
                    enemy_tate_image_re,
                    (
                        enemy_number_direction_dict[i][0],
                        enemy_number_direction_dict[i][1],
                    ),
                )
            elif enemy_number_direction_dict[i][2] == 1:
                dis.blit(
                    enemy_yoko_image_re,
                    (
                        enemy_number_direction_dict[i][0],
                        enemy_number_direction_dict[i][1],
                    ),
                )


# field背景/userの描画
def draw_back(dis, user_window):
    pygame.draw.rect(
        dis,
        w_black,
        [
            0,
            0,
            (num_block_width + 1) * size_block,
            (num_block_height + 1) * size_block,
        ],
    )

    dis.blit(
        user_window,
        (
            0,
            num_block_height * size_block,
        ),
    )

    for i in range(int(num_block_width / item_expand)):
        for j in range(int(num_block_height / item_expand)):
            if i == 0:
                if j == 0:
                    dis.blit(wall_l_up_image_re, (i, 0))
                elif j == (num_block_height / item_expand) - 1:
                    dis.blit(
                        wall_l_down_image_re,
                        (i, (num_block_height - item_expand) * size_block),
                    )
                else:
                    dis.blit(wall_tate_l_image_re, (i, j * size_block * item_expand))
            elif i == (num_block_width / item_expand) - 1:
                if j == 0:
                    dis.blit(wall_r_up_image_re, (i * size_block * item_expand, 0))
                elif j == (num_block_height / item_expand) - 1:
                    dis.blit(
                        wall_r_down_image_re,
                        (
                            i * size_block * item_expand,
                            (num_block_height - item_expand) * size_block,
                        ),
                    )
                else:
                    dis.blit(
                        wall_tate_r_image_re,
                        (i * size_block * item_expand, j * size_block * item_expand),
                    )
            elif j == 0:
                dis.blit(wall_yoko_up_image_re, (i * size_block * item_expand, j))
            elif j == (num_block_height / item_expand) - 1:
                dis.blit(
                    wall_yoko_down_image_re,
                    (i * size_block * item_expand, j * size_block * item_expand),
                )


# メッセージの表示
def message(dis, font, msg, color, x, y):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [x, y])


# 新しい餌,アイテムの位置を決める
def make_food(foodxy_point_dict, num_food):
    while len(foodxy_point_dict) < num_food:
        food_x = random.randrange(
            (wall_thick + 2 * item_expand),
            num_block_width - (wall_thick + 2 * item_expand),
            3 * item_expand,
        )
        food_y = random.randrange(
            (wall_thick + 2 * item_expand),
            num_block_height - (wall_thick + 2 * item_expand),
            3 * item_expand,
        )
        # 0はアイテム、餌は1～7になる
        point = random.randrange(0, 7)
        if (food_x, food_y) not in foodxy_point_dict:
            foodxy_point_dict[(food_x, food_y)] = point
    return foodxy_point_dict


# 動く敵を作成する
def make_enemy(enemy_add_num, enemy_num):
    # 進行方向　[敵番号] = {X,Y,進行方向(0上下,1左右),X移動,Y移動,生成時経過fps,点滅回数} (表示回数=5,3,1)
    for i in range(enemy_add_num):
        enemy_x = random.randrange(
            wall_thick + 1, int(num_block_width / item_expand - (wall_thick + 1))
        )
        enemy_y = random.randrange(
            wall_thick + 1, int(num_block_height / item_expand - (wall_thick + 1))
        )
        enemy_number_direction_dict[enemy_num + i + 1] = (
            enemy_x * item_expand * size_block,
            enemy_y * item_expand * size_block,
            random.randrange(0, 2),
            random.choice([4, -4]),
            random.choice([4, -4]),
            fps_counter,
            5,
        )

    enemy_num += enemy_add_num


# 敵の座標を更新する
def change_enemy(enemy_number_direction_dict):
    for i in enemy_number_direction_dict:
        enemy_number_direction_dict[i] = list(enemy_number_direction_dict[i])
        # 敵の点滅動作(無敵期間)
        if enemy_number_direction_dict[i][6] != 0:
            # 一定時間で点滅の切り替え
            if fps_counter == enemy_number_direction_dict[i][5] + blinking_fps:
                enemy_number_direction_dict[i][6] += -1
                enemy_number_direction_dict[i][5] += blinking_fps
        # もし上下ならy座標だけを動かす
        elif enemy_number_direction_dict[i][2] == 0:
            if enemy_number_direction_dict[i][1] == (
                (wall_thick - 0.5) * size_block * item_expand
            ) or enemy_number_direction_dict[i][1] == (
                size_block * (num_block_height - (item_expand * (wall_thick + 0.5)))
            ):
                enemy_number_direction_dict[i][4] = -enemy_number_direction_dict[i][4]
            enemy_number_direction_dict[i][1] += enemy_number_direction_dict[i][4]
        # もし左右ならX座標だけを動かす
        elif enemy_number_direction_dict[i][2] == 1:
            if enemy_number_direction_dict[i][0] == (
                (wall_thick - 0.5) * size_block * item_expand
            ) or enemy_number_direction_dict[i][0] == (
                size_block * (num_block_width - (item_expand * (wall_thick + 0.5)))
            ):
                enemy_number_direction_dict[i][3] = -enemy_number_direction_dict[i][3]
            enemy_number_direction_dict[i][0] += enemy_number_direction_dict[i][3]
        enemy_number_direction_dict[i] = tuple(enemy_number_direction_dict[i])


# アイテムをユーザ画面に表示する


# item_value HP enemy_1del,all_HP,food_allchange,10pt,food_1add,20pt,enemy_alldel,-50pt,place_change,4atack
def display_item(dis, p1_item_list, x_dis, y_dis):
    item_value = p1_item_list[2]
    for key in item_value_dict:
        if item_value_dict[key][0] <= item_value < item_value_dict[key][1]:
            if p1_item_list[1] == 0:
                if (key == item_3_re) or (key == item_8_re):
                    play_sound(item_great)
                elif key == item_9_re:
                    play_sound(item_bad)
                elif key == item_10_re:
                    play_sound(item_happen)
                else:
                    play_sound(item_good)
            elif p1_item_list[1] == -1:
                dis.blit(key, [x_dis, y_dis])


# rouletteアイテムを表示
def display_roulette_item(dis, x_dis, y_dis, item_random):
    item_list = [
        item_1_re,
        item_2_re,
        item_3_re,
        item_4_re,
        item_5_re,
        item_6_re,
        item_7_re,
        item_8_re,
        item_9_re,
        item_10_re,
        item_11_re,
        item_1_re,
        item_2_re,
        item_3_re,
        item_4_re,
        item_5_re,
        item_6_re,
        item_7_re,
        item_8_re,
        item_9_re,
        item_10_re,
        item_11_re,
    ]
    dis.blit(item_list[item_random - 1], [x_dis, y_dis])


# 結果を表示する画面
def show_result(dis, snake_score):
    text_value = pygame.font.SysFont("Gill Sans MT", 100).render(
        "Your final Score", True, white
    )
    dis.blit(
        text_value,
        [
            (num_block_width // 3 - 13) * size_block,
            size_block * (num_block_height // 4),
        ],
    )
    point_value = pygame.font.SysFont("Gill Sans MT", 150).render(
        f"{snake_score} pt", True, white
    )
    dis.blit(
        point_value,
        [
            (num_block_width // 3 - 12) * size_block,
            size_block * (num_block_height // 3 + 3),
        ],
    )
    play_value = pygame.font.SysFont("Gill Sans MT", 50).render(
        "Push Back: finish game", True, white
    )
    dis.blit(
        play_value,
        [
            (num_block_width // 3 - 13) * size_block,
            size_block * (num_block_height // 1.7),
        ],
    )


# %%
# メインループ
async def main():
    game_init = True
    game_over = False
    game_close = False
    # bgmの読み込み
    random.seed()

    pygame.mixer.music.load("./music/bgm/bgm_vs_normal.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    foodxy_point_dict = {}
    global enemy_counter
    global fps_counter
    global p1_life
    global p1_hit_list
    global p1_item_list
    global num_food
    global snake_score
    global enemy_number_direction_dict
    global enemy_num
    global user_window

    attack = 0

    # pygameの初期化
    pygame.init()

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption("CANTAUP!")

    clock = pygame.time.Clock()
    font_message = pygame.font.SysFont("Gill Sans MT", 60)
    font_score = pygame.font.SysFont("Gill Sans MT", 35)
    snake_score = 0
    while True:
        if game_init:
            # ゲームの初期化。
            x = num_block_width // 2
            y = num_block_height // 2

            x_change = 0
            y_change = 0

            foodxy_point_dict = make_food(foodxy_point_dict, num_food)

            game_init = False
            game_over = False

        elif game_close:
            # ゲーム終了

            # # 画面を閉じる処理
            # pygame.quit()
            break

        elif game_over:
            pygame.mixer.music.stop()
            global stop
            # ゲームオーバー
            if snake_score >= 200 and stop == 1:
                play_sound(game_over_over_200)
                stop += 1
            elif snake_score < 200 and stop == 1:
                stop += 1
                play_sound(game_over_under_200)
            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        game_over = False
                        game_close = True
            # 描画系
            dis.blit(result_re, [0, 0])
            message(
                dis,
                font_message,
                "Game over!",
                red,
                (num_block_width // 3 - 13) * size_block,
                size_block * (num_block_height // 5.3),
            )
            show_result(dis, snake_score)
            pygame.display.update()

        else:
            if x == ((wall_thick - 0.5) * item_expand) or x == num_block_width - (
                item_expand * (wall_thick + 0.5)
            ):
                x_change = -x_change
            elif y == ((wall_thick - 0.5) * item_expand) or y == num_block_height - (
                item_expand * (wall_thick + 0.5)
            ):
                y_change = -y_change

            else:
                for event in pygame.event.get():
                    user_window = user_window_d
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.QUIT:
                        game_close = True
                    elif keys[pygame.K_w]:
                        user_window = user_window_up
                    elif keys[pygame.K_s]:
                        user_window = user_window_down
                    elif keys[pygame.K_d]:
                        user_window = user_window_right
                    elif keys[pygame.K_a]:
                        user_window = user_window_left
                    elif keys[pygame.K_RETURN]:
                        user_window = user_window_enter
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            x_change = -0.5
                            y_change = 0
                        elif event.key == pygame.K_d:
                            x_change = 0.5
                            y_change = 0
                        elif event.key == pygame.K_w:
                            x_change = 0
                            y_change = -0.5
                        elif event.key == pygame.K_s:
                            y_change = 0.5
                            x_change = 0
                        if event.key == pygame.K_RETURN:
                            if p1_item_list != [] and p1_item_list[1] == -1:
                                for key in item_value_dict:
                                    if (
                                        item_value_dict[key][0]
                                        <= p1_item_list[2]
                                        < item_value_dict[key][1]
                                    ):
                                        # 1(1HP追加)
                                        if key == item_1_re:
                                            if p1_life < 4:
                                                p1_life += 1
                                                play_sound(life_up)
                                            p1_item_list = []
                                            break
                                        # 2(1enemy消去)
                                        elif key == item_2_re:
                                            if enemy_number_direction_dict != {}:
                                                enemy_list = []
                                                del enemy_number_direction_dict[1]
                                                play_sound(del_enemy)
                                                for i in range(
                                                    len(enemy_number_direction_dict)
                                                ):
                                                    enemy_list.append(
                                                        enemy_number_direction_dict[
                                                            i + 2
                                                        ]
                                                    )
                                                enemy_number_direction_dict = {}
                                                for i in range(len(enemy_list)):
                                                    enemy_number_direction_dict[
                                                        i + 1
                                                    ] = enemy_list[i]
                                                enemy_num = len(enemy_list)

                                            p1_item_list = []
                                            break
                                        # 3(ALL_HP追加)
                                        elif key == item_3_re:
                                            if p1_life < 4:
                                                p1_life = 4
                                                play_sound(life_up)
                                            p1_item_list = []
                                            break
                                        # 4(Food_change)
                                        elif key == item_4_re:
                                            play_sound(food_add)
                                            foodxy_point_dict = {}
                                            foodxy_point_dict = make_food(
                                                foodxy_point_dict, num_food
                                            )
                                            p1_item_list = []
                                            break
                                        # 8(ALLenemy消去)
                                        elif key == item_8_re:
                                            enemy_number_direction_dict = {}
                                            enemy_num = 0
                                            play_sound(del_enemy)
                                            p1_item_list = []
                                            break
                                        # 10(PlaceChange)
                                        elif key == item_10_re:
                                            x = random.randrange(
                                                (wall_thick + 1) * item_expand,
                                                num_block_width
                                                - (wall_thick * (item_expand + 5)),
                                            )
                                            y = random.randrange(
                                                (wall_thick + 1) * item_expand,
                                                num_block_height
                                                - (wall_thick * (item_expand + 5)),
                                            )
                                            p1_item_list = []
                                            play_sound(place_change)
                                            break
                                        # 11(4attack)
                                        elif key == item_11_re:
                                            play_sound(beam)
                                            attack += 1
                                            attack_dict[attack] = (
                                                [x, y],
                                                [x, y],
                                                [x, y],
                                                [x, y],
                                            )
                                            p1_item_list = []
                                            break
            # 蛇の移動処理
            x += x_change
            y += y_change
            fps_counter += 1
            draw_back(dis, user_window)

            # 自分自身との当たり判定
            snake_head = (x, y)
            # 餌を食べたかどうかの判定
            for key in foodxy_point_dict:
                if (key[0] - item_expand) < x < (key[0] + item_expand) and (
                    key[1] - item_expand
                ) < y < (key[1] + item_expand):
                    if foodxy_point_dict[key] == 0 and p1_item_list == []:
                        play_sound(get_item)
                        play_sound(roulette)
                        del foodxy_point_dict[(key[0], key[1])]
                        p1_item_list.append(fps_counter)
                        p1_item_list.append(18)
                        p1_item_list.append(random.randrange(1, 101))
                        foodxy_point_dict = make_food(foodxy_point_dict, num_food)
                        break
                    else:
                        play_sound(food_eat_sound)
                        snake_score += foodxy_point_dict[(key[0], key[1])]
                        del foodxy_point_dict[(key[0], key[1])]
                        foodxy_point_dict = make_food(foodxy_point_dict, num_food)
                        break

            # 敵に当たったかどうかの判定
            if p1_hit_list == []:
                for key in enemy_number_direction_dict:
                    if (
                        enemy_number_direction_dict[key][6] == 0
                        and (
                            enemy_number_direction_dict[key][0] / size_block
                            - (item_expand * 0.5)
                        )
                        < x
                        < (
                            enemy_number_direction_dict[key][0] / size_block
                            + (item_expand * 0.5)
                        )
                        and (
                            enemy_number_direction_dict[key][1] / size_block
                            - (item_expand * 0.5)
                        )
                        < y
                        < (
                            enemy_number_direction_dict[key][1] / size_block
                            + (item_expand * 0.5)
                        )
                    ):
                        play_sound(enemy_hit)
                        p1_hit_list.append(fps_counter)
                        p1_hit_list.append(7)
                        p1_life += -1
            elif p1_hit_list[1] == 1:
                p1_hit_list = []
            elif fps_counter == p1_hit_list[0] + blinking_fps:
                p1_hit_list[0] += blinking_fps
                p1_hit_list[1] += -1
            if p1_life == 0:
                game_over = True
            # アイテムルーレット開始
            if p1_item_list != []:
                if p1_item_list[1] == -1:
                    display_item(
                        dis,
                        p1_item_list,
                        7.2 * size_block * item_expand,
                        size_block * (num_block_height + 0.2),
                    )
                elif p1_item_list[1] == 0:
                    p1_item_list[1] = -1
                elif fps_counter == p1_item_list[0] + 5:
                    p1_item_list[1] += -1
                    p1_item_list[0] += 5
                if p1_item_list[1] > 0:
                    display_roulette_item(
                        dis,
                        7.2 * size_block * item_expand,
                        size_block * (num_block_height + 0.2),
                        p1_item_list[1],
                    )
                elif p1_item_list[1] == 0:
                    display_item(
                        dis,
                        p1_item_list,
                        7.2 * size_block * item_expand,
                        size_block * (num_block_height + 0.2),
                    )
                if p1_item_list[1] == -1:
                    for key in item_value_dict:
                        if (
                            item_value_dict[key][0]
                            <= p1_item_list[2]
                            < item_value_dict[key][1]
                        ) and (fps_counter == p1_item_list[0] + 100):
                            # 5(10pt追加)
                            if key == item_5_re:
                                snake_score += 10
                                play_sound(money)
                                p1_item_list = []
                                enemy_counter += 20
                                break
                            # 7(20pt追加)
                            elif key == item_7_re:
                                snake_score += 20
                                play_sound(money)
                                p1_item_list = []
                                enemy_counter += 20
                                break
                            # 6(food1追加)
                            elif key == item_6_re:
                                if num_food <= 14:
                                    num_food += 1
                                    foodxy_point_dict = make_food(
                                        foodxy_point_dict, num_food
                                    )
                                    play_sound(food_add)
                                p1_item_list = []
                                break
                            # 9(-50pt没収)
                            elif key == item_9_re:
                                snake_score += -50
                                if snake_score < 0:
                                    snake_score = 0
                                else:
                                    enemy_counter += -50
                                play_sound(money)
                                p1_item_list = []
                                break

            # Attackアイテム座標描写/更新
            if attack_dict != {}:
                enemy_hit_list = []
                enemy_list = []
                for key in attack_dict:
                    for i in range(len(attack_dict[key])):
                        if (0 <= attack_dict[key][i][0] <= num_block_width) and (
                            0
                            <= attack_dict[key][i][1]
                            <= num_block_height - item_expand
                        ):
                            for key_e in enemy_number_direction_dict:
                                if (
                                    enemy_number_direction_dict[key_e][6] == 0
                                    and (
                                        enemy_number_direction_dict[key_e][0]
                                        / size_block
                                        - item_expand
                                    )
                                    < attack_dict[key][i][0]
                                    < (
                                        enemy_number_direction_dict[key_e][0]
                                        / size_block
                                        + item_expand
                                    )
                                    and (
                                        enemy_number_direction_dict[key_e][1]
                                        / size_block
                                        - item_expand
                                    )
                                    < attack_dict[key][i][1]
                                    < (
                                        enemy_number_direction_dict[key_e][1]
                                        / size_block
                                        + item_expand
                                    )
                                ):
                                    enemy_hit_list.append(key_e)
                                    play_sound(del_enemy)
                            if i == 0:
                                dis.blit(
                                    left_re,
                                    [
                                        attack_dict[key][i][0] * size_block,
                                        attack_dict[key][i][1] * size_block,
                                    ],
                                )
                                attack_dict[key][i][0] += -2
                            elif i == 1:
                                dis.blit(
                                    right_re,
                                    [
                                        attack_dict[key][i][0] * size_block,
                                        attack_dict[key][i][1] * size_block,
                                    ],
                                )
                                attack_dict[key][i][0] += 2
                            elif i == 2:
                                dis.blit(
                                    up_re,
                                    [
                                        attack_dict[key][i][0] * size_block,
                                        attack_dict[key][i][1] * size_block,
                                    ],
                                )
                                attack_dict[key][i][1] += -2
                            elif i == 3:
                                dis.blit(
                                    down_re,
                                    [
                                        attack_dict[key][i][0] * size_block,
                                        attack_dict[key][i][1] * size_block,
                                    ],
                                )
                                attack_dict[key][i][1] += 2
                for key_s in enemy_number_direction_dict:
                    if key_s not in enemy_hit_list:
                        enemy_list.append(enemy_number_direction_dict[key_s])
                enemy_number_direction_dict = {}
                for s in range(len(enemy_list)):
                    enemy_number_direction_dict[s + 1] = enemy_list[s]
                enemy_num += -(len(enemy_hit_list))

            # スコアアップごとに敵を出現させる
            if snake_score >= enemy_counter:
                make_enemy(1, enemy_num)
                play_sound(enemy_notice_sound)
                enemy_num += 1
                enemy_counter += 20
            # 敵の移動処理
            change_enemy(enemy_number_direction_dict)

            draw_food_item(dis, foodxy_point_dict, font_score)
            draw_enemy(dis)
            show_score(dis, snake_score)
            draw_life(dis, p1_life)
            draw_snake(dis, snake_head, p1_hit_list)

            pygame.display.update()
            # 時間制御
            await asyncio.sleep(0)
            clock.tick(snake_speed)


# %%
# メインループの実行
asyncio.run(main())


# %%


# %%
