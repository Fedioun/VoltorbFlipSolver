from copy import deepcopy

valid_grids = []
def main():
    #
    #
    global valid_grids
    grid = [[-1 for x in range(5)] for k in range(5)]
    played_grid = [[0 for x in range(5)] for k in range(5)]


    hclues = [[6, 1], [9, 1], [5, 2], [4, 3], [3, 3]]
    vclues = [[6, 3], [4, 2], [4, 1], [6, 2], [7, 2]]

    """
    vclues = []
    hclues = []
    


    for i in range(5):
        p = int(input("Points ligne " + str(i+1) + " : "))
        m = int(input("Mines ligne " + str(i + 1) + " : "))
        vclues.append([p,m])
    for i in range(5):
        p = int(input("Points colonne " + str(i+1) + " : "))
        m = int(input("Mines colonne " + str(i + 1) + " : "))
        hclues.append([p,m])

    print(hclues)
    print(vclues)
    """
    place_elt(grid, vclues, hclues, 0, 0)

    p_mines = get_probas(0)
    p_2 = get_probas(2)
    p_3 = get_probas(3)
    print("Probas mines : ")
    print_probas(p_mines)
    print("Probas 2 : ")
    print_probas(p_2)
    print("Probas 3 : ")
    print_probas(p_3)

    x, y = get_next_move(p_mines, p_2, p_3, played_grid)
    print("Next move : x=" + str(x+1) + " y=" + str(y+1))

    while(True):
        #x = int(input("x :")) -1
        #y = int(input("y :")) -1
        num = int(input("Num : "))
        nvalid_grids = []
        for p in valid_grids:
            #print(p[y][x])
            if p[y][x] == num:
                nvalid_grids.append(p)
        played_grid[y][x] = 1

        valid_grids = nvalid_grids
        p_mines = get_probas(0)
        p_2 = get_probas(2)
        p_3 = get_probas(3)
        print("Probas mines : ")
        print_probas(p_mines)
        print("Probas 2 : ")
        print_probas(p_2)
        print("Probas 3 : ")
        print_probas(p_3)

        x, y = get_next_move(p_mines, p_2, p_3, played_grid)
        print("Next move : x=" + str(x+1) + " y=" + str(y+1))


def get_next_move(p_mines, p_2, p_3, played_grid):
    by = 0
    bx = 0
    best_proba = 1
    best_proba_2 = 0
    safe = (sum([sum(p) for p in played_grid]) < 7)

    for x in range(5):
        for y in range(5):
            if safe :
                if p_mines[y][x] < best_proba and played_grid[y][x] == 0:
                    bx = x
                    by = y
                    best_proba = p_mines[y][x]

            else:
                if (p_2[y][x] > 0 or p_3[y][x] > 0) and played_grid[y][x] == 0:
                    if p_mines[y][x] < best_proba:
                        bx = x
                        by = y
                        best_proba = p_mines[y][x]
                        best_proba_2 = p_2[y][x] + p_3[y][x]
                    elif p_mines[y][x] == best_proba:
                        if p_2[y][x] + p_3[y][x] > best_proba_2:
                            bx = x
                            by = y
                            best_proba = p_mines[y][x]
                            best_proba_2 = p_2[y][x] + p_3[y][x]

    return bx, by


def get_probas(value):
    p_mines = [[-1 for x in range(5)] for k in range(5)]
    for x in range(5):
        for y in range(5):
            c = 0
            for p in valid_grids:
                if p[y][x] == value:
                    c += 1
            p_mines[y][x] = c / len(valid_grids)
    return p_mines

def print_probas(probas):
    for y in range(5):
        s = "   "
        for k in range(5):
            s += '{:.2f}%'.format(probas[y][k]) + " " * 7
        print(s)

def place_elt(grid, vclues, hclues, x, y):
    #print("test")
    #print_grid(grid, vclues, hclues)
    for k in range(1, 4):
        #print(k, x, y)
        if hclues[x][0] - k > -1 and vclues[y][0] - k > -1:
            ngrid = deepcopy(grid)
            ngrid[y][x] = k
            nhclues = deepcopy(hclues)
            nhclues[x][0] -= k
            nvclues = deepcopy(vclues)
            nvclues[y][0] -= k

            if not (x == 4 and nvclues[y][0] + nvclues[y][1] > 0) and not (y == 4 and nhclues[x][0] + nhclues[x][1] > 0):
                if x + y == 8 :
                    #print_grid(ngrid, nvclues, nhclues)
                    valid_grids.append(ngrid)
                else:
                    nx, ny = increment(x, y)
                    place_elt(ngrid, nvclues, nhclues, nx, ny)

    if hclues[x][1] > 0 and vclues[y][1] > 0:
        ngrid = deepcopy(grid)
        ngrid[y][x] = 0
        nhclues = deepcopy(hclues)
        nhclues[x][1] -= 1
        nvclues = deepcopy(vclues)
        nvclues[y][1] -= 1

        if not (x == 4 and nvclues[y][0] + nvclues[y][1] > 0) and not (y == 4 and nhclues[x][0] + nhclues[x][1] > 0):

            if x + y == 8:
                #print_grid(ngrid, nvclues, nhclues)
                valid_grids.append(ngrid)
            else:
                nx, ny = increment(x, y)
                place_elt(ngrid, nvclues, nhclues, nx, ny)

def print_grid(grid, vclues, hclues):
    for y in range(5):
        s = "   "
        for k in range(5):
             s +=  '{:.2f}%'.format(grid[y][k]) + " " * 7
        print(s, vclues[y])
    print(hclues)

def increment(x, y):
    if x == 0:
        x = y + 1
        y = 0
    else:
        x -= 1
        y += 1
    while x > 4 or y > 4:
        #print(x, y)
        if x == 0:
            x = y + 1
            y = 0
        else:
            x -= 1
            y += 1
    return x, y

main()