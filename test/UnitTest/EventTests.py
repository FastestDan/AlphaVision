import pytest
from lib.Engine.EventsModule import EventSystem as es


class TestsEvent:
    def test_init(self=None):
        evdict = dict({"W": [list.append]})
        a = es(evdict)

        res = "W"

        assert list(a.events.keys())[0] == res

    def test_add(self=None):
        evdict = dict({"W": [list.append]})
        a = es(evdict)
        new = "S"
        a.add(new)

        res = list()

        assert res == a.events.get("S")

    def test_remove(self=None):
        evdict = dict({"W": [list.append], "S": []})
        a = es(evdict)
        a.remove("S")

        res = 1

        assert ("S" not in list(a.events.keys())) is True
        assert len(list(a.events.keys())) == res

    def test_handle(self=None):
        evdict = dict({"W": [list.append], "S": []})
        a = es(evdict)
        a.handle("S", list.remove)

        res = [list.remove]

        assert res == a.events.get("S")

    def test_trigger(self=None):
        b = list()
        evdict = dict({"W": [b.append, b.remove, b.append, b.append], "S": []})
        a = es(evdict)
        a.trigger("W", 1)

        res = [1, 1]

        assert res == b

    def test_get_handled(self=None):
        evdict = dict({"W": [list.append], "S": [list.remove]})
        a = es(evdict)
        b = a.get_handled("W")

        res = [list.append]

        assert res == b
