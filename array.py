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
        return self.col_fifos[i][-1]
        # print(self.col_fifos[i])
        # val = self.col_fifos[i].pop()
        # self.col_fifos[i].appendleft(0)

        # return val

    def read_row(self, i):
        return self.row_fifos[i][-1]
        # print(self.row_fifos[i])
        # val = self.row_fifos[i].pop()
        # self.row_fifos[i].appendleft(0)

        # return val
        
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


                self.get_tile(i, j).update_val(left, top)


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


                self.get_tile(i, j).update_outputs(left, top)

        for i in range(self.nrows):
            self.push_to_row(i, 0)
        for i in range(self.ncols):
            self.push_to_col(i, 0)
                
    def __str__(self):
        s = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                s += str(self.get_tile(i, j).stored_val) + ' '
            s += '\n'
        return s

    def push_to_row(self, i, fresh):
        val = self.row_fifos[i].pop()
        self.row_fifos[i].appendleft(fresh)
        return val

    def push_to_col(self, i, fresh):
        val = self.col_fifos[i].pop()
        self.col_fifos[i].appendleft(fresh)
        return val
    
    def print_row_fifos(self):
        for f in self.row_fifos:
            print(f)

    def print_col_fifos(self):
        for f in self.col_fifos:
            print(f)
            
    def load_left_operand(self, a):
        assert(a.num_rows() == self.nrows)

        row_start = 0
        for i in range(a.num_rows()):
            # Push zero prefix
            for z in range(row_start):
                self.push_to_row(i, 0)

            for j in range(a.num_cols()):
                self.push_to_row(i, a.get(i, j))

            for z in range(self.fifo_depth - a.num_cols() - row_start):
                self.push_to_row(i, 0)

            row_start += 1

    def load_right_operand(self, b):
        assert(b.num_cols() == self.ncols)

        col_start = 0
        for i in range(b.num_cols()):
            # Push zero prefix
            for z in range(col_start):
                self.push_to_col(i, 0)

            for j in range(a.num_cols()):
                self.push_to_col(i, b.get(j, i))

            for z in range(self.fifo_depth - b.num_cols() - col_start):
                self.push_to_col(i, 0)

            col_start += 1
            

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

sa.load_left_operand(a)
sa.print_row_fifos()

print('cols')

sa.load_right_operand(b)
sa.print_col_fifos()

print('Initial sum')
print(sa)

sa.update()

print('after first update values:')
print(sa)
print('row fifos')
sa.print_row_fifos()

print('col fifos')
sa.print_col_fifos()

sa.update()

print(sa)


print('row fifos')
sa.print_row_fifos()

print('col fifos')
sa.print_col_fifos()

sa.update()

print(sa)


print('row fifos')
sa.print_row_fifos()

print('col fifos')
sa.print_col_fifos()

sa.update()

print(sa)


print('row fifos')
sa.print_row_fifos()

print('col fifos')
sa.print_col_fifos()
