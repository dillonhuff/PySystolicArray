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
        self.nrows = nrows
        self.ncols = ncols

        self.col_fifos = []
        self.row_fifos = []

        self.fifo_depth = max(nrows, ncols) + 1

        for i in range(self.nrows):
            zeros = []
            for j in range(self.fifo_depth):
                zeros.append(0)

            self.row_fifos.append(deque(zeros))

        for j in range(self.ncols):
            zeros = []
            for j in range(self.fifo_depth):
                zeros.append(0)
            
            self.col_fifos.append(deque(zeros))

        self.tile_rows = {}
        for i in range(self.nrows):
            tile_row = {}
            for j in range(self.ncols):
                tile_row[j] = Tile()

            self.tile_rows[i] = tile_row


    def get_tile(self, i, j):
        return self.tile_rows[i][j]

    def read_col(self, i):
        print(self.col_fifos[i])
        val = self.col_fifos[i].pop()
        self.col_fifos[i].appendleft(0)

        return val

    def read_row(self, i):
        print(self.row_fifos[i])
        val = self.row_fifos[i].pop()
        self.row_fifos[i].appendleft(0)

        return val
        
    def update(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if i == 0:
                    top = self.read_col(j)
                else:
                    top = self.get_tile(i - 1, j).down

                if j == 0:
                    left = self.read_row(i)
                else:
                    left = self.get_tile(i, j - 1).right


                self.get_tile(i, j).update_val(top, left)


        for i in range(self.nrows):
            for j in range(self.ncols):
                if i == 0:
                    top = self.read_col(j)
                else:
                    top = self.get_tile(i - 1, j).down

                if j == 0:
                    left = self.read_row(i)
                else:
                    left = self.get_tile(i, j - 1).right


                self.get_tile(i, j).update_outputs(top, left)
                
    def __str__(self):
        s = ''
        return s

sa = SysArray(1, 2)

print(sa)

sa.update()

print(sa)

a = Matrix(1, 2)
a.set(0, 0, 1)
a.set(0, 1, 2)

print(a)


b = Matrix(2, 2)
b.set(0, 0, 4)
b.set(0, 1, 5)
b.set(1, 0, 6)
b.set(1, 1, 7)

print(b)

print('Correct product')
prod = mul(a, b)
print(prod)
