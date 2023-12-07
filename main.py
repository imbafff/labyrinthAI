def check_x(route: int, point_x, point_z):
    if matrix[point_x + route][point_z] == ' ':
        return True
    return False


def move_x(route: int, point_x, point_z, history):
    point_x += route
    history.append((point_x, point_z))
    matrix[point_x][point_z] = '│'
    return point_x, point_z


def check_z(route: int, point_x, point_z):
    if matrix[point_x][point_z + route] and matrix[point_x][point_z + route * 2] == ' ':
        return True
    return False


def move_z(route: int, point_x, point_z, history):
    for i in (0, 1):
        point_z += route
        history.append((point_x, point_z))
        matrix[point_x][point_z] = '─'
    return point_x, point_z

def find_way(point_x, point_z, move_arg=None):
    global history_main
    history = []
    while point_x != b_x or point_z != b_z:
        if move_arg != None:
            point_x, point_z = move_arg[1](move_arg[0], point_x, point_z, history)
            move_arg = None
            continue
        moves = []
        for route in (1, -1):
            if check_x(route, point_x, point_z):
                moves.append((route, move_x))
            if check_z(route, point_x, point_z):
                moves.append((route, move_z))
        if len(moves) == 1:
            point_x, point_z = moves[0][1](moves[0][0], point_x, point_z, history)
        elif len(moves) > 1:
            for move in moves:
                s = find_way(point_x, point_z, move)
                if s:
                    point_x, point_z = s
                    break
            else:
                for hist in history:
                    matrix[hist[0]][hist[1]] = ' '
                return False
        else:
            for hist in history:
                 matrix[hist[0]][hist[1]] = ' '
            return False
    history_main = history + history_main
    return (point_x, point_z)






with open('input.txt', 'r', encoding='UTF8') as f:
    matrix = []
    for line in f:
        matrix.append(list(line.rstrip()))


point: int = 0
point_: int = 0

matrix.pop(0)
b_x, b_z = 0, 0
for i, line in enumerate(matrix):
    if 'A' in line:
        point, point_ = i, line.index('A')
    if 'B' in line:
        b_x, b_z = i, line.index('B')
        matrix[b_x][b_z] = ' '


history_main = []
s = find_way(point, point_)
matrix[history_main[-1][0]][history_main[-1][1]] = 'B'
for hist in history_main:
    xx = matrix[hist[0] + 1][hist[1]]
    x = matrix[hist[0] - 1][hist[1]]
    zz = matrix[hist[0]][hist[1] + 1]
    z = matrix[hist[0]][hist[1] - 1]
    if xx == '│' and zz == '─':
        matrix[hist[0]][hist[1]] = '┌'
    elif x in '│╷' and zz == '─':
        matrix[hist[0]][hist[1]] = '└'
    elif x == '│' and z == '─':
        matrix[hist[0]][hist[1]] = '┘'
    elif xx == '│' and z == '─':
        matrix[hist[0]][hist[1]] = '┐'
    elif zz in 'AB':
        matrix[hist[0]][hist[1]] = ' '
        matrix[hist[0]][hist[1] - 1] = '╴'
    elif z in 'AB':
        matrix[hist[0]][hist[1]] = ' '
        matrix[hist[0]][hist[1] + 1] = '╶'
    elif xx in 'AB':
        matrix[hist[0]][hist[1]] = '╵'
    elif x in 'AB':
        matrix[hist[0]][hist[1]] = '╷'

with open('output.txt', 'w', encoding='utf8') as f:
    for i in matrix:
        f.write(''.join(i) + '\n')
