class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None
