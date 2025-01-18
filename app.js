// Connect to the WebSocket server on localhost:5000
let ws = io.connect('http://localhost:5000');  // Ensure this points to the correct port

let currentMatch = null;

// Function to update the score (runs, isOut flag)
function updateScore(runs, isOut = false) {
    if (!currentMatch) {
        console.error('Current match data is not available');
        return;  // Exit if currentMatch is null or not initialized yet
    }

    // Sending score update to the server
    fetch('http://localhost:5000/update_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            runs,
            isOut,
            overNumber: currentMatch.current_over,
            ballNumber: currentMatch.current_ball
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            fetchMatchData();  // Refresh the match data after updating the score
        }
    })
    .catch(error => {
        console.error('Error updating score:', error);
    });
}

// Function to reset the score
function resetScore() {
    fetch('http://localhost:5000/reset_score', {  // Add this endpoint to your Flask backend
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            fetchMatchData();  // Refresh the match data after resetting the score
        }
    })
    .catch(error => {
        console.error('Error resetting score:', error);
    });
}

// Function to fetch the match data
function fetchMatchData() {
    fetch('http://localhost:5000/get_match')
        .then(response => response.json())
        .then(data => {
            currentMatch = data;  // Set the current match data
            updateUI(data);        // Update the UI with new match data
        })
        .catch(error => {
            console.error('Error fetching match data:', error);
        });
}

// Function to calculate over statistics (runs and wickets)
function calculateOverStats(balls) {
    const runs = balls.reduce((sum, ball) => sum + ball.runs, 0);
    const wickets = balls.filter(ball => ball.is_out).length;
    return { runs, wickets };
}

// Function to update the UI with match data
function updateUI(match) {
    // Update score and over display
    document.getElementById('score').textContent = `${match.current_score}/${match.wickets}`;
    document.getElementById('over').textContent = `Over: ${match.current_over}.${match.current_ball}`;
    
    // Generate HTML for ball display
    const ballsHtml = Array(6).fill(0).map((_, i) => {
        const ball = match.balls.find(b => b.over_number === match.current_over && b.ball_number === i);
        const value = ball ? (ball.is_out ? 'W' : ball.runs) : '';
        const current = i === match.current_ball ? 'current' : '';
        return `<div class="ball ${current}" data-runs="${value}">${value}</div>`;
    }).join('');
    document.getElementById('balls').innerHTML = ballsHtml;

    // Update over statistics
    const oversMap = match.balls.reduce((acc, ball) => {
        if (!acc[ball.over_number]) acc[ball.over_number] = [];
        acc[ball.over_number].push(ball);
        return acc;
    }, {});

    const oversHtml = Object.entries(oversMap)
        .sort((a, b) => b[0] - a[0]) // Sort in descending order
        .map(([overNum, balls]) => {
            const stats = calculateOverStats(balls);
            return ` 
                <div class="over">
                    <h3>Over ${overNum }</h3>
                    <div class="balls-container">
                        ${balls
                            .sort((a, b) => a.ball_number - b.ball_number)
                            .map(ball => `
                                <div class="ball" data-runs="${ball.is_out ? 'W' : ball.runs}">
                                    ${ball.is_out ? 'W' : ball.runs}
                                </div>
                            `).join('')}
                    </div>
                    <div class="over-summary">
                        <span>Runs: ${stats.runs}</span>
                        <span>Wickets: ${stats.wickets}</span>
                    </div>
                </div>
            `;
        }).join('');
    document.getElementById('overs').innerHTML = `
        <h2>Previous Overs</h2>
        ${oversHtml}
    `;
}


fetchMatchData(); // Initial data fetch 

// WebSocket event for receiving match updates
ws.on('match_update', function (data) {
    updateUI(data);  // Update the UI when WebSocket message is received
});

// WebSocket event handler for messages
ws.onmessage = function(event) {
    const match = JSON.parse(event.data);
    updateUI(match);  // Update UI when WebSocket message is received
};
