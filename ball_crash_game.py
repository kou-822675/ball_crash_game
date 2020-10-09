# ブロック崩しゲーム
from tkinter import *
import random

# 変数まとめ
blocks = []
block_size = {"x": 75, "y": 30}
ball = {"dir_x": 15, "dir_y": -15, "x": 350, "y": 300, "w": 10}
bar = {"x": 0, "w": 100}
game_over = False
point = 0

# ウィンドウの作成
win = Tk()
cv = Canvas(win, width=600, height=400)
cv.pack()


# 初期化
def init_game():
    global game_over, point
    game_over = False
    ball["y"] = 250
    ball["dir_y"] = -10
    point = 0
    # ブロックの配置
    for n in range(0, 5):
        for i in range(0, 8):
            color = "red"
            if (n + i) % 2 == 1:
                color = "blue"
            x1 = 4 + i * block_size["x"]
            x2 = x1 + block_size["x"]
            y1 = 4 + n * block_size["y"]
            y2 = y1 + block_size["y"]
            blocks.append([x1, y1, x2, y2, color])
    win.title("Start")


# モノの配置
def draw_objects():
    cv.delete("all")
    cv.create_rectangle(0, 0, 600, 400, fill="black", width=0)
    # ブロック
    for w in blocks:
        x1, y1, x2, y2, c = w
        cv.create_rectangle(x1, y1, x2, y2, fill=c, width=0)
    # ボール
    cv.create_oval(ball["x"] - ball["w"], ball["y"] - ball["w"],
                   ball["x"] + ball["w"], ball["y"] + ball["w"], fill="green")
    # バー
    cv.create_rectangle(bar["x"], 390, bar["x"] + bar["w"],
                        400, fill="yellow")


# ボールの移動
def move_ball():
    global game_over, point
    if game_over:
        return
    xx = ball["x"] + ball["dir_x"]
    yy = ball["y"] + ball["dir_y"]
    # 上下左右の最大に衝突
    if xx < 0 or xx > 600:
        ball["dir_x"] *= -1
    if yy < 0:
        ball["dir_y"] *= -1
    # バーに衝突
    if yy > 390 and (bar["x"] <= xx <= (bar["x"] + bar["w"])):
        ball["dir_y"] *= -1
        if random.randint(0, 1) == 0:
            ball["dir_x"] *= -1
        yy = 380
    # ブロックに衝突
    hit_i = -1
    for i, w, in enumerate(blocks):
        x1, y1, x2, y2, color = w
        w3 = ball["w"] / 3
        if (x1 - w3 <= xx <= x2 + w3) and (y1 - w3 <= yy <= y2 + w3):
            hit_i = i
            break
    if hit_i >= 0:
        del blocks[hit_i]
        if random.randint(0, 1) == 0:
            ball["dir_x"] += -1
        ball["dir_y"] *= -1
        point += 10
        win.title("Score = " + str(point))
    # ゲームオーバー
    if yy >= 400:
        win.title("Game over. score = " + str(point))
        game_over = True
    if 0 <= xx <= 600:
        ball["x"] = xx
    if 0 <= yy <= 400:
        ball["y"] = yy


# ループ
def game_loop():
    draw_objects()
    move_ball()
    win.after(50, game_loop)


# マウスの移動処理
def motion(e):
    bar["x"] = e.x


# クリックでリスタート
def click(e):
    if game_over:
        init_game()


# マウス処理まとめ
win.bind("<Motion>", motion)
win.bind("<Button-1>", click)

# メイン処理
init_game()
game_loop()
win.mainloop()
