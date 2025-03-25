import pytest
import pygame
from src.sprites.player import Player
from src.utils.constants import WIDTH, HEIGHT, BASE_PLAYER_SPEED, JUMP_FORCE

@pytest.fixture
def player():
    pygame.init()
    return Player()

def test_player_initial_position(player):
    assert player.rect.centerx == WIDTH // 2
    assert player.rect.centery == HEIGHT // 2
    assert player.is_grounded == False  # Should start in air

def test_player_movement(player):
    """Test player movement within screen boundaries"""
    initial_x = player.rect.x
    
    # Test no movement when grounded
    player.is_grounded = True
    player.velocity_x = BASE_PLAYER_SPEED
    player.update()
    assert player.rect.x == initial_x, "Player shouldn't move while grounded"
    
    # Test movement in air
    player.is_grounded = False
    player.velocity_x = BASE_PLAYER_SPEED
    player.update()
    # Since Pygame rects use integer positions, we need to account for rounding
    expected_x = round(initial_x + BASE_PLAYER_SPEED)
    assert player.rect.x == expected_x, \
        f"Player should move right by ~{BASE_PLAYER_SPEED} units (rounded to nearest pixel)"
    
    # Test screen boundaries
    player.rect.x = 0
    player.velocity_x = -BASE_PLAYER_SPEED
    player.update()
    assert player.rect.left >= 0, "Player should not move beyond left boundary"
    
    player.rect.x = WIDTH
    player.velocity_x = BASE_PLAYER_SPEED
    player.update()
    assert player.rect.right <= WIDTH, "Player should not move beyond right boundary"

def test_player_jump(player):
    """Test player jumping mechanics"""
    initial_y = player.rect.y
    
    # Test jump
    player.velocity_y = JUMP_FORCE
    player.update()
    assert player.rect.y < initial_y, "Player should move up when jumping"
    assert player.is_grounded == False, "Player should be in air while jumping"
    
    # Test gravity
    initial_velocity = player.velocity_y
    player.update()
    assert player.velocity_y > initial_velocity, "Gravity should increase downward velocity"

def test_ground_collision(player):
    """Test ground collision and grounded state"""
    # Move player to ground
    player.rect.bottom = HEIGHT
    player.velocity_y = 1
    player.update()
    
    assert player.is_grounded == True, "Player should be grounded when on floor"
    assert player.velocity_y == 0, "Vertical velocity should be 0 when grounded"
    assert player.velocity_x == 0, "Horizontal velocity should be 0 when grounded" 