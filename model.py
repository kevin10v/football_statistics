"""
Machine Learning model for predicting player performance
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Tuple, Dict
import config


class PlayerPerformanceModel:
    """
    ML Model for predicting player performance ratings
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = config.FEATURE_COLUMNS
        self.target_column = config.TARGET_COLUMN
        self.is_trained = False
        
    def prepare_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for training/prediction
        
        Args:
            df: Input dataframe
            
        Returns:
            Tuple of (features, target)
        """
        X = df[self.feature_columns].copy()
        y = df[self.target_column].copy() if self.target_column in df.columns else None
        
        return X, y
    
    def train(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Train the model on player statistics data
        
        Args:
            df: Training dataframe
            
        Returns:
            Dictionary with training metrics
        """
        X, y = self.prepare_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=config.MODEL_CONFIG['test_size'],
            random_state=config.MODEL_CONFIG['random_state']
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=config.MODEL_CONFIG['n_estimators'],
            max_depth=config.MODEL_CONFIG['max_depth'],
            random_state=config.MODEL_CONFIG['random_state'],
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Evaluate
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
        }
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, 
            cv=5, scoring='r2'
        )
        metrics['cv_r2_mean'] = cv_scores.mean()
        metrics['cv_r2_std'] = cv_scores.std()
        
        return metrics
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Make predictions on new data
        
        Args:
            df: Input dataframe with features
            
        Returns:
            Array of predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X, _ = self.prepare_data(df)
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        return predictions
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from the trained model
        
        Returns:
            DataFrame with feature names and importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def save_model(self, filepath: str = 'player_performance_model.pkl'):
        """Save the trained model to disk"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }, filepath)
        
    def load_model(self, filepath: str = 'player_performance_model.pkl'):
        """Load a trained model from disk"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']
        self.target_column = data['target_column']
        self.is_trained = True


def train_and_save_model(data_path: str = 'player_statistics.csv'):
    """
    Train the model and save it
    
    Args:
        data_path: Path to the training data CSV
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Initialize and train model
    model = PlayerPerformanceModel()
    metrics = model.train(df)
    
    # Print metrics
    print("Model Training Complete!")
    print("\n=== Training Metrics ===")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Print feature importance
    print("\n=== Feature Importance ===")
    importance_df = model.get_feature_importance()
    print(importance_df.to_string(index=False))
    
    # Save model
    model.save_model()
    print("\nModel saved to 'player_performance_model.pkl'")
    
    return model, metrics


if __name__ == "__main__":
    train_and_save_model()

