from simplix import Simplix
from config import F, A

def main() -> None:
    data = Simplix(
        F=F,
        A=A
    )
    data.print()
    data.solve()

if __name__ == "__main__":
    main()