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
    new_board.input_sudoku()
    #new_board.save()
    #new_board.load()
    solved_board = Solver(new_board.return_board())
    solved_board.solve()


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

    def get_row(self, y):
        row = [self.list[y][i] for i in range(9)]
        return row

    def get_column(self, x):
        column = [self.list[i][x] for i in range(9)]
        return column

    def get_square(self, x, y):
        x_ganz = (x//3) * 3
        y_ganz = (y//3) * 3

        square = [self.list[y_ganz+i][x_ganz+j] for i in range(3) for j in range(3)]
        return square

        # for i in range(3):
        #     for j in range(3):
        #         square.append(self.list[y_ganz+i][x_ganz+j])
        # return square

    def is_solved(self):
        for i in self.list:
            for j in i:
                if j == 0:
                    return False
        return True

    def solve(self):
        while True:
            if self.is_solved():
                break
            if self.solve_naked_single():
                continue
            if self.solve_hidden_single():
                continue
            break
        print_sudoku(self.list)
        if self.is_solved():
            print("Board gelöst!")
        else:
            print("Board konnte nicht gelöst werden")
        return self.list

    # Singles
    def add_single(self, a_set, x, y):
        """Falls das Set, dass wir gereicht bekommen aus nur einem Wert besteht, wird dieser eingetragen. """
        if len(a_set) == 1:
            self.list[y][x] = next(iter(a_set))
            return True
        return False

    def solve_naked_single(self):
        """Naked Singles sind im Feld alleinstehende Zahlen. Wir fügen diese direkt in unser Soduku ein."""
        for y, row in enumerate(self.list, 0):
            for x, item in enumerate(row, 0):
                if item == 0:
                    if self.add_single(self.fits_pos(x, y), x, y):
                        return True
        return False

    def fits_pos(self, x, y, possible_num=None):
        """Hier werden die passenden Zahlen für die angegebene Position im Feld ermittelt und weitergereicht."""
        if possible_num is None:
            possible_num = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        row = self.get_row(y)
        column = self.get_column(x)
        square = self.get_square(x, y)
        rcs = row, column, square

        for i in rcs:
            for j, item in enumerate(i):
                if i[j] in possible_num:
                    possible_num.remove(item)

        return possible_num

    # hidden singles
    def solve_hidden_single(self):
        for y, row in enumerate(self.list, 0):
            for x, item in enumerate(row, 0):
                if item == 0:
                    if self.add_single(self.h_s(x, y), x, y):
                        return True
        return False

    def h_s(self, x, y):
        current_pos = self.fits_pos(x, y)
        row, column, square = self.get_row(y), self.get_column(x), self.get_square(x, y)

        row_possible = set()
        for i, item in enumerate(row, 0):
            if item == 0 and i != x:
                row_possible |= self.fits_pos(i, y)
        all_row = current_pos - row_possible
        if len(all_row) == 1:
            return all_row

        column_possible = set()
        for i, item in enumerate(column, 0):
            if item == 0 and i != y:
                column_possible |= self.fits_pos(x, i)
        all_column = current_pos - column_possible
        if len(all_column) == 1:
            return all_column

        square_possible = set()
        x_ganz = (x // 3) * 3
        y_ganz = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.list[y_ganz+i][x_ganz+j] == 0 and (x, y) != (x_ganz+j, y_ganz+i):
                    square_possible |= self.fits_pos(x_ganz+j, y_ganz+i)
        all_square = current_pos - square_possible
        if len(all_square) == 1:
            return all_square
        return current_pos


start_solve()
input()
