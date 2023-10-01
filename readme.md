# Simplix method
Симплекс-метод для поиска оптимального решения задачи линейного программирования.  

Данный репозиторий подойдет для случаев, когда число линейно независимых уравнений равно $m$, а число переменных равно $n + m$. В остальных случаях СЛАУ либо имеет единственное решение, либо несовместна.  

<p align="center"><img src="/misc/example.png" width="300"></p>  

## Принцип работы
У нас имеется **F** - целевая функция и **A** - матрица системы ограничений или матрица коэффициентов СЛАУ.  
F и СЛАУ приведены к канонической форме:
```math
F = c_1x_1 + c_2x_2 + \dots + c_{n+m} \to min
```
```math
\begin{cases}
a_{11}x_1 + a_{12}x_2 + \dots + a_{1(n+m)}x_{n+m} = b_1 \\
a_{21}x_1 + a_{22}x_2 + \dots + a_{2(n+m)}x_{n+m} = b_2 \\
\vdots \\
a_{m1}x_1 + a_{m2}x_2 + \dots + a_{m(n+m)}x_{n+m} = b_m
\end{cases}
```
Соответственно **F** выглядит так
```math
\begin{pmatrix}
c_1 & c_2 & \dots & c_{n+m}
\end{pmatrix}
```
и **A** выглядит так
```math
\begin{pmatrix}
a_{11} & a_{12} & \dots  & a_{1(n+m)} & b_1    \\
a_{21} & a_{22} & \dots  & a_{2(n+m)} & b_2    \\
\vdots & \vdots & \vdots & \ddots     & \vdots \\
a_{m1} & a_{m2} & \dots  & a_{m(n+m)} & b_m    \\
\end{pmatrix}
```
Программа проходит два этапа:
1. Поиск опорного решения
2. Поиск оптимального решения  

Преобразования коэффициентов в симплексной таблице  производятся используя *жордановы исключения* (это когда мы меняем переменные местами и, соответственно, меняем базис)
## Конфигурация src/config.py
- В переменную F вводим коэффиценты при $x$ в целевой функции.
- В переменную A вводим матрицу коэффицентов при $x$ СЛАУ и вектор правой части системы ограничений так, чтобы он являлся последним столбцом матрицы (см. выше).
## Команды
```console
# Установка
git clone https://github.com/TheRealMal/simplix-method.git
cd simplix-method
pip install -r requirements.txt

# Тесты
pytest

# Запуск
python3 src/main.py

# Запуск телеграм бота 
# В директории src создать файл bot_token.py и в нем создать переменную bot_token = "ВАШ_ТОКЕН"
python3 src/bot.py
```
