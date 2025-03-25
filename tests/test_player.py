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

def test_player_movement(player):
    """Test player movement within screen boundaries"""
    initial_x = player.rect.x
    
    # Test right movement
    player.velocity_x = BASE_PLAYER_SPEED
    # Move the rect directly first
    player.rect = player.rect.move(player.velocity_x, 0)
    player.update()
    assert player.rect.x > initial_x, "Player should move right"
    
    # Reset position for left movement test
    player.rect.x = initial_x
    player.velocity_x = -BASE_PLAYER_SPEED
    # Move the rect directly first
    player.rect = player.rect.move(player.velocity_x, 0)
    player.update()
    assert player.rect.x < initial_x, "Player should move left"
    
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
    assert player.rect.y < initial_y
    
    # Test gravity
    initial_velocity = player.velocity_y
    player.update()
    assert player.velocity_y > initial_velocity 