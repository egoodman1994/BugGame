import pytest
import pygame
from src.game import Game
from src.sprites.bug import Bug
from src.utils.constants import (SPEED_POWER_DURATION, GOLDEN_POWER_DURATION,
                               WIDTH, HEIGHT, BLACK_BUG_SPAWN_THRESHOLD, SPEED_MULTIPLIER, BASE_PLAYER_SPEED, NORMAL_BUG_MAX_COUNT, MAX_BLACK_BUGS, BLACK_BUG_SPEED)

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
    game.player.speed = BASE_PLAYER_SPEED  # Ensure player has base speed
    
    # Update should decrease timers
    game.handle_normal_game_update()
    
    # Check that timers decreased by 1
    assert game.speed_boost_timer == initial_speed_timer - 1
    assert game.golden_power_timer == initial_golden_timer - 1
    assert game.player.speed == BASE_PLAYER_SPEED * SPEED_MULTIPLIER  # Check speed boost applied

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
    initial_speed = game.player.speed
    
    # Test speed boost
    power_bug = Bug("power")
    game.power_bug = power_bug
    game.power_bug_active = True
    power_bug.rect.x = game.player.rect.x
    power_bug.rect.y = game.player.rect.y
    game.handle_other_collisions()
    
    # Check that speed is increased by the correct multiplier
    assert game.player.speed == pytest.approx(initial_speed * SPEED_MULTIPLIER), \
        "Speed boost should multiply player speed by SPEED_MULTIPLIER (1.7)"
    assert game.speed_boost_timer == SPEED_POWER_DURATION, \
        "Speed boost timer should be set to SPEED_POWER_DURATION"

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

def test_bug_load_performance(game):
    """Test game performance with maximum bug load"""
    # Set up initial conditions
    game.game_started = True
    game.score = 1000  # High score to trigger many bugs
    
    # Track initial bug counts
    initial_normal_bugs = len(game.normal_bugs)
    initial_black_bugs = len(game.black_bugs)
    
    # Update multiple times to stress test
    for _ in range(60):  # Simulate 1 second of gameplay
        game.update_normal_bugs()
        game.update_black_bugs()
        
        # Assert bug counts don't exceed safe limits
        assert len(game.normal_bugs) <= NORMAL_BUG_MAX_COUNT, "Too many normal bugs spawned"
        assert len(game.black_bugs) <= MAX_BLACK_BUGS, "Too many black bugs spawned"
        
        # Test that bugs are being properly cleaned up
        assert all(0 <= bug.rect.x <= WIDTH for bug in game.normal_bugs), "Bugs outside screen bounds"
        assert all(0 <= bug.rect.x <= WIDTH for bug in game.black_bugs), "Black bugs outside screen bounds"

def test_black_bug_movement(game):
    """Test that black bugs move after spawning"""
    # Set up conditions for black bug spawn
    game.score = BLACK_BUG_SPAWN_THRESHOLD
    game.update_black_bugs()
    
    # Verify we have at least one black bug
    assert len(game.black_bugs) > 0, "Black bug should spawn at threshold"
    
    # Record initial position
    bug = game.black_bugs[0]
    initial_x = bug.rect.x
    initial_y = bug.rect.y
    
    # Update and verify movement
    game.update_black_bugs()
    
    # Bug should have moved
    assert (bug.rect.x != initial_x or bug.rect.y != initial_y), \
        "Black bug should move after spawning"
    
    # Verify speed is correctly set
    expected_speed = BLACK_BUG_SPEED * game.current_speed_multiplier
    assert bug.speed == expected_speed, \
        f"Black bug speed should be {expected_speed} (base * multiplier)" 