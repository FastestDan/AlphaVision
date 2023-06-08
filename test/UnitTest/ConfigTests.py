import pytest
from lib.Engine.ConfigurationModule import GameConfiguration


class TestsConfig:
    def test_init(self=None):
        a = GameConfiguration("C:/Python/AlphaVision/config/TEST.txt")

        res = ["SASISKA", "IC003969", "CHAOS EMERALD", "POWERED BY"]

        assert list(a.configuration.keys()) == res

    def test_get_variable(self=None):
        a = GameConfiguration("C:/Python/AlphaVision/config/TEST.txt")
        item = "SASISKA"

        res = "GET"

        assert res == a.get_variable(item)

    def test_set_variable(self=None):
        a = GameConfiguration("C:/Python/AlphaVision/config/TEST.txt")
        item = "SASISKA"
        var = "SOSIK"

        a.set_variable(item, var)

        res = "SOSIK"

        assert a[item] == res

    def test_execute(self=None):
        a = GameConfiguration("C:/Python/AlphaVision/config/TEST.txt")
        item = "SASISKA"
        var = "SOSIK"

        a.set_variable(item, var)
        a.execute_file("C:/Python/AlphaVision/config/TEST.txt")

        res = "GET"

        assert a[item] == res

    def test_save(self=None):
        a = GameConfiguration("C:/Python/AlphaVision/config/TEST.txt")
        a.set_variable("NEW", "NEO")
        a.save("C:/Python/AlphaVision/config/TEST1.txt")

        b = GameConfiguration("C:/Python/AlphaVision/config/TEST1.txt")
        item = "NEW"

        res = "NEO"

        assert b[item] == res

