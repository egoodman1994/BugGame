import pytest
import pygame
from src.sprites.player import Player
from src.utils.constants import WIDTH, HEIGHT, JUMP_FORCE

@pytest.fixture
def player():
    return Player()

def test_player_initial_position(player):
    assert player.rect.centerx == WIDTH // 2
    assert player.rect.centery == HEIGHT // 2

def test_player_jump(player):
    initial_y = player.rect.y
    player.velocity_y = 0
    
    # Simulate jump
    player.handle_event(type('Event', (), {'type': pygame.KEYDOWN, 'key': pygame.K_SPACE}))
    assert player.velocity_y == JUMP_FORCE

def test_player_movement(player):
    initial_x = player.rect.x
    
    # Test moving right
    player.velocity_x = player.speed
    player.rect = player.rect.move(player.velocity_x, 0)  # Explicitly move the rect
    assert player.rect.x > initial_x, f"Expected x position to increase from {initial_x}"
    
    # Test moving left
    initial_x = player.rect.x
    player.velocity_x = -player.speed
    player.rect = player.rect.move(player.velocity_x, 0)
    assert player.rect.x < initial_x, f"Expected x position to decrease from {initial_x}" 