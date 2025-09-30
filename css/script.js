function lastedit() {
    document.getElementById("last-updated-date").innerHTML = "September 29th, 2025 10:35pm";
}

// Function to initialize the view (only goalie or skater at a time)
function initializeView() {
    document.getElementById('career-tile').style.display = 'block';
    document.getElementById('season-tile').style.display = 'block';
    document.getElementById('goalie-tile').style.display = 'none';
    document.getElementById('training-tile').style.display = 'none';
    document.getElementById('skater-stats').style.display = 'block';
    document.getElementById('goalie-stats').style.display = 'none';
}

// Function to toggle between Skater and Goalie modes
function toggleTiles() {
    const career = document.getElementById('career-tile');
    const season = document.getElementById('season-tile');
    const goalie = document.getElementById('goalie-tile');
    const training = document.getElementById('training-tile');
    const skaterStats = document.getElementById('skater-stats');
    const goalieStats = document.getElementById('goalie-stats');
    const toggleBtn = document.getElementById('toggle-btn');

    const isSkaterMode = career.style.display !== 'none';

    career.style.display = isSkaterMode ? 'none' : 'block';
    season.style.display = isSkaterMode ? 'none' : 'block';
    goalie.style.display = isSkaterMode ? 'block' : 'none';
    training.style.display = isSkaterMode ? 'block' : 'none';

    skaterStats.style.display = isSkaterMode ? 'none' : 'block';
    goalieStats.style.display = isSkaterMode ? 'block' : 'none';

    toggleBtn.textContent = isSkaterMode ? 'Skater Mode' : 'Goalie Mode';
}