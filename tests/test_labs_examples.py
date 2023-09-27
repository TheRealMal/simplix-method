import pytest

from src.simplix import Simplix

class TestLabsExamples:
    def test_lab_1(self):
        F = [0,-1,1,0,0,0]
        A = [
            [0, 1, -2, 1,  0, 0, 2],
            [0, 2, -1, 0, -1, 0, 2],
            [0, 1,  1, 0,  0, 1, 5]
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
            [0, 3, 1, -4, -1, 1, 0, -3],
            [0, -2, -4, -1, 1, 0, 1, -3]
        ]
        a = Simplix(F, A)
        a.solve()
        assert str(a.simplix_table[1][1]) == "15/17" 
        assert str(a.simplix_table[2][1]) == "9/17"
        assert str(a.simplix_table[3][1]) == "36" 