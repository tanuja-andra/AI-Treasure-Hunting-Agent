import streamlit as st
import random
import heapq
import time

if "obstacles" not in st.session_state:
    st.session_state.obstacles = set()
if "discovered_obstacles" not in st.session_state:
    st.session_state.discovered_obstacles = set()
if "discovered_free" not in st.session_state:
    st.session_state.discovered_free = set()
if "bfs_cells" not in st.session_state:
    st.session_state.bfs_cells = None
if "bfs_path" not in st.session_state:
    st.session_state.bfs_path = None
if "a_cells" not in st.session_state:
    st.session_state.a_cells = None
if "a_path" not in st.session_state:
    st.session_state.a_path = None
if "visited" not in st.session_state:
    st.session_state.visited = None
if "path" not in st.session_state:
    st.session_state.path = None
if "action" not in st.session_state:
    st.session_state.action = None
if "prev_environment" not in st.session_state:
    st.session_state.prev_environment = None
if "prev_algorithm" not in st.session_state:
    st.session_state.prev_algorithm = None
if "graph_id" not in st.session_state:
    st.session_state.graph_id = 0
if "bfs_graph_id" not in st.session_state:
    st.session_state.bfs_graph_id = None
if "a_graph_id" not in st.session_state:
    st.session_state.a_graph_id = None
if "bfs_time" not in st.session_state:
    st.session_state.bfs_time = None
if "a_time" not in st.session_state:
    st.session_state.a_time = None

# Generates the grid
def generate():
    grid = []
    for row in range(10):
        current_row = []
        for col in range(10):
            if(row, col) == (0, 0):
                current_row.append(" S ")
            elif(row, col) == (9, 9):
                current_row.append(" T ")
            else:
                if environment == "Known":
                    current_row.append(" . ")
                else:
                    current_row.append(" ? ")
        grid.append(current_row)
    return grid

# Heuristic value
def heuristic(position):
    row, col = position
    dest_row = 9
    dest_col = 9
    return abs(row - dest_row) + abs(col - dest_col)

# Best First Search
def best_first_search():
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic((0,0)), (0, 0)))
    visited = set()
    parent = {}
    while priority_queue:
        h, curr = heapq.heappop(priority_queue)
        if curr in visited:
            continue
        visited.add(curr)
        if curr == (9, 9):
            break
        row, col = curr
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_col <= 9 and 0 <= new_row <= 9:
                neighbour = (new_row, new_col)
                if neighbour in st.session_state.obstacles:
                    continue
                if neighbour in visited:
                    continue
                if neighbour not in parent:
                    parent[neighbour] = curr
                    h = heuristic(neighbour)
                    heapq.heappush(priority_queue, (h, neighbour))
    return visited, parent

# A* Search
def a_star_search():
    priority_queue = []
    g_cost = {(0, 0) : 0}
    parent = {}
    visited = set()
    heapq.heappush(priority_queue, (heuristic((0, 0)), (0, 0)))
    while priority_queue:
        f, curr = heapq.heappop(priority_queue)
        if curr in visited:
            continue
        visited.add(curr)
        if curr == (9, 9):
            break
        row, col = curr
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_col <= 9 and 0 <= new_row <= 9:
                neighbour = (new_row, new_col)
                if neighbour in st.session_state.obstacles:
                    continue
                new_g = g_cost[curr] + 1
                if (neighbour not in g_cost or new_g < g_cost[neighbour]):
                    g_cost[neighbour] = new_g
                    h = heuristic(neighbour)
                    f = new_g + h
                    parent[neighbour] = curr
                    heapq.heappush(priority_queue, (f, neighbour))
    return visited, parent

# Construct path
def construct_path(parent):
    path = []
    curr = (9, 9)
    if curr not in parent:
        return []
    while curr != (0, 0):
        path.append(curr)
        curr = parent[curr]
    path.append((0, 0))
    path.reverse()
    return path

# Find cells in unknown environment
def discover_cells(current):
    if current not in st.session_state.obstacles :
        st.session_state.discovered_free.add(current)
    row, col = current
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for d_row, d_col in directions:
        new_row = row + d_row
        new_col = col + d_col
        if 0 <= new_row <= 9 and 0 <= new_col <= 9:
            neighbour = (new_row, new_col)
            if neighbour in st.session_state.obstacles:
                st.session_state.discovered_obstacles.add(neighbour)
            else:
                st.session_state.discovered_free.add(neighbour)

# Best First Search for unknown environment
def best_first_unknown(start):
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(start), start))
    visited = set()
    parent = {}
    while priority_queue:
        h, curr = heapq.heappop(priority_queue)
        if curr in visited:
            continue
        visited.add(curr)
        if curr == (9, 9):
            break
        row, col = curr
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row <= 9 and 0 <= new_col <= 9:
                neighbour = (new_row, new_col)
                if neighbour in st.session_state.discovered_obstacles:
                    continue
                if neighbour in visited:
                    continue
                if neighbour not in parent:
                    parent[neighbour] = curr
                    h = heuristic(neighbour)
                    heapq.heappush(priority_queue,(h, neighbour))
    return visited, parent

# A* Search for unknown environment
def a_star_unknown(start):
    priority_queue = []
    g_cost = {start : 0}
    heapq.heappush(priority_queue, (heuristic(start), start))
    visited = set()
    parent = {}
    while priority_queue:
        f, curr = heapq.heappop(priority_queue)
        if curr in visited:
            continue
        visited.add(curr)
        if curr == (9, 9):
            break
        row, col = curr
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row <= 9 and 0 <= new_col <= 9:
                neighbour = (new_row, new_col)
                if neighbour in st.session_state.discovered_obstacles:
                    continue
                new_g = g_cost[curr] + 1
                if (neighbour not in g_cost or new_g < g_cost[neighbour]):
                    parent[neighbour] = curr
                    g_cost[neighbour] = new_g
                    h = heuristic(neighbour)
                    f = h + new_g
                    heapq.heappush(priority_queue, (f, neighbour))
    return visited, parent

# Construct path in unknown environment
def construct_unknown_path(parent, start, goal):
    path = []
    curr = goal
    if curr != start and curr not in parent:
        return []
    while curr != start:
        path.append(curr)
        curr = parent[curr]
    path.append(start)
    path.reverse()
    return path

# Searching in unknown environment
def unknown_search(algorithm):
    st.session_state.discovered_obstacles.clear()
    st.session_state.discovered_free.clear()
    current = (0, 0)
    all_visited = set()
    discover_cells(current)
    while current != (9, 9):
        # discover_cells(current)
        if algorithm == "Best First Search" :
            visited, parent = best_first_unknown(current)
        else :
            visited, parent = a_star_unknown(current)
        all_visited.update(visited)
        path = construct_unknown_path(parent, current, (9, 9))
        if not path :
            return all_visited, []
        blocked = False
        for next_cell in path[1:] :
            if next_cell in st.session_state.obstacles :
                st.session_state.discovered_obstacles.add(next_cell)
                blocked = True
                break
            current = next_cell
            st.session_state.discovered_free.add(current)
            discover_cells(current)
            if current == (9, 9):
                break
        if current == (9, 9):
            break
    if algorithm == "Best First Search" :
        visited, parent = best_first_unknown((0, 0))
    else : 
        visited, parent = a_star_unknown((0, 0))
    final_path = construct_unknown_path(parent, (0, 0), (9, 9))
    all_visited.update(visited)
    return all_visited, final_path

# Prints the grid
def print_grid():
    grid = generate()
    for row in range(10):
        cols = st.columns(10)
        for col in range(10):
            position = (row, col)
            if position == (0, 0) :
                value = "🔎"
            elif position == (9, 9) :
                value = "🪙"
            elif environment == "Unknown":
                    value = "❓"
            elif position in st.session_state.obstacles:
                value = "❌"
            else:
                value = "⬜"
            with cols[col] :
                if st.button(value, key = f"cell_{row}_{col}") :
                    if position != (0, 0) and position != (9, 9) :
                        if position in st.session_state.obstacles:
                            st.session_state.obstacles.remove(position)
                        else:
                            st.session_state.obstacles.add(position)
                        st.session_state.graph_id += 1
                        st.session_state.action = None
                    st.rerun()

# Display final grid
def final_grid(visited, path):
    #grid = generate()
    for row in range(10):
        cols = st.columns(10)
        for col in range(10):
            position = (row, col)
            if position == (0, 0) :
                value = "🔎"
            elif position == (9, 9) :
                value = "🪙"
            elif environment == "Unknown" :
                if position in st.session_state.discovered_obstacles :
                    value = "❌"
                elif position in path :
                    value = "🟩"
                # elif position in visited :
                #     value = "🟦"
                elif position in st.session_state.discovered_free :
                    value = "⬜"
                else :
                    value = "❓"

            else :
                if position in st.session_state.obstacles:
                    value = "❌"
                elif position in path:
                    value = "🟩"
                elif position in visited:
                    value = "🟦"
                else:
                    value = "⬜"
            with cols[col]:
                st.button(value, key = f"final_{row}_{col}")

# Main function
st.set_page_config(page_title="AI Treasure Hunting Agent")                            
st.title("AI Treasure Hunting Agent")

col1, col2 = st.columns(2)
with col1:
    environment = st.selectbox("Choose an environment: ", ["Known", "Unknown"])
with col2:
    algorithm = st.selectbox("Choose an algorithm: ", ["Best First Search", "A* Search"])

# Tracks if the environment has changed
if(st.session_state.prev_environment is not None and st.session_state.prev_environment != environment):
    st.session_state.action = None
if(st.session_state.prev_algorithm is not None and st.session_state.prev_algorithm != algorithm):
    st.session_state.action = None
st.session_state.prev_environment = environment
st.session_state.prev_algorithm = algorithm

col3, col4 = st.columns(2)

# Clears the obstacles
with col3 :
    if st.button("Clear"):
        st.session_state.obstacles.clear()
        st.session_state.discovered_obstacles.clear()
        st.session_state.discovered_free.clear()
        st.session_state.graph_id += 1
        st.session_state.bfs_graph_id = None
        st.session_state.a_graph_id = None
        st.session_state.bfs_cells = None
        st.session_state.bfs_path = None
        st.session_state.a_cells = None
        st.session_state.a_path = None
        st.session_state.visited = None
        st.session_state.path = None
        st.session_state.action = None
        st.rerun()

# Generates random obstacles
with col4 :
    if st.button("Generate Random Obstacles"):
        st.session_state.obstacles.clear()
        positions = [(row, col) 
                    for row in range(10) 
                    for col in range(10)
                    if (row, col) != (0, 0) and (row, col) != (9, 9)]
        st.session_state.obstacles = set(random.sample(positions, 20))
        st.session_state.discovered_obstacles.clear()
        st.session_state.discovered_free.clear()
        st.session_state.graph_id += 1
        st.session_state.action = None
        st.rerun()

st.write("Number of obstacles: ", len(st.session_state.obstacles))
st.write("Click to generate obstacles:")
print_grid()

col5, col6 = st.columns(2)
with col5 :
    if algorithm == "Best First Search":
        if st.button("Run Best First Search"):
            if not st.session_state.obstacles:
                st.error("Generate obstacles first!")
            else :
                start = time.perf_counter()
                if environment == "Unknown" :
                    visited, path = unknown_search("Best First Search")
                else :
                    visited, parent = best_first_search()
                    path = construct_path(parent)
                end = time.perf_counter()
                total_time = end - start
                if path:
                    st.success("Treasure found!")
                    if environment == "Known" :
                        st.session_state.bfs_cells = len(visited) - 1
                        st.write("Cells explored : ", st.session_state.bfs_cells)
                    else :
                        st.session_state.bfs_cells = (len(st.session_state.discovered_obstacles) + len(st.session_state.discovered_free) - 2)
                        st.write("Cells discovered : ", st.session_state.bfs_cells)
                    st.session_state.bfs_path = len(path) - 1
                    st.write("Path length : ", st.session_state.bfs_path)
                    st.session_state.bfs_time = total_time
                    st.write("Execution time : ", f"{st.session_state.bfs_time:.6f} s")
                    st.session_state.bfs_graph_id = st.session_state.graph_id
                    st.session_state.visited = visited
                    st.session_state.path = path
                    st.session_state.action = "run"
                    
                else :
                    st.error("No path exists!")
    else:
        if st.button("Run A* Search"):
            if not st.session_state.obstacles:
                st.error("Generate obstacles first!")
            else :
                start = time.perf_counter()
                if environment == "Unknown" :
                    visited, path = unknown_search("A* Search")
                else :
                    visited, parent = a_star_search()
                    path = construct_path(parent)
                end = time.perf_counter()
                total_time = end - start
                
                if path:
                    st.success("Treasure found!")
                    if environment == "Known" : 
                        st.session_state.a_cells = len(visited) - 1
                        st.write("Cells explored : ", st.session_state.a_cells)
                    else :
                        st.session_state.a_cells = (len(st.session_state.discovered_free) + len(st.session_state.discovered_obstacles) - 2)
                        st.write("Cells discovered : ", st.session_state.a_cells)
                    st.session_state.a_path = len(path) - 1
                    st.write("Path length : ", st.session_state.a_path)
                    st.session_state.a_time = total_time
                    st.write("Execution time : ", f"{st.session_state.a_time:.6f} s")
                    st.session_state.a_graph_id = st.session_state.graph_id
                    st.session_state.visited = visited
                    st.session_state.path = path
                    st.session_state.action = "run"
                else :
                    st.error("No path exists!")

with col6 :
    if st.button("Compare Results") :
        st.session_state.action = "compare"

if(st.session_state.action == "compare"):
    if(st.session_state.bfs_graph_id is None or st.session_state.a_graph_id is None):
        st.warning("Run both algorithms first!")
    elif(st.session_state.bfs_graph_id != st.session_state.a_graph_id):
        st.warning("Grid has changed! \n\n Run the algorithms again!")   
    else:
        data = {"Properties" : ["Cells explored", "Path length", "Execution time"],
                "Best First Search" : [int(st.session_state.bfs_cells), int(st.session_state.bfs_path), f"{st.session_state.bfs_time:.6f} s"],
                "A* Search" : [int(st.session_state.a_cells), int(st.session_state.a_path), f"{st.session_state.a_time:.6f} s"]}
        st.table(data)

if st.session_state.action == "run" and st.session_state.visited is not None and st.session_state.path is not None:
    st.write("Path : ")
    final_grid(st.session_state.visited, st.session_state.path)