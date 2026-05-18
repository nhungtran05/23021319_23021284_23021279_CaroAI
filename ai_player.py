# ai_player
import math
from scoring import evaluate_board

class AI_Agent:
    def __init__(self, board_logic):
        self.game = board_logic
        self.states_explored = 0  

    # --- THUẬT TOÁN 1: MINIMAX CƠ BẢN ---
    def minimax(self, depth, is_maximizing, last_move=None):
        self.states_explored += 1 # Đếm trạng thái
        
        if last_move:
            r, c = last_move
            if self.game.check_winner(r, c, 'O'): return 100000, None
            if self.game.check_winner(r, c, 'X'): return -100000, None
        
        if self.game.is_draw(): return 0, None
        if depth == 0: return evaluate_board(self.game.board, self.game.size), None

        available_moves = self.game.get_available_moves()
        best_move = available_moves[0] if available_moves else None

        if is_maximizing:
            max_eval = -math.inf
            for move in available_moves:
                r, c = move
                self.game.make_move(r, c, 'O')
                eval_score, _ = self.minimax(depth - 1, False, move)
                self.game.undo_move(r, c)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in available_moves:
                r, c = move
                self.game.make_move(r, c, 'X')
                eval_score, _ = self.minimax(depth - 1, True, move)
                self.game.undo_move(r, c)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    # --- THUẬT TOÁN 2: ALPHA-BETA PRUNING ---
    def alpha_beta(self, depth, is_maximizing, alpha, beta, last_move=None):
        self.states_explored += 1 # Đếm trạng thái
        
        if last_move:
            r, c = last_move
            if self.game.check_winner(r, c, 'O'): return 100000, None
            if self.game.check_winner(r, c, 'X'): return -100000, None
        
        if self.game.is_draw(): return 0, None
        if depth == 0: return evaluate_board(self.game.board, self.game.size), None

        available_moves = self.game.get_available_moves()
        best_move = available_moves[0] if available_moves else None

        if is_maximizing:
            max_eval = -math.inf
            for move in available_moves:
                r, c = move
                self.game.make_move(r, c, 'O')
                eval_score, _ = self.alpha_beta(depth - 1, False, alpha, beta, move)
                self.game.undo_move(r, c)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha: break # Cắt nhánh
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in available_moves:
                r, c = move
                self.game.make_move(r, c, 'X')
                eval_score, _ = self.alpha_beta(depth - 1, True, alpha, beta, move)
                self.game.undo_move(r, c)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
                beta = min(beta, eval_score)
                if beta <= alpha: break # Cắt nhánh
            return min_eval, best_move