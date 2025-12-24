// Global variables
let currentPlayer = null;
let radarChart = null;
let trendChart = null;
let importanceChart = null;

// Load player data
async function loadPlayerData(playerName) {
    showLoading(true);
    currentPlayer = playerName;
    
    try {
        // Fetch player stats
        const response = await fetch(`/api/player/${encodeURIComponent(playerName)}`);
        const data = await response.json();
        
        // Update UI
        updatePlayerInfo(data);
        updateDetailedStats(data);
        updateRadarChart(data.radar_stats);
        updateTrendChart(data.performance_trend);
        updateRecentMatches(data.recent_matches);
        loadHeatmap(playerName);
        loadFeatureImportance();
        
        // Show dashboard
        document.getElementById('playerDashboard').style.display = 'block';
        showLoading(false);
        
    } catch (error) {
        console.error('Error loading player data:', error);
        alert('Failed to load player data. Please try again.');
        showLoading(false);
    }
}

// Update player profile (with photo and complete info)
function updatePlayerProfile(data) {
    // Photo
    const photoEl = document.getElementById('playerPhoto');
    if (photoEl && data.photo_url) {
        photoEl.src = data.photo_url;
        photoEl.alt = data.player_name;
    }
    
    // Full name
    const nameEl = document.getElementById('playerFullName');
    if (nameEl) {
        nameEl.textContent = data.full_name || data.player_name;
    }
    
    // Profile details
    if (document.getElementById('playerBirthdate')) {
        document.getElementById('playerBirthdate').textContent = data.birth_date || 'Unknown';
    }
    if (document.getElementById('playerAge')) {
        document.getElementById('playerAge').textContent = data.age ? data.age + ' years' : 'Unknown';
    }
    if (document.getElementById('playerNationality')) {
        document.getElementById('playerNationality').textContent = data.nationality || 'Unknown';
    }
    if (document.getElementById('playerPosition')) {
        document.getElementById('playerPosition').textContent = data.positions_full || data.position || 'Unknown';
    }
    if (document.getElementById('playerHeight')) {
        document.getElementById('playerHeight').textContent = data.height_cm || 'Unknown';
    }
    if (document.getElementById('playerWeight')) {
        document.getElementById('playerWeight').textContent = data.weight_kg || 'Unknown';
    }
    if (document.getElementById('playerRating')) {
        document.getElementById('playerRating').textContent = data.overall_rating || '-';
    }
    if (document.getElementById('playerFoot')) {
        document.getElementById('playerFoot').textContent = data.preferred_foot || 'Unknown';
    }
}

// Update player info cards
function updatePlayerInfo(data) {
    // Update profile if elements exist
    if (document.getElementById('playerPhoto')) {
        updatePlayerProfile(data);
    }
    
    // Update stat cards
    if (document.getElementById('statPosition')) {
        document.getElementById('statPosition').textContent = data.position;
    }
    if (document.getElementById('statMatches')) {
        document.getElementById('statMatches').textContent = data.total_matches;
    }
    if (document.getElementById('statPerformance')) {
        document.getElementById('statPerformance').textContent = data.avg_performance;
    }
    if (document.getElementById('statGoals')) {
        document.getElementById('statGoals').textContent = data.total_goals;
    }
    if (document.getElementById('statAssists')) {
        document.getElementById('statAssists').textContent = data.total_assists;
    }
}

// Update detailed statistics
function updateDetailedStats(data) {
    // Attacking
    document.getElementById('detailGoals').textContent = data.total_goals;
    document.getElementById('detailAssists').textContent = data.total_assists;
    document.getElementById('detailShots').textContent = data.avg_shots;
    document.getElementById('detailShotAccuracy').textContent = data.shot_accuracy + '%';
    
    // Passing
    document.getElementById('detailPasses').textContent = data.total_passes;
    document.getElementById('detailPassAcc').textContent = data.avg_pass_accuracy + '%';
    document.getElementById('detailAvgPasses').textContent = data.avg_passes_per_match;
    
    // Defensive
    document.getElementById('detailTackles').textContent = data.total_tackles;
    document.getElementById('detailInterceptions').textContent = data.total_interceptions;
    document.getElementById('detailDribbles').textContent = data.avg_dribbles;
}

// Update radar chart
function updateRadarChart(stats) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    // Normalize stats for radar chart
    const normalizedStats = [
        (stats.goals / 2) * 100,
        (stats.assists / 2) * 100,
        (stats.shots_on_target / 5) * 100,
        stats.pass_accuracy,
        (stats.tackles / 8) * 100,
        (stats.interceptions / 8) * 100,
        (stats.dribbles_completed / 5) * 100
    ];
    
    if (radarChart) {
        radarChart.destroy();
    }
    
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Goals', 'Assists', 'Shots on Target', 'Pass Accuracy', 'Tackles', 'Interceptions', 'Dribbles'],
            datasets: [{
                label: 'Player Stats',
                data: normalizedStats,
                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(37, 99, 235, 1)'
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Update trend chart
function updateTrendChart(trend) {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    if (trendChart) {
        trendChart.destroy();
    }
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: trend.matches,
            datasets: [{
                label: 'Performance Rating',
                data: trend.ratings,
                borderColor: 'rgba(37, 99, 235, 1)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Performance Rating'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Match Number'
                    }
                }
            }
        }
    });
}

// Load heatmap
async function loadHeatmap(playerName) {
    try {
        const response = await fetch(`/api/heatmap/${encodeURIComponent(playerName)}`);
        const data = await response.json();
        
        // Create football field with heatmap
        const trace = {
            x: data.x,
            y: data.y,
            type: 'histogram2d',
            colorscale: 'Hot',
            showscale: true,
            nbinsx: 30,
            nbinsy: 20,
            opacity: 0.7
        };
        
        // Field markings
        const shapes = [
            // Field outline
            {type: 'rect', x0: 0, y0: 0, x1: 105, y1: 68, line: {color: 'white', width: 2}},
            // Center line
            {type: 'line', x0: 52.5, y0: 0, x1: 52.5, y1: 68, line: {color: 'white', width: 2}},
            // Penalty areas
            {type: 'rect', x0: 0, y0: 13.84, x1: 16.5, y1: 54.16, line: {color: 'white', width: 2}},
            {type: 'rect', x0: 88.5, y0: 13.84, x1: 105, y1: 54.16, line: {color: 'white', width: 2}},
            // Goal areas
            {type: 'rect', x0: 0, y0: 24.84, x1: 5.5, y1: 43.16, line: {color: 'white', width: 2}},
            {type: 'rect', x0: 99.5, y0: 24.84, x1: 105, y1: 43.16, line: {color: 'white', width: 2}}
        ];
        
        const layout = {
            title: '',
            xaxis: {range: [0, 105], showgrid: false, zeroline: false, visible: false},
            yaxis: {range: [0, 68], showgrid: false, zeroline: false, visible: false},
            plot_bgcolor: 'green',
            paper_bgcolor: 'white',
            shapes: shapes,
            height: 400,
            margin: {l: 20, r: 20, t: 20, b: 20}
        };
        
        Plotly.newPlot('heatmapContainer', [trace], layout, {responsive: true});
        
    } catch (error) {
        console.error('Error loading heatmap:', error);
    }
}

// Update recent matches table
function updateRecentMatches(matches) {
    const tbody = document.getElementById('matchesTableBody');
    tbody.innerHTML = '';
    
    matches.forEach(match => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>Match ${match.match_id}</td>
            <td>${match.goals}</td>
            <td>${match.assists}</td>
            <td>${match.passes_completed}</td>
            <td>${match.pass_accuracy}%</td>
            <td>${match.tackles}</td>
            <td>${match.interceptions}</td>
            <td><strong>${match.performance_rating}</strong></td>
        `;
        tbody.appendChild(row);
    });
}

// Load feature importance
async function loadFeatureImportance() {
    try {
        const response = await fetch('/api/feature_importance');
        const data = await response.json();
        
        const ctx = document.getElementById('importanceChart').getContext('2d');
        
        if (importanceChart) {
            importanceChart.destroy();
        }
        
        importanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.features,
                datasets: [{
                    label: 'Importance',
                    data: data.importance,
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Importance Score'
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading feature importance:', error);
    }
}

// Prediction functionality
function setupPredictionInputs() {
    const inputs = [
        'predMinutes', 'predGoals', 'predAssists', 'predShots', 'predShotsTarget',
        'predPasses', 'predPassAcc', 'predTackles', 'predInterceptions', 'predDribbles'
    ];
    
    inputs.forEach(id => {
        const input = document.getElementById(id);
        const valueSpan = document.getElementById(id + 'Value');
        
        if (input && valueSpan) {
            input.addEventListener('input', function() {
                valueSpan.textContent = this.value;
            });
        }
    });
    
    // Predict button
    const predictBtn = document.getElementById('predictBtn');
    if (predictBtn) {
        predictBtn.addEventListener('click', makePrediction);
    }
}

async function makePrediction() {
    const predictionData = {
        minutes_played: parseInt(document.getElementById('predMinutes').value),
        goals: parseInt(document.getElementById('predGoals').value),
        assists: parseInt(document.getElementById('predAssists').value),
        shots: parseInt(document.getElementById('predShots').value),
        shots_on_target: parseInt(document.getElementById('predShotsTarget').value),
        passes_completed: parseInt(document.getElementById('predPasses').value),
        pass_accuracy: parseFloat(document.getElementById('predPassAcc').value),
        tackles: parseInt(document.getElementById('predTackles').value),
        interceptions: parseInt(document.getElementById('predInterceptions').value),
        dribbles_completed: parseInt(document.getElementById('predDribbles').value)
    };
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(predictionData)
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const predictionValue = document.getElementById('predictionValue');
            predictionValue.textContent = data.prediction;
            
            // Add animation
            predictionValue.style.transform = 'scale(1.2)';
            setTimeout(() => {
                predictionValue.style.transform = 'scale(1)';
            }, 300);
        }
        
    } catch (error) {
        console.error('Error making prediction:', error);
        alert('Failed to make prediction. Please try again.');
    }
}

// Show/hide loading spinner
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'block' : 'none';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupPredictionInputs();
});

