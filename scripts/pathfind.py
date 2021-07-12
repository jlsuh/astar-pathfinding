class AStar():

    def find_path(self, map_of_costs, html_nodes, wall_nodes, start_node, end_node, rows, columns):
        step = 1
        open_set = set()
        closed_set = set()
        open_set.add(start_node)
        self.print_list(wall_nodes)
        while open_set:
            current = min(open_set, key=lambda n: n.g_cost + n.h_cost)
            html_nodes[current.x][current.y].text = str(step)
            if current.x == end_node.x and current.y == end_node.y:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]
            open_set.remove(current)
            closed_set.add(current)
            self.set_color(html_nodes, current, start_node, end_node, '#8B0000')
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
                    self.set_color(html_nodes, node, start_node, end_node, '#0f0')
            step += 1
        raise ValueError("No path found")


    def is_same_position(self, node1, node2):
        return node1.x == node2.x and node1.y == node2.y


    def set_color(self, html_matrix_nodes, current, start, end, color):
        if not self.is_same_position(current, start) and not self.is_same_position(current, end):
            html_matrix_nodes[current.x][current.y].style.backgroundColor = color


    def print_list(self, set_):
        for i in set_:
            print(f"({i.x}, {i.y})", end=" ")
        print()


    def get_path(self, final_map, nodes, rows, columns):
        for i in range(columns):
            for j in range(rows):
                if final_map[j][i].parent is None:
                    continue
                else:
                    nodes[j][i] = " "
        return nodes


    def print_node(self, node):
        print(f"Current node: g: {node.g_cost} | h: {node.h_cost} | f: {node.f_cost} | ({node.x}, {node.y})")


    def print_costs(self, map_of_nodes, rows, columns):
        for i in range(rows):
            for j in range(columns):
                node = map_of_nodes[i][j]
                print(f"g: {node.g_cost} | h: {node.h_cost} | f: {node.f_cost} | ({node.x}, {node.y})")


    def find_element(self, list, target):
        for i in list:
            if target is list[i]:
                return list[i]


    def is_position_of_any(self, set_, target):
        for node in set_:
            if target.x == node.x and target.y == node.y:
                return True
        return False


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


    def get_node_with_lowest_f_cost(self, list):
        sorted_list = sorted(list, key = lambda x: x.f_cost)
        return sorted_list[0]


    def set_costs(self, map_of_nodes, start_node, end_node, rows, columns):
        for i in range(columns):
            for j in range(rows):
                distance_to_start = self.manhattan_distance(map_of_nodes[i][j], start_node)
                distance_to_end = self.manhattan_distance(map_of_nodes[i][j], end_node)
                map_of_nodes[i][j].g_cost = distance_to_start
                map_of_nodes[i][j].h_cost = distance_to_end
                map_of_nodes[i][j].f_cost = distance_to_start + distance_to_end


    def manhattan_distance(self, start, goal):
        return abs(start.x - goal.x) + abs(start.y - goal.y)
