import sys
sys.setrecursionlimit(5000)
maze,health_maze,visited_cells,visited_cells_health = [],[],[],[]

with open(sys.argv[1],"r") as file1:
    a = file1.read()
    a = a.split("\n")

with open(sys.argv[2],"r") as file2:
    b = file2.read()
    b = b.split("\n")

file3 = open(sys.argv[4],"w")
file3.close()

health_time = int(sys.argv[3])

for i in a:
    maze.append(list(i))

for i in b:
    health_maze.append(list(i))

health_maze1 = health_maze[:]

def find_ending1(itr):
    for item in itr:
        if "F" in item:
            return itr.index(item)

def find_ending2(itr):
    for item in itr:
        for j in item:
            if j == "F":
                return item.index(j)

def find_beginning1(itr):
    for item in itr:
        if "S" in item:
            return itr.index(item)

def find_beginning2(itr):
    for item in itr:
        for j in item:
            if j == "S":
                return item.index(j)

def upward_neighbour(x,y,maze_itr):
    try:
        if x <= 0 or y < 0:
            return None
        return maze_itr[x-1][y]
    except IndexError:
        pass

def downward_neighbour(x,y,maze_itr):
    try:
        if x < 0 or y < 0:
            return None
        return maze_itr[x+1][y]
    except IndexError:
        pass

def left_neighbour(x,y,maze_itr):
    try:
        if x < 0 or y <= 0:
            return None
        return maze_itr[x][y-1]
    except IndexError:
        pass

def right_neighbour(x,y,maze_itr):
    try:
        if x < 0 or y < 0:
            return None
        return maze_itr[x][y+1]
    except IndexError:
        pass

def solve_maze(x,y,maze_itr):
    while (x,y) != (find_ending1(maze_itr),find_ending2(maze_itr)):
        if maze_itr[x][y] != "S":
            maze_itr[x][y] = "1"
        if (x,y) not in visited_cells:
            visited_cells.append((x,y))

        if (upward_neighbour(x,y,maze_itr) == "P" or upward_neighbour(x,y,maze_itr) == "F") and (x-1,y) not in visited_cells:
            return solve_maze(x-1,y,maze_itr)
        elif (downward_neighbour(x,y,maze_itr) == "P" or downward_neighbour(x,y,maze_itr) == "F") and (x+1,y) not in visited_cells:
            return solve_maze(x+1,y,maze_itr)
        elif (left_neighbour(x,y,maze_itr) == "P" or left_neighbour(x,y,maze_itr) == "F") and (x,y-1) not in visited_cells:
            return solve_maze(x,y-1,maze_itr)
        elif (right_neighbour(x,y,maze_itr) == "P" or right_neighbour(x,y,maze_itr) == "F") and (x,y+1) not in visited_cells:
            return solve_maze(x,y+1,maze_itr)
        else:
            maze_itr[x][y] = "0"
            for i,j in [visited_cells[-2]]:
                visited_cells.pop()
                return solve_maze(i, j, maze_itr)

solve_maze(find_beginning1(maze),find_beginning2(maze),maze)
for i in maze:
    for j in range(len(i)):
        if i[j] == "W" or i[j] == "P":
            i[j] = "0"

for i in range(len(maze)):
    maze[i] = ",".join(maze[i])

with open(sys.argv[4],"a") as file3:
    for i in maze:
        file3.writelines(i)
        file3.write("\n")

x1,x2 = find_beginning1(health_maze),find_beginning2(health_maze)

def solve_maze_health(x,y,maze_itr):
    try:
        global health_time
        if maze_itr[x][y] == "H":
            health_time = int(sys.argv[3])
        while (x, y) != (find_ending1(maze_itr), find_ending2(maze_itr)) and health_time >= 0:
            if (x, y) not in visited_cells_health:
                visited_cells_health.append((x, y))
            if maze_itr[x][y] == "H":
                health_time = int(sys.argv[3])

            if maze_itr[x][y] != "S" and maze_itr[x][y] != "H":
                maze_itr[x][y] = "1"

            if (upward_neighbour(x, y, maze_itr) == "P" or upward_neighbour(x, y, maze_itr) == "F" or upward_neighbour(x,y,maze_itr) == "H") and (x - 1, y) not in visited_cells_health:
                health_time -= 1
                return solve_maze_health(x - 1, y, maze_itr)
            elif (left_neighbour(x, y, maze_itr) == "P" or left_neighbour(x, y, maze_itr) == "F" or left_neighbour(x,y,maze_itr) == "H") and (x, y - 1) not in visited_cells_health:
                health_time -= 1
                return solve_maze_health(x, y - 1, maze_itr)
            elif (downward_neighbour(x, y, maze_itr) == "P" or downward_neighbour(x, y, maze_itr) == "F" or downward_neighbour(x,y,maze_itr) == "H") and (x + 1, y) not in visited_cells_health:
                health_time -= 1
                return solve_maze_health(x + 1, y, maze_itr)
            elif (right_neighbour(x, y, maze_itr) == "P" or right_neighbour(x, y, maze_itr) == "F" or right_neighbour(x,y,maze_itr) == "H") and (x, y + 1) not in visited_cells_health:
                health_time -= 1
                return solve_maze_health(x, y + 1, maze_itr)
            else:
                maze_itr[x][y] = "0"
                for i, j in [visited_cells_health[-2]]:
                    visited_cells_health.pop()
                    return solve_maze_health(i, j, maze_itr)
        if (x, y) == (find_ending1(maze_itr), find_ending2(maze_itr)):
            pass
        else:
            maze_itr[x][y] = "0"
            health_time = int(sys.argv[3])
            for i,j in [visited_cells_health[-1]]:
                maze_itr[i][j] = "0"
            for i, j in [visited_cells_health[-2]]:
                maze_itr[i][j] = "0"
                visited_cells_health.pop()
                return solve_maze_health(i, j, maze_itr)
    except IndexError:
        print("This maze cannot be solved with this health.")
        return 42

a = solve_maze_health(find_beginning1(health_maze),find_beginning2(health_maze),health_maze)
if a != 42:
    health_maze[x1][x2] = "S"
    for i in health_maze:
        for j in range(len(i)):
            if i[j] == "W" or i[j] == "P":
                i[j] = "0"
    for i in range(len(health_maze)):
        health_maze[i] = ",".join(health_maze[i])

with open(sys.argv[4],"a") as file3:
    file3.write("\n\n")
    for i in health_maze:
        file3.writelines(i)
        file3.write("\n")
