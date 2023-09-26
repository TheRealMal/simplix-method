from fractions import Fraction

class Simplix:
    def __init__(self, F: list[int], A: list[list[int]]) -> None:
        self.F = F
        self.A = A
        self.basis_vars = self._set_basis()
        self.free_vars = self._set_free()
        self.simplix_table = self._simplix_table_init()
        self.iterations = 0

    def _set_basis(self) -> list[int]:
        def basis_loop(line: list[int]) -> int:
            for i in range(len(line) - 2, 0, -1):
                if line[i] != 0: return i
        
        arr = []
        for i in range(len(self.A)):
            arr.append(
                basis_loop(self.A[i])
            )
        return arr
    
    def _set_free(self) -> list[int]:
        arr = []
        for i in range(1, len(self.F) - 1):
            if i not in self.basis_vars:
                arr.append(i)
        return arr

    def _simplix_table_init(self) -> list[list]:
        table = [[" ", "Sjo"]]
        # Fill first line
        for i in range(len(self.free_vars)):
            table[0].append(self.free_vars[i])
        # Fill every line
        # If coeff within i'th X < 0 -> inverse line
        for i in range(len(self.basis_vars)):
            table.append([self.basis_vars[i]])
            table[i + 1].append(
                Fraction(self.A[i][-1]) if self.A[i][self.basis_vars[i]] > 0 else Fraction(-self.A[i][-1])
                )
            for j in range(1, len(self.A[i]) - 1):
                if j not in self.basis_vars:
                    if self.A[i][self.basis_vars[i]] < 0:
                        self.A[i][j] = -self.A[i][j]
                    table[i + 1].append(Fraction(self.A[i][j]))
        # Fill last line (inverse all values)
        table.append(["F"])
        for i in range(len(self.F)):
            if i not in self.basis_vars:
                table[-1].append(Fraction(-self.F[i]))
        return table
    
    def solve(self) -> None:
        while not self._simplix_check():
            self.print()
        while not self._simplix_check_second():
            self.print()

    def _simplix_check(self) -> bool:
        for i in range(1, len(self.simplix_table) - 1):
            if self.simplix_table[i][1] < 0:
                perm_col = self._simplix_perm_col(i)
                perm_row = self._simplix_perm_row(self.simplix_table[i][perm_col], self.iterations == 0)
                print("Итерация #{} | Разрешающая строка: {} | Разрешающий столбец: {}".format(self.iterations, perm_row, perm_col))
                self._simplix_step(perm_col, perm_row)
                self.iterations += 1
                return False
        return True
    
    def _simplix_check_second(self) -> bool:
        for i in range(2, len(self.simplix_table[-1])):
            if self.simplix_table[-1][i] > 0:
                perm_col = i
                perm_row = self._find_min_free_rel(self.simplix_table[-1][i])
                print("Итерация #{} | Разрешающая строка: {} | Разрешающий столбец: {}".format(self.iterations, perm_row, perm_col))
                self._simplix_step(perm_col, perm_row)
                self.iterations += 1
                return False
        return True
    
    def _find_min_free_rel(self, el: int) -> int:
        min_value, min_index = 10**10, 0
        for i in range(1, len(self.simplix_table) - 1):
            value = self.simplix_table[i][1] / el
            if value < min_value and value > 0:
                min_value, min_index = value, i
        return min_index
        
    def _simplix_step(self, perm_col: int, perm_row: int) -> None:
        new_matrix = [[0 for __ in range(len(self.simplix_table[_]))] for _ in range(len(self.simplix_table))]
        for i in range(len(self.simplix_table[0])):
            new_matrix[0][i] = self.simplix_table[0][i]
        for i in range(len(self.simplix_table)):
            new_matrix[i][0] = self.simplix_table[i][0]
        new_matrix[0][perm_col], new_matrix[perm_row][0] = new_matrix[perm_row][0], new_matrix[0][perm_col]
        for i in range(1, len(self.simplix_table)):
            for j in range(1, len(self.simplix_table[i])):
                if i == perm_row and j == perm_col:
                    new_matrix[perm_row][perm_col] = 1 / self.simplix_table[perm_row][perm_col]
                elif i == perm_row:
                    new_matrix[i][j] = self.simplix_table[i][j] / self.simplix_table[perm_row][perm_col]
                elif j == perm_col:
                    new_matrix[i][j] = - self.simplix_table[i][j] / self.simplix_table[perm_row][perm_col]
                else:
                    new_matrix[i][j] = self.simplix_table[i][j] - self.simplix_table[i][perm_col] * self.simplix_table[perm_row][j] / self.simplix_table[perm_row][perm_col]
        self.simplix_table = new_matrix

    def _simplix_perm_col(self, row_index: int) -> int:
        for i in range(2, len(self.simplix_table[row_index])):
            if self.simplix_table[row_index][i] < 0:
                return i
            
    def _simplix_perm_row(self, el: int, first_iter: bool = True) -> int:
        min_value, min_index = 10**10, 1
        for i in range(1, len(self.simplix_table) - 1):
            value = self.simplix_table[i][1] / el
            if value < min_value and ((value > 0 and first_iter) or (value >= 0 and not first_iter)):
                min_value, min_index = value, i
        return min_index

    def _log_state(self, perm_row: int, perm_col: int) -> None:
        print("Итерация #{} | Разрешающая строка: {} | Разрешающий столбец: {}".format(self.iterations, perm_row, perm_col))

    def print(self) -> None:
        import pandas as pd
        matrix = []
        for i in range(len(self.simplix_table)):
            matrix.append([])
            for j in range(len(self.simplix_table[i])):
                if (i == 0 or j == 0) and type(self.simplix_table[i][j]) == int:
                    matrix[i].append("X{}".format(self.simplix_table[i][j]))
                elif type(self.simplix_table[i][j]) == float:
                    matrix[i].append(self.simplix_table[i][j])
                else:
                    matrix[i].append(str(self.simplix_table[i][j]))
        df = pd.DataFrame(matrix, columns=None)
        print(df.to_string(index=0, header=0))
