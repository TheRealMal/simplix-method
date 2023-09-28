# -*- coding: utf-8 -*-
# Copyright (c) 2023, Roman Malyutin
from fractions import Fraction
import tabulate

class Simplix:
    def __init__(self, F: list[int], A: list[list[int]]) -> None:
        self.F = F
        self.A = A
        self.simplix_table = self._simplix_table_init()
        self.iterations = 0
        self._last_switched = (-1, -1)

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
    
    def _set_free(self, basis_vars: list[int]) -> list[int]:
        arr = []
        for i in range(1, len(self.F) - 1):
            if i not in basis_vars:
                arr.append(i)
        return arr

    def _simplix_table_init(self) -> list[list]:
        basis_vars = self._set_basis()
        free_vars = self._set_free(basis_vars)
        table = [[" ", "Sjo"]]
        # Fill first line
        for i in range(len(free_vars)):
            table[0].append(free_vars[i])
        # Fill every line
        # If coeff within i'th X < 0 -> inverse line
        for i in range(len(basis_vars)):
            table.append([basis_vars[i]])
            table[i + 1].append(
                Fraction(self.A[i][-1]) if self.A[i][basis_vars[i]] > 0 else Fraction(-self.A[i][-1])
                )
            for j in range(1, len(self.A[i]) - 1):
                if j not in basis_vars:
                    if self.A[i][basis_vars[i]] < 0:
                        self.A[i][j] = -self.A[i][j]
                    table[i + 1].append(Fraction(self.A[i][j]))
        # Fill last line (inverse all values)
        table.append(["F"])
        for i in range(len(self.F)):
            if i not in basis_vars:
                table[-1].append(Fraction(-self.F[i]))
        return table
    
    def print(self) -> None:
        matrix = []
        for i in range(len(self.simplix_table)):
            matrix.append([])
            for j in range(len(self.simplix_table[i])):
                if (i == 0 or j == 0) and type(self.simplix_table[i][j]) == int:
                    matrix[i].append("X{}".format(self.simplix_table[i][j]))
                else:
                    matrix[i].append(str(self.simplix_table[i][j]))
        if self._last_switched[0] > 0 and self._last_switched[1] > 0:
            matrix[self._last_switched[0]][0] = matrix[self._last_switched[0]][0].replace("X", "*X")
            matrix[0][self._last_switched[1]] = matrix[0][self._last_switched[1]].replace("X", "*X")
        matrix = list(tabulate.tabulate(matrix, tablefmt='simple_grid', stralign='right', showindex=False))
        if self._last_switched[0] > 0 and self._last_switched[1] > 0:
            self._bold_row_col(matrix)
        for ch in matrix:
            print(ch, end="")
        print()
                
    def _bold_row_col(self, matrix: list) -> None:
        current_row, current_col = 0, 0
        tmp = {
            '├': '┣',
            '─': '━',
            '┼': '╋',
            '┤': '┫',
            '│': '┃',
            '┐': '┓',
            '┘': '┛',
            '┬': '┳',
            '┴': '┻'
        }
        for i in range(len(matrix)):
            if matrix[i] == '\n':
                current_row += 1
                current_col = 0
            elif current_row in (self._last_switched[0] * 2, self._last_switched[0] * 2 + 1, self._last_switched[0] * 2 + 2):
                matrix[i] = tmp.get(matrix[i], matrix[i])
            if matrix[i] in ("┬", "│", "┼", "┴", "┐" "┘") and matrix[i - 1] != '\n':
                current_col += 1
            if current_col == self._last_switched[1] or (current_col == self._last_switched[1] + 1 and matrix[i] not in ('─', '┘', '┤', '┐')):
                matrix[i] = tmp.get(matrix[i], matrix[i])

    def solve(self) -> None:
        while not self._simplix_check():
            self.print()
        while not self._simplix_check_second():
            self.print()
        self._print_result()

    def _simplix_check(self) -> bool:
        for i in range(1, len(self.simplix_table) - 1):
            if self.simplix_table[i][1] < 0:
                perm_col = self._simplix_perm_col(i)
                perm_row = self._simplix_perm_row(self.simplix_table[i][perm_col], self.iterations == 0)
                self._log_state(perm_row, perm_col)
                self._simplix_step(perm_col, perm_row)
                self._last_switched = (perm_row, perm_col)
                self.iterations += 1
                return False
        return True
    
    def _simplix_check_second(self) -> bool:
        for i in range(2, len(self.simplix_table[-1])):
            if self.simplix_table[-1][i] > 0:
                perm_col = i
                perm_row = self._find_min_free_rel(self.simplix_table[-1][i])
                self._log_state(perm_row, perm_col)
                self._simplix_step(perm_col, perm_row)
                self._last_switched = (perm_row, perm_col)
                self.iterations += 1
                return False
        return True
    
    def _print_result(self) -> None:
        result = "#----- Optimal solution & target F -----#\n"
        # Add free variables to result string
        tmp = []
        for i in range(2, len(self.simplix_table[0])):
            tmp.append("X{}".format(str(self.simplix_table[0][i])))
        tmp.append("0")
        result += " = ".join(tmp) + "\n"

        # Add basis variables to result string
        for i in range(1, len(self.simplix_table) - 1):
            result += "X{} = {}{}".format(
                self.simplix_table[i][0],
                self.simplix_table[i][1],
                ", " if i != len(self.simplix_table) - 2 else "\n"
            )
            
        # Add F = ...
        result += "{} = {}".format(
            self.simplix_table[-1][0],
            self.simplix_table[-1][1],
        )
        result += "\n#---------------------------------------#"
        print(result)
    
    def _find_min_free_rel(self, el: int) -> int:
        min_value, min_index = 10**10, 1
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
        print("Итерация #{} | Разрешающая строка: {} | Разрешающий столбец: {}".format(self.iterations + 1, perm_row, perm_col))
