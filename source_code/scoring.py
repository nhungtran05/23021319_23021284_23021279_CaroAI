# evaluate.py

def evaluate_board(board_state, size=9):
    if hasattr(board_state, 'board'):
        board_state = board_state.board
        
    score = 0
    
    def evaluate_window(window):
        o_count = window.count('O')
        x_count = window.count('X')
        
        # NẾU CỬA SỔ 4 Ô CHỨA CẢ X VÀ O -> ĐƯỜNG NÀY ĐÃ CHẾT, KHÔNG THỂ TẠO 4 QUÂN LIÊN TIẾP
        if o_count > 0 and x_count > 0:
            return 0
            
        # ---- ĐIỂM CHO AI (O) ----
        if o_count == 4:
            return 100000       # Thắng luôn
        elif o_count == 3:
            return 5000         # Sắp thắng
        elif o_count == 2:
            return 100          
        elif o_count == 1:
            return 5            
            
        # ---- ĐIỂM PHẠT CHẶN NGƯỜI CHƠI (X) ----
        if x_count == 4:
            return -100000       
        elif x_count == 3:
            return -20000       # Ưu tiên chặn người chơi cao hơn là AI tự xây
        elif x_count == 2:
            return -200          
        elif x_count == 1:
            return -10
            
        return 0

    # Duyệt tất cả các cửa sổ kích thước 4 trên bàn cờ 9x9
    for r in range(size):
        for c in range(size - 3):
            score += evaluate_window([board_state[r][c+i] for i in range(4)])
            
    for c in range(size):
        for r in range(size - 3):
            score += evaluate_window([board_state[r+i][c] for i in range(4)])
            
    for r in range(size - 3):
        for c in range(size - 3):
            score += evaluate_window([board_state[r+i][c+i] for i in range(4)])
            
    for r in range(3, size):
        for c in range(size - 3):
            score += evaluate_window([board_state[r-i][c+i] for i in range(4)])
            
    # PHÁ THẾ BẾ TẮC: Cộng điểm ưu tiên các ô gần tâm bàn cờ
    center = size // 2
    for r in range(size):
        for c in range(size):
            if board_state[r][c] == 'O':
                score += (size - abs(r - center) - abs(c - center))
            elif board_state[r][c] == 'X':
                score -= (size - abs(r - center) - abs(c - center))
                
    return score
