import pygame
import sys
from solana_devnet import launch_memecoin
from config import SETTINGS

# Initialize PyGame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 900, 650
FPS = 60

# Colors
DARK_BG = (18, 18, 29)
PRIMARY = (138, 99, 210)  # Solana purple
SECONDARY = (0, 255, 163)  # Teal accent
WHITE = (245, 246, 250)
BLACK = (12, 12, 18)

# Fonts
try:
    TITLE_FONT = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 42)
    BUTTON_FONT = pygame.font.Font("assets/fonts/Poppins-SemiBold.ttf", 24)
    BODY_FONT = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 18)
except:
    # Fallback fonts
    TITLE_FONT = pygame.font.SysFont("arial", 42, bold=True)
    BUTTON_FONT = pygame.font.SysFont("arial", 24)
    BODY_FONT = pygame.font.SysFont("arial", 18)

# Load assets
try:
    SOLANA_ICON = pygame.image.load("assets/icons/solana.png")
    SOLANA_ICON = pygame.transform.scale(SOLANA_ICON, (40, 40))
except:
    SOLANA_ICON = None

class MemeCoinLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MemeCoin Launcher")
        self.clock = pygame.time.Clock()
        self.result = None
        self.loading = False
        self.button_rect = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
        
        # Animation vars
        self.particles = []
        self.coin_rotation = 0

    def draw_gradient_bg(self):
        """Draw vertical gradient background"""
        for y in range(HEIGHT):
            # Interpolate between dark blue and purple
            r = int(18 + (138 - 18) * (y / HEIGHT))
            g = int(18 + (99 - 18) * (y / HEIGHT))
            b = int(29 + (210 - 29) * (y / HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    def draw_button(self):
        """Animated button with hover effect"""
        mouse_pos = pygame.mouse.get_pos()
        hover = self.button_rect.collidepoint(mouse_pos)
        
        # Button color pulse effect
        pulse = int(10 * abs(pygame.time.get_ticks() % 2000 - 1000) / 1000)
        btn_color = (
            min(PRIMARY[0] + pulse, 255),
            min(PRIMARY[1] + pulse, 255),
            min(PRIMARY[2] + pulse, 255)
        ) if hover else PRIMARY
        
        # Button shadow
        shadow_rect = self.button_rect.move(5, 5)
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=12)
        
        # Button main
        pygame.draw.rect(self.screen, btn_color, self.button_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, self.button_rect, 2, border_radius=10)
        
        # Button text
        btn_text = BUTTON_FONT.render(
            "LAUNCHING..." if self.loading else "LAUNCH COIN", 
            True, 
            WHITE if hover else WHITE
        )
        text_rect = btn_text.get_rect(center=self.button_rect.center)
        self.screen.blit(btn_text, text_rect)

    def draw_header(self):
        """Title and network status"""
        # Title
        title = TITLE_FONT.render("MEME COIN LAUNCHER", True, WHITE)
        title_shadow = TITLE_FONT.render("MEME COIN LAUNCHER", True, (0, 0, 0, 100))
        self.screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 3, 80 + 3))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        # Network indicator
        network_text = BODY_FONT.render(
            f"NETWORK: {SETTINGS['network'].upper()} | MODE: {'MOCK' if SETTINGS['mock_mode'] else 'LIVE'}", 
            True, 
            SECONDARY
        )
        self.screen.blit(network_text, (20, 20))
        
        # Solana icon
        if SOLANA_ICON:
            self.screen.blit(SOLANA_ICON, (WIDTH - 60, 15))

    def draw_result(self):
        """Show transaction details after launch"""
        if self.result:
            # Success box
            result_rect = pygame.Rect(50, 300, WIDTH - 100, 200)
            pygame.draw.rect(self.screen, (30, 30, 46), result_rect, border_radius=12)
            pygame.draw.rect(self.screen, SECONDARY, result_rect, 2, border_radius=12)
            
            # Result text
            texts = [
                f"COIN LAUNCHED SUCCESSFULLY!",
                f"Transaction: {self.result['tx_id']}",
                f"View on Solscan: {self.result['solscan_url']}",
                f"Time: {self.result['timestamp']}"
            ]
            
            for i, text in enumerate(texts):
                text_surf = BODY_FONT.render(text, True, WHITE if i == 0 else SECONDARY)
                self.screen.blit(text_surf, (70, 330 + i * 35))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos) and not self.loading:
                        self.loading = True
                        self.result = None
                        # Simulate async launch
                        pygame.time.set_timer(pygame.USEREVENT, 1500)  # 1.5s delay
            
                if event.type == pygame.USEREVENT:
                    self.result = launch_memecoin()
                    self.loading = False
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop timer
            
            # Render
            self.draw_gradient_bg()
            self.draw_header()
            self.draw_button()
            self.draw_result()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = MemeCoinLauncher()
    app.run()