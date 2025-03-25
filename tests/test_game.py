import pytest
import pygame
from src.game import Game
from src.sprites.bug import Bug
from src.utils.constants import (SPEED_POWER_DURATION, GOLDEN_POWER_DURATION,
                               WIDTH, HEIGHT, BLACK_BUG_SPAWN_THRESHOLD)

@pytest.fixture
def game():
    pygame.init()
    return Game()

def test_game_initial_state(game):
    assert game.score == 0
    assert game.game_started == False
    assert game.game_over == False
    assert len(game.black_bugs) == 0

def test_black_bug_spawning(game):
    """Test black bug spawning mechanics"""
    # Should have no black bugs below threshold
    game.score = BLACK_BUG_SPAWN_THRESHOLD - 1
    game.update_black_bugs()
    assert len(game.black_bugs) == 0
    
    # Should spawn one black bug at threshold
    game.score = BLACK_BUG_SPAWN_THRESHOLD
    game.black_bug_timer = 0  # Reset timer to force spawn
    game.update_black_bugs()
    assert len(game.black_bugs) == 1

def test_power_up_timers(game):
    initial_speed_timer = 60  # 1 second
    initial_golden_timer = 60  # 1 second
    
    # Set initial values
    game.speed_boost_timer = initial_speed_timer
    game.golden_power_timer = initial_golden_timer
    
    # Update should decrease timers
    game.handle_normal_game_update()
    
    # Check that timers decreased by 1
    assert game.speed_boost_timer == initial_speed_timer - 1
    assert game.golden_power_timer == initial_golden_timer - 1

def test_score_system(game):
    """Test scoring mechanics"""
    initial_score = game.score
    
    # Create a normal bug and simulate collision
    normal_bug = Bug("normal")
    game.normal_bugs = [normal_bug]
    normal_bug.rect.x = game.player.rect.x
    normal_bug.rect.y = game.player.rect.y
    game.handle_other_collisions()
    assert game.score > initial_score

def test_power_ups(game):
    """Test power-up mechanics"""
    # Test speed boost
    power_bug = Bug("power")
    game.power_bug = power_bug
    game.power_bug_active = True
    power_bug.rect.x = game.player.rect.x
    power_bug.rect.y = game.player.rect.y
    game.handle_other_collisions()
    assert game.speed_boost_timer == SPEED_POWER_DURATION

def test_game_over(game):
    """Test game over conditions"""
    game.game_started = True
    game.score = 100  # Set a score that would be a high score
    
    # Simulate black bug collision
    black_bug = Bug("black")
    game.black_bugs = [black_bug]
    black_bug.rect.x = game.player.rect.x
    black_bug.rect.y = game.player.rect.y
    game.handle_black_bug_collisions()
    
    assert game.entering_name or game.game_over 