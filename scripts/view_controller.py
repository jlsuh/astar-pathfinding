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
            map_of_nodes = get_map_of_nodes(map)
            start = get_node(map, start_node)
            end = get_node(map, end_node)
            walls = get_wall_nodes(map)
            result = a_star(map_of_nodes, walls, start, end, ROWS, COLUMNS)
            print(result)
            # document.unbind("keydown"): might be good to cancel out various executions of this algorithm while solving
        except NameError:
            pass
        # TODO: except UndefinedCriticalNodes:
    ev.preventDefault()


def get_node(map, target_node):
    for i in range(COLUMNS):
        for j in range(ROWS):
            if target_node is map[i][j]:
                return Node(i, j)
    return None


def get_wall_nodes(map):
    walls = []
    for x in range(COLUMNS):
        for y in range(ROWS):
            if 'wall-node' in map[x][y].classList:
                walls.append(Node(x,y))
                # walls.append(f"({x}, {y})")
    return walls


def get_map_of_nodes(map):
    rows = []
    for x in range(COLUMNS):
        column = []
        for y in range(ROWS):
            column.append(Node(x,y))
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

    ROWS = 40
    COLUMNS = 40

    initiate_grid(ROWS, COLUMNS)

    nodes = document.select('.node')

    current_class = 'node'

    bind_event(nodes, 'click', paint_node)
