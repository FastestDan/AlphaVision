# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Engine.CoreModule as cm


class GameCanvas:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.distances = dm.Matrix(n, m)  # Matrix n*m {[float]}

    def draw(self):
        pass

    def update(self, camera):
        pass


# class GameConsole(GameCanvas):
#     charmap = ".:;><+r*zsvfwqkP694VOGbUAKXH8RD#$B0MNWQ%&@"
#
#     def draw(self):
#         pass
