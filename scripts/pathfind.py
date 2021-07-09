from scripts import Node
from browser import timer


def a_star(map_of_nodes, wall_nodes, start_node, end_node, rows, columns):
    open = []
    open.append(start_node)
    closed = set()
    set_costs(map_of_nodes, start_node, end_node, rows, columns)
    print_costs(map_of_nodes, rows, columns)
    while len(open) > 0:
        lowest_f_node = get_node_with_lowest_f_cost(open)
        print_after(lowest_f_node)
        if lowest_f_node is end_node:
            return "End node found"
        open.remove(lowest_f_node)
        closed.add(lowest_f_node)
        for node in possible_nodes_from(lowest_f_node, wall_nodes, rows, columns):
            print_after(node)
            if node in closed:
                continue
            if node not in open:
                open.append(node)
            else:
                current_node = open.pop(open.index(node))
                print_after(current_node)
                if node.g_cost < current_node.g_cost:
                    current_node.g_cost = node.g_cost
                    current_node.f_cost = node.f_cost
                    current_node.parent = node.parent
                open.append(current_node)
                print_after(current_node)
    return "No path found"


def print_after(node):
    timer.set_timeout(print_node(node), 2000)


def print_node(node):
    print(f"Current node: g: {node.g_cost} | h: {node.h_cost} | f: {node.f_cost} | ({node.x}, {node.y})")


def print_costs(map_of_nodes, rows, columns):
    for i in range(rows):
        for j in range(columns):
            node = map_of_nodes[i][j]
            print(f"g: {node.g_cost} | h: {node.h_cost} | f: {node.f_cost} | ({node.x}, {node.y})")


def find_element(list, target):
    for i in list:
        if target is list[i]:
            return list[i]


def possible_nodes_from(pivot, wall_nodes, rows, columns):
    possible_nodes = []
    if pivot.x - 1 >= 0 and pivot not in wall_nodes:
        possible_nodes.append(Node(pivot.x - 1, pivot.y))
    if pivot.y - 1 >= 0 and pivot not in wall_nodes:
        possible_nodes.append(Node(pivot.x, pivot.y - 1))
    if pivot.x + 1 < columns and pivot not in wall_nodes:
        possible_nodes.append(Node(pivot.x + 1, pivot.y))
    if pivot.y + 1 < rows and pivot not in wall_nodes:
        possible_nodes.append(Node(pivot.x, pivot.y + 1))
    return possible_nodes


def get_node_with_lowest_f_cost(list):
    sorted_list = sorted(list, key = lambda x: x.f_cost)
    return sorted_list[0]


def set_costs(map_of_nodes, start_node, end_node, rows, columns):
    for i in range(columns):
        for j in range(rows):
            distance_to_start = manhattan_distance(map_of_nodes[i][j], start_node)
            distance_to_end = manhattan_distance(map_of_nodes[i][j], end_node)
            map_of_nodes[i][j].g_cost = distance_to_start
            map_of_nodes[i][j].h_cost = distance_to_end
            map_of_nodes[i][j].f_cost = distance_to_start + distance_to_end


def manhattan_distance(start, goal):
    return abs(start.x - goal.x) + abs(start.y - goal.y)
