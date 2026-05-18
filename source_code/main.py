# main.py
import pygame
import sys
from caro_logic import CaroBoard
from ai_player import AI_Agent
from ai_tester import run_ai_with_benchmark

# --- 1. CẤU HÌNH GIAO DIỆN ---
pygame.init()
SIZE = 9
CELL_SIZE = 60

BOARD_WIDTH = SIZE * CELL_SIZE
BOARD_HEIGHT = SIZE * CELL_SIZE
UI_WIDTH = 260
INFO_HEIGHT = 130 

WINDOW_WIDTH = BOARD_WIDTH + UI_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + INFO_HEIGHT

WHITE, BLACK, RED, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)
GRAY, LIGHT_GRAY = (200, 200, 200), (230, 230, 230)
GREEN = (0, 200, 0)
DARK_RED = (180, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cờ Caro AI - Bảng điều khiển")
font = pygame.font.SysFont("tahoma", 19, bold=True) # Đã đổi sang Tahoma tránh lỗi font
small_font = pygame.font.SysFont("tahoma", 15)

# Khai báo tọa độ các nút bấm UI
btn_minimax = pygame.Rect(BOARD_WIDTH + 30, 40, 200, 40)
btn_alphabeta = pygame.Rect(BOARD_WIDTH + 30, 90, 200, 40)
btn_depth1 = pygame.Rect(BOARD_WIDTH + 30, 180, 55, 40)
btn_depth2 = pygame.Rect(BOARD_WIDTH + 100, 180, 55, 40)
btn_depth3 = pygame.Rect(BOARD_WIDTH + 170, 180, 55, 40)

# --- 2. CÁC HÀM VẼ ĐỒ HỌA ---
def draw_grid():
    pygame.draw.rect(screen, WHITE, (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
    for i in range(1, SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (BOARD_WIDTH, i * CELL_SIZE), 2)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (BOARD_WIDTH, 0), (BOARD_WIDTH, BOARD_HEIGHT), 4)
    pygame.draw.line(screen, BLACK, (0, BOARD_HEIGHT), (WINDOW_WIDTH, BOARD_HEIGHT), 4)

def draw_board_state(board_logic):
    for r in range(board_logic.size):
        for c in range(board_logic.size):
            if board_logic.board[r][c] == 'X':
                offset = 15
                x, y = c * CELL_SIZE, r * CELL_SIZE
                pygame.draw.line(screen, RED, (x + offset, y + offset), (x + CELL_SIZE - offset, y + CELL_SIZE - offset), 3)
                pygame.draw.line(screen, RED, (x + CELL_SIZE - offset, y + offset), (x + offset, y + CELL_SIZE - offset), 3)
            elif board_logic.board[r][c] == 'O':
                center = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                radius = CELL_SIZE // 2 - 15
                pygame.draw.circle(screen, BLUE, center, radius, 3)

def draw_ui(current_mode, current_depth, eval_score, status_text, time_taken):
    pygame.draw.rect(screen, LIGHT_GRAY, (BOARD_WIDTH + 2, 0, UI_WIDTH, BOARD_HEIGHT))
    pygame.draw.rect(screen, LIGHT_GRAY, (0, BOARD_HEIGHT + 2, WINDOW_WIDTH, INFO_HEIGHT))
    
    # Vẽ các nút chọn thuật toán
    color_minimax = GREEN if current_mode == "MINIMAX" else GRAY
    pygame.draw.rect(screen, color_minimax, btn_minimax, border_radius=10)
    text_mm = font.render("MINIMAX", True, BLACK)
    screen.blit(text_mm, (btn_minimax.x + 55, btn_minimax.y + 8))

    color_ab = GREEN if current_mode == "ALPHA-BETA" else GRAY
    pygame.draw.rect(screen, color_ab, btn_alphabeta, border_radius=10)
    text_ab = font.render("ALPHA-BETA", True, BLACK)
    screen.blit(text_ab, (btn_alphabeta.x + 35, btn_alphabeta.y + 8))
    
    # Vẽ các nút chọn Depth
    txt_depth_title = font.render("Chọn độ sâu (Depth):", True, BLACK)
    screen.blit(txt_depth_title, (BOARD_WIDTH + 30, 150))
    
    for btn, d_val in [(btn_depth1, 1), (btn_depth2, 2), (btn_depth3, 3)]:
        color_d = GREEN if current_depth == d_val else GRAY
        pygame.draw.rect(screen, color_d, btn, border_radius=8)
        txt_d = font.render(str(d_val), True, BLACK)
        screen.blit(txt_d, (btn.x + 22, btn.y + 8))

    txt_guide = small_font.render("Nhấn 'R' để chơi lại ván mới", True, BLACK)
    screen.blit(txt_guide, (BOARD_WIDTH + 45, BOARD_HEIGHT - 30))

    # Hiển thị thông số bên dưới
    txt_status = font.render(f"Trạng thái: {status_text}", True, BLACK)
    screen.blit(txt_status, (20, BOARD_HEIGHT + 15))
    
    txt_eval = font.render(f"Giá trị đánh giá AI: {eval_score}", True, BLUE)
    screen.blit(txt_eval, (20, BOARD_HEIGHT + 50))
    
    txt_time = font.render(f"Thời gian AI nghĩ (Depth {current_depth}): {time_taken:.4f} giây", True, DARK_RED)
    screen.blit(txt_time, (20, BOARD_HEIGHT + 85))

# --- 3. VÒNG LẶP CHÍNH ---
def main():
    game_board = CaroBoard(SIZE)
    ai_agent = AI_Agent(game_board)
    
    running = True
    game_over = False
    
    # Quản lý trạng thái game
    ai_mode = "ALPHA-BETA" 
    ai_depth = 2           
    last_eval_score = 0
    last_time_taken = 0.0  
    status_msg = "Lượt của bạn (X)"
    
    turn = 'X'             # Biến kiểm soát lượt đi ('X' là Người, 'O' là Máy)
    last_player_move = None

    while running:
        # Làm mới và vẽ toàn bộ giao diện lên màn hình
        screen.fill(LIGHT_GRAY)
        draw_grid()
        draw_board_state(game_board)
        draw_ui(ai_mode, ai_depth, last_eval_score, status_msg, last_time_taken)
        pygame.display.flip()

        # --- [QUAN TRỌNG] XỬ LÝ LƯỢT CỦA MÁY (NẰM NGOÀI EVENT LOOP) ---
        if not game_over and turn == 'O':
            # AI bắt đầu tính toán
            score, best_move, time_taken = run_ai_with_benchmark(ai_agent, depth=ai_depth, last_move=last_player_move, mode=ai_mode)
            
            if best_move:
                ai_row, ai_col = best_move
                game_board.make_move(ai_row, ai_col, 'O')
                last_eval_score = score
                last_time_taken = time_taken 
                
                if game_board.check_winner(ai_row, ai_col, 'O'):
                    status_msg = "MÁY TÍNH THẮNG!"
                    game_over = True
                elif game_board.is_draw():
                    status_msg = "HÒA!"
                    game_over = True
                else:
                    status_msg = "Lượt của bạn (X)"
                    turn = 'X' # Trả lượt lại cho Người chơi
            
            pygame.event.clear() # Xóa sạch mọi cú click chuột thừa thãi của người dùng trong lúc đợi AI nghĩ
            continue # Bỏ qua phần quét sự kiện dưới để vòng lặp quay lại vẽ quân 'O' mới lên màn hình ngay

        # --- VÒNG LẶP SỰ KIỆN (CHỈ XỬ LÝ KHI KHÔNG BỊ KHÓA LƯỢT) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Reset game
                    game_board = CaroBoard(SIZE)
                    ai_agent = AI_Agent(game_board)
                    game_over = False
                    last_eval_score = 0
                    last_time_taken = 0.0
                    status_msg = "Lượt của bạn (X)"
                    turn = 'X'
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos_x, pos_y = event.pos
                
                # Click chọn cấu hình trên thanh UI (Luôn cho phép click kể cả lúc nào)
                if btn_minimax.collidepoint(pos_x, pos_y):
                    ai_mode = "MINIMAX"
                elif btn_alphabeta.collidepoint(pos_x, pos_y):
                    ai_mode = "ALPHA-BETA"
                elif btn_depth1.collidepoint(pos_x, pos_y):
                    ai_depth = 1
                elif btn_depth2.collidepoint(pos_x, pos_y):
                    ai_depth = 2
                elif btn_depth3.collidepoint(pos_x, pos_y):
                    ai_depth = 3
                
                # Click đánh cờ (CHỈ HỢP LỆ KHI ĐANG TRONG LƯỢT CỦA 'X')
                elif turn == 'X' and pos_x < BOARD_WIDTH and pos_y < BOARD_HEIGHT:
                    col, row = pos_x // CELL_SIZE, pos_y // CELL_SIZE
                    
                    if game_board.is_valid_move(row, col):
                        game_board.make_move(row, col, 'X')
                        last_player_move = (row, col)
                        
                        if game_board.check_winner(row, col, 'X'):
                            status_msg = "NGƯỜI CHƠI THẮNG!"
                            game_over = True
                        elif game_board.is_draw():
                            status_msg = "HÒA!"
                            game_over = True
                        else:
                            status_msg = "AI đang suy nghĩ..."
                            turn = 'O' # Khóa lượt người chơi, chuyển sang cho AI

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()