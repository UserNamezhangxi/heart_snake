import pygame as pg
import random
import time
from tkinter import messagebox

W = 1080
H = 720

ROW = 72

COL = 108

pg.init()
pg.mixer.init()

eat_sound = pg.mixer.Sound("eat.mp3")

SCREE0N_SIZE = (W, H)
screen = pg.display.set_mode(SCREE0N_SIZE)

snake_color = (250, 250, 250)
food_color = (250, 0, 0)
bg_clor = (0, 0, 0)

img_point = pg.image.load("point.png")  # 10*10 像素
img_apple = pg.image.load("apple.png")  # 10*10 像素


img_point_rect = img_point.get_rect()
img_apple_rect = img_apple.get_rect()


def show_dialog():
    result = messagebox.askyesno("游戏结束", "是否继续游戏?")
    if result:
        # 用户选择继续游戏，这里可以添加重新开始游戏的逻辑
        print("重新开始游戏")
        restartplay()

    else:
        # 用户选择退出游戏，这里可以添加退出游戏的逻辑
        print("退出游戏")
        exit(0)


# 一个像素点的定义
class Point:
    row = 0
    col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def copy(self):
        return Point(row=self.row, col=self.col)


# 绘制一个点
def draw_rect(point, color, type):
    cell_width = W / COL
    cell_height = H / ROW

    left = point.col * cell_width
    top = point.row * cell_height

    if type == 0:  # 蛇
        img_point_rect.x = left
        img_point_rect.y = top
        screen.blit(img_point, img_point_rect)
    elif type == 1:  # 食物
        img_apple_rect.x = left
        img_apple_rect.y = top
        screen.blit(img_apple, img_apple_rect)

    # pg.draw.rect(screen, color, (left, top, cell_width, cell_height))


clock = pg.time.Clock()
pg.display.set_caption("贪吃蛇")
head = Point(row=int(ROW / 2), col=int(COL / 2))

SNAKE_DIRECTION = "RIGHT"
is_eat = False

# 初始化蛇的长度
snakes = [
    Point(head.row, head.col),
    Point(head.row, head.col + 1),
    Point(head.row, head.col + 2),
    Point(head.row, head.col + 3),
]


def gen_food():
    random_row = random.randint(0, ROW - 1)
    random_col = random.randint(0, COL - 1)

    return Point(random_row, random_col)


food_point = gen_food()

quit = False


def restartplay():
    global head
    head = Point(row=int(ROW / 2), col=int(COL / 2))
    snakes.clear()
    snakes.append(Point(head.row, head.col))
    snakes.append(Point(head.row, head.col + 1))
    snakes.append(Point(head.row, head.col + 2))
    snakes.append(Point(head.row, head.col + 3))
    start_play()


def start_play():
    global SNAKE_DIRECTION
    SNAKE_DIRECTION = "RIGHT"
    global food_point
    pg.mixer.music.load("bg_music.mp3")
    pg.mixer.music.play(-1)
    while True:
        pg.display.set_caption("得分：" + str(len(snakes) - 4))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if SNAKE_DIRECTION == "RIGHT" or SNAKE_DIRECTION == "LEFT":
                        SNAKE_DIRECTION = "UP"
                elif event.key == pg.K_DOWN:
                    if SNAKE_DIRECTION == "RIGHT" or SNAKE_DIRECTION == "LEFT":
                        SNAKE_DIRECTION = "DOWN"
                elif event.key == pg.K_LEFT:
                    if SNAKE_DIRECTION == "UP" or SNAKE_DIRECTION == "DOWN":
                        SNAKE_DIRECTION = "LEFT"
                elif event.key == pg.K_RIGHT:
                    if SNAKE_DIRECTION == "UP" or SNAKE_DIRECTION == "DOWN":
                        SNAKE_DIRECTION = "RIGHT"

        # 根据用户的方向去更新数据
        if SNAKE_DIRECTION == "LEFT":
            head.col = head.col - 1
        elif SNAKE_DIRECTION == "RIGHT":
            head.col = head.col + 1
        elif SNAKE_DIRECTION == "UP":
            head.row = head.row - 1
        elif SNAKE_DIRECTION == "DOWN":
            head.row = head.row + 1

        # 是否触及四壁死亡
        dead = head.col < 0 or head.col > COL or head.row < 0 or head.row > ROW
        if dead:
            pg.mixer.music.load("gameover.mp3")
            pg.mixer.music.play(1)
            print("game over,socre = " + str(len(snakes) - 4))
            show_dialog()
            time.sleep(3)
            break

        # 绘制窗口
        pg.draw.rect(screen, bg_clor, (0, 0, W, H))

        # 蛇尾部移除
        snakes.pop()
        # 给list 0 位置插入一条数据 这样for循环 蛇就动了
        snakes.insert(0, head.copy())

        # 绘制蛇身体数组
        for snake in snakes:
            draw_rect(snake, snake_color, 0)

        # 蛇头和食物坐标相等的情况下说明是吃了食物
        is_eat = food_point.row == head.row and food_point.col == head.col

        if is_eat:
            eat_sound.play()  # 吃掉食物音效
            food_point = gen_food()  # 吃掉食物，重新生成食物
            snakes.insert(0, head.copy())  # 蛇的长度加一

        draw_rect(food_point, food_color, 1)  # 绘制食物

        pg.display.flip()  # 刷新窗口（很重要！！）
        clock.tick(10)


start_play()
