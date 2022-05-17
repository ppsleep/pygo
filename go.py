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


class Go():
    def __init__(self):
        pygame.init()
        # 当前步数
        self.__steps = 0
        self.__font = pygame.font.Font("./static/font/MICROSS.TTF", 14)

    def run(self):
        screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption("Go")
        background = pygame.image.load("./static/img/bg.jpg")
        # 最后落子
        later = -1
        while True:
            screen.blit(background, (0, 0))
            self.chessboard(screen)
            self.getChesses(screen)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                elif e.type == pygame.MOUSEMOTION:
                    self.chessMove(screen, later)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    later = later * -1
                    self.chessMove(screen, later, True)

            self.chessMove(screen, later)
            pygame.display.flip()

    def chessboard(self, screen):
        color = (0, 0, 0)
        width = interval * 19
        for i in range(19):
            x = i * interval + margin
            pygame.draw.line(screen, color, (x, margin), (x, width + 1), 1)
            pygame.draw.line(screen, color, (margin, x), (width + 1, x), 1)

            text = self.__font.render(str(i + 1), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (margin / 2, i * interval + margin)
            screen.blit(text, textRect)
            text = self.__font.render(chr(i + 65), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (i * interval + margin, margin / 2)
            screen.blit(text, textRect)

    def chessMove(self, screen, later, down=False):
        p = self.getPosition()
        bottom = size - margin + 6
        bg = (255, 255, 255) if later == -1 else (0, 0, 0)
        color = (0, 0, 0) if later == -1 else (255, 255, 255)

        if p[0] >= margin and p[1] >= margin and p[0] <= bottom and p[1] <= bottom:
            if down:
                return self.chessDown(p, later)
            key = self.getKey(p)
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

    def chessDown(self, p, later):
        key = self.getKey(p)
        if key not in chesses:
            self.__steps += 1
            chesses[key] = [p, later, self.__steps]

    def getKey(self, p):
        return ",".join(str(i) for i in p)

    def getChesses(self, screen):
        for item in chesses.values():
            color = (0, 0, 0) if item[1] == 1 else (226, 226, 212)
            pygame.gfxdraw.aacircle(
                screen, item[0][0], item[0][1], csize, color)
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
            self.makeHighlight(
                screen,
                highlight[0],
                highlight[1],
                pygame.Rect(item[0][0] - 11, item[0][1] - 11, 5, 3)
            )
            fcolor = (255, 0, 0) if item[2] == self.__steps else (
                0, 0, 0) if item[2] % 2 == 0 else (255, 255, 255)
            text = self.__font.render(str(item[2]), True, fcolor)
            textRect = text.get_rect()
            textRect.center = item[0]
            screen.blit(text, textRect)

    def makeHighlight(self, screen, left_color, right_color, target_rect):
        colour_rect = pygame.Surface((2, 2))
        pygame.draw.line(colour_rect, left_color,  (0, 0), (0, 1))
        pygame.draw.line(colour_rect, right_color, (1, 0), (1, 1))

        colour_rect = pygame.transform.rotozoom(colour_rect, 330, 2)
        screen.blit(colour_rect, target_rect)

    def getPosition(self):
        p = pygame.mouse.get_pos()
        x = p[0] - margin
        y = p[1] - margin
        x = round(x / interval) * interval + margin
        y = round(y / interval) * interval + margin
        return (x, y)


go = Go()
go.run()
