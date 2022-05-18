import pygame
import pygame.gfxdraw
import sys
# import threading

# 棋盘大小
size = 760
# 棋盘留白
margin = 40
# 棋子半径
csize = 16
# 棋盘线间隔
interval = 38


class Go():
    def __init__(self):
        sys.setrecursionlimit(361 * 361)
        # threading.stack_size(1073741824)
        pygame.init()
        # 棋子列表
        self.__chesses = {}
        # 最后落子
        self.__later = -1
        # 当前步数
        self.__steps = 0
        # 打劫
        self.__ko = ""
        self.__font = pygame.font.Font("./static/font/MICROSS.TTF", 14)

    def run(self):
        screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption("Go")
        background = pygame.image.load("./static/img/bg.jpg")
        while True:
            screen.blit(background, (0, 0))
            self.chessboard(screen)
            self.getChesses(screen)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                elif e.type == pygame.MOUSEMOTION:
                    self.chessMove(screen)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.chessMove(screen, True)

            self.chessMove(screen)
            pygame.display.flip()

    def chessboard(self, screen):
        color = (0, 0, 0)
        width = interval * 19
        for i in range(19):
            x = i * interval + margin
            # 网格线
            pygame.draw.line(screen, color, (x, margin), (x, width + 1), 1)
            pygame.draw.line(screen, color, (margin, x), (width + 1, x), 1)
            # 棋盘坐标
            text = self.__font.render(str(i + 1), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (margin / 2, i * interval + margin)
            screen.blit(text, textRect)
            text = self.__font.render(chr(i + 65), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (i * interval + margin, margin / 2)
            screen.blit(text, textRect)
        # 添加星位点
        for x in [4, 10, 16]:
            piont_x = x * interval
            for y in [4, 10, 16]:
                # 圆滑星位点
                pygame.gfxdraw.aacircle(
                    screen, piont_x + 2, y * interval + 2, 4, color)
                pygame.gfxdraw.aacircle(
                    screen, piont_x + 2, y * interval + 2, 3, color)
                pygame.draw.circle(
                    screen, color, (piont_x + 2, y * interval + 2), 4)

    def getPosition(self):
        p = pygame.mouse.get_pos()
        x = p[0] - margin
        y = p[1] - margin
        x = round(x / interval) * interval + margin
        y = round(y / interval) * interval + margin
        return (x, y)

    def getPos(self):
        p = self.getPosition()
        return (
            int((p[0] - margin) / interval + 1),
            int((p[1] - margin) / interval + 1)
        )

    def getKey(self, p):
        return self.makeKey((
            int((p[0] - margin) / interval + 1),
            int((p[1] - margin) / interval + 1)
        ))

    def makeKey(self, p):
        return ",".join((
            str(p[0]),
            str(p[1])
        ))

    def chessMove(self, screen, down=False):
        p = self.getPosition()
        bottom = size - margin + 6
        bg = (255, 255, 255) if self.__later == -1 else (0, 0, 0)
        color = (0, 0, 0) if self.__later == -1 else (255, 255, 255)

        if p[0] >= margin and p[1] >= margin and p[0] <= bottom and p[1] <= bottom:
            if down:
                return self.chessDown(p)
            key = self.getKey(p)
            if key in self.__chesses:
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

    def chessDown(self, p):
        key = self.getKey(p)
        if key in self.__chesses:
            return
        # 打劫判断
        if key == self.__ko:
            return
        else:
            self.__ko = ""

        self.__later *= -1
        self.__steps += 1
        self.__chesses[key] = [p, self.__later, self.__steps]
        liberties = self.getLiberties(key, self.__later)
        remove = self.removeFromBoard(self.__later, {})
        if liberties == 0 and not remove:
            self.__later *= -1
            self.__steps -= 1
            del(self.__chesses[key])
            return

    # 获取已落子棋子并渲染

    def getChesses(self, screen):
        for item in self.__chesses.values():
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
        color_rect = pygame.Surface((2, 2))
        pygame.draw.line(color_rect, left_color,  (0, 0), (0, 1))
        pygame.draw.line(color_rect, right_color, (1, 0), (1, 1))

        color_rect = pygame.transform.rotozoom(color_rect, 330, 2)
        screen.blit(color_rect, target_rect)

    def getLiberties(self, key, chess):
        result = self.setLiberties(self.getPos(), chess, {}, {})
        liberties = len(result[1])
        if liberties == 1 and key in result[1]:
            return 0
        return liberties

    """
    数气
    Args:
        key: 落子坐标
        chess: 落子（黑子/白子）
        chess_checked: 落子已计算气数
        territory_checked: 空已计算气数
    """

    def setLiberties(self, p, chess, chess_checked={}, territory_checked={}):
        key = self.makeKey(p)
        chess_checked[key] = 1
        for mx in [p[0] - 1, p[0] + 1]:
            if mx < 1 or mx > 19:
                continue
            k = self.makeKey((mx, p[1]))
            # 该坐标无子且未算气
            if k not in self.__chesses and k not in territory_checked:
                territory_checked[k] = 1
            elif k in self.__chesses:
                # 坐标有同色子且此子未算气
                if self.__chesses[k][1] == chess and k not in chess_checked:
                    result = self.setLiberties(
                        (mx, p[1]), chess, chess_checked, territory_checked
                    )
                    chess_checked = {**chess_checked, **result[0]}
                    territory_checked = {**territory_checked, **result[1]}

        for my in [p[1] - 1, p[1] + 1]:
            if my < 1 or my > 19:
                continue
            k = self.makeKey((p[0], my))
            # 该坐标无子且未算气
            if k not in self.__chesses and k not in territory_checked:
                territory_checked[k] = 1
            elif k in self.__chesses:
                # 坐标有同色子且此子未算气
                if self.__chesses[k][1] == chess and k not in chess_checked:
                    result = self.setLiberties(
                        (p[0], my), chess, chess_checked, territory_checked
                    )
                    chess_checked = {**chess_checked, **result[0]}
                    territory_checked = {**territory_checked, **result[1]}

        return (chess_checked, territory_checked)

    def removeFromBoard(self, chess, chess_checked={}):
        p = self.getPos()
        waitRemove = {}
        key = self.makeKey(p)
        chess_checked[key] = 1
        for mx in [p[0] - 1, p[0] + 1]:
            if mx < 1 or mx > 19:
                continue
            k = self.makeKey((mx, p[1]))
            if k in self.__chesses and k not in chess_checked:
                if self.__chesses[k][1] != chess:
                    result = self.getDeadStone(
                        (mx, p[1]), self.__chesses[k][1]
                    )
                    if self.isRemove(p, result):
                        waitRemove = {**waitRemove, **result[0]}

        for my in [p[1] - 1, p[1] + 1]:
            if my < 1 or my > 19:
                continue
            k = self.makeKey((p[0], my))
            if k in self.__chesses and k not in chess_checked:
                if self.__chesses[k][1] != chess:
                    result = self.getDeadStone(
                        (p[0], my), self.__chesses[k][1]
                    )
                    if self.isRemove(p, result):
                        waitRemove = {**waitRemove, **result[0]}
        for k in waitRemove:
            del(self.__chesses[k])
        dead = len(waitRemove)
        if dead == 1:
            self.__ko = list(waitRemove.keys())[0]
        return True if dead > 0 else False

    def getDeadStone(self, p, chess):
        result = self.setLiberties(p, chess, {}, {})
        return result

    def isRemove(self, p, result):
        if len(result[0]) > 0:
            # k = self.makeKey(p)
            if len(result[1]) == 0:
                return True
        return False


go = Go()
go.run()
