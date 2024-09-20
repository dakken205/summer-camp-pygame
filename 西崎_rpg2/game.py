import pygame
import sys
import random
import math
from pygame.locals import *

img_map = [pygame.image.load("map_chip/chip{}.png".format(str(i))) for i in range(14)]
img_pl = pygame.image.load("player0.png")
img_emy = [
    pygame.image.load("enemy/emy{}.png".format("0" * (3 - len(str(i))) + str(i)))
    for i in range(61)
]

# fmt: off
map_data1 = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,16,17,16, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,16,18,16, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,17,19,17, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0,15, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 7, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

cave_data = [
    [ 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,12,12,12,12,12,12,12,12,12,12,12],
    [ 9,10,10,10,10,10,10,10,10,10,10,10,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [ 9, 9, 9, 9,10,10, 9, 9, 9, 9, 9, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12, 9,10,10, 9,12,12,12,12, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12, 9,10,10, 9, 9, 9, 9,12, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12, 9,10,10,10,10,10, 9,12, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12, 9,10,10, 9, 9, 9, 9,12, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [ 9, 9, 9, 9,10,10, 9,12,12,12,12, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [ 9,10,10,10,10,10, 9,12,12,12,12, 9,10, 9,12,12,12,12,12,12,12,12,12,12,12],
    [ 9,13,10,10,10,10, 9,12,12,12,12, 9, 8, 9,12,12,12,12,12,12,12,12,12,12,12],
    [ 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12], 
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12],
    [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12]
]

map_data2 = [
    [ 4, 5, 5, 6, 6, 6,11, 6, 6, 6, 6, 6, 6, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 4, 5, 5, 6, 6, 6, 6, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 4, 4, 5, 6, 6, 6, 6, 5, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 4, 4, 5, 5, 6, 6, 6, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 4, 4, 5, 4, 6, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [16,17,17, 4, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [16,18,19,15, 4, 4, 4, 4, 4, 5, 5, 4,14, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [17,17,17, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

# fmt: on
map_list = [map_data1, cave_data, map_data2]

img_map_dict = {
    0: img_map[0],
    1: img_map[1],
    2: img_map[2],
    3: img_map[3],
    4: img_map[0],
    5: img_map[1],
    6: img_map[2],
    7: img_map[4],
    8: img_map[5],
    9: img_map[6],
    10: img_map[7],
    11: img_map[8],
    12: img_map[9],
    13: img_map[5],
    14: img_map[4],
    15: img_map[0],
    16: img_map[10],
    17: img_map[11],
    18: img_map[12],
    19: img_map[13],
}
encount_rate_dict = {
    0: 0.10,
    1: 0.10,
    2: 0.25,
    3: 0.00,
    4: 0.10,
    5: 0.10,
    6: 0.25,
    7: 0.00,
    8: 0.00,
    9: 0.00,
    10: 0.25,
    11: 0.00,
    12: 0.00,
    13: 0.00,
    14: 0.00,
    15: 0.00,
    16: 0.00,
    17: 0.00,
    18: 0.00,
    19: 0.00,
}

map_id = 0
now_map = map_list[map_id]

pl_name = "ロト"
pl_st_dict = {
    1: [28, 0, 5, 2, 4],
    2: [46, 0, 9, 4, 6],
    3: [52, 0, 19, 6, 10],
    4: [68, 0, 29, 6, 10],
    5: [72, 0, 31, 10, 18],
    6: [78, 0, 35, 16, 24],
    7: [80, 0, 47, 18, 28],
    8: [84, 0, 53, 22, 32],
    9: [84, 0, 57, 24, 32],
    10: [90, 0, 63, 26, 36],
    11: [94, 0, 67, 28, 38],
    12: [96, 0, 75, 30, 40],
    13: [102, 0, 81, 32, 44],
    14: [110, 0, 85, 34, 44],
    15: [110, 0, 87, 38, 46],
    16: [112, 0, 87, 40, 50],
    17: [118, 0, 91, 42, 52],
    18: [132, 0, 99, 46, 58],
    19: [148, 0, 107, 50, 62],
    20: [164, 0, 115, 52, 70],
    21: [170, 0, 117, 56, 74],
    22: [176, 0, 117, 58, 76],
    23: [180, 0, 119, 64, 80],
    24: [184, 0, 121, 68, 82],
    25: [198, 0, 131, 72, 94],
    26: [208, 0, 137, 74, 102],
    27: [216, 0, 143, 76, 110],
    28: [222, 0, 153, 80, 110],
    29: [222, 0, 163, 84, 112],
    30: [224, 0, 171, 86, 118],
    31: [226, 0, 183, 90, 122],
    32: [246, 0, 199, 98, 136],
    33: [258, 0, 209, 102, 140],
    34: [272, 0, 221, 106, 148],
    35: [284, 0, 235, 110, 152],
    36: [292, 0, 241, 112, 154],
    37: [298, 0, 247, 118, 162],
    38: [302, 0, 255, 124, 168],
    39: [312, 0, 261, 128, 176],
    40: [326, 0, 271, 134, 186],
    41: [350, 0, 301, 154, 204],
    42: [372, 0, 325, 172, 224],
    43: [392, 0, 341, 192, 246],
    44: [422, 0, 361, 224, 270],
    45: [500, 0, 401, 256, 290],
}
pl_lv_dict = {
    1: 0,
    2: 6,
    3: 30,
    4: 84,
    5: 180,
    6: 330,
    7: 546,
    8: 840,
    9: 1224,
    10: 1710,
    11: 2310,
    12: 3036,
    13: 3900,
    14: 4914,
    15: 6090,
    16: 7440,
    17: 8976,
    18: 10710,
    19: 12654,
    20: 14820,
    21: 17220,
    22: 19866,
    23: 22770,
    24: 25944,
    25: 29400,
    26: 33150,
    27: 37206,
    28: 41580,
    29: 46284,
    30: 51330,
    31: 56730,
    32: 62496,
    33: 68640,
    34: 75174,
    35: 82110,
    36: 89460,
    37: 97236,
    38: 105450,
    39: 114114,
    40: 123240,
    41: 132840,
    42: 142926,
    43: 153510,
    44: 164604,
    45: 176220,
}
pl_exp = 0
pl_gold = 0
pl_lv = 1
pl_st = pl_st_dict[pl_lv]
pl_buki = "どうのつるぎ"

buki_dict = {
    "こんぼう": [5, 10],
    "どうのつるぎ": [15, 100],
    "てつのおの": [30, 1000],
    "はがねのつるぎ": [100, 5000],
    "はじゃのつるぎ": [115, 20000],
    "ほのおのつるぎ": [150, 25000],
    "おうじゃのけん": [200, 50000],
    "ロトのつるぎ": [250, 50000],
}

emy_list1 = {
    1: ["スライム", "スライムベス"],
    2: ["ドラキー", "いっかくうさぎ"],
    3: ["バブルスライム", "おおさそり"],
    4: ["おおねずみ", "おばけキノコ"],
    5: ["アルミラージ", "キラービー"],
    6: ["うみうし", "がいこつ"],
    7: ["おばけねずみ", "アニマルゾンビ"],
    8: ["しびれあげは", "しにがみ"],
    9: ["かえんムカデ", "あばれザル"],
    10: ["おおくちばし", "アンデッドマン"],
}

emy_list2 = {
    11: ["アントベア", "アンデッドマン"],
    12: ["かぶとムカデ", "げんじゅつし"],
    13: ["オーク", "ウドラー"],
    14: ["あくまのめだま", "ヒババンゴ"],
    15: ["ダークアイ", "しりょうのきし"],
    16: ["ガルーダ", "かげのきし"],
    17: ["ガーゴイル", "くびかりぞく"],
    18: ["グール", "キラーリカント", "メタルスライム"],
    19: ["ガニラス", "ゴールドオーク"],
    20: ["あくまのきし", "オークキング"],
}

emy_list3 = {
    21: ["ブリザード", "キラータイガー"],
    22: ["ようじゅつし", "ストーンマン"],
    23: ["テンタクルス", "しにがみのきし"],
    24: ["ハーゴンのきし", "サイクロプス"],
    25: ["ゴーレム", "あくましんかん"],
    26: ["オーガー", "わらいぶくろ"],
    27: ["メタルスライム", "はぐれメタル"],
    28: ["ギガンテス", "ブラッディハンド"],
    29: ["やつざきアニマル", "ミミック"],
    30: ["カンダタ", "いどまじん"],
}

emy_dict = {
    "スライム": [3, 0, 5, 3, 2, 2, 1, img_emy[0]],
    "スライムベス": [4, 0, 7, 3, 4, 2, 1, img_emy[1]],
    "ドラキー": [6, 0, 9, 6, 5, 8, 4, img_emy[2]],
    "いっかくうさぎ": [10, 0, 12, 8, 5, 8, 4, img_emy[3]],
    "バブルスライム": [13, 0, 16, 13, 9, 18, 9, img_emy[4]],
    "おおさそり": [20, 0, 18, 16, 4, 18, 9, img_emy[5]],
    "おおねずみ": [16, 0, 19, 11, 15, 32, 16, img_emy[6]],
    "おばけキノコ": [24, 0, 30, 12, 8, 32, 16, img_emy[7]],
    "アルミラージ": [20, 20, 19, 12, 9, 50, 25, img_emy[8]],
    "キラービー": [25, 0, 18, 11, 32, 50, 25, img_emy[9]],
    "うみうし": [32, 0, 38, 11, 16, 72, 36, img_emy[10]],
    "がいこつ": [30, 0, 28, 22, 17, 72, 36, img_emy[11]],
    "おばけねずみ": [25, 0, 41, 12, 41, 98, 49, img_emy[12]],
    "アニマルゾンビ": [50, 30, 28, 4, 11, 98, 49, img_emy[13]],
    "しびれあげは": [40, 0, 62, 10, 30, 128, 64, img_emy[14]],
    "しにがみ": [48, 0, 51, 16, 31, 128, 64, img_emy[15]],
    "かえんムカデ": [45, 0, 45, 40, 20, 162, 81, img_emy[16]],
    "あばれザル": [50, 0, 55, 25, 21, 162, 81, img_emy[17]],
    "おおくちばし": [43, 0, 55, 43, 24, 200, 100, img_emy[18]],
    "アントベア": [50, 0, 69, 45, 10, 242, 121, img_emy[20]],
    "アンデッドマン": [65, 0, 63, 17, 33, 242, 121, img_emy[21]],
    "かぶとムカデ": [20, 0, 39, 110, 13, 288, 144, img_emy[22]],
    "げんじゅつし": [42, 10, 60, 46, 25, 288, 144, img_emy[23]],
    "オーク": [60, 0, 75, 23, 36, 338, 169, img_emy[24]],
    "ウドラー": [63, 0, 72, 27, 45, 338, 169, img_emy[25]],
    "あくまのめだま": [50, 0, 77, 30, 55, 392, 196, img_emy[26]],
    "ヒババンゴ": [60, 0, 74, 29, 52, 392, 196, img_emy[27]],
    "ダークアイ": [67, 0, 74, 22, 55, 450, 225, img_emy[28]],
    "しりょうのきし": [46, 0, 68, 56, 56, 450, 225, img_emy[29]],
    "ガルーダ": [60, 12, 65, 60, 30, 512, 256, img_emy[30]],
    "かげのきし": [50, 0, 79, 64, 40, 512, 256, img_emy[31]],
    "ガーゴイル": [60, 0, 85, 31, 64, 578, 289, img_emy[32]],
    "くびかりぞく": [65, 0, 82, 25, 70, 578, 289, img_emy[33]],
    "グール": [80, 0, 120, 19, 41, 648, 324, img_emy[34]],
    "キラーリカント": [60, 0, 86, 70, 45, 648, 324, img_emy[35]],
    "ガニラス": [50, 0, 68, 150, 25, 722, 361, img_emy[36]],
    "ゴールドオーク": [100, 0, 80, 56, 57, 722, 361, img_emy[37]],
    "あくまのきし": [70, 4, 94, 82, 53, 800, 400, img_emy[38]],
    "オークキング": [110, 0, 99, 35, 60, 800, 400, img_emy[39]],
    "ブリザード": [90, 0, 111, 33, 85, 882, 441, img_emy[40]],
    "キラータイガー": [80, 0, 95, 76, 71, 882, 441, img_emy[41]],
    "ようじゅつし": [96, 30, 72, 80, 58, 968, 484, img_emy[42]],
    "ストーンマン": [160, 0, 100, 40, 40, 968, 484, img_emy[43]],
    "テンタクルス": [200, 0, 97, 15, 36, 1058, 529, img_emy[44]],
    "しにがみのきし": [90, 14, 105, 86, 57, 1058, 529, img_emy[45]],
    "ハーゴンのきし": [77, 25, 115, 72, 65, 1152, 576, img_emy[46]],
    "サイクロプス": [115, 0, 121, 32, 90, 1152, 576, img_emy[47]],
    "ゴーレム": [155, 0, 120, 60, 39, 1250, 625, img_emy[48]],
    "あくましんかん": [158, 0, 92, 38, 100, 1250, 625, img_emy[49]],
    "ドラゴン": [120, 0, 140, 75, 62, 1352, 676, img_emy[50]],
    "わらいぶくろ": [40, 255, 15, 37, 64, 1352, 676, img_emy[51]],
    "メタルスライム": [4, 6, 10, 255, 153, 1458, 50, img_emy[52]],
    "オーガー": [210, 0, 143, 40, 47, 1458, 729, img_emy[53]],
    "ギガンテス": [155, 0, 145, 41, 100, 1568, 784, img_emy[54]],
    "ブラッディハンド": [150, 0, 112, 88, 96, 1568, 784, img_emy[55]],
    "やつざきアニマル": [200, 0, 110, 90, 57, 1682, 841, img_emy[56]],
    "ミミック": [190, 7, 120, 72, 70, 1682, 841, img_emy[57]],
    "いどまじん": [210, 20, 120, 75, 61, 1800, 900, img_emy[58]],
    "カンダタ": [190, 0, 200, 80, 30, 1922, 1000, img_emy[59]],
    "はぐれメタル": [35, 0, 75, 255, 200, 5072, 100, img_emy[60]],
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pl_x = 12
pl_y = 9

key_up = 0
key_down = 0
key_left = 0
key_right = 0
key_enter = 0
key_esc = 0
key_S = 0


def make_map(screen):
    global pl_x, pl_y, now_map
    x = pl_x - 10
    y = pl_y - 7
    for i in range(21):
        for j in range(15):
            map_no = now_map[y + j][x + i]
            screen.blit(img_map_dict[map_no], [i * 48, j * 48, 48, 48])


def move_map(screen, key):
    global pl_x, pl_y, key_up, key_down, key_left, key_right, key_enter, key_S, now_map, buki_list
    key_up = (key_up + 1) * key[K_UP]
    key_down = (key_down + 1) * key[K_DOWN]
    key_left = (key_left + 1) * key[K_LEFT]
    key_right = (key_right + 1) * key[K_RIGHT]
    key_enter = (key_enter + 1) * key[K_RETURN]
    key_S = (key_S + 1) * key[K_s]
    if key_up == 1:
        if (
            now_map[pl_y - 1][pl_x] == 3
            or now_map[pl_y - 1][pl_x] == 9
            or now_map[pl_y - 1][pl_x] == 16
            or now_map[pl_y - 1][pl_x] == 17
            or now_map[pl_y - 1][pl_x] == 18
            or now_map[pl_y - 1][pl_x] == 19
        ):
            return
        pl_y -= 1
        map_action(screen)
    if key_down == 1:
        if (
            now_map[pl_y + 1][pl_x] == 3
            or now_map[pl_y + 1][pl_x] == 9
            or now_map[pl_y + 1][pl_x] == 16
            or now_map[pl_y + 1][pl_x] == 17
            or now_map[pl_y + 1][pl_x] == 18
            or now_map[pl_y + 1][pl_x] == 19
        ):
            return
        pl_y += 1
        map_action(screen)
    if key_left == 1:
        if (
            now_map[pl_y][pl_x - 1] == 3
            or now_map[pl_y][pl_x - 1] == 9
            or now_map[pl_y][pl_x - 1] == 16
            or now_map[pl_y][pl_x - 1] == 17
            or now_map[pl_y][pl_x - 1] == 18
            or now_map[pl_y][pl_x - 1] == 19
        ):
            return
        pl_x -= 1
        map_action(screen)
    if key_right == 1:
        if (
            now_map[pl_y][pl_x + 1] == 3
            or now_map[pl_y][pl_x + 1] == 9
            or now_map[pl_y][pl_x + 1] == 16
            or now_map[pl_y][pl_x + 1] == 17
            or now_map[pl_y][pl_x + 1] == 18
            or now_map[pl_y][pl_x + 1] == 19
        ):
            return
        pl_x += 1
        map_action(screen)
    if key_enter == 1:
        if now_map[pl_y][pl_x] == 15:
            if now_map == map_data1:
                buki_list = ["こんぼう", "どうのつるぎ", "てつのおの"]
            else:
                buki_list = ["はじゃのつるぎ", "ほのおのつるぎ", "おうじゃのけん"]
            bukiya(screen)
        else:
            return
    if key_S == 1:
        save(screen)


def map_action(screen):
    global pl_x, pl_y, now_map, buki_list, map_id
    if random.random() <= encount_rate_dict[now_map[pl_y][pl_x]]:
        encount(screen)
    if now_map[pl_y][pl_x] == 7:
        map_id = 1
        now_map = map_list[map_id]
        pl_x = 12
        pl_y = 9
    elif now_map[pl_y][pl_x] == 8:
        map_id = 0
        now_map = map_list[map_id]
        pl_x = 1
        pl_y = 9
    elif now_map[pl_y][pl_x] == 13:
        map_id = 2
        now_map = map_list[map_id]
        pl_x = 12
        pl_y = 9
    elif now_map[pl_y][pl_x] == 14:
        map_id = 1
        now_map = map_list[map_id]
        pl_x = 1
        pl_y = 9
    elif now_map[pl_y][pl_x] == 11:
        boss_encount(screen)


def save(screen):
    global map_id, pl_name, pl_lv, pl_exp, pl_gold, pl_buki, pl_x, pl_y
    with open("save.txt", mode="w", encoding="utf-8") as f:
        f.write(str(map_id) + "\n")
        f.write(str(pl_name) + "\n")
        f.write(str(pl_lv) + "\n")
        f.write(str(pl_exp) + "\n")
        f.write(str(pl_gold) + "\n")
        f.write(str(pl_buki) + "\n")
        f.write(str(pl_x) + "\n")
        f.write(str(pl_y))
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
    txt = font.render("セーブしました", True, WHITE)
    screen.blit(txt, [100, 420])
    pygame.display.update()
    pygame.time.wait(1000)


def load(screen):
    global key_enter, map_id, now_map, pl_name, pl_lv, pl_exp, pl_gold, pl_buki, pl_x, pl_y, tri_y
    tri_x = 100
    tri_y = 420
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        screen.fill(BLACK)
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                [15 + tri_x, 15 + tri_y],
                [15 + tri_x, 45 + tri_y],
                [45 + tri_x, 30 + tri_y],
            ],
        )
        key = pygame.key.get_pressed()
        load_command(screen, key)
        pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
        txt4 = font.render("はじめから", True, WHITE)
        txt5 = font.render("つづきから".format(pl_gold), True, WHITE)
        screen.blit(txt4, [155, 420])
        screen.blit(txt5, [155, 480])
        pygame.display.update()

        key_enter = (key_enter + 1) * key[K_RETURN]
        if key_enter == 1:
            if tri_y == 420:
                return
            else:
                with open("save.txt", encoding="utf-8") as f:
                    save_data = [s.rstrip() for s in f.readlines()]
                    if save_data == []:
                        return
                    map_id = int(save_data[0])
                    now_map = map_list[map_id]
                    pl_name = str(save_data[1])
                    pl_lv = int(save_data[2])
                    pl_exp = int(save_data[3])
                    pl_gold = int(save_data[4])
                    pl_buki = str(save_data[5])
                    pl_x = int(save_data[6])
                    pl_y = int(save_data[7])
                    return


def load_command(key):
    global key_up, key_down, tri_y
    key_up = (key_up + 1) * key[K_UP]
    key_down = (key_down + 1) * key[K_DOWN]
    if key_up == 1:
        if tri_y == 420:
            return
        tri_y -= 60
    if key_down == 1:
        if tri_y == 480:
            return
        tri_y += 60


def bukiya(screen):
    global pl_gold, buki_list, buki, pl_buki, buki_dict, tri_y, font, key_esc
    tri_x = 100
    tri_y = 30
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                [15 + tri_x, 15 + tri_y],
                [15 + tri_x, 45 + tri_y],
                [45 + tri_x, 30 + tri_y],
            ],
        )
        key = pygame.key.get_pressed()
        buki_command(screen, key)
        pygame.draw.rect(screen, WHITE, [100, 30, 700, 360], width=1)
        txt1 = font.render(
            "{}-----{}G".format(buki_list[0], buki_dict[buki_list[0]][1]), True, WHITE
        )
        txt2 = font.render(
            "{}-----{}G".format(buki_list[1], buki_dict[buki_list[1]][1]), True, WHITE
        )
        txt3 = font.render(
            "{}-----{}G".format(buki_list[2], buki_dict[buki_list[2]][1]), True, WHITE
        )
        screen.blit(txt1, [155, 30])
        screen.blit(txt2, [155, 90])
        screen.blit(txt3, [155, 150])
        pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
        txt4 = font.render("何を買うかね?", True, WHITE)
        txt5 = font.render("(所持金:{}G)".format(pl_gold), True, WHITE)
        txt6 = font.render("(装備:{})".format(pl_buki), True, WHITE)
        screen.blit(txt4, [100, 420])
        screen.blit(txt5, [100, 480])
        screen.blit(txt6, [100, 540])
        pygame.display.update()

        key_esc = (key_esc + 1) * key[K_ESCAPE]
        if key_esc == 1:
            return


def buki_command(screen, key):
    global key_up, key_down, key_enter, key_esc, tri_y, pl_gold, pl_buki, buki_list
    key_up = (key_up + 1) * key[K_UP]
    key_down = (key_down + 1) * key[K_DOWN]
    key_enter = (key_enter + 1) * key[K_RETURN]
    if key_up == 1:
        if tri_y == 30:
            return
        tri_y -= 60
    if key_down == 1:
        if tri_y == 150:
            return
        tri_y += 60
    if tri_y == 30:
        buki = buki_list[0]
    elif tri_y == 90:
        buki = buki_list[1]
    elif tri_y == 150:
        buki = buki_list[2]
    if key_enter == 1:
        if pl_gold < buki_dict[buki][1]:
            screen.fill(BLACK)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            txt4 = font.render("それを買うにはお金が足りないようだ", True, WHITE)
            screen.blit(txt4, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)
        else:
            pl_gold -= buki_dict[buki][1]
            pl_buki = buki
            screen.fill(BLACK)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            txt4 = font.render("{}を装備した".format(buki), True, WHITE)
            screen.blit(txt4, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)


def command(screen, key):
    global key_up, key_down, key_enter, tri_y
    key_up = (key_up + 1) * key[K_UP]
    key_down = (key_down + 1) * key[K_DOWN]
    key_enter = (key_enter + 1) * key[K_RETURN]
    if key_up == 1:
        if tri_y == 450:
            return
        tri_y -= 60
    if key_down == 1:
        if tri_y == 630:
            return
        tri_y += 60
    if key_enter == 1:
        if tri_y == 450:
            attack(screen)
        elif tri_y == 510:
            escape(screen)
        elif tri_y == 570:
            item(screen)
        elif tri_y == 630:
            guard(screen)


def attack(screen):
    global enemy, enemy_list, enemy_hp, pl_hp, pl_name, font
    if pl_st[4] >= enemy_list[4]:
        damage = math.floor(
            (pl_attack - enemy_list[3] / 2) * random.randrange(54, 198) / 256
        )
        if damage <= 0:
            damage = random.randrange(0, 2)
        enemy_hp -= damage
        if enemy_hp <= 0:
            enemy_hp = 0
        screen.fill(BLACK)
        playerstatus(screen)
        pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
        screen.blit(
            enemy_list[7],
            [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
        )
        txtdamage = font.render(
            "{}は{}ダメージを受けた".format(enemy, damage), True, WHITE
        )
        screen.blit(txtdamage, [100, 420])
        pygame.display.update()
        pygame.time.wait(1000)
        if enemy_hp == 0:
            return
        damage = math.floor(
            (enemy_list[2] - pl_st[3] / 2) * random.randrange(54, 198) / 256
        )
        if damage <= 0:
            damage = random.randrange(0, 2)
        pl_hp -= damage
        if pl_hp <= 0:
            pl_hp = 0
        screen.fill(BLACK)
        playerstatus(screen)
        pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
        screen.blit(
            enemy_list[7],
            [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
        )
        txtdamage = font.render(
            "{}は{}ダメージを受けた".format(pl_name, damage), True, WHITE
        )
        screen.blit(txtdamage, [100, 420])
        pygame.display.update()
        pygame.time.wait(1000)
        if pl_hp == 0:
            return
    if enemy_list[4] > pl_st[4]:
        damage = math.floor(
            (enemy_list[2] - pl_st[3] / 2) * random.randrange(54, 198) / 256
        )
        if damage <= 0:
            damage = random.randrange(0, 2)
        pl_hp -= damage
        if pl_hp <= 0:
            pl_hp = 0
        screen.fill(BLACK)
        playerstatus(screen)
        pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
        screen.blit(
            enemy_list[7],
            [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
        )
        txtdamage = font.render(
            "{}は{}ダメージを受けた".format(pl_name, damage), True, WHITE
        )
        screen.blit(txtdamage, [100, 420])
        pygame.display.update()
        pygame.time.wait(1000)
        if pl_hp == 0:
            return
        damage = math.floor(
            (pl_attack - enemy_list[3] / 2) * random.randrange(54, 198) / 256
        )
        if damage <= 0:
            damage = random.randrange(0, 2)
        enemy_hp -= damage
        if enemy_hp <= 0:
            enemy_hp = 0
        screen.fill(BLACK)
        playerstatus(screen)
        pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
        screen.blit(
            enemy_list[7],
            [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
        )
        txtdamage = font.render(
            "{}は{}ダメージを受けた".format(enemy, damage), True, WHITE
        )
        screen.blit(txtdamage, [100, 420])
        pygame.display.update()
        pygame.time.wait(1000)
        if enemy_hp == 0:
            return


def item(screen):
    screen.fill(BLACK)
    playerstatus(screen)
    pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
    screen.blit(
        enemy_list[7],
        [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
    )
    txtdamage = font.render("どうぐを持っていない", True, WHITE)
    screen.blit(txtdamage, [100, 420])
    pygame.display.update()
    pygame.time.wait(1000)


def escape(screen):
    global enemy, enemy_list, enemy_hp, pl_hp, pl_name, font
    screen.fill(BLACK)
    playerstatus(screen)
    pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
    screen.blit(
        enemy_list[7],
        [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
    )
    txtdamage = font.render("ただし逃げられなかった", True, WHITE)
    screen.blit(txtdamage, [100, 420])
    pygame.display.update()
    pygame.time.wait(1000)

    damage = math.floor(
        (enemy_list[2] - pl_st[3] / 2) * random.randrange(54, 198) / 256
    )
    if damage <= 0:
        damage = random.randrange(0, 2)
    pl_hp -= damage
    if pl_hp <= 0:
        pl_hp = 0
    screen.fill(BLACK)
    playerstatus(screen)
    pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
    screen.blit(
        enemy_list[7],
        [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
    )
    txtdamage = font.render(
        "{}は{}ダメージを受けた".format(pl_name, damage), True, WHITE
    )
    screen.blit(txtdamage, [100, 420])
    pygame.display.update()
    pygame.time.wait(1000)
    if pl_hp == 0:
        return


def guard(screen):
    global enemy, enemy_list, enemy_hp, pl_hp, pl_name, font
    screen.fill(BLACK)
    playerstatus(screen)
    pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
    screen.blit(
        enemy_list[7],
        [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
    )
    txtguard = font.render("{}は防御している".format(pl_name), True, WHITE)
    screen.blit(txtguard, [100, 420])
    pygame.display.update()
    pygame.time.wait(1000)

    damage = math.floor((enemy_list[2] - pl_st[3]) * random.randrange(54, 198) / 256)
    if damage <= 0:
        damage = random.randrange(0, 2)
    pl_hp -= damage
    if pl_hp <= 0:
        pl_hp = 0
    screen.fill(BLACK)
    playerstatus(screen)
    pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
    screen.blit(
        enemy_list[7],
        [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
    )
    txtdamage = font.render(
        "{}は{}ダメージを受けた".format(pl_name, damage), True, WHITE
    )
    screen.blit(txtdamage, [100, 420])
    pygame.display.update()
    pygame.time.wait(1000)
    if pl_hp == 0:
        return


def playerstatus(screen):
    global pl_name, pl_hp, pl_mp, pl_lv, font
    pygame.draw.rect(screen, WHITE, [50, 30, 200, 240], width=1)
    txt1 = font.render("{}".format(pl_name), True, WHITE)
    txt2 = font.render("Ｈ：{}".format(pl_hp), True, WHITE)
    txt3 = font.render("Ｍ：{}".format(pl_mp), True, WHITE)
    txt4 = font.render("Lv：{}".format(pl_lv), True, WHITE)
    screen.blit(txt1, [50, 30])
    screen.blit(txt2, [50, 90])
    screen.blit(txt3, [50, 150])
    screen.blit(txt4, [50, 210])


def commandpanel(screen):
    global pl_name, enemy, enemy_list, font
    pygame.draw.rect(screen, WHITE, [50, 390, 300, 300], width=1)
    pygame.draw.rect(screen, WHITE, [50, 450, 300, 1], width=0)
    pygame.draw.rect(screen, WHITE, [400, 450, 500, 60], width=1)
    txt1 = font.render("{}".format(pl_name), True, WHITE)
    txt5 = font.render("こうげき", True, WHITE)
    txt6 = font.render("にげる", True, WHITE)
    txt7 = font.render("どうぐ", True, WHITE)
    txt8 = font.render("ぼうぎょ", True, WHITE)
    txt9 = font.render("{}".format(enemy), True, WHITE)
    screen.blit(txt1, [105, 390])
    screen.blit(txt5, [105, 450])
    screen.blit(txt6, [105, 510])
    screen.blit(txt7, [105, 570])
    screen.blit(txt8, [105, 630])
    screen.blit(txt9, [455, 450])
    screen.blit(
        enemy_list[7],
        [504 - enemy_list[7].get_width() / 2, 300 - enemy_list[7].get_height() / 2],
    )


def encount(screen):
    global pl_lv, tri_x, tri_y, enemy, enemy_list, enemy_hp, pl_hp, pl_mp, pl_exp, pl_gold, pl_st, font, pl_x, pl_y, now_map
    if now_map[pl_y][pl_x] == 0 or now_map[pl_y][pl_x] == 1 or now_map[pl_y][pl_x] == 2:
        if pl_lv >= 10:
            alist = emy_list1[10]
        else:
            alist = emy_list1[pl_lv]
    elif now_map[pl_y][pl_x] == 10:
        if pl_lv <= 11:
            alist = emy_list2[11]
        elif pl_lv <= 19:
            alist = emy_list2[pl_lv]
        else:
            alist = emy_list2[20]
    elif (
        now_map[pl_y][pl_x] == 4 or now_map[pl_y][pl_x] == 5 or now_map[pl_y][pl_x] == 6
    ):
        if pl_lv <= 21:
            alist = emy_list3[21]
        elif pl_lv <= 29:
            alist = emy_list3[pl_lv]
        else:
            alist = emy_list3[30]
    enemy = random.choice(alist)
    enemy_list = emy_dict[enemy]
    enemy_hp = enemy_list[0]

    pl_hp = pl_st[0]
    pl_mp = pl_st[1]

    tri_x = 50
    tri_y = 450

    clock = pygame.time.Clock()
    alist = []
    for x in pygame.font.get_fonts():
        alist.append(x)
    font = pygame.font.SysFont(alist[28], 40)
    font.set_bold(True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        playerstatus(screen)
        commandpanel(screen)
        if enemy_hp == 0:
            screen.fill(BLACK)
            playerstatus(screen)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            txtlv = font.render("{}を倒した".format(enemy), True, WHITE)
            screen.blit(txtlv, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)

            screen.fill(BLACK)
            playerstatus(screen)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            pl_exp += enemy_list[5]
            pl_gold += enemy_list[6]
            txtlv = font.render(
                "{}ポイントの経験値を獲得".format(enemy_list[5]), True, WHITE
            )
            txtgld = font.render("{}ゴールドを獲得".format(enemy_list[6]), True, WHITE)
            screen.blit(txtlv, [100, 420])
            screen.blit(txtgld, [100, 480])
            pygame.display.update()
            pygame.time.wait(1000)
            if pl_lv != len(pl_lv_dict) and pl_exp >= pl_lv_dict[pl_lv + 1]:
                pl_lv += 1
                pl_st = pl_st_dict[pl_lv]
                screen.fill(BLACK)
                playerstatus(screen)
                pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
                txtlv = font.render("{}のレベルが上がった".format(pl_name), True, WHITE)
                screen.blit(txtlv, [100, 420])
                pygame.display.update()
                pygame.time.wait(1000)
            return
        if pl_hp == 0:
            screen.fill(BLACK)
            playerstatus(screen)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            txtdie = font.render("死んでしまうとは情けない", True, WHITE)
            screen.blit(txtdie, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)
            now_map = map_data1
            pl_x = 12
            pl_y = 9
            return

        pygame.draw.polygon(
            screen,
            WHITE,
            [
                [15 + tri_x, 15 + tri_y],
                [15 + tri_x, 45 + tri_y],
                [45 + tri_x, 30 + tri_y],
            ],
        )
        key = pygame.key.get_pressed()
        command(screen, key)

        pygame.display.update()
        clock.tick(30)


def boss_encount(screen):
    global pl_lv, tri_x, tri_y, enemy, enemy_list, enemy_hp, pl_hp, pl_mp, pl_exp, pl_gold, pl_st, font, pl_x, pl_y, now_map, pl_buki
    enemy = "ドラゴン"
    enemy_list = emy_dict[enemy]
    enemy_hp = enemy_list[0]

    pl_hp = pl_st[0]
    pl_mp = pl_st[1]

    tri_x = 50
    tri_y = 450

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        playerstatus(screen)
        commandpanel(screen)
        if enemy_hp == 0:
            screen.fill(BLACK)
            playerstatus(screen)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            txtlv = font.render("{}を倒した".format(enemy), True, WHITE)
            screen.blit(txtlv, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)

            screen.fill(BLACK)
            playerstatus(screen)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            pl_exp += enemy_list[5]
            pl_gold += enemy_list[6]
            txtlv = font.render("ゲームクリア".format(enemy_list[5]), True, WHITE)
            screen.blit(txtlv, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)
            pl_buki = "ロトのつるぎ"
            if pl_lv != len(pl_lv_dict) and pl_exp >= pl_lv_dict[pl_lv + 1]:
                pl_lv += 1
            now_map = map_data1
            pl_x = 12
            pl_y = 9
            return
        if pl_hp == 0:
            screen.fill(BLACK)
            playerstatus(screen)
            pygame.draw.rect(screen, WHITE, [100, 420, 700, 240], width=1)
            txtdie = font.render("死んでしまうとは情けない", True, WHITE)
            screen.blit(txtdie, [100, 420])
            pygame.display.update()
            pygame.time.wait(1000)
            now_map = map_data1
            pl_x = 12
            pl_y = 9
            return

        pygame.draw.polygon(
            screen,
            WHITE,
            [
                [15 + tri_x, 15 + tri_y],
                [15 + tri_x, 45 + tri_y],
                [45 + tri_x, 30 + tri_y],
            ],
        )
        key = pygame.key.get_pressed()
        command(screen, key)

        pygame.display.update()
        clock.tick(30)


def main():
    global pl_attack, font
    pygame.init()
    pygame.display.set_caption("RPG")
    screen = pygame.display.set_mode((1008, 720))
    clock = pygame.time.Clock()
    alist = []
    for x in pygame.font.get_fonts():
        alist.append(x)
    font = pygame.font.SysFont(alist[28], 40)
    font.set_bold(True)

    load(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        key = pygame.key.get_pressed()
        pl_attack = pl_st[2] + buki_dict[pl_buki][0]
        make_map(screen)
        move_map(screen, key)
        screen.blit(img_pl, [480, 336])

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
