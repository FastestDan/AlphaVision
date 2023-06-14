# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Engine.CoreModule as cm
import curses
import time


class GameCanvas:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.distances = dm.Matrix(n, m)  # Matrix n*m {[float]}
        self.out = None

    def draw(self, screen, key):
        pass


    def update(self, camera, entities):
        rays = camera.get_rays_matrix(self.n, self.m)

        for i in range(0, self.n):
            for j in range(0, self.m):
                res = []
                for entity in entities:
                    res.append(entity.intersection_distance(rays[i][j]))
                res = [x for x in res if x > 0]
                if len(res) == 0:
                    res = 0
                else:
                    res = min(res)
                self.distances[i][j] = res


class GameConsole(GameCanvas):
    charmap = "MNBQWRPAw9876543210fghjkqertyzxcv;:-----------------                           "

    def __init__(self, n, m):
        super().__init__(n, m)

    def update(self, camera, entities):
        dd = camera.get_property("drawdist")
        rays = camera.get_rays_matrix(self.n, self.m)

        for i in range(0, self.n):
            for j in range(0, self.m):
                temp = list()
                for elem in entities:
                    temp.append(elem.intersection_distance(rays[j][i]))
                temp = [x for x in temp if x > 0]
                if len(temp) == 0:
                    temp = 0
                else:
                    temp = min(temp)
                self.distances.floatlist[i][j] = temp


        dchar = dd / len(GameConsole.charmap)
        step = [dchar * i for i in range(len(GameConsole.charmap))]

        mat = self.distances
        out = dm.Matrix(self.n, self.m)

        for i in range(0, self.n):
            for j in range(0, self.m):
                for k in range(0, len(GameConsole.charmap)):
                    if mat.floatlist[i][j] == 0 or mat.floatlist[i][j] > dd:
                        out.floatlist[i][j] = '-'
                        break
                    if mat.floatlist[i][j] < step[k]:
                        out.floatlist[i][j] = GameConsole.charmap[k]
                        break

        self.out = out

    def draw(self, screen, key=None):
        dims = [self.n, self.m]
        start = ["           _       _        __      ___     _             ",
                 "     /\   | |     | |       \ \    / (_)   (_)            ",
                 "    /  \  | |_ __ | |__   __ \ \  / / _ ___ _  ___  _ __  ",
                 "   / /\ \ | | '_ \| '_ \ / _` \ \/ / | / __| |/ _ \| '_ \ ",
                 "  / ____ \| | |_) | | | | (_| |\  /  | \__ \ | (_) | | | |",
                 " /_/    \_\_| .__/|_| |_|\__,_| \/   |_|___/_|\___/|_| |_|",
                 "            | |                                           ",
                 "            |_|                                           "]
        if key == "0":

            j = -3

            for i in range(0, len(start)):
                screen.addstr((dims[0] // 2 + j), dims[1] // 2 - 29, start[i], curses.color_pair(2))
                screen.refresh()
                time.sleep(0.25)
                j += 1
            screen.clear()
            j = -3
            for i in range(0, len(start)):
                screen.addstr((dims[0] // 2 + j), dims[1] // 2 - 29, start[i], curses.color_pair(1))
                j += 1
            screen.refresh()
            # time.sleep(0.5)
            screen.clear()
        elif key == '-1':
            screen.addstr(dims[0] // 2, dims[1] // 2, "See you later!", curses.color_pair(1))
            screen.addstr(dims[0] // 2 + 1, dims[1] // 2, "Shutting down...", curses.color_pair(1))
            # screen.border(5, 5, 6, 6, 1, 2, 3, 4)
            screen.refresh()
            screen.getch()
            z = 0
            j = -3
            while z != len(start):
                screen.clear()
                for i in range(0, len(start) - z):
                    screen.addstr(dims[0] // 2 + j, dims[1] // 2 - 29, start[i],
                                         curses.color_pair(1))
                    screen.refresh()
                    j += 1
                z += 1
                j = -3
                time.sleep(0.10)
            curses.endwin()
        elif key is None:
            for j in range(1, self.n-1):
                for k in range(1, self.m-1):
                    screen.addstr(j, k, self.out.floatlist[j][k])
            # screen.border(5, 5, 6, 6, 1, 2, 3, 4)
            screen.refresh()

        else:
            screen.addstr(dims[0] - 4, dims[1] - 30, key, curses.color_pair(1))
            # screen.border(5, 5, 6, 6, 1, 2, 3, 4)
            screen.refresh()
