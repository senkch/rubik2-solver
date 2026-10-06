import numpy as np

class Cubik2:
    def __init__(self):
        """Симулятор кубика рубика 2x2"""
        # изнчально все 8 углов на своем месте, 0-3 верхние, 4-7 нижние
        # считаем по часовой от заднего левого
        # i стоит над i+4
        self.corners = np.arange(8)
        # 0 - цвет верхней/нижней грани смотрит вверх или вниз
        # 1 - цвет верхней/нижней грани смотрит влево или вправо
        # 2 - цвет верхней/нижней грани смотрит назад или вперед
        self.rotation = np.zeros(8,dtype=int)

    def move(self, m : str) -> None:
        """Выполняет ход по нотации Сингмастера (без обратных)"""
        moves = {
        'R': [[1, 2, 5, 6], [2, 6, 1, 5], 0, 2],
        'L': [[0, 3, 4, 7], [4, 0, 7, 3], 0, 2],

        'U': [[0, 1, 2, 3], [3, 0, 1, 2], 1, 2],
        'D': [[4, 5, 6, 7], [5, 6, 7, 4], 1, 2],

        'F': [[2, 3, 6, 7], [3, 7, 2, 6], 0, 1],
        'B': [[0, 1, 4, 5], [1, 5, 0, 4], 0, 1],
        }

        isReverse = False

        if len(m) == 1:
            m = m.upper()
        elif len(m) == 2 and m[1] == "'":
            m = m[0].upper()
            isReverse = True
        else:
            raise ValueError(f"Неверное значение хода: {m}")
        if m not in moves:
            raise ValueError(f"Неверное значение хода: {m}")

        if isReverse:
            for _ in range(3):
                self.move(m)
        else:
            move = moves[m]
            self.corners[move[0]] = self.corners[move[1]]
            self.rotation[move[0]] = self.rotation[move[1]]
            for i in move[0]:
                if self.rotation[i] == move[2]:
                    self.rotation[i] = move[3]
                elif self.rotation[i] == move[3]:
                    self.rotation[i] = move[2]

    def moves(self, moves : str) -> None:
        """Выполняет серию ходов по нотации Сингмастера (без обратных)"""
        for m in moves:
            self.move(m)

    def rotate(self, r : int) -> None:
        """Переворачивает весь кубик"""
        r = str(r)
        rotations = {
        '0': [[3, 2, 6, 7, 0, 1, 5, 4], 0, 2],
        '1': [[3, 0, 1, 2, 7, 4, 5, 6], 1, 2],
        '2': [[4, 0, 3, 7, 5, 1, 2, 6], 0, 1],
        }
        if r not in rotations:
            raise ValueError(f"Неверное значение поворота: {r}")
        rotat = rotations[r]
        self.corners = self.corners[rotat[0]]
        self.rotation = self.rotation[rotat[0]]
        for i in rotat[0]:
            if self.rotation[i] == rotat[1]:
                self.rotation[i] = rotat[2]
            elif self.rotation[i] == rotat[2]:
                self.rotation[i] = rotat[1]

    def isSolved(self) -> bool:
        """Проверяет собран ли кубик"""
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    c = Cubik2()
                    c.corners = self.corners.copy()
                    c.rotation = self.rotation.copy()
                    for _ in range(i):  c.rotate(0)
                    for _ in range(j):  c.rotate(1)
                    for _ in range(k):  c.rotate(2)
                    check1 = (c.corners == np.array([i for i in range(8)]))
                    check2 = (c.rotation == np.array([0 for _ in range(8)]))
                    if np.all(check1 & check2):
                        return True
        return False

    def scramble(self, n : int = 40, seed : int | None = None) -> None:
        """Разбирает кубик на n шагов заданных сидом seed"""
        moves = np.array(["R","L","U","D","F","B",
                        "R'", "L'","U'","D'","F'","B'"])
        rng = np.random.default_rng(seed=seed)
        res = rng.choice(moves, size=n)
        self.moves(res)
        if self.isSolved():
            self.move(rng.choice(moves))



