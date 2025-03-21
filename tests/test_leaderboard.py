import pytest
import os
from src.utils.leaderboard import save_score, get_top_scores, is_high_score

@pytest.fixture
def clean_leaderboard():
    # Setup
    if os.path.exists("leaderboard.json"):
        os.remove("leaderboard.json")
    yield
    # Teardown
    if os.path.exists("leaderboard.json"):
        os.remove("leaderboard.json")

def test_save_and_get_scores(clean_leaderboard):
    save_score("ABC", 100)
    scores = get_top_scores()
    assert len(scores) == 1
    assert scores[0]["name"] == "ABC"
    assert scores[0]["score"] == 100

def test_high_score_detection(clean_leaderboard):
    # Empty leaderboard should always be high score
    assert is_high_score(1) == True
    
    # Add some scores
    save_score("ABC", 100)
    save_score("DEF", 50)
    save_score("GHI", 25)
    
    # Test high score detection
    assert is_high_score(101) == True  # Higher than highest
    assert is_high_score(99) == True   # Would make top 5
    assert is_high_score(10) == False  # Too low 