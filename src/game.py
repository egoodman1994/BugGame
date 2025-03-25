import pygame
import random  # Add at the top with other imports
from .sprites.player import Player
from .sprites.bug import Bug
from .utils.constants import (WIDTH, HEIGHT, FPS, WHITE, BLACK, BLUE, GOLD, 
                            POWER_UP_DURATION, BACKGROUND_WIDTH, BACKGROUND_HEIGHT,
                            SPEED_THRESHOLD_1, SPEED_THRESHOLD_2, SPEED_THRESHOLD_3, SPEED_THRESHOLD_4,
                            NORMAL_BUG_SPEED, GOLDEN_BUG_SPEED, POWER_BUG_SPEED,
                            SPEED_MULTIPLIER, BASE_PLAYER_SPEED,
                            BLACK_BUG_SPEED, BLACK_BUG_SPAWN_THRESHOLD, BLACK_BUG_SPAWN_INTERVAL,
                            GOLDEN_POWER_DURATION, SPEED_POWER_DURATION,
                            POWER_BUG_MIN_SPAWN_TIME, POWER_BUG_MAX_SPAWN_TIME,
                            GOLDEN_BUG_MIN_SPAWN_TIME, GOLDEN_BUG_MAX_SPAWN_TIME,
                            NORMAL_BUG_POINTS_THRESHOLD, NORMAL_BUG_MAX_COUNT)
from .utils.leaderboard import save_score, get_top_scores, is_high_score
import os
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bug Catcher Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 74)  # Larger font for title
        self.instruction_font = pygame.font.Font(None, 25)  # ~30% smaller than regular font
        
        # Add background loading
        self.load_background()
        
        self.running = True
        self.game_started = False  # New flag for title screen
        self.score = 0
        self.speed_boost_timer = 0
        self.golden_power_timer = 0  # Add new timer for golden power-up
        self.current_speed_multiplier = 1.0
        self.last_threshold_reached = 0
        self.black_bugs = []  # List to hold multiple black bugs
        self.game_over = False
        self.reset_game()
        self.name_input = ""
        self.entering_name = False
        
        # Create sprites
        self.player = Player()
        self.golden_bug = Bug("golden")
        self.power_bug = Bug("power")
        
        self.high_scores = get_top_scores()
        
        # Add power bug spawn timer
        self.power_bug_timer = random.randint(POWER_BUG_MIN_SPAWN_TIME, POWER_BUG_MAX_SPAWN_TIME)
        self.golden_bug_timer = random.randint(GOLDEN_BUG_MIN_SPAWN_TIME, GOLDEN_BUG_MAX_SPAWN_TIME)
        self.power_bug_active = False
        self.golden_bug_active = False
        self.normal_bugs = []  # List to hold normal bugs

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        # Make sure to handle the assets directory correctly
        if relative_path.startswith("assets/"):
            return os.path.join(base_path, relative_path)
        return os.path.join(base_path, "assets", relative_path)

    def load_background(self):
        try:
            # Use resource_path for loading assets
            path = self.resource_path("images/background.png")
            self.background = pygame.image.load(path)
            self.background = pygame.transform.scale(self.background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill(WHITE)

    def check_game_over(self):
        print(f"Checking game over - Score: {self.score}, Golden Power: {self.golden_power_timer}")  # Debug
        if self.golden_power_timer > 0:  # Don't end game if powered up
            return False
        
        # Set the appropriate state
        if is_high_score(self.score):
            self.entering_name = True
            self.game_over = False  # Make sure game_over is False when entering name
        else:
            self.game_over = True
            self.entering_name = False
        
        # Stop all movement
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        
        print("Game over state set successfully")  # Add debug print
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Add ESC key check
                    self.running = False
                elif self.entering_name:
                    if event.key == pygame.K_RETURN and len(self.name_input) > 0:
                        save_score(self.name_input, self.score)
                        self.high_scores = get_top_scores()
                        self.entering_name = False
                        self.game_over = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif len(self.name_input) < 3 and event.unicode.isalpha():
                        self.name_input += event.unicode
                elif self.game_over and event.key == pygame.K_r:
                    self.reset_game()
                elif not self.game_started and event.key == pygame.K_SPACE:
                    self.game_started = True
            
            if self.game_started and not self.game_over and not self.entering_name:
                self.player.handle_event(event)

    def update_speed_multiplier(self):
        # Check if we've reached a new threshold
        if (self.score >= SPEED_THRESHOLD_4 and self.last_threshold_reached < SPEED_THRESHOLD_4):
            self.current_speed_multiplier = 2.0
            self.last_threshold_reached = SPEED_THRESHOLD_4
        elif (self.score >= SPEED_THRESHOLD_3 and self.last_threshold_reached < SPEED_THRESHOLD_3):
            self.current_speed_multiplier = 1.8
            self.last_threshold_reached = SPEED_THRESHOLD_3
        elif (self.score >= SPEED_THRESHOLD_2 and self.last_threshold_reached < SPEED_THRESHOLD_2):
            self.current_speed_multiplier = 1.5
            self.last_threshold_reached = SPEED_THRESHOLD_2
        elif (self.score >= SPEED_THRESHOLD_1 and self.last_threshold_reached < SPEED_THRESHOLD_1):
            self.current_speed_multiplier = 1.2
            self.last_threshold_reached = SPEED_THRESHOLD_1

    def reset_game(self):
        self.score = 0
        self.speed_boost_timer = 0
        self.golden_power_timer = 0
        self.current_speed_multiplier = 1.0
        self.last_threshold_reached = 0
        self.black_bugs = []
        self.game_over = False
        self.entering_name = False
        self.name_input = ""
        
        # Reset sprites
        self.player = Player()
        self.golden_bug = Bug("golden")
        self.power_bug = Bug("power")
        
        # Reset power bug state
        self.power_bug_timer = random.randint(POWER_BUG_MIN_SPAWN_TIME, POWER_BUG_MAX_SPAWN_TIME)
        self.golden_bug_timer = random.randint(GOLDEN_BUG_MIN_SPAWN_TIME, GOLDEN_BUG_MAX_SPAWN_TIME)
        self.power_bug_active = False
        self.golden_bug_active = False
        self.power_bug = None
        self.golden_bug = None
        self.normal_bugs = [Bug("normal")]  # Start with one normal bug

    def update_black_bugs(self):
        # Only proceed if score is at or above threshold
        if self.score < BLACK_BUG_SPAWN_THRESHOLD:
            self.black_bugs = []  # Clear any existing black bugs
            return
            
        # Calculate how many black bugs should be active
        expected_black_bugs = max(0, self.score - BLACK_BUG_SPAWN_THRESHOLD) // BLACK_BUG_SPAWN_INTERVAL + 1
        
        # Add new black bugs if needed
        while len(self.black_bugs) < expected_black_bugs:
            self.black_bugs.append(Bug("black"))

        # Update existing black bugs
        for bug in self.black_bugs:
            bug.speed = BLACK_BUG_SPEED * self.current_speed_multiplier
            bug.update()

    def update_normal_bugs(self):
        # Calculate how many normal bugs should be active
        expected_bugs = min(1 + (self.score // NORMAL_BUG_POINTS_THRESHOLD), NORMAL_BUG_MAX_COUNT)
        
        # Add new bugs if needed
        while len(self.normal_bugs) < expected_bugs:
            self.normal_bugs.append(Bug("normal"))
            
        # Update all normal bugs
        for bug in self.normal_bugs:
            bug.update()

    def update(self):
        if not self.game_started:
            return

        # Handle game over state first
        if self.game_over or self.entering_name:
            self.handle_game_over_state()
            return

        # Rest of normal game update...
        self.handle_normal_game_update()

    def handle_game_over_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.reset_game()

    def handle_normal_game_update(self):
        # Update power-up timers
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            self.player.speed = BASE_PLAYER_SPEED * SPEED_MULTIPLIER  # Apply speed multiplier
            if self.speed_boost_timer == 0:
                self.player.speed = BASE_PLAYER_SPEED

        if self.golden_power_timer > 0:
            self.golden_power_timer -= 1

        # Update speed multiplier based on score
        self.update_speed_multiplier()

        # Handle power bug spawning
        if not self.power_bug_active:
            self.power_bug_timer -= 1
            if self.power_bug_timer <= 0:
                self.power_bug = Bug("power")
                self.power_bug_active = True
        else:
            self.power_bug.update()

        # Handle golden bug spawning
        if not self.golden_bug_active:
            self.golden_bug_timer -= 1
            if self.golden_bug_timer <= 0:
                self.golden_bug = Bug("golden")
                self.golden_bug_active = True
        else:
            self.golden_bug.update()

        # Update normal bugs
        self.update_normal_bugs()
        
        # Update other sprites
        self.player.update()

        # Handle black bugs
        if self.score >= BLACK_BUG_SPAWN_THRESHOLD:
            self.update_black_bugs()
            self.handle_black_bug_collisions()
            if self.game_over or self.entering_name:  # Add this check
                return

        # Only handle other collisions if game isn't over
        if not self.game_over and not self.entering_name:
            self.handle_other_collisions()

    def handle_black_bug_collisions(self):
        black_bugs_to_remove = []
        for i, bug in enumerate(self.black_bugs):
            if self.player.rect.colliderect(bug.rect):
                if self.golden_power_timer > 0:
                    self.score += 5
                    black_bugs_to_remove.append(i)
                else:
                    print("Black bug collision - ending game")  # Debug
                    self.check_game_over()  # Remove the if and return here
                    break  # Just break the loop instead of return

        # Remove eaten black bugs
        for i in reversed(black_bugs_to_remove):
            self.black_bugs.pop(i)

    def handle_other_collisions(self):
        # Handle normal bug collisions
        bugs_to_remove = []
        for i, bug in enumerate(self.normal_bugs):
            if self.player.rect.colliderect(bug.rect):
                self.score += bug.points
                bugs_to_remove.append(i)
        
        # Remove eaten bugs and spawn new ones
        for i in reversed(bugs_to_remove):
            self.normal_bugs.pop(i)
            self.normal_bugs.append(Bug("normal"))

        if self.golden_bug_active and self.player.rect.colliderect(self.golden_bug.rect):
            self.score += self.golden_bug.points
            self.golden_power_timer = GOLDEN_POWER_DURATION
            self.golden_bug_active = False
            self.golden_bug_timer = random.randint(GOLDEN_BUG_MIN_SPAWN_TIME, GOLDEN_BUG_MAX_SPAWN_TIME)

        if self.power_bug_active and self.player.rect.colliderect(self.power_bug.rect):
            self.speed_boost_timer = SPEED_POWER_DURATION
            self.player.speed = BASE_PLAYER_SPEED * SPEED_MULTIPLIER  # Set speed immediately
            self.power_bug_active = False
            self.power_bug_timer = random.randint(POWER_BUG_MIN_SPAWN_TIME, POWER_BUG_MAX_SPAWN_TIME)

    def draw_title_screen(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title and subtitle with same color
        title_text = self.title_font.render("EB catches bugs", True, BLACK)
        subtitle_text = self.font.render("We don't make them", True, BLACK)  # Changed from BLUE to BLACK
        
        # Center the text, moving subtitle closer to title
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 45))  # Moved closer to title
        
        # Draw text
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw instructions with smaller font
        instructions = [
            "Catch green bugs for 1 point",
            "Golden bugs are worth 5 points!",
            "Blue bugs give speed boost",
            "Avoid black bugs - they're deadly!",
            "Use arrow keys to move, SPACE to jump"
        ]
        
        for i, text in enumerate(instructions):
            instruction_text = self.instruction_font.render(text, True, BLACK)  # Using smaller font
            text_rect = instruction_text.get_rect(
                center=(WIDTH//2, HEIGHT//2 + 50 + i * 25)  # Reduced spacing between lines
            )
            self.screen.blit(instruction_text, text_rect)

        # Draw high scores
        if self.high_scores:
            high_score = self.high_scores[0]
            high_score_text = self.font.render(
                f"High Score: {high_score['name']} - {high_score['score']}", 
                True, 
                BLUE
            )
            high_score_rect = high_score_text.get_rect(
                center=(WIDTH//2, HEIGHT - 50)
            )
            self.screen.blit(high_score_text, high_score_rect)

    def draw_game_over(self):
        if self.entering_name:
            # Draw name input screen
            name_prompt = self.font.render('Enter your initials:', True, BLACK)
            name_text = self.font.render(self.name_input + ('_' * (3 - len(self.name_input))), True, BLUE)
            
            prompt_rect = name_prompt.get_rect(center=(WIDTH//2, HEIGHT//3))
            name_rect = name_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 40))
            
            self.screen.blit(name_prompt, prompt_rect)
            self.screen.blit(name_text, name_rect)
            
            score_text = self.font.render(f'Final Score: {self.score}', True, BLACK)
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 80))
            self.screen.blit(score_text, score_rect)
            
        else:
            # Draw regular game over screen
            game_over_text = self.font.render('Game Over! Press R to Restart', True, BLACK)
            final_score_text = self.font.render(f'Final Score: {self.score}', True, BLACK)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//3))
            score_rect = final_score_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 40))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(final_score_text, score_rect)

            # Draw leaderboard
            leaderboard_title = self.font.render('High Scores:', True, BLUE)
            self.screen.blit(leaderboard_title, (WIDTH//2 - 60, HEIGHT//2))
            
            for i, score_data in enumerate(self.high_scores):
                score_text = self.font.render(
                    f"{i+1}. {score_data['name']} - {score_data['score']}", 
                    True, 
                    BLACK
                )
                self.screen.blit(score_text, (WIDTH//2 - 40, HEIGHT//2 + 40 + i*30))

    def draw(self):
        if not self.game_started:
            self.draw_title_screen()
            pygame.display.flip()
            return
            
        # Draw background first
        self.screen.blit(self.background, (0, 0))
        
        # Draw all sprites
        if self.golden_bug_active:
            self.golden_bug.draw(self.screen)
        if self.power_bug_active:
            self.power_bug.draw(self.screen)
        for black_bug in self.black_bugs:
            black_bug.draw(self.screen)
        for bug in self.normal_bugs:
            bug.draw(self.screen)
        self.player.draw(self.screen)

        # Draw UI
        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (10, 10))

        if self.game_over or self.entering_name:  # Changed this line to include entering_name
            self.draw_game_over()  # Use our new game over drawing method
        else:
            # Draw power-up timers
            if self.speed_boost_timer > 0:
                boost_text = self.font.render(f'Speed Boost: {self.speed_boost_timer // 60 + 1}s', True, BLUE)
                self.screen.blit(boost_text, (10, 50))

            if self.golden_power_timer > 0:
                golden_text = self.font.render(f'Golden Power: {self.golden_power_timer // 60 + 1}s', True, GOLD)
                self.screen.blit(golden_text, (10, 90))

            if self.current_speed_multiplier > 1.0:
                speed_text = self.font.render(f'Speed Level: {int((self.current_speed_multiplier - 1) * 5)}', True, BLUE)
                self.screen.blit(speed_text, (10, 130))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit() 