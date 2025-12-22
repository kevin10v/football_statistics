"""
Streamlit Dashboard for Football Player Statistics and Predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from model import PlayerPerformanceModel
from data_generator import generate_heatmap_data
import config
import os


# Page configuration
st.set_page_config(
    page_title=config.DASHBOARD_CONFIG['title'],
    page_icon=config.DASHBOARD_CONFIG['page_icon'],
    layout=config.DASHBOARD_CONFIG['layout']
)


@st.cache_data
def load_data():
    """Load player statistics data"""
    if os.path.exists('player_statistics.csv'):
        return pd.read_csv('player_statistics.csv')
    else:
        st.error("Data file not found. Please run data_generator.py first.")
        return None


@st.cache_resource
def load_model():
    """Load the trained ML model"""
    model = PlayerPerformanceModel()
    if os.path.exists('player_performance_model.pkl'):
        model.load_model()
        return model
    else:
        st.warning("Model not found. Please train the model first.")
        return None


def create_football_field():
    """Create a football field visualization"""
    fig = go.Figure()
    
    # Field outline
    fig.add_shape(type="rect", x0=0, y0=0, x1=105, y1=68,
                  line=dict(color="white", width=2), fillcolor="green")
    
    # Center line
    fig.add_shape(type="line", x0=52.5, y0=0, x1=52.5, y1=68,
                  line=dict(color="white", width=2))
    
    # Center circle
    fig.add_shape(type="circle", x0=52.5-9.15, y0=34-9.15, x1=52.5+9.15, y1=34+9.15,
                  line=dict(color="white", width=2))
    
    # Penalty areas
    fig.add_shape(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16,
                  line=dict(color="white", width=2))
    fig.add_shape(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16,
                  line=dict(color="white", width=2))
    
    # Goal areas
    fig.add_shape(type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16,
                  line=dict(color="white", width=2))
    fig.add_shape(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16,
                  line=dict(color="white", width=2))
    
    fig.update_xaxes(range=[0, 105], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[0, 68], showgrid=False, zeroline=False, visible=False)
    fig.update_layout(
        plot_bgcolor='green',
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    return fig


def plot_heatmap(player_name: str):
    """Create a heatmap of player's field coverage"""
    x_pos, y_pos = generate_heatmap_data(player_name)
    
    fig = create_football_field()
    
    # Add heatmap
    fig.add_trace(go.Histogram2d(
        x=x_pos,
        y=y_pos,
        colorscale='Hot',
        showscale=True,
        nbinsx=30,
        nbinsy=20,
        opacity=0.7,
        colorbar=dict(title="Density")
    ))
    
    fig.update_layout(title=f"Field Coverage Heatmap - {player_name}")
    
    return fig


def plot_player_stats_radar(player_data: pd.DataFrame):
    """Create a radar chart for player statistics"""
    # Normalize stats to 0-100 scale for visualization
    stats_to_plot = ['goals', 'assists', 'shots_on_target', 'pass_accuracy', 
                     'tackles', 'interceptions', 'dribbles_completed']
    
    avg_stats = player_data[stats_to_plot].mean()
    
    # Normalize
    max_vals = {
        'goals': 2, 'assists': 2, 'shots_on_target': 5,
        'pass_accuracy': 100, 'tackles': 8, 'interceptions': 8,
        'dribbles_completed': 5
    }
    
    normalized = [(avg_stats[stat] / max_vals[stat] * 100) for stat in stats_to_plot]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized,
        theta=[s.replace('_', ' ').title() for s in stats_to_plot],
        fill='toself',
        name='Player Stats'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Player Performance Radar"
    )
    
    return fig


def plot_performance_trend(player_data: pd.DataFrame):
    """Plot performance rating trend over matches"""
    fig = px.line(player_data, x='match_id', y='performance_rating',
                  title='Performance Rating Trend',
                  labels={'match_id': 'Match Number', 'performance_rating': 'Performance Rating'})
    
    fig.add_scatter(x=player_data['match_id'], y=player_data['performance_rating'],
                    mode='markers', marker=dict(size=8, color='red'))
    
    return fig


def main():
    """Main dashboard function"""
    
    st.title("⚽ Football Player Statistics & Predictions Dashboard")
    st.markdown("---")
    
    # Load data and model
    df = load_data()
    model = load_model()
    
    if df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.header("🎯 Player Selection")
    
    # Player selection
    players = sorted(df['player_name'].unique())
    selected_player = st.sidebar.selectbox("Select Player", players)
    
    # Filter data for selected player
    player_data = df[df['player_name'] == selected_player].copy()
    
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Statistics")
    st.sidebar.metric("Total Matches", len(player_data))
    st.sidebar.metric("Position", player_data['position'].iloc[0])
    st.sidebar.metric("Avg Performance", f"{player_data['performance_rating'].mean():.2f}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"📍 Field Coverage - {selected_player}")
        heatmap_fig = plot_heatmap(selected_player)
        st.plotly_chart(heatmap_fig, use_container_width=True)
    
    with col2:
        st.header("📈 Performance Radar")
        radar_fig = plot_player_stats_radar(player_data)
        st.plotly_chart(radar_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Performance trend
    st.header("📊 Performance Trend")
    trend_fig = plot_performance_trend(player_data)
    st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("⚽ Attacking Stats")
        st.metric("Total Goals", int(player_data['goals'].sum()))
        st.metric("Total Assists", int(player_data['assists'].sum()))
        st.metric("Avg Shots per Match", f"{player_data['shots'].mean():.2f}")
        st.metric("Shot Accuracy", f"{(player_data['shots_on_target'].sum() / max(player_data['shots'].sum(), 1) * 100):.1f}%")
    
    with col2:
        st.subheader("🎯 Passing Stats")
        st.metric("Total Passes", int(player_data['passes_completed'].sum()))
        st.metric("Avg Pass Accuracy", f"{player_data['pass_accuracy'].mean():.1f}%")
        st.metric("Passes per Match", f"{player_data['passes_completed'].mean():.1f}")
    
    with col3:
        st.subheader("🛡️ Defensive Stats")
        st.metric("Total Tackles", int(player_data['tackles'].sum()))
        st.metric("Total Interceptions", int(player_data['interceptions'].sum()))
        st.metric("Avg Dribbles", f"{player_data['dribbles_completed'].mean():.2f}")
    
    st.markdown("---")
    
    # ML Predictions
    if model and model.is_trained:
        st.header("🤖 Performance Prediction")
        
        st.write("Adjust the statistics to predict performance rating:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            minutes = st.slider("Minutes Played", 0, 90, 90)
            goals = st.slider("Goals", 0, 5, 0)
            assists = st.slider("Assists", 0, 5, 0)
            shots = st.slider("Shots", 0, 15, 5)
        
        with col2:
            shots_on_target = st.slider("Shots on Target", 0, shots, min(shots, 3))
            passes = st.slider("Passes Completed", 0, 100, 50)
            pass_acc = st.slider("Pass Accuracy %", 0.0, 100.0, 85.0)
        
        with col3:
            tackles = st.slider("Tackles", 0, 15, 3)
            interceptions = st.slider("Interceptions", 0, 15, 3)
            dribbles = st.slider("Dribbles Completed", 0, 10, 2)
        
        # Create prediction dataframe
        prediction_data = pd.DataFrame({
            'minutes_played': [minutes],
            'goals': [goals],
            'assists': [assists],
            'shots': [shots],
            'shots_on_target': [shots_on_target],
            'passes_completed': [passes],
            'pass_accuracy': [pass_acc],
            'tackles': [tackles],
            'interceptions': [interceptions],
            'dribbles_completed': [dribbles],
        })
        
        # Make prediction
        prediction = model.predict(prediction_data)[0]
        
        st.markdown("### Predicted Performance Rating")
        st.markdown(f"<h1 style='text-align: center; color: {'green' if prediction > 50 else 'orange'};'>{prediction:.2f} / 100</h1>", 
                   unsafe_allow_html=True)
        
        # Feature importance
        st.markdown("---")
        st.subheader("🔍 Feature Importance")
        importance_df = model.get_feature_importance()
        
        fig = px.bar(importance_df, x='importance', y='feature', orientation='h',
                    title='Feature Importance in Prediction Model')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent matches table
    st.markdown("---")
    st.header("📋 Recent Matches")
    recent_matches = player_data.sort_values('match_id', ascending=False).head(10)
    st.dataframe(recent_matches[['match_id', 'goals', 'assists', 'passes_completed', 
                                  'pass_accuracy', 'tackles', 'interceptions', 
                                  'performance_rating']], use_container_width=True)


if __name__ == "__main__":
    main()

