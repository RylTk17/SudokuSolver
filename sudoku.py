import pickle


def pretty_list(a_list):
    for i in range(len(a_list)):
        print(a_list[i])


def make_default_list():
    default_list = []
    for row in range(9):
        temp = []
        for entry in range(9):
            temp.append(0)
        default_list.append(list(temp))
    return default_list


def start_solve():
    new_board = Board()
    # save/load
    solved_board = Solver(new_board.input_sudoku()).solve()
    print_sudoku(solved_board)


def print_sudoku(a_list):
    temp = []
    horiz_hyphen = " ------- ------- ------- "

    for i, row in enumerate(a_list, 1):
        if i == 1:
            print(horiz_hyphen)
        # Jeden 3ten Eintrag wird dieser mit dem vertikalen Trennstrich anführend gedruckt.
        for j, item in enumerate(row, 1):
            temp.append(str(item))
            if j % 3 == 0:
                print("| " + " ".join(temp), end=" ")
                temp.clear()
            if j % 9 == 0:
                print("|")

        if i % 3 == 0:
            print(horiz_hyphen)


class Board:
    def __init__(self, size=81, mn=0, mx=9):
        self.size = size
        self.min = mn
        self.max = mx
        self.list = make_default_list()

    def input_sudoku(self):
        for y in range(self.max):
            for x in range(self.max):
                print_sudoku(self.list)
                self.list[y][x] = self.set_value()
        return self.list

    def set_value(self):
        value = input("Zahl zwischen 1-9. Oder 0 zum frei lassen: ")
        if self.valid_input(value):
            return int(value)
        else:
            print("Keine gültige Eingabe.")
            return self.set_value()

    def valid_input(self, user_input):
        try:
            number = int(user_input)
        except ValueError:
            return False
        else:
            return self.min <= number <= self.max

    def save(self):
        with open("save.pickle", "wb") as handle:
            pickle.dump(self.list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open("save.pickle", "rb") as handle:
            self.list = pickle.load(handle)

    # def save_new(self):
    #     save_name = input("Sudoku speichern als (Ohne Dateiendung): ")
    #     with open(f"{save_name}.pickle", "wb") as handle:
    #         pickle.dump(self.list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #
    # def load_new(self):
    #     save_name = input("Sudoku laden (Ohne Dateiendung): ")
    #     with open(f"{save_name}.pickle", "rb") as handle:
    #         self.list = pickle.load(handle)

    def return_board(self):
        return self.list


class Solver:
    def __init__(self, sudoku_board):
        self.list = sudoku_board

    def solve(self):
        if self.solve_naked():
            if self.is_solved():
                print_sudoku(self.list)
                print("Board gelöst!")
        return self.list

    def solve_naked(self):
        for y, row in enumerate(self.list, 0):
            for x, item in enumerate(row, 0):
                if item == 0:
                    if self.add_single(self.fits_pos(x, y), x, y):
                        return self.solve_naked()
        return True

    def is_solved(self):
        for i in self.list:
            for j in i:
                if j == 0:
                    return False
        return True

    # def naked_singles_solve(self, x, y):
    #     """Naked Singles sind im Feld alleinstehende Zahlen. Wir fügen diese direkt in unser Soduku ein."""
    #     if self.add_single(self.fits_pos(x, y), x, y):
    #         return True
    #     return False

    def add_single(self, a_set, x, y):
        """Falls das Set, dass wir gereicht bekommen aus nur einem Wert besteht, wird dieser eingetragen. """
        if len(a_set) == 1:
            self.list[y][x] = next(iter(a_set))
            return True
        return False

    def fits_pos(self, x, y, possible_num=None):
        """Hier werden die passenden Zahlen für die angegebene Position im Feld ermittelt und weitergereicht."""
        if possible_num is None:
            possible_num = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        # row / Reihe
        for i in range(len(self.list[y])):  # 9
            for j in range(1, 10):
                if self.list[y][i] == j and j in possible_num:
                    possible_num.remove(j)
        # column / spalte
        for i in range(len(self.list[x])):  # 9
            for j in range(1, 10):
                if self.list[i][x] == j and j in possible_num:
                    possible_num.remove(j)
        # square / Quadrat
        x_ganz = (x//3) * 3
        y_ganz = (y//3) * 3
        for i in range(3):
            for j in range(3):
                for k in range(1, 10):
                    if self.list[y_ganz+i][x_ganz+j] == k and k in possible_num:
                        possible_num.remove(k)

        return possible_num


start_solve()
input()
