import pytest
import pygame
from src.sprites.bug import Bug
from src.utils.constants import (NORMAL_BUG_SPEED, GOLDEN_BUG_SPEED, 
                               POWER_BUG_SPEED, WIDTH, HEIGHT)

@pytest.fixture
def setup_pygame():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))

def test_bug_initialization(setup_pygame):
    """Test different bug types are created correctly"""
    normal_bug = Bug("normal")
    assert normal_bug.points == 1
    assert normal_bug.speed == NORMAL_BUG_SPEED
    
    golden_bug = Bug("golden")
    assert golden_bug.points == 5
    assert golden_bug.speed == GOLDEN_BUG_SPEED
    
    power_bug = Bug("power")
    assert power_bug.points == 0
    assert power_bug.speed == POWER_BUG_SPEED

def test_bug_movement(setup_pygame):
    """Test bug movement patterns"""
    bug = Bug("normal")
    initial_pos = (bug.rect.x, bug.rect.y)
    
    # Test movement
    bug.update()
    current_pos = (bug.rect.x, bug.rect.y)
    assert current_pos != initial_pos
    
    # Test screen boundaries
    bug.rect.x = -1
    bug.update()
    assert bug.rect.left >= 0 