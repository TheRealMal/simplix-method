import pytest

from src.simplix import Simplix

class TestLabsExamples:
    def test_lab_1(self):
        F = [0,-1,1,0,0,0]
        A = [
            [1, -2, 1,  0, 0, 2],
            [2, -1, 0, -1, 0, 2],
            [1,  1, 0,  0, 1, 5]
        ]
        a = Simplix(F, A)
        a.solve()
        assert str(a.simplix_table[1][1]) == "1" 
        assert str(a.simplix_table[2][1]) == "5"
        assert str(a.simplix_table[3][1]) == "4"
        assert str(a.simplix_table[4][1]) == "-3" 
    
    def test_lab_2(self):
        F = [0,4,18,30,5,0,0]
        A = [
            [3, 1, -4, -1, 1, 0, -3],
            [-2, -4, -1, 1, 0, 1, -3]
        ]
        a = Simplix(F, A)
        a.solve()
        assert str(a.simplix_table[1][1]) == "15/17" 
        assert str(a.simplix_table[2][1]) == "9/17"
        assert str(a.simplix_table[3][1]) == "36"

    # def test_lab_3_1(self):
    #     F = [0,5,6,4,0,0,0]
    #     A = [
    #         [1, 1, 1, 1, 0, 0, 7],
    #         [1, 3, 0, 0, 1, 0, 8],
    #         [0, 0.5, 4, 0, 0, 1, 6]
    #     ]
    #     a = Simplix(F, A)
    #     a.solve()
    #     assert str(a.simplix_table[1][1]) == "7" 
    #     assert str(a.simplix_table[2][1]) == "8"
    #     assert str(a.simplix_table[3][1]) == "6" 
    
    # def test_lab_3_2(self):
    #     F = [0,2,5,3,0,0,0]
    #     A = [
    #         [2, 1, 2, 1, 0, 0, 6],
    #         [1, 2, 0, 0, 1, 0, 6],
    #         [0, 0.5, 1, 0, 0, 1, 2]
    #     ]
    #     a = Simplix(F, A)
    #     a.solve()
    #     assert str(a.simplix_table[1][1]) == "6" 
    #     assert str(a.simplix_table[2][1]) == "6"
    #     assert str(a.simplix_table[3][1]) == "2" 