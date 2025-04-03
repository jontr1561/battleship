"""This program runs through a game of battlehship with two players given the board creation information from a file
"""
from battleship.files import Files
from battleship.player import Player
from battleship.board import Board


def getting_board_info() -> (int, int, dict):
    """This function iterates through a file and saves the information about the dimensions of the battleship board as
    well as information regarding the ships
        Parameters: None
        Returns:
            rows (int): the number of rows of the board
            columns (int): the number of columns of the board
            ship_dict (dict): a dictionary with the letter representing the ship as keys and the number of spaces it
            takes up as values
    """
    file_path = Files()
    file = file_path.get_file("Please enter the path to the configuration file for this game: ")
    line_count = 0
    ship_dict = {}
    with open(file, 'r') as configuration:
        for line in configuration:
            line_count += 1
            if line_count == 1:
                rows = int(line)
            if line_count == 2:
                columns = int(line)
            if line_count == 3:
                continue
            if line_count >= 4:
                ship_info = line.split()
                character = ship_info[0]
                size = int(ship_info[1])
                ship_dict[character] = size
        ship_dict = dict(sorted(ship_dict.items(), key=lambda item: item[0]))
    return rows, columns, ship_dict


def creating_placement_board(rows: int, columns: int) -> Board:
    """This functions creates a battleship board by using the Board class that acts like a nested list
        Parameters:
            rows (int): the number of rows of the board
            columns (int): the number of columns of the board
        Returns:
            placement_board (Board): the created battleship board
    """
    placement_board = Board(rows, columns)
    return placement_board


def display_board(placement_board: Board) -> None:
    """This functions displays the battleship board on the screen
        Parameters:
            placement_board (Board): a battleship board
        Returns: None
    """
    print(' ', *range(len(placement_board[0])))
    for pos, row in list(enumerate(placement_board)):
        print(pos, *row)


def making_two_boards(placement_board: Board) -> (list[list[str]], list[list[str]]):
    """Creates each player's placement board
        Parameters:
            placement_board (Board): a battleship board
        Returns:
            placement_board1 (list[list[str]]): player 1's placement board
            placement_board2 (list[list[str]]): player 2's placement board
    """
    placement_board1 = [row[:] for row in placement_board]
    placement_board2 = [row[:] for row in placement_board]
    return placement_board1, placement_board2


def create_firing_boards(placement_board: Board) -> (list[list[str]], list[list[str]]):
    """Creates each player's firing board
        Parameters:
            placement_board (Board): a battleship board
        Returns:
            placement_board1 (list[list[str]]): player 1's firing board
            placement_board2 (list[list[str]]): player 2's firing board
    """
    firing_board1 = [row[:] for row in placement_board]
    firing_board2 = [row[:] for row in placement_board]
    return firing_board1, firing_board2


def get_orientation(player: str, letter: str, size: int) -> str:
    """This functions asks the player to choose the orientation of the ship they are currently placing on their board
        Parameters:
            player (str): the player who's currently placing the ship
            letter (str): the letter that represents the ship
            size (int): the amount of space that the ship takes up on the board
        Returns:
            orientation (str): the orientation of the ship they are currently placing on their board
    """
    v = 'vertically'
    h = 'horizontally'
    orientation = 0
    while True:
        try:
            orientation = input(f'{player}, enter the orientation of your {letter}, which is {size} long: ')
            orientation = orientation.lower()
            if h.startswith(orientation):
                orientation = 'horizontal'
                break
            if v.startswith(orientation):
                orientation = 'vertical'
                break
            else:
                continue
        except ValueError:
            continue
    return orientation


def get_placement(player: str, letter: str, size: int, board: list[list[str]]) -> (int, int, str):
    """Gets the coordinate of where to place the ship on the placement board
        Parameters:
            player (str): the player who's currently placing the ship
            letter (str): the letter that represents the ship
            size (int): the amount of space that the ship takes up on the board
            board (list[list[str]]): the board that the player is currently placing the ship on
        Returns:
            row (int): the row of the coordinate of where the ship will be placed
            column (int): the column of the coordinate of where the ship will be placed
            orientation (str): the orientation of the ship they are currently placing on their board
    """
    while True:
        try:
            orientation = get_orientation(player, letter, size)
            position = input(f"Enter the starting location for your {letter}, which is {size} long, in the form row col: ")
            position = position.split(' ')
            row, col = int(position[0]), int(position[1])
            if orientation == 'horizontal':
                separate_row = board[row]
                end = col + size + 1
                sublist = separate_row[col: col + end]
                count = 0
                for spot in sublist:
                    if spot == '*':
                        count += 1
                    else:
                        break
                    if count == size:
                        return row, col, orientation
            if orientation == 'vertical':
                vert_count = 0
                end = col + size + 1
                for rows in board[row: row + end]:
                    if rows[col] == '*':
                        vert_count += 1
                    else:
                        break
                    if vert_count == size:
                        return row, col, orientation
        except ValueError:
            continue
        except IndexError:
            continue


def create_player_dict(player1: str, player2: str, placement1: list[list[str]] , placement2: list[list[str]],
                       firing1: list[list[str]], firing2: list[list[str]]):
    """This function creates a dictionary associating each player with their respective placement board and firing board
        Parameters:
            player1 (str): the first player
            player2 (str): the second player
            placement1 (list[list[str]]): player 1's placement board
            placement2 (list[list[str]]): player 2's placement board
            firing1 (list[list[str]]): player 1's firing board
            firing2 (list[list[str]]): player 2's firing board
        Returns:
            player_dict (dict): a dictionary associating each player with their respective placement board and firing
            board
    """
    player_dict = {
        player1: (placement1, firing1),
        player2: (placement2, firing2)
    }
    return player_dict


def place_ship(player_dict: dict, ship_dict: dict) -> dict:
    """This function places the ships onto each player's placement boards
        Parameters:
            player_dict (dict): a dictionary associating each player with their respective placement board and firing board
            ship_dict (dict): a dictionary with each ship's letter being the key and space being the value
        Returns:
            player_dict (dict): a dictionary associating each player with their respective placement board and firing board with the ships placed on their placement board
    """
    for player, board in player_dict.items():
        print(f'{player}\'s Placement Board')
        display_board(board[0])
        board = board[0]
        for letter, size in ship_dict.items():
            row, col, orientation = get_placement(player, letter, size, board)
            if size == 1:
                board[row][col] = letter
                print(f'{player}\'s Placement Board')
                display_board(board)
            elif orientation == 'vertical':
                end = col + size + 1
                count = 0
                for rows in board[row: end]:
                    count += 1
                    rows[col] = letter
                    if count == size:
                        break
                print(f'{player}\'s Placement Board')
                display_board(board)
            elif orientation == 'horizontal':
                col_index = col - 1
                for times in range(size):
                    col_index += 1
                    board[row][col_index] = letter
                print(f'{player}\'s Placement Board')
                display_board(board)
    return player_dict


def turn_change(current_turn: int) -> int:
    """This function changes the turns in the game
        Parameters:
            current_turn (int): the current turn
        Returns:
            turn (int): the new turn
    """
    if current_turn == 1:
        turn = 2
    if current_turn == 2:
        turn = 1
    return turn


def check_win(placement_board: list[list[str]]) -> bool:
    """This function checks if a player has won the game
        Parameters:
            placement_board (list[list[str]]): the current player's placement board
        Returns:
            bool: True if a player has won the game, false otherwise
    """
    win_con = ['X', 'O', '*']
    for row in placement_board:
        for element in row:
            if element not in win_con:
                return False
    else:
        return True


def valid_fire(player: str, rows: int, columns: int, fire_list: list) -> (int, int, str):
    """Functions checks if a firing coordinate is valid, and if it is, returns the coordinates
        Parameters:
            player (str): the player who's currently firing
            rows (int): the number of rows on the board
            columns (int): the number of columns on the board
            fire_list (list): a list of coordinates that has already been fired at by that player
        Returns:
            row (int): the row of the coordinate to be fired at
            column (int): the column of the coordinate to be fired at
            coord (str): the coordinates of the firing coordinate
    """
    while True:
        try:
            coord = input(f'{player}, enter the location you want to fire at in the form row col: ')
            if coord in fire_list:
                continue
            coord_split = coord.split(' ')
            row, col = int(coord_split[0]), int(coord_split[1])
            if 0 <= row <= rows - 1 and  0 <= col <= columns - 1:
                fire_list.append(coord)
                return row, col, coord
        except ValueError:
            continue
        except IndexError:
            continue


def check_sink(placement_board: list[list[str]], letter: str) -> bool:
    """This function checks if a boat has been destroyed after a turn of firing
        Parameters:
            placement_board (list[list[str]]): the opposing player's placement board
            letter (str): the letter that represents the boat we are checking
        Returns:
            bool: True if a boat has been destroyed, False otherwise
    """
    for row in placement_board:
        for element in row:
            if element == letter:
                return False
    else:
        return True


def firing(player_dict: dict, rows: int, columns: int) -> None:
    """This function conducts the action of each player taking a turn and firing at each other's placement boards and doen't stop until the game ends
        Parameters:
            player_dict (dict): a dictionary associating each player with their respective placement board and firing board
            rows (int): the number of rows on the board
            columns (int): the number of columns on the board
        Returns: None
    """
    win = False
    fire_list1 = []
    fire_list2 = []
    while win != True:
        turn = 1
        player1, boards1 = list(player_dict.items())[0]
        player2, boards2 = list(player_dict.items())[1]
        placement_board1 = boards1[0]
        firing_board1 = boards1[1]
        placement_board2 = boards2[0]
        firing_board2 = boards2[1]
        if turn == 1:
            print(f'{player1}\'s Firing Board')
            display_board(firing_board1)
            print(f'{player1}\'s Placement Board')
            display_board(placement_board1)
            row, col, coord = valid_fire(player1, rows, columns, fire_list1)
            fire_list1.append(coord)
            if placement_board2[row][col] == '*':
                print(f'{player1} missed.')
                firing_board1[row][col] = 'O'
                placement_board2[row][col] = 'O'
            else:
                letter = placement_board2[row][col]
                print(f'{player1} hit {player2}\'s {letter}!')
                firing_board1[row][col] = 'X'
                placement_board2[row][col] = 'X'
                check_sink(placement_board2, letter)
                if check_sink(placement_board2, letter) == True:
                    print(f'{player1} destroyed {player2}\'s {letter}!')
        win = check_win(placement_board2)
        turn = turn_change(turn)
        if win == True:
            if turn == 2:
                print(f'{player1}\'s Firing Board')
                display_board(firing_board1)
                print(f'{player1}\'s Placement Board')
                display_board(placement_board1)
                print(f'{player1} won!')
            break
        if turn == 2:
            print(f'{player2}\'s Firing Board')
            display_board(firing_board2)
            print(f'{player2}\'s Placement Board')
            display_board(placement_board2)
            row, col, coord = valid_fire(player2, rows, columns, fire_list2)
            fire_list2.append(coord)
            if placement_board1[row][col] == '*':
                print(f'{player2} missed.')
                firing_board2[row][col] = 'O'
                placement_board1[row][col] = 'O'
            else:
                letter = placement_board1[row][col]
                print(f'{player2} hit {player1}\'s {letter}!')
                firing_board2[row][col] = 'X'
                placement_board1[row][col] = 'X'
                check_sink(placement_board1, letter)
                if check_sink(placement_board1, letter) == True:
                    print(f'{player2} destroyed {player1}\'s {letter}!')
        win = check_win(placement_board1)
        turn = turn_change(turn)
        if win == True:
            print(f'{player2}\'s Firing Board')
            display_board(firing_board2)
            print(f'{player2}\'s Placement Board')
            display_board(placement_board2)
            if turn == 1:
                print(f'{player2} won!')
            break


def main() -> None:
    """ The main function of the program that runs through the entire game
        Parameters: None
        Returns: None
    """
    rows, columns, ship_dict = getting_board_info()
    placement_board = creating_placement_board(rows, columns)
    placement_board1, placement_board2 = making_two_boards(placement_board)
    firing_board1, firing_board2 = create_firing_boards(placement_board)
    name_place = Player()
    players = name_place.asking_name()
    player1, player2 = players
    player_dict = create_player_dict(player1, player2, placement_board1, placement_board2, firing_board1, firing_board2)
    player_dict_finished = place_ship(player_dict, ship_dict)
    firing(player_dict, rows, columns)


main()
