from browser import document, bind


class Node:

    def __init__(self, x, y, g_cost, h_cost):
        self.x = x
        self.y = y
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.parent = None


class AStar:

    def find_path(self, map_of_costs, html_nodes, wall_nodes, start_node, end_node, rows, columns):
        open_set = set()
        closed_set = set()
        open_set.add(start_node)
        while open_set:
            current = min(open_set, key=lambda n: n.g_cost + n.h_cost)
            if current.x == end_node.x and current.y == end_node.y:
                return self.path(current)
            open_set.remove(current)
            closed_set.add(current)
            self.set_color(html_nodes, current, start_node, end_node, 'closed-node')
            possible_nodes = self.possible_nodes_from(current, wall_nodes, rows, columns, map_of_costs, closed_set)
            for node in possible_nodes:
                if node in closed_set:
                    continue
                if node in open_set:
                    new_g_cost = current.g_cost + 1
                    if node.g_cost > new_g_cost:
                        node.g_cost = new_g_cost
                        node.parent = current
                else:
                    node.g_cost = current.g_cost + 1
                    node.h_cost = self.manhattan_distance(node, end_node)
                    node.parent = current
                    open_set.add(node)
                    self.set_color(html_nodes, node, start_node, end_node, 'open-node')
        raise ValueError("No path found")


    def set_color(self, html_matrix_nodes, current, start, end, node_status):
        if not self.is_same_position(current, start) and not self.is_same_position(current, end):
            html_matrix_nodes[current.x][current.y].classList.add(node_status)


    def path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]


    def is_same_position(self, node1, node2):
        return node1.x == node2.x and node1.y == node2.y


    def is_position_of_any(self, set_, target):
        for node in set_:
            if target.x == node.x and target.y == node.y:
                return True
        return False


    # TODO: There are several ways of improving this
    def possible_nodes_from(self, pivot, wall_nodes_, rows, columns, map_of_nodes_, closed_set):
        possible_nodes = []
        if pivot.x - 1 >= 0:
            node = map_of_nodes_[pivot.x - 1][pivot.y]
            if not self.is_position_of_any(wall_nodes_, node) and not self.is_position_of_any(closed_set, node):
                possible_nodes.append(node)
        if pivot.y - 1 >= 0:
            node = map_of_nodes_[pivot.x][pivot.y - 1]
            if not self.is_position_of_any(wall_nodes_, node) and not self.is_position_of_any(closed_set, node):
                possible_nodes.append(node)
        if pivot.x + 1 < columns:
            node = map_of_nodes_[pivot.x + 1][pivot.y]
            if not self.is_position_of_any(wall_nodes_, node) and not self.is_position_of_any(closed_set, node):
                possible_nodes.append(node)
        if pivot.y + 1 < rows:
            node = map_of_nodes_[pivot.x][pivot.y + 1]
            if not self.is_position_of_any(wall_nodes_, node) and not self.is_position_of_any(closed_set, node):
                possible_nodes.append(node)
        return possible_nodes


    def manhattan_distance(self, start, goal):
        return abs(start.x - goal.x) + abs(start.y - goal.y)


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
    id_ = ev.currentTarget.id
    if id_ is 'start-button':
        _current_class = 'start-node'
    elif id_ is 'wall-button':
        _current_class = 'wall-node'
    elif id_ is 'end-button':
        _current_class = 'end-node'
    elif id_ is 'restore-button':
        _current_class = 'node'


@bind(document, 'keydown')
def start_pathfind(ev):
    global start_html_node
    global end_html_node
    global ROWS
    global COLUMNS
    space_bar = 32
    if ev.keyCode is space_bar:
        try:
            map_html_nodes = get_matrix_from_list(document.select('.node'))
            nodes = generate_map_of_nodes()
            start_node = get_node(map_html_nodes, start_html_node)
            end_node = get_node(map_html_nodes, end_html_node)
            walls = get_wall_nodes(map_html_nodes)

            map_of_costs = set_costs(nodes, start_node, end_node)

            set_node_costs(start_node, map_of_costs)
            set_node_costs(end_node, map_of_costs)

            path = AStar().find_path(map_of_costs, map_html_nodes, walls, start_node, end_node, ROWS, COLUMNS)
            paint_path(path, start_node, end_node)
        except NameError:
            pass
        # TODO: except UndefinedCriticalNodes:
    ev.preventDefault()


@bind(document['restore-map-button'], 'click')
def restore_map(_):
    for i in document.select('.node'):
        i.classList.remove('path-node')
        i.classList.remove('open-node')
        i.classList.remove('closed-node')


@bind(document['new-map-button'], 'click')
def new_map(_):
    for i in document.select('.node'):
        i.classList.remove('start-node')
        i.classList.remove('end-node')
        i.classList.remove('wall-node')
    restore_map(_)


def paint_path(path, start_node, end_node):
    matrix = get_matrix_from_list(document.select('.node'))
    for node in path:
        if not AStar().is_same_position(node, start_node) and not AStar().is_same_position(node, end_node):
            matrix[node.x][node.y].classList.add('path-node')


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
