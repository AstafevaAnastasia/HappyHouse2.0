import random
import PyQt5
from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtMultimedia import QSoundEffect
import sys

def create_board(size: int) -> list:
    """
    Creates a Tic Tac Toe board of specified size.
    """
    return [[' ' for _ in range(size)] for _ in range(size)]

def print_board(board: list):
    """
    Prints the current state of the board.
    """
    size = len(board)
    cnt = 1
    print("  " + " ".join(list(map(str, (range(1, size+1))))))
    for row in board:
        print(f"{cnt} " + "|".join(row))
        print("  " + "-" * (size * 2 - 1))
        cnt += 1

def get_player_move(board: list) -> tuple:
    """
    Gets the player's move coordinates.
    """
    size = len(board)
    while True:
        try:
            row, col = map(int, input("Enter row and column (1-{}): ".format(size)).split())
            if 1 <= row <= size and 1 <= col <= size and board[row-1][col-1] == ' ':
                return row-1, col-1
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

def get_ai_move(board: list, player_symbol: str, ai_symbol: str, fail_chance: float = 0.1) -> tuple:
    
    size = len(board)
    win_condition = 4 if size > 3 else 3

    # 0. Check if AI moves randomly
    if random.random() <= fail_chance:
        available_moves = [(i, j) for i in range(size) for j in range(size) if board[i][j] == ' ']
        #print("Check 0")
        return random.choice(available_moves)

    # 1. Check if AI can win in the next move
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = ai_symbol  # Temporarily place the AI symbol
                if check_win(board, ai_symbol):
                    #print("Check 1")
                    return i, j
                board[i][j] = ' '  # Reset the cell
    
    # 2. Check if the player is about to win and block
    # TODO: Instead of two loops, write down i, j into the list and prioritise ones that are from depth 1
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = player_symbol  # Temporarily place the player symbol
                if check_win(board, player_symbol):
                    #print("Check 2 depth 1")
                    board[i][j] = ' '  # Reset the cell
                    return i, j
                board[i][j] = ' '  # Reset the cell

    if win_condition != 3:
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = player_symbol  # Temporarily place the player symbol 
                    for i2 in range(size):
                        for j2 in range(size):
                            if board[i2][j2] == ' ':
                                board[i2][j2] = player_symbol
                                if check_win(board, player_symbol):
                                    #print("Check 2 depth 2")
                                    board[i][j] = ' '  # Reset the cell
                                    board[i2][j2] = ' '  # Reset the cell
                                    return i2, j2
                                board[i2][j2] = ' '
                    board[i][j] = ' '  # Reset the cell
                   

    # 3. Try to create a row of AI symbols
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = ai_symbol
                if check_potential_win(board, ai_symbol, win_condition - 1):
                    #print("Check 3")
                    return i, j
                board[i][j] = ' '

    # 4. If no strategic move, choose randomly
    available_moves = [(i, j) for i in range(size) for j in range(size) if board[i][j] == ' ']
    #print("Check 4")
    return random.choice(available_moves)

def check_potential_win(board: list, symbol: str, consecutive_count: int) -> bool:
    """
    Checks if placing the symbol at any empty cell would create 
    a row with the specified number of consecutive symbols.
    """
    size = len(board)

    # Check rows and columns
    for i in range(size):
        count_row = 0
        count_col = 0
        for j in range(size):
            if board[i][j] == symbol:
                count_row += 1
            else:
                count_row = 0
            if board[j][i] == symbol:
                count_col += 1
            else:
                count_col = 0
            if count_row == consecutive_count or count_col == consecutive_count:
                #print(f"Player wins on row {i} col {j}")
                return True

    # Check diagonals (top-left to bottom-right)
    for i in range(size - consecutive_count + 1):
        count = 0
        for k in range(consecutive_count):
            if board[i+k][i+k] == symbol:
                count += 1
            else:
                count = 0
        if count == consecutive_count:
            #print(f"Player wins on {i} diag top-left to bottom-right")
            return True

    # Check diagonals (bottom-left to top-right)
    for i in range(consecutive_count - 1, size):
        count = 0
        for k in range(consecutive_count):
            if board[i-k][k] == symbol:
                count += 1
            else:
                count = 0
        if count == consecutive_count:
            #print(f"Player wins on {i} diag bottom-left to top-right")
            return True

    return False

def check_win(board: list, symbol: str) -> bool:
    """
    Checks if the given symbol has won the game.
    """
    size = len(board)
    win_condition = 4 if size >= 4 else 3

    # Check rows
    for row in board:
        for i in range(size - win_condition + 1):
            if all(row[i+k] == symbol for k in range(win_condition)):
                return True

    # Check columns
    for col in range(size):
        for i in range(size - win_condition + 1):
            if all(board[i+k][col] == symbol for k in range(win_condition)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(size - win_condition + 1):
        for col in range(size - win_condition + 1):
            if all(board[row+k][col+k] == symbol for k in range(win_condition)):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(win_condition - 1, size):
        for col in range(size - win_condition + 1):
            if all(board[row-k][col+k] == symbol for k in range(win_condition)):
                return True

    return False

def is_board_full(board: list) -> bool:
    """
    Checks if the board is full.
    """
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game(size: int):
    """
    Main game loop.
    """
    board = create_board(size)
    player_symbol = 'X'
    ai_symbol = 'O'
    player_turn = True
    while True:
        print_board(board)

        if player_turn:
            row, col = get_player_move(board)
            board[row][col] = player_symbol
        else:
            row, col = get_ai_move(board, player_symbol, ai_symbol)
            board[row][col] = ai_symbol
            print("AI played at ({}, {})".format(row+1, col+1))

        if check_win(board, player_symbol):
            print_board(board)
            print("You win!")
            break
        elif check_win(board, ai_symbol):
            print_board(board)
            print("AI wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

        player_turn = not player_turn


#* =========================
#* Functions, related to UI:
#* =========================

#* GLOBAL VARIABLES
VOLUME = 0.5
FAIL_CHANCE = 0.1
#* ================

class start_ui(QtWidgets.QWidget):

    def __init__(self):
        super(start_ui, self).__init__()
        uic.loadUi("start.ui", self)


        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(4)
        shadow.setYOffset(4)

        self.setStyleSheet("background-color: #545454;")
        self.playButton.setStyleSheet("color: #98be03;")
        self.playButton.setGraphicsEffect(shadow)

        self.playButton.clicked.connect(self.create_main_window)
    
    def create_main_window(self):
        main_window = main_ui()
        main_window.show()
        self.close()


class main_ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(main_ui, self).__init__()
        uic.loadUi("main.ui", self)

        shadow1 = QtWidgets.QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(4)
        shadow1.setXOffset(4)
        shadow1.setYOffset(4)
        shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(4)
        shadow2.setXOffset(4)
        shadow2.setYOffset(4)

        self.setStyleSheet("background-color: #545454;")
        self.playAI.setStyleSheet("color: #98be03;")
        self.playAI.setGraphicsEffect(shadow1)
        self.playFriend.setStyleSheet("color: #98be03;")
        self.playFriend.setGraphicsEffect(shadow2)
        self.radiobtn3x3.setStyleSheet("color: #98be03;")
        self.radiobtn5x5.setStyleSheet("color: #98be03;")


        self.playAI.clicked.connect(lambda: self.play_game(against_ai=True))
        self.playFriend.clicked.connect(lambda: self.play_game(against_ai=False))

        self.musicBtn.clicked.connect(self.play_music)
        self.musicBtn.setStyleSheet("background-image: url('music_off.png');")

        self.music = QSoundEffect()
        self.music.setSource(QtCore.QUrl.fromLocalFile("all_star.wav"))
        self.music.setLoopCount(QSoundEffect.Infinite)
        self.music.setVolume(VOLUME)

    def play_game(self, against_ai=True):
        if self.radiobtn3x3.isChecked():
            board_size = 3
        elif self.radiobtn5x5.isChecked():
            board_size = 5
        
        self.play_window = play_ui(board_size=board_size, against_ai=against_ai, fail_chance=0.05)
        self.play_window.show()
        
    def play_music(self):
        if self.sender().isChecked():
            self.sender().setStyleSheet("background-image: url('music_on.png');")
            self.music.play()
        else:
            self.sender().setStyleSheet("background-image: url('music_off.png');")
            self.music.stop()

class play_ui(QtWidgets.QWidget):
    
    def __init__(self, board_size=3, against_ai=True, fail_chance=FAIL_CHANCE):
        super(play_ui, self).__init__()
        uic.loadUi("play_field.ui", self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #545454;")


        self.initial_fail_chance = fail_chance
        self.fail_chance = self.initial_fail_chance

        self.board_size = board_size
        self.board = create_board(self.board_size)
        self.buttons = []

        self.PLAYER_1 = "X"
        self.PLAYER_2 = "O"
        self.player_to_play = 1
        self.against_ai = against_ai

        self.win_message = "" # Message that shows in QMessageBox after the game has ended
        self.gameover_message_box = QtWidgets.QMessageBox()
        self.gameover_message_box.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.gameover_message_box.addButton("Играть снова!", QtWidgets.QMessageBox.YesRole)
        self.gameover_message_box.addButton("Закрыть", QtWidgets.QMessageBox.NoRole)
        self.gameover_message_box.setWindowTitle("Игра закончена!")
        #self.gameover_message_box.setStyleSheet("background-color: #545454;")
        #self.gameover_message_box.setStyleSheet("color: #98be03;")

        self.isGameFinished = False

        #* Generate buttons
        for i in range(self.board_size):
            buttons = []
            for j in range(self.board_size):
                test_button = QtWidgets.QPushButton()
                test_button.setMinimumSize(75, 75)
                #test_button.setMaximumSize(50, 50)
                test_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                font = QtGui.QFont("MS Shell", 15)
                font.setBold(True)
                test_button.setFont(font)
                test_button.setText("")
                test_button.x_coord = i
                test_button.y_coord = j
                test_button.clicked.connect(self.process_button_press)
                test_button.setFocusPolicy(QtCore.Qt.NoFocus)

                self.playfield_grid.addWidget(test_button, i, j)
                buttons.append(test_button)

            self.buttons.append(buttons)

        self.groupBox.setTitle("Игра против Шрека" if self.against_ai else "Игра с другом: ход Х")
        self.groupBox.setStyleSheet("color: #98be03;")
        self.setFixedSize(self.minimumSizeHint())
    
    def process_button_press(self):
        #* If playing against an AI:
        if self.against_ai:
            #* Player move
            #self.sender().setIcon(QtGui.QIcon("x.png"))
            #self.sender().setIconSize(QtCore.QSize(75,75))
            self.sender().setStyleSheet("background-image: url('x.png');")
            self.board[self.sender().x_coord][self.sender().y_coord] = self.PLAYER_1
            #self.sender().setText(self.PLAYER_1)
            self.sender().setEnabled(False)
            if check_win(self.board, self.PLAYER_1):
                #print("You win!")
                self.win_message = "Вы выиграли!"
                self.isGameFinished = True
            elif is_board_full(self.board):
                #print("It's a tie!")
                self.win_message = "Ничья!"
                self.isGameFinished = True
            
            if self.isGameFinished == False:
                #* AI move
                #? Small workaround to add pseudorandom to fail chance
                #? and to keep code working both as GUI app and in console.
                if random.random() <= self.fail_chance: #* If roll succeeded
                    self.fail_chance = self.initial_fail_chance
                    will_fail = 1
                    #print("Fail roll succeeded.")
                else: #* If roll failed
                    self.fail_chance += self.initial_fail_chance #* Add initial fail chance to fail chance until roll succeeds
                    will_fail = -1
                    #print(f"Fail roll failed. Fail chance is now {self.fail_chance}")
                row, col = get_ai_move(self.board, self.PLAYER_1, self.PLAYER_2, will_fail)
                self.board[row][col] = self.PLAYER_2
                #self.buttons[row][col].setIcon(QtGui.QIcon("o.png"))
                #self.buttons[row][col].setIconSize(QtCore.QSize(75,75))
                self.buttons[row][col].setStyleSheet("background-image: url('o.png');")
                #self.buttons[row][col].setText(self.PLAYER_2)
                self.buttons[row][col].setEnabled(False)

                if check_win(self.board, self.PLAYER_2):
                    #print("AI wins!")
                    self.win_message = "Шрек победил!"
                    self.isGameFinished = True
                elif is_board_full(self.board):
                    #print("It's a tie!")
                    self.win_message = "Ничья!"
                    self.isGameFinished = True

            #* Check if it is a tie or someone won
            if self.isGameFinished:
                for i in range(len(self.buttons)):
                    for j in range(len(self.buttons)):
                        self.buttons[i][j].setEnabled(False)
                
                self.gameover_message_box.setText(self.win_message)
                self.gameover_message_box.exec_()
                btn = self.gameover_message_box.buttonRole(self.gameover_message_box.clickedButton())
                if btn == QtWidgets.QMessageBox.YesRole: #* Restart the game
                    for i in range(len(self.buttons)):
                        for j in range(len(self.buttons)):
                            self.buttons[i][j].setEnabled(True)
                            #self.buttons[i][j].setText("")
                            self.buttons[i][j].setStyleSheet("")
                    self.board = create_board(self.board_size)
                    self.player_to_play = 1
                    self.isGameFinished = False
                    self.win_message = ""
        
        #* If playing against friend:
        else:
            #* 1st player's turn
            if self.player_to_play == 1:
                #self.sender().setIcon(QtGui.QIcon("x.png"))
                #self.sender().setIconSize(QtCore.QSize(75,75))
                self.sender().setStyleSheet("background-image: url('x.png');")
                self.board[self.sender().x_coord][self.sender().y_coord] = self.PLAYER_1
                #self.sender().setText(self.PLAYER_1)
                self.sender().setEnabled(False)
                if check_win(self.board, self.PLAYER_1):
                    #print("Player 1 won!")
                    self.win_message = "Первый игрок победил!"
                    self.isGameFinished = True
                elif is_board_full(self.board):
                    #print("It's a tie!")
                    self.win_message = "Ничья!"
                    self.isGameFinished = True
                self.player_to_play = 2
                self.groupBox.setTitle("Игра с другом: ход О")

            #* 2nd player's turn
            elif self.player_to_play == 2:
                #self.sender().setIcon(QtGui.QIcon("o.png"))
                #self.sender().setIconSize(QtCore.QSize(75,75))
                self.sender().setStyleSheet("background-image: url('o.png');")
                self.board[self.sender().x_coord][self.sender().y_coord] = self.PLAYER_2
                #self.sender().setText(self.PLAYER_2)
                self.sender().setEnabled(False)
                if check_win(self.board, self.PLAYER_2):
                    #print("Player 2 won!")
                    self.win_message = "Второй игрок победил!"
                    self.isGameFinished = True
                elif is_board_full(self.board):
                    #print("It's a tie!")
                    self.win_message = "Ничья!"
                    self.isGameFinished = True
                self.player_to_play = 1
                self.groupBox.setTitle("Игра с другом: ход Х")
            
            #* Check if it is a tie or someone won
            if self.isGameFinished:
                for i in range(len(self.buttons)):
                    for j in range(len(self.buttons)):
                        self.buttons[i][j].setEnabled(False)

                self.gameover_message_box.setText(self.win_message)
                self.gameover_message_box.exec_()
                btn = self.gameover_message_box.buttonRole(self.gameover_message_box.clickedButton())
                if btn == QtWidgets.QMessageBox.YesRole: #* Restart the game
                    for i in range(len(self.buttons)):
                        for j in range(len(self.buttons)):
                            self.buttons[i][j].setEnabled(True)
                            #self.buttons[i][j].setText("")
                            self.buttons[i][j].setStyleSheet("")
                    self.board = create_board(self.board_size)
                    self.player_to_play = 1
                    self.isGameFinished = False
                    self.win_message = ""

if __name__ == "__main__":
    #board_size = int(input("Enter board size (e.g., 3 for 3x3): "))
    #play_game(board_size)
    app = QtWidgets.QApplication(sys.argv)
    #window = main_ui()
    window = start_ui()
    window.show()

    app.exec()