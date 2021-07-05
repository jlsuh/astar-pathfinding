class Node:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._f_cost = 0
        self._g_cost = 0
        self._h_cost = 0
        self._parent = None
