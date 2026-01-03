import joblib
import pickle

# Try joblib first (common for scikit-learn models)
try:
    model = joblib.load('model.pkl')
    print("✓ Loaded with joblib")
    print("Model type:", type(model))
    print("Model:", model)
    
    # Check if it has feature information
    if hasattr(model, 'feature_names_in_'):
        print("\nFeatures used:", model.feature_names_in_)
    if hasattr(model, 'n_features_in_'):
        print("Number of features:", model.n_features_in_)
        
except Exception as e:
    print("Joblib failed:", e)
    
    # Try regular pickle
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("\n✓ Loaded with pickle")
        print("Model type:", type(model))
        print("Model:", model)
    except Exception as e2:
        print("Pickle also failed:", e2)
