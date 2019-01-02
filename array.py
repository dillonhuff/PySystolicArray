from collections import deque

class Matrix:
    def __init__(self, rows, cols):
        self.rows = {}
        for i in range(rows):
            col_vals = {}
            for j in range(cols):
                col_vals[j] = 0
            self.rows[i] = col_vals

    def set(self, i, j, val):
        self.rows[i][j] = val

    def get(self, i, j):
        return self.rows[i][j]

    def __str__(self):
        s = ''
        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):
              s += str(self.get(i, j))
              s += ' '
            s += '\n'

        return s

    def num_rows(self):
        return len(self.rows)

    def num_cols(self):
        return len(self.rows[0])

def mul(a, b):
    assert(a.num_cols() == b.num_cols())

    c = Matrix(a.num_rows(), b.num_cols())

    for i in range(c.num_rows()):
        for j in range(c.num_cols()):
            c.set(i, j, 0)
            for k in range(a.num_cols()):
                c.set(i, j, c.get(i, j) + a.get(i, k)*b.get(k, j))

    return c
    
m = Matrix(5, 5)

print(m)

m.set(0, 2, 3)
m.set(1, 2, 1)
m.set(0, 0, 4)

print(m)

assert(m.get(0, 2) == 3)

print(mul(m, m))

class Tile:
    def __init__(self):
        self.stored_val = 0
        self.down = 0
        self.right = 0

    def update_val(self, left, top):
        self.stored_val = self.stored_val + left*top

    def update_outputs(self, left, top):
        self.down = top
        self.right = left

class SysArray:
    def __init__(self, nrows, ncols):
        self.row_fifos = []
        for i in range(nrows):
            self.row_fifos = deque()

        for j in range(ncols):
            self.col_fifos = deque()

        self.tile_rows = {}
        for i in range(nrows):
            tile_row = {}
            for j in range(ncols):
                tile_row[j] = Tile()

            self.tile_rows[i] = tile_row

sa = SysArray(5, 5)
            
