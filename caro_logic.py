# game.py

class CaroBoard:
    def __init__(self, size=9):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.move_history = []

    def is_valid_move(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col] == '.'
        return False

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.move_history.append((row, col))
            return True
        return False
        
    def undo_move(self, row, col):
        self.board[row][col] = '.'
        if self.move_history and self.move_history[-1] == (row, col):
            self.move_history.pop()

    def check_winner(self, last_row, last_col, player):
        if self.board[last_row][last_col] != player:
            return False
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            r, c = last_row + dr, last_col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1; r += dr; c += dc
            r, c = last_row - dr, last_col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1; r -= dr; c -= dc
            if count >= 4: # LUẬT: THẮNG KHI CÓ 4 QUÂN LIÊN TIẾP
                return True
        return False

    def is_draw(self):
        return len(self.move_history) == self.size * self.size

    def has_adjacent_piece(self, row, col, radius=1):
        """Kiểm tra xem xung quanh ô (row, col) trong bán kính radius có quân cờ nào không."""
        start_row = max(0, row - radius)
        end_row = min(self.size - 1, row + radius)
        start_col = max(0, col - radius)
        end_col = min(self.size - 1, col + radius)

        for i in range(start_row, end_row + 1):
            for j in range(start_col, end_col + 1):
                if self.board[i][j] != '.': 
                    return True
        return False

    def get_available_moves(self):
        moves = []
        is_empty_board = True
        
        # Kiểm tra xem bàn cờ có đang trống trơn không
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != '.':
                    is_empty_board = False
                    break
            if not is_empty_board:
                break
                
        # Nếu bàn cờ trống (AI đi nước đầu tiên), chỉ trả về ô chính giữa để tiết kiệm thời gian
        if is_empty_board:
            return [(self.size // 2, self.size // 2)]

        # BƯỚC 1: Tìm các ô trống có quân cờ nằm kề cạnh (bán kính 1 ô)
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    if self.has_adjacent_piece(r, c, radius=1): 
                        moves.append((r, c))
                        
        # BƯỚC 2: Nếu bán kính 1 không có ô nào, mở rộng ra bán kính 2
        if not moves:
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == '.':
                        if self.has_adjacent_piece(r, c, radius=2): 
                            moves.append((r, c))

        # BƯỚC 3: PHÒNG HỜ TỐI ĐA
        if not moves:
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == '.':
                        moves.append((r, c))
                        
        # --- MOVE ORDERING (QUAN TRỌNG NHẤT ĐỂ GIẢM LAG) ---
        # Sắp xếp các nước đi ưu tiên gần tâm bàn cờ nhất. 
        # Giúp Alpha-Beta Pruning cắt nhánh (prune) nhanh gấp hàng chục lần.
        center = self.size // 2
        moves.sort(key=lambda m: abs(m[0] - center) + abs(m[1] - center))
                        
        return moves