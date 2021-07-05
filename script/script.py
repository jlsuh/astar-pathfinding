from browser import document, bind


def paint_node(ev):
    global current_class
    current_target = ev.currentTarget
    current_target['class'] = 'node'
    current_target.classList.add(current_class)
    update_critical_nodes(current_target)


# TODO: this is so ugly
def update_critical_nodes(current_target):
    global start_node
    global end_node
    global current_class
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
    global pathfind_map
    pathfind_map.style.setProperty('--grid-rows', rows)
    pathfind_map.style.setProperty('--grid-columns', columns)


def initiate_grid(rows, columns):
    global pathfind_map
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
    global start_node
    global end_node
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
def a_star_pathfind(ev):
    if ev.keyCode is 32:
        print("Something")
        # document.unbind("keydown") -> might be good to cancel out various executions of this algorithm while solving
    ev.preventDefault()


if __name__ == '__main__':
    pathfind_map = document['pathfinding-map']

    start_node = None
    end_node = None

    initiate_grid(40, 40)

    nodes = document.select('.node')

    current_class = 'node'

    bind_event(nodes, 'click', paint_node)
