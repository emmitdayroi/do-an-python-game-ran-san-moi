import pygame
import random
import sys

# Khởi tạo pygame
pygame.init()

# Cài đặt cửa sổ game
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rắn Săn Mồi Bắn Súng - Python")
clock = pygame.time.Clock()

# Định nghĩa màu sắc (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# Định nghĩa Font chữ (To và Nhỏ)
font_small = pygame.font.SysFont("Arial", 20, bold=True)
font_large = pygame.font.SysFont("Arial", 36, bold=True)

# Khai báo các biến dùng chung
snake = []
dx = dy = next_dx = next_dy = score = tick_counter = 0
bullets = []
food = None
enemies = []

def spawn_entity():
    """Hàm tạo ngẫu nhiên vị trí mới không đè lên rắn và địch"""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake and (x, y) not in enemies:
            return (x, y)

def reset_game():
    """Hàm thiết lập lại game từ đầu khi bắt đầu hoặc chơi lại"""
    global snake, dx, dy, next_dx, next_dy, bullets, score, tick_counter, food, enemies
    snake = [(10, 10)]
    dx, dy = 0, -1
    next_dx, next_dy = 0, -1
    bullets = []
    score = 0
    tick_counter = 0
    enemies = [] # Xóa địch cũ trước
    food = spawn_entity()
    enemies = [spawn_entity(), spawn_entity()] # Tạo 2 địch mới

# Khởi tạo dữ liệu lần đầu
reset_game()

# Trạng thái game ban đầu
game_state = "START" # Gồm 3 trạng thái: START, PLAYING, GAME_OVER

while True:
    screen.fill(BLACK) # Luôn xóa màn hình cũ ở mỗi khung hình

    # 1. XỬ LÝ SỰ KIỆN CHUNG
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Phím bấm lúc màn hình BẮT ĐẦU
        if game_state == "START":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "PLAYING" # Đổi trạng thái sang chơi

        # Phím bấm lúc ĐANG CHƠI
        elif game_state == "PLAYING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    next_dx, next_dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    next_dx, next_dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    next_dx, next_dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    next_dx, next_dy = 1, 0
                elif event.key == pygame.K_SPACE:
                    # Bắn đạn
                    bullets.append({'x': snake[0][0], 'y': snake[0][1], 'dx': dx, 'dy': dy})

        # Phím bấm lúc GAME OVER
        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Nhấn R để chơi lại
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_q: # Nhấn Q để thoát
                    pygame.quit()
                    sys.exit()

    # 2. HIỂN THỊ DỰA THEO TRẠNG THÁI (STATE)
    if game_state == "START":
        title_text = font_large.render("SNAKE SHOOTER", True, GREEN)
        prompt_text = font_small.render("Nhấn phím SPACE để Bắt Đầu", True, WHITE)
        
        # Canh giữa màn hình
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2))

    elif game_state == "PLAYING":
        tick_counter += 1

        # CẬP NHẬT ĐẠN
        if tick_counter % 1 == 0:
            for b in bullets[:]:
                b['x'] += b['dx']
                b['y'] += b['dy']
                
                if b['x'] < 0 or b['x'] >= GRID_WIDTH or b['y'] < 0 or b['y'] >= GRID_HEIGHT:
                    bullets.remove(b)
                    continue
                    
                for e in enemies[:]:
                    if b['x'] == e[0] and b['y'] == e[1]:
                        bullets.remove(b)
                        enemies.remove(e)
                        score += 20
                        enemies.append(spawn_entity())
                        break

        # CẬP NHẬT RẮN
        if tick_counter % 3 == 0:
            dx, dy = next_dx, next_dy
            head_x = snake[0][0] + dx
            head_y = snake[0][1] + dy
            head = (head_x, head_y)
            
            # Kiểm tra thua game (Đổi trạng thái thay vì thoát luôn)
            if (head_x < 0 or head_x >= GRID_WIDTH or 
                head_y < 0 or head_y >= GRID_HEIGHT or 
                head in snake or head in enemies):
                game_state = "GAME_OVER"
            else:
                snake.insert(0, head)
                # Kiểm tra ăn mồi
                if head == food:
                    score += 10
                    food = spawn_entity()
                    if score % 50 == 0:
                        enemies.append(spawn_entity())
                else:
                    snake.pop()

        # VẼ ĐỒ HỌA RA MÀN HÌNH
        # Vẽ mồi
        pygame.draw.rect(screen, GREEN, (food[0]*GRID_SIZE, food[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
        # Vẽ địch
        for e in enemies:
            pygame.draw.rect(screen, RED, (e[0]*GRID_SIZE, e[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
        # Vẽ đạn
        for b in bullets:
            pygame.draw.circle(screen, CYAN, (b['x']*GRID_SIZE + GRID_SIZE//2, b['y']*GRID_SIZE + GRID_SIZE//2), GRID_SIZE//4)
        # Vẽ rắn
        for i, s in enumerate(snake):
            color = YELLOW if i == 0 else WHITE
            pygame.draw.rect(screen, color, (s[0]*GRID_SIZE, s[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))
            
        # Vẽ điểm số
        score_text = font_small.render(f"Điểm: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_state == "GAME_OVER":
        title_text = font_large.render("GAME OVER!", True, RED)
        score_info = font_small.render(f"Tổng điểm của bạn: {score}", True, YELLOW)
        restart_text = font_small.render("Nhấn 'R' để Chơi Lại", True, WHITE)
        quit_text = font_small.render("Nhấn 'Q' để Thoát", True, WHITE)
        
        # Canh giữa các dòng chữ
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
        screen.blit(score_info, (WIDTH//2 - score_info.get_width()//2, HEIGHT//2 - 20))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 60))

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(30)