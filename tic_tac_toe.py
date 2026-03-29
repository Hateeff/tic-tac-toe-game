import random
import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional, Tuple

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TicTacToeGame:
    """Manage the board state and game rules."""

    WINNING_COMBINATIONS = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board: List[str] = [""] * 9
        self.current_player: str = "X"
        self.game_over: bool = False

    def make_move(self, index: int, player: str) -> bool:
        if self.board[index] or self.game_over:
            return False
        self.board[index] = player
        return True

    def check_winner(self) -> Optional[str]:
        return self.calculate_winner(self.board)

    def is_draw(self) -> bool:
        return all(self.board) and self.check_winner() is None

    def available_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if not cell]

    @staticmethod
    def available_moves_for(board: List[str]) -> List[int]:
        return [i for i, cell in enumerate(board) if not cell]

    @staticmethod
    def calculate_winner(board: List[str]) -> Optional[str]:
        for a, b, c in TicTacToeGame.WINNING_COMBINATIONS:
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        return None


class TicTacToeAI:
    """Separate AI logic from the game rules."""

    def __init__(self, ai_player: str = "O", human_player: str = "X") -> None:
        self.ai_player = ai_player
        self.human_player = human_player

    def choose_move(self, board: List[str], difficulty: str) -> int:
        moves = TicTacToeGame.available_moves_for(board)
        if not moves:
            raise ValueError("No available moves")

        if difficulty == "Easy":
            return random.choice(moves)

        if difficulty == "Medium":
            if random.random() < 0.5:
                return random.choice(moves)
            return self._best_move(board)

        return self._best_move(board)

    def _best_move(self, board: List[str]) -> int:
        _, move = self._minimax(board, self.ai_player)
        return move if move is not None else random.choice(TicTacToeGame.available_moves_for(board))

    def _minimax(self, board: List[str], player: str) -> Tuple[int, Optional[int]]:
        """
        Minimax algorithm explores all possible future board states.
        It chooses the move that maximizes the AI score and minimizes the opponent score.
        """
        winner = TicTacToeGame.calculate_winner(board)
        if winner == self.ai_player:
            return 1, None
        if winner == self.human_player:
            return -1, None
        if all(board):
            return 0, None

        if player == self.ai_player:
            best_score = -float("inf")
            best_move: Optional[int] = None
            for index in TicTacToeGame.available_moves_for(board):
                board[index] = player
                score, _ = self._minimax(board, self.human_player)
                board[index] = ""
                if score > best_score:
                    best_score = score
                    best_move = index
            return best_score, best_move

        best_score = float("inf")
        best_move: Optional[int] = None
        for index in TicTacToeGame.available_moves_for(board):
            board[index] = player
            score, _ = self._minimax(board, self.ai_player)
            board[index] = ""
            if score < best_score:
                best_score = score
                best_move = index
        return best_score, best_move


class TicTacToeApp:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("420x500")
        self.root.minsize(420, 500)
        self.game = TicTacToeGame()
        self.ai = TicTacToeAI()
        self.difficulty = ctk.StringVar(value="Hard")
        self.buttons: List[ctk.CTkButton] = []

        self._configure_grid()
        self._create_widgets()
        self._update_status("Your turn (X)")

    def _configure_grid(self) -> None:
        self.root.grid_columnconfigure((0, 1, 2), weight=1)
        self.root.grid_rowconfigure(3, weight=1)

    def _create_widgets(self) -> None:
        self.root.configure(padx=18, pady=18)

        title = ctk.CTkLabel(
            self.root,
            text="Tic Tac Toe",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#eef2ff",
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 12))

        self.status_label = ctk.CTkLabel(
            self.root,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#cbd5ff",
        )
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 16))

        difficulty_label = ctk.CTkLabel(
            self.root,
            text="Difficulty:",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5ff",
        )
        difficulty_label.grid(row=2, column=0, pady=(0, 8), sticky="e")

        difficulty_menu = ctk.CTkOptionMenu(
            self.root,
            variable=self.difficulty,
            values=["Easy", "Medium", "Hard"],
            width=120,
            corner_radius=14,
        )
        difficulty_menu.grid(row=2, column=1, pady=(0, 8),padx=(15, 0), sticky="w")

        board_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color="#1f2937",
            border_width=0,
        )
        board_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=4, pady=(0, 14))
        board_frame.grid_columnconfigure((0, 1, 2), weight=1)
        board_frame.grid_rowconfigure((0, 1, 2), weight=1)

        button_font = ctk.CTkFont(size=28, weight="bold")
        for index in range(9):
            button = ctk.CTkButton(
                board_frame,
                text="",
                font=button_font,
                corner_radius=16,
                fg_color="#334155",
                hover_color="#475569",
                text_color="#f8fafc",
                command=lambda idx=index: self._on_cell_click(idx),
            )
            row = index // 3
            column = index % 3
            button.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")
            self.buttons.append(button)

        restart_button = ctk.CTkButton(
            self.root,
            text="Restart",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=18,
            fg_color="#7c3aed",
            hover_color="#8b5cf6",
            command=self._restart_game,
        )
        restart_button.grid(row=4, column=0, columnspan=3, pady=(4, 0), sticky="ew")

    def _on_cell_click(self, index: int) -> None:
        if self.game.game_over or self.game.board[index]:
            return

        if not self.game.make_move(index, "X"):
            return

        self._update_button(index, "X")
        self._process_turn()

    def _process_turn(self) -> None:
        winner = self.game.check_winner()
        if winner or self.game.is_draw():
            self._finish_game(winner)
            return

        self._take_ai_turn()

    def _take_ai_turn(self) -> None:
        ai_move = self.ai.choose_move(self.game.board, self.difficulty.get())
        self.game.make_move(ai_move, "O")
        self._update_button(ai_move, "O")

        winner = self.game.check_winner()
        if winner or self.game.is_draw():
            self._finish_game(winner)
            return

        self._update_status("Your turn (X)")

    def _update_button(self, index: int, symbol: str) -> None:
        self.buttons[index].configure(text=symbol, state="disabled")

    def _finish_game(self, winner: Optional[str]) -> None:
        self.game.game_over = True
        for button in self.buttons:
            button.configure(state="disabled")

        if winner == "X":
            message = "You win!"
        elif winner == "O":
            message = "AI wins!"
        else:
            message = "It's a draw!"

        self._update_status(message)
        messagebox.showinfo("Game Over", message)

    def _restart_game(self) -> None:
        self.game.reset()
        for button in self.buttons:
            button.configure(text="", state="normal")
        self._update_status("Your turn (X)")

    def _update_status(self, message: str) -> None:
        self.status_label.configure(text=message)


def main() -> None:
    root = ctk.CTk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
