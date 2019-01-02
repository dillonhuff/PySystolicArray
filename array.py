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

    return c
    
m = Matrix(5, 5)

print(m)

m.set(0, 2, 3)

print(m)

assert(m.get(0, 2) == 3)

