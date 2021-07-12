from browser import document, bind
from scripts import Node, AStar


def paint_node(ev):
    global _current_class
    current_target = ev.currentTarget
    current_target['class'] = 'node'
    current_target.classList.add(_current_class)
    update_critical_nodes(current_target)


# TODO: this is so ugly
def update_critical_nodes(current_target):
    global _current_class
    global start_html_node
    global end_html_node
    aux = None
    if _current_class is 'start-node':
        aux = start_html_node
        start_html_node = current_target
        if start_html_node is end_html_node:
            end_html_node = None
    elif _current_class is 'end-node':
        aux = end_html_node
        end_html_node = current_target
        if end_html_node is start_html_node:
            start_html_node = None
    elif _current_class is 'node' or _current_class is 'wall-node':
        if current_target is start_html_node:
            start_html_node = None
        elif current_target is end_html_node:
            end_html_node = None

    if aux is not None and aux is not current_target:
        aux['class'] = 'node'


def set_dimentions(rows, columns):
    global pathfind_map
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
def add_colored_class(ev):
    global _current_class
    id = ev.currentTarget.id
    if id is 'start-button':
        _current_class = 'start-node'
    elif id is 'wall-button':
        _current_class = 'wall-node'
    elif id is 'end-button':
        _current_class = 'end-node'
    elif id is 'restore-button':
        _current_class = 'node'


@bind(document, 'keydown')
def start_pathfind(ev):
    global html_nodes
    global start_html_node
    global end_html_node
    global ROWS
    global COLUMNS
    space_bar = 32
    if ev.keyCode is space_bar:
        try:
            map_html_nodes = get_matrix_from_list(html_nodes)
            nodes = generate_map_of_nodes()
            start_node = get_node(map_html_nodes, start_html_node)
            end_node = get_node(map_html_nodes, end_html_node)
            walls = get_wall_nodes(map_html_nodes)

            map_of_costs = set_costs(nodes, start_node, end_node)

            set_node_costs(start_node, map_of_costs)
            set_node_costs(end_node, map_of_costs)

            path = AStar().find_path(map_of_costs, map_html_nodes, walls, start_node, end_node, ROWS, COLUMNS)
            paint_path(path, start_node, end_node)

            # TODO: document.unbind("keydown")
        except NameError:
            pass
        # TODO: except UndefinedCriticalNodes:
    ev.preventDefault()


def paint_path(path, start_node, end_node):
    global html_nodes
    matrix = get_matrix_from_list(html_nodes)
    for node in path:
        if not AStar().is_same_position(node, start_node) and not AStar().is_same_position(node, end_node):
            matrix[node.x][node.y].style.backgroundColor = '#d4af37'


def set_node_costs(node, map_of_costs):
    global ROWS
    global COLUMNS
    for i in range(ROWS):
        for j in range(COLUMNS):
            if node.x == map_of_costs[i][j].x and node.y == map_of_costs[i][j].y:
                node.g_cost = map_of_costs[i][j].g_cost
                node.h_cost = map_of_costs[i][j].h_cost


def set_costs(map_of_nodes, start_node, end_node):
    global ROWS
    global COLUMNS
    row = []
    for x in range(ROWS):
        column = []
        for y in range(COLUMNS):
            distance_to_start = AStar().manhattan_distance(map_of_nodes[x][y], start_node)
            distance_to_end = AStar().manhattan_distance(map_of_nodes[x][y], end_node)
            column.append(Node(x, y, distance_to_start, distance_to_end))
        row.append(column)
    return row


def get_node(map_of_nodes, target):
    global ROWS
    global COLUMNS
    for j in range(ROWS):
        for i in range(COLUMNS):
            candidate = map_of_nodes[i][j]
            if target is candidate:
                return Node(i, j, 0, 0)
    return None


def get_wall_nodes(map_):
    global ROWS
    global COLUMNS
    walls = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if 'wall-node' in map_[i][j].classList:
                walls.append(Node(i, j, 0, 0))
    return walls


def generate_map_of_nodes():
    global ROWS
    global COLUMNS
    rows = []
    for x in range(ROWS):
        column = []
        for y in range(COLUMNS):
            column.append(Node(x, y, 0, 0))
        rows.append(column)
    return rows


def get_matrix_from_list(list_):
    global ROWS
    global COLUMNS
    i = 0
    rows = []
    for _ in range(ROWS):
        column = []
        for _ in range(COLUMNS):
            column.append(list_[i])
            i += 1
        rows.append(column)
    return rows


if __name__ == '__main__':
    pathfind_map = document['pathfinding-map']
    start_html_node = None
    end_html_node = None
    ROWS = 30
    COLUMNS = 30

    initiate_grid(ROWS, COLUMNS)

    _current_class = 'node'
    html_nodes = document.select('.node')

    bind_event(html_nodes, 'click', paint_node)
