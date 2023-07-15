import pygame as pg

pg.init()
pg.mixer.init()

W = 1080
H = 720
num = 0
SCREE0N_SIZE = (W, H)
screen = pg.display.set_mode(SCREE0N_SIZE)
block_color = (255, 100, 100)
bottom_color = (100, 180, 100)
bg_clor = (0, 0, 0)
bullet_color = (0, 122, 255)

# 定义挡板的宽度和高度
paddle_width, paddle_height = 100, 10
paddle_x = W // 2 - paddle_width // 2
paddle_y = H - paddle_height - 10
paddle_speed = 1


ball_radius = 10
ball_x = W // 2
ball_y = H // 2
ball_speed_x = 0.3
ball_speed_y = 0.3

# 定义砖块的宽度和高度
brick_width, brick_height = 55, 20

# 定义砖块行列数及间隔
num_rows = 4
brick_padding = 5
num_cols = 1080 // (brick_width + brick_padding)

# 创建砖块数组
bricks = []
for row in range(num_rows):
    for col in range(num_cols - row - 5):
        brick_x = col * (brick_width + brick_padding)
        brick_y = row * (brick_height + brick_padding) + 50
        brick_rect = pg.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append(brick_rect)

pg.display.set_caption("打砖头块")

while True:
    # 清空屏幕
    screen.fill(bg_clor)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    # 绘制砖块
    for brick in bricks:
        pg.draw.rect(screen, block_color, brick)

    # 绘制球
    pg.draw.circle(screen, bullet_color, (int(ball_x), int(ball_y)), ball_radius)

    # 绘制挡板
    pg.draw.rect(
        screen, bottom_color, (paddle_x, paddle_y, paddle_width, paddle_height)
    )

    # 更新球的位置
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 更新挡板位置
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pg.K_RIGHT] and paddle_x < W - paddle_width:
        paddle_x += paddle_speed

    # 检测球与砖块的碰撞
    for brick in bricks:
        if brick.colliderect(
            pg.Rect(
                ball_x - ball_radius,
                ball_y - ball_radius,
                ball_radius * 2,
                ball_radius * 2,
            )
        ):
            pg.mixer.music.load("ding.mp3")
            pg.mixer.music.play(1)
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y

    # 检测球与窗口边界的碰撞
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= W:
        ball_speed_x = -ball_speed_x
    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y

    if paddle_x < ball_x - ball_radius < paddle_x + paddle_width:
        if paddle_y - paddle_height <= ball_y - ball_radius:
            num = num + 1
            print(str(num), "接住了")
            pg.mixer.music.load("tan.mp3")
            pg.mixer.music.play(1)
            ball_speed_y = -ball_speed_y

    if ball_y >= H:
        print("Game Over")
        pg.mixer.music.load("gameover.mp3")
        pg.mixer.music.play(1)
        pg.time.delay(3000)
        break

    # 更新窗口
    pg.display.update()
