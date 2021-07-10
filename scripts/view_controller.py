from scripts.pathfind import manhattan_distance
from browser import document, bind
from scripts import Node, a_star


def paint_node(ev):
    current_target = ev.currentTarget
    current_target['class'] = 'node'
    current_target.classList.add(current_class)
    update_critical_nodes(current_target)
    print("Start node: " + str(start_node) + "\nEnd node: " + str(end_node) + '\n')


# TODO: this is so ugly
def update_critical_nodes(current_target):
    global start_node
    global end_node
    aux = None
    if current_class is 'start-node':
        aux = start_node
        start_node = current_target
        if start_node is end_node:
            end_node = None
    elif current_class is 'end-node':
        aux = end_node
        end_node = current_target
        if end_node is start_node:
            start_node = None
    elif current_class is 'node' or current_class is 'wall-node':
        if current_target is start_node:
            start_node = None
        elif current_target is end_node:
            end_node = None

    if aux is not None and aux is not current_target:
        aux['class'] = 'node'


def set_dimentions(rows, columns):
    pathfind_map.style.setProperty('--grid-rows', rows)
    pathfind_map.style.setProperty('--grid-columns', columns)


def initiate_grid(rows, columns):
    set_dimentions(rows, columns)
    for _ in range(rows * columns):
        cell = document.createElement('div')
        cell['class'] = 'node'
        # cell.style.backgroundColor = '#fff'
        pathfind_map <= cell


def bind_event(elems, on_event, f):
    for elem in elems:
        elem.bind(on_event, f)


@bind(document['start-button'], 'click')
@bind(document['wall-button'], 'click')
@bind(document['end-button'], 'click')
@bind(document['restore-button'], 'click')
def add_class_colored(ev):
    global current_class
    id = ev.currentTarget.id
    if id is 'start-button':
        current_class = 'start-node'
    elif id is 'wall-button':
        current_class = 'wall-node'
    elif id is 'end-button':
        current_class = 'end-node'
    elif id is 'restore-button':
        current_class = 'node'


@bind(document, 'keydown')
def start_pathfind(ev):
    space_bar = 32
    if ev.keyCode is space_bar:
        try:
            map = get_map()
            print(map)
            map_of_nodes = generate_map_of_nodes()
            start = get_node(map, start_node) # start_node is an html element
            end = get_node(map, end_node) # end_node is an html element
            walls = get_wall_nodes(map)

            map_of_costs = set_costs(map_of_nodes, start, end, ROWS, COLUMNS)

            set_node_costs(start, map_of_costs)
            set_node_costs(end, map_of_costs)

            # print_list([start])
            # print_list([end])
            # print_list(walls)
            # print(start.g_cost, start.h_cost)
            # print(end.g_cost, end.h_cost)

            result = a_star(map_of_costs, map, walls, start, end, ROWS, COLUMNS)
            print(result)

            # document.unbind("keydown"): might be good to cancel out various executions of this algorithm while solving
        except NameError:
            pass
        # TODO: except UndefinedCriticalNodes:
    ev.preventDefault()


def set_node_costs(node, map_of_costs):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if node.x == map_of_costs[i][j].x and node.y == map_of_costs[i][j].y:
                node.g_cost = map_of_costs[i][j].g_cost
                node.h_cost = map_of_costs[i][j].h_cost


def set_costs(map_of_nodes_, start_node_, end_node_, rows, columns):
    row = []
    for x in range(columns):
        column = []
        for y in range(rows):
            distance_to_start = manhattan_distance(map_of_nodes_[x][y], start_node_)
            distance_to_end = manhattan_distance(map_of_nodes_[x][y], end_node_)
            column.append(Node(x, y, distance_to_start, distance_to_end))
        row.append(column)
    return row


def print_list(set_):
    for i in set_:
        print(f"({i.x}, {i.y})", end=" ")
    print()


def get_node(a_map_, target):
    for j in range(ROWS):
        for i in range(COLUMNS):
            candidate = a_map_[i][j]
            if target is candidate:
                return Node(i, j, 0, 0)
    return None


def get_wall_nodes(map):
    walls = []
    for i in range(ROWS):
        for j in range(ROWS):
            if 'wall-node' in map[i][j].classList:
                walls.append(Node(i, j, 0, 0))
                # walls.append(f"({x}, {y})")
    return walls


def generate_map_of_nodes():
    rows = []
    for x in range(COLUMNS):
        column = []
        for y in range(ROWS):
            column.append(Node(x, y, 0, 0))
        rows.append(column)
    return rows


def get_map():
    k = 0
    rows = []
    for x in range(COLUMNS):
        column = []
        for y in range(ROWS):
            column.append(nodes[k])
            k += 1
        rows.append(column)
    return rows


if __name__ == '__main__':
    pathfind_map = document['pathfinding-map']

    start_node = None
    end_node = None

    ROWS = 10
    COLUMNS = 10

    initiate_grid(ROWS, COLUMNS)

    nodes = document.select('.node')

    current_class = 'node'

    bind_event(nodes, 'click', paint_node)
