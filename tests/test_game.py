import pytest
from src.game import Game
from src.utils.constants import BLACK_BUG_SPAWN_THRESHOLD

@pytest.fixture
def game():
    return Game()

def test_game_initial_state(game):
    assert game.score == 0
    assert game.game_started == False
    assert game.game_over == False
    assert len(game.black_bugs) == 0

def test_black_bug_spawning(game):
    # Should have no black bugs below threshold
    game.score = BLACK_BUG_SPAWN_THRESHOLD - 1
    game.update_black_bugs()
    assert len(game.black_bugs) == 0
    
    # Should spawn one black bug at threshold
    game.score = BLACK_BUG_SPAWN_THRESHOLD
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