import os
import sys
import pygame as pg
import random
import time
import math

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面外か判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT <rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面

    引数：画面Surface
    戻り値：なし
    """
    # 黒背景
    black = pg.Surface(screen.get_size())
    black.fill((0, 0, 0))
    black.set_alpha(200)

    if black.get_alpha() is None:
        black.set_alpha(200)

    # フォント
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = screen.get_rect().center

    # こうかとん画像（左）
    kk_img_left = pg.image.load("fig/8.png")
    kk_rct_left = kk_img_left.get_rect()

    # こうかとん画像（右）
    kk_img_right = pg.image.load("fig/8.png")
    kk_rct_right = kk_img_right.get_rect()

    # 配置（文字の左右）
    kk_rct_left.center = (text_rect.left - 100, text_rect.centery)
    kk_rct_right.center = (text_rect.right + 100, text_rect.centery)

    # 描画
    screen.blit(black, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(kk_img_left, kk_rct_left)
    screen.blit(kk_img_right, kk_rct_right)

    pg.display.update()
    time.sleep(5)

def calc_orientation(
    org: pg.Rect,
    dst: pg.Rect,
    current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    爆弾からこうかとんへの方向ベクトルを計算する

    引数：
        org: 爆弾Rect
        dst: こうかとんRect
        current_xy: 現在の速度ベクトル

    戻り値：
        正規化された方向ベクトル
    """
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery

    dist = math.sqrt(dx**2 + dy**2)

    # 近すぎるときはそのまま
    if dist < 300:
        return current_xy

    # 正規化（長さ√50 ≒ 7.07）
    if dist != 0:
        dx = dx / dist * 7
        dy = dy / dist * 7

    return dx, dy

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  
    bb_img.set_colorkey((0, 0, 0))  
    bb_rct = bb_img.get_rect()  
    bb_rct.centerx = random.randint(0, WIDTH)  
    bb_rct.centery = random.randint(0, HEIGHT)  
    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            return
        screen.blit(bg_img, [0, 0])

        DELTA = {
            pg.K_UP: (0 , -5), 
            pg.K_DOWN: (0 , +5),  
            pg.K_LEFT: (-5, 0), 
            pg.K_RIGHT: (+5, 0),  
        }

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  
        yoko, tate = check_bound( bb_rct)
        if not yoko:
            vx *=-1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        bb_rct.move_ip(vx, vy)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

