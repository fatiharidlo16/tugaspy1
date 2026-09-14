import random
import tkinter as tk
from tkinter import messagebox


BOARD_SIZE = 8
CELL_SIZE = 48
BOARD_COLOR = "#20304a"
EMPTY_COLOR = "#31435f"
PIECE_COLORS = ["#ff6b6b", "#ffd166", "#06d6a0", "#4dabf7", "#c77dff"]

SHAPES = [
	[(0, 0)],
	[(0, 0), (1, 0)],
	[(0, 0), (0, 1)],
	[(0, 0), (1, 0), (0, 1)],
	[(0, 0), (1, 0), (2, 0)],
	[(0, 0), (0, 1), (0, 2)],
	[(0, 0), (1, 0), (2, 0), (1, 1)],
	[(0, 0), (1, 0), (0, 1), (1, 1)],
	[(0, 0), (0, 1), (1, 1), (1, 2)],
	[(0, 0), (1, 0), (1, 1), (2, 1)],
	[(0, 0), (1, 0), (2, 0), (3, 0)],
	[(0, 0), (0, 1), (0, 2), (0, 3)],
]


class BlockBlast:
	def __init__(self, root):
		self.root = root
		self.root.title("Block Blast - Poltera")
		self.root.configure(bg="#101827")
		self.root.resizable(False, False)
		self.score = 0
		self.selected_piece = None
		self.board = []
		self.pieces = []

		header = tk.Frame(root, bg="#101827")
		header.pack(fill="x", padx=20, pady=(18, 8))
		tk.Label(
			header,
			text="BLOCK BLAST",
			font=("Segoe UI", 22, "bold"),
			fg="#f8f9fa",
			bg="#101827",
		).pack(side="left")
		self.score_label = tk.Label(
			header,
			text="SKOR  0",
			font=("Segoe UI", 12, "bold"),
			fg="#ffd166",
			bg="#101827",
		)
		self.score_label.pack(side="right", pady=6)

		self.status_label = tk.Label(
			root,
			text="Pilih bentuk, lalu klik kotak papan untuk menaruhnya.",
			font=("Segoe UI", 10),
			fg="#a9b8d0",
			bg="#101827",
		)
		self.status_label.pack(pady=(0, 10))

		self.board_canvas = tk.Canvas(
			root,
			width=BOARD_SIZE * CELL_SIZE,
			height=BOARD_SIZE * CELL_SIZE,
			bg=BOARD_COLOR,
			highlightthickness=0,
		)
		self.board_canvas.pack(padx=20)
		self.board_canvas.bind("<Button-1>", self.place_selected_piece)

		self.piece_frame = tk.Frame(root, bg="#101827")
		self.piece_frame.pack(padx=20, pady=16)

		tk.Button(
			root,
			text="PERMAINAN BARU",
			command=self.new_game,
			font=("Segoe UI", 10, "bold"),
			fg="#101827",
			bg="#ffd166",
			activebackground="#ffe29a",
			relief="flat",
			padx=16,
			pady=8,
			cursor="hand2",
		).pack(pady=(0, 18))

		self.new_game()

	def new_game(self):
		self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
		self.score = 0
		self.selected_piece = None
		self.pieces = [random.choice(SHAPES) for _ in range(3)]
		self.status_label.config(text="Pilih bentuk, lalu klik kotak papan untuk menaruhnya.")
		self.draw_board()
		self.draw_pieces()
		self.update_score()

	def draw_board(self):
		self.board_canvas.delete("all")
		for row in range(BOARD_SIZE):
			for column in range(BOARD_SIZE):
				x1 = column * CELL_SIZE + 2
				y1 = row * CELL_SIZE + 2
				x2 = x1 + CELL_SIZE - 4
				y2 = y1 + CELL_SIZE - 4
				color = self.board[row][column] or EMPTY_COLOR
				self.board_canvas.create_rectangle(
					x1,
					y1,
					x2,
					y2,
					fill=color,
					outline=BOARD_COLOR,
					width=2,
				)

	def draw_pieces(self):
		for child in self.piece_frame.winfo_children():
			child.destroy()
		for index, shape in enumerate(self.pieces):
			canvas = tk.Canvas(
				self.piece_frame,
				width=105,
				height=90,
				bg="#17243a",
				highlightthickness=3 if index == self.selected_piece else 0,
				highlightbackground="#ffd166",
				cursor="hand2",
			)
			canvas.grid(row=0, column=index, padx=5)
			canvas.bind("<Button-1>", lambda _event, i=index: self.select_piece(i))
			color = PIECE_COLORS[index % len(PIECE_COLORS)]
			min_x = min(x for x, _ in shape)
			max_x = max(x for x, _ in shape)
			min_y = min(y for _, y in shape)
			max_y = max(y for _, y in shape)
			offset_x = (105 - (max_x - min_x + 1) * 20) // 2
			offset_y = (90 - (max_y - min_y + 1) * 20) // 2
			for x, y in shape:
				left = offset_x + (x - min_x) * 20
				top = offset_y + (y - min_y) * 20
				canvas.create_rectangle(
					left,
					top,
					left + 18,
					top + 18,
					fill=color,
					outline="#f8f9fa",
					width=1,
				)

	def select_piece(self, index):
		if self.pieces[index] is None:
			return
		self.selected_piece = index
		self.status_label.config(text="Sekarang klik posisi awal bentuk di papan.")
		self.draw_pieces()

	def place_selected_piece(self, event):
		if self.selected_piece is None:
			self.status_label.config(text="Pilih salah satu bentuk di bawah papan terlebih dahulu.")
			return
		row = event.y // CELL_SIZE
		column = event.x // CELL_SIZE
		shape = self.pieces[self.selected_piece]
		if not self.can_place(shape, row, column):
			self.status_label.config(text="Bentuk tidak muat di posisi itu. Coba tempat lain.")
			return
		color = PIECE_COLORS[self.selected_piece % len(PIECE_COLORS)]
		for x, y in shape:
			self.board[row + y][column + x] = color
		self.score += len(shape)
		self.pieces[self.selected_piece] = None
		self.clear_completed_lines()
		self.selected_piece = None
		self.draw_board()
		self.draw_pieces()
		self.update_score()
		if all(piece is None for piece in self.pieces):
			self.pieces = [random.choice(SHAPES) for _ in range(3)]
			self.draw_pieces()
		if not self.has_any_move():
			messagebox.showinfo("Permainan selesai", f"Tidak ada ruang lagi. Skor akhir: {self.score}")
			self.status_label.config(text="Permainan selesai. Tekan PERMAINAN BARU untuk mencoba lagi.")
		else:
			self.status_label.config(text="Bagus! Pilih bentuk berikutnya.")

	def can_place(self, shape, row, column):
		for x, y in shape:
			target_row = row + y
			target_column = column + x
			if (
				target_row >= BOARD_SIZE
				or target_column >= BOARD_SIZE
				or self.board[target_row][target_column] is not None
			):
				return False
		return True

	def clear_completed_lines(self):
		full_rows = [row for row in range(BOARD_SIZE) if all(self.board[row])]
		full_columns = [
			column
			for column in range(BOARD_SIZE)
			if all(self.board[row][column] for row in range(BOARD_SIZE))
		]
		for row in full_rows:
			self.board[row] = [None for _ in range(BOARD_SIZE)]
		for column in full_columns:
			for row in range(BOARD_SIZE):
				self.board[row][column] = None
		lines_cleared = len(full_rows) + len(full_columns)
		self.score += lines_cleared * 10

	def has_any_move(self):
		for shape in self.pieces:
			if shape is not None:
				for row in range(BOARD_SIZE):
					for column in range(BOARD_SIZE):
						if self.can_place(shape, row, column):
							return True
		return False

	def update_score(self):
		self.score_label.config(text=f"SKOR  {self.score}")


if __name__ == "__main__":
	root = tk.Tk()
	BlockBlast(root)
	root.mainloop()