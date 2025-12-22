"""
Configuration file for the Football Statistics ML Project
"""

# Model Configuration
MODEL_CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'n_estimators': 100,
    'max_depth': 10,
}

# Feature columns for prediction
FEATURE_COLUMNS = [
    'minutes_played',
    'goals',
    'assists',
    'shots',
    'shots_on_target',
    'passes_completed',
    'pass_accuracy',
    'tackles',
    'interceptions',
    'dribbles_completed',
]

# Target column
TARGET_COLUMN = 'performance_rating'

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'title': 'Football Player Statistics & Predictions Dashboard',
    'page_icon': '⚽',
    'layout': 'wide',
}

# Field dimensions (in meters)
FIELD_CONFIG = {
    'length': 105,
    'width': 68,
}

