#ai_tester.py
import time
import math

# Lưu ý: Hàm này ĐÃ CÓ tham số mode ở cuối cùng
def run_ai_with_benchmark(ai_agent, depth, last_move, mode):
    print(f"\n--- AI ĐANG TÌM KIẾM ({mode} - Depth: {depth}) ---")
    
    ai_agent.states_explored = 0  
    start_time = time.time()      
    
    # KIỂM TRA MODE ĐỂ GỌI ĐÚNG THUẬT TOÁN
    if mode == "MINIMAX":
        score, best_move = ai_agent.minimax(depth, True, last_move)
    else:
        # Mặc định là Alpha-Beta
        score, best_move = ai_agent.alpha_beta(depth, True, -math.inf, math.inf, last_move)
    
    end_time = time.time()        
    time_taken = end_time - start_time
    
    print(f"Nước đi chọn: {best_move}")
    print(f"Giá trị đánh giá: {score}")
    print(f"Số trạng thái đã xét: {ai_agent.states_explored}")
    print(f"Thời gian chạy: {time_taken:.4f} giây")
    print("----------------------------------------\n")
    
    return score, best_move, time_taken