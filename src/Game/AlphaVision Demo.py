# Created by X-Corporation

import lib.Math.DimensionModule as dm
import lib.Engine.CoreModule as cm
import lib.Engine.EventsModule as em
import lib.Engine.ConfigurationModule as config
import lib.Engine.VisualisationModule as vm
import sys
import os
import curses


class Game(cm.Game):
    start = ["           _       _        __      ___     _             ",
             "     /\   | |     | |       \ \    / (_)   (_)            ",
             "    /  \  | |_ __ | |__   __ \ \  / / _ ___ _  ___  _ __  ",
             "   / /\ \ | | '_ \| '_ \ / _` \ \/ / | / __| |/ _ \| '_ \ ",
             "  / ____ \| | |_) | | | | (_| |\  /  | \__ \ | (_) | | | |",
             " /_/    \_\_| .__/|_| |_|\__,_| \/   |_|___/_|\___/|_| |_|",
             "            | |                                           ",
             "            |_|                                           "]

    def __init__(self, cs, entities):
        self.myscreen = curses.initscr()
        curses.start_color()
        self.myscreen.keypad(True)
        curses.noecho()
        self.dims = self.myscreen.getmaxyx()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
        events = em.EventSystem(dict({
            "KeyPress": [self.myscreen.addstr]
        }))
        super().__init__(cs, entities, events)
        self.default_config_check()
        self.config = config.GameConfiguration()
        self.config.set_variable("Screen Width", int(self.dims[1]))
        self.config.set_variable("Screen Height", int(self.dims[0]))
        self.apply_configuration(self.config)
        self.player = self.get_camera_class()(dm.Point([4, 1, 1]), 90, 6, dm.Vector([3, 0, 0]))
        self.el = self.get_hyper_ellipsoid_class()(dm.Point([5, 1, 1]), dm.Vector([3, 2, 1]), [3, 2, 1])

        self.console = vm.GameConsole(self.config.get_variable("Screen Width"), self.config.get_variable("Screen Height"))
        self.vision = self.player.get_rays_matrix(self.dims[0], self.dims[1])
        events.add("Move")
        events.handle("Move", self.player.move)
        events.add("Nod")
        events.handle("Nod", self.player.set_direction)
        events.add("Shake")
        events.handle("Shake", self.player.planar_rotate)


    def run(self):
        self.boot_up_anim()
        self.console.update(self.player, self.entities)
        self.myscreen.clear()
        # curses.endwin()
        # print(self.console.distances.floatlist)
        # a = input()
        self.console.draw(self.myscreen)
        # self.console.draw(self.myscreen, ', '.join(list(map(str, self.player.position.floatlist[0]))))

        while True:
            self.update()

    def update(self):
        key = self.myscreen.getch()
        if key in [ord("z"), ord("я"), ord("Z"), ord('Я')]:
            self.exit()
        elif key in [curses.KEY_UP, ord('w'), ord('ц'), ord("W"), ord("Ц")]:
            go = dm.Vector([1, 0, 0])
            self.es.trigger("Move", go)
        elif key in [curses.KEY_DOWN, ord("s"), ord("ы"), ord("S"), ord("Ы")]:
            go = dm.Vector([-1, 0, 0])
            self.es.trigger("Move", go)
        elif key in [curses.KEY_LEFT, ord("a"), ord("A"), ord("ф"), ord("Ф")]:
            go = dm.Vector([0, 1, 0])
            self.es.trigger("Move", go)
        elif key in [curses.KEY_RIGHT, ord("d"), ord("D"), ord("в"), ord("В")]:
            go = dm.Vector([0, -1, 0])
            self.es.trigger("Move", go)
        elif key == curses.KEY_PPAGE:
            go = dm.Vector([0, 0, 1])
            self.es.trigger("Move", go)
        elif key == curses.KEY_NPAGE:
            go = dm.Vector([0, 0, -1])
            self.es.trigger("Move", go)
        elif key in [ord("i"), ord("I"), ord("ш"), ord("Ш")]:
            go = dm.Vector([0, 0.25, 0])
            self.es.trigger("Nod", self.player.direction - go)
        elif key in [ord("k"), ord("K"), ord("л"), ord("Л")]:
            go = dm.Vector([0, 0.25, 0])
            self.es.trigger("Nod", self.player.direction + go)
        elif key in [ord("J"), ord("j"), ord("о"), ord("О")]:
            go = -25
            self.es.trigger("Shake", [1, 2], go)
        elif key in [ord("l"), ord("L"), ord("д"), ord("Д")]:
            go = 25
            self.es.trigger("Shake", [1, 2], go)
        self.console.update(self.player, self.entities)
        self.console.draw(self.myscreen)
        # self.console.draw(self.myscreen, ', '.join(list(map(str, self.player.position.floatlist[0]))))

    def exit(self):
        self.console.draw(self.myscreen, "-1")
        sys.exit()

    def default_config_check(self):
        par_dir = ""
        cur_dir = os.path.dirname(__file__)
        for i in range(0, 2):
            par_dir = os.path.split(cur_dir)[0]
            cur_dir = par_dir
        try:
            file = open((par_dir + "\config\default.txt"), "r")
            file.close()
        except Exception:
            file = open((par_dir + "\config\default.txt"), "w")
            file.write("Screen Width: 1280\n")
            file.write("Screen Height: 720")
        self.apply_configuration(config.GameConfiguration())

    def boot_up_anim(self):
        self.console.draw(self.myscreen, "0")
        # self.console.draw(self.myscreen, ', '.join(list(map(str, self.player.position.floatlist[0]))))


def main():
    basis = dm.VectorSpace([dm.Vector([1, 0, 0]), dm.Vector([0, 1, 0]), dm.Vector([0, 0, 1])])
    game = Game(dm.CoordinateSystem(dm.Point([0, 0, 0]), basis), cm.EntitiesList([]))
    game.run()


if __name__ == "__main__":
    main()