class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = self._create_board(rows, columns)

    def _create_board(self, rows, columns):
        placement_board = []
        for row in range(rows):
            row_list = ["*"] * columns
            placement_board.append(row_list)
        return placement_board

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def __delitem__(self, index):
        del self.board[index]

    def __len__(self):
        return len(self.board)

    def __repr__(self):
        return '\n'.join([' '.join(row) for row in self.board])

    def clear_board(self):
        self.board = self._create_board(self.rows, self.columns)
