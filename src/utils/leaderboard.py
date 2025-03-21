import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def migrate_old_scores():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                old_scores = json.load(f)
            # Check if we need to migrate
            if old_scores and isinstance(old_scores[0], int):
                # Convert old scores to new format
                new_scores = [{"name": "???", "score": score} for score in old_scores]
                with open(LEADERBOARD_FILE, 'w') as f:
                    json.dump(new_scores, f)
                return new_scores
    except:
        pass
    return []

def load_scores():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                scores = json.load(f)
                # Check if scores need migration
                if scores and isinstance(scores[0], int):
                    return migrate_old_scores()
                return scores
        return []
    except:
        return []

def save_score(name, score):
    scores = load_scores()
    # Add new score with name
    scores.append({"name": name.upper()[:3], "score": score})
    # Sort in descending order by score and keep top 5
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]
    
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(scores, f)

def get_top_scores():
    return load_scores()

def is_high_score(score):
    scores = load_scores()
    if len(scores) < 5:  # Less than 5 scores
        # Check if the score is higher than any existing score
        return len(scores) == 0 or score > min(s["score"] for s in scores)
    
    # We have 5 or more scores
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]
    lowest_score = sorted_scores[-1]["score"]
    return score > lowest_score 