import pygame
import pygame.gfxdraw
import sys

# 棋盘大小
size = 760
# 棋盘留白
margin = 40
# 棋子半径
csize = 16
# 棋盘线间隔
interval = 38
# 棋子列表
chesses = {}


def run():
    pygame.init()
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Go")
    background = pygame.image.load("./static/img/bg.jpg")
    # 最后落子
    later = -1
    while True:
        screen.blit(background, (0, 0))
        chessboard(screen)
        getChesses(screen)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.MOUSEMOTION:
                chessMove(screen, later)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                later = later * -1
                chessMove(screen, later, True)

        chessMove(screen, later)
        pygame.display.flip()


def chessboard(screen):
    color = (0, 0, 0)
    width = interval * 19
    for i in range(19):
        x = i * interval + margin
        pygame.draw.line(screen, color, (x, margin), (x, width + 1), 1)
        pygame.draw.line(screen, color, (margin, x), (width + 1, x), 1)


def chessMove(screen, later, down=False):
    p = getPosition()
    bottom = size - margin + 6
    bg = (255, 255, 255) if later == -1 else (0, 0, 0)
    color = (0, 0, 0) if later == -1 else (255, 255, 255)

    if p[0] >= margin and p[1] >= margin and p[0] <= bottom and p[1] <= bottom:
        if down:
            return chessDown(p, later)
        key = getKey(p)
        if key in chesses:
            return
        screen_chess = pygame.Surface((100, 100))
        screen_chess.set_colorkey(bg)
        screen_chess.set_alpha(128)
        pygame.gfxdraw.aacircle(screen, p[0], p[1], csize, color)
        # aacircle 在右侧有个微小的缺口，画一个像素弥补这个缺口
        pygame.gfxdraw.pixel(screen, p[0] + csize, p[1], color)
        pygame.draw.circle(screen_chess, color, (50, 50), csize)
        # 填补因为锯齿带来的空隙
        pygame.draw.circle(screen_chess, color, (51, 51), csize)
        screen.blit(screen_chess, (p[0] - 50, p[1] - 50))


def chessDown(p, later):
    key = getKey(p)
    if key not in chesses:
        chesses[key] = [p, later]


def getKey(p):
    return ",".join(str(i) for i in p)


def getChesses(screen):

    for item in chesses.values():
        color = (0, 0, 0) if item[1] == 1 else (226, 226, 212)
        pygame.gfxdraw.aacircle(screen, item[0][0], item[0][1], csize, color)
        # 填补因为锯齿带来的空隙
        pygame.gfxdraw.aacircle(
            screen, item[0][0], item[0][1], csize - 1, color
        )
        # aacircle 在右侧有个微小的缺口，画一个像素弥补这个缺口
        pygame.gfxdraw.pixel(screen, item[0][0] + csize, item[0][1], color)
        pygame.draw.circle(screen, color, item[0], csize)

        highlight = ((205, 205, 205), (0, 0, 0)) if item[1] == 1 else (
            (255, 255, 255), (226, 226, 212)
        )
        makeHighlight(
            screen,
            highlight[0],
            highlight[1],
            pygame.Rect(item[0][0] - 11, item[0][1] - 11, 5, 3)
        )


def makeHighlight(screen, left_color, right_color, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_color,  (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_color, (1, 0), (1, 1))

    colour_rect = pygame.transform.rotozoom(colour_rect, 330, 2)
    screen.blit(colour_rect, target_rect)


def getPosition():
    p = pygame.mouse.get_pos()
    x = p[0] - margin
    y = p[1] - margin
    x = round(x / interval) * interval + margin
    y = round(y / interval) * interval + margin
    return (x, y)


run()
