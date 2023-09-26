from config import F, A

x_counter = len(A) - 1

class Simplix:
    def __init__(self, F: list[int], A: list[list[int]]) -> None:
        self.F = F
        self.A = A
        self.x_counter = len(A)
        self.basis_vars = self.set_basis()
        self.free_vars = self.set_free()

        self.simplix_table = self.simplix_table_init()

    def simplix_table_init(self) -> list[list]:
        table = [[" ", "Sjo"]]
        # Fill first line
        for i in range(len(self.free_vars)):
            table[0].append(self.free_vars[i])
        # Fill every line
        # If coeff within i'th X < 0 -> inverse line
        for i in range(len(self.basis_vars)):
            table.append([self.basis_vars[i]])
            table[i + 1].append(
                self.A[i][-1] if self.A[i][self.basis_vars[i]] > 0 else -self.A[i][-1]
                )
            for j in range(1, len(self.A[i]) - 1):
                if j not in self.basis_vars:
                    if self.A[i][self.basis_vars[i]] < 0:
                        self.A[i][j] = -self.A[i][j]
                    table[i + 1].append(self.A[i][j])
        # Fill last line (inverse all values)
        table.append(["F"])
        for i in range(len(self.F)):
            if i not in self.basis_vars:
                table[-1].append(-self.F[i])
        return table
    
    def simplix_check(self) -> None:
        for i in range(1, len(self.simplix_table) - 1):
            if self.simplix_table[i][1] < 0:
                perm_col = self.simplix_perm_col(i)
                perm_row = self.simplix_perm_row(self.simplix_table[i][perm_col])
                print(perm_row, perm_col)
                break

    def simplix_perm_col(self, row_index: int) -> int:
        for i in range(2, len(self.simplix_table[row_index])):
            if self.simplix_table[row_index][i] < 0:
                return i
            
    def simplix_perm_row(self, el: int, first_iter: bool = True) -> int:
        min_value, min_index = 10**10, 1
        for i in range(1, len(self.simplix_table) - 1):
            value = self.simplix_table[i][1] / el
            if value < min_value and ((value > 0 and first_iter) or (value >= 0 and not first_iter)):
                min_value, min_index = value, i
        return min_index


    def print(self) -> None:
        s = []
        for i in range(len(self.simplix_table)):
            s.append([])
            for j in range(len(self.simplix_table[i])):
                if (i == 0 or j == 0) and type(self.simplix_table[i][j]) == int:
                    s[i].append("X{}".format(self.simplix_table[i][j]))
                else:
                    s[i].append(str(self.simplix_table[i][j]))
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))

    def set_basis(self) -> list[int]:
        result = []
        for i in range(len(self.A)):
            result.append(
                self.basis_loop(self.A[i])
            )
        return result
    
    def basis_loop(self, line: list[int]) -> int:
        for i in range(len(line) - 2, 0, -1):
            if line[i] != 0: return i
    
    def set_free(self) -> list[int]:
        result = []
        for i in range(1, len(self.F) - 1):
            if i not in self.basis_vars:
                result.append(i)
        return result

def main() -> None:
    data = Simplix(
        F=F,
        A=A
    )
    data.print()
    data.simplix_check()

if __name__ == "__main__":
    main()