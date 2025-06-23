function updateClock() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    
    // Calculate angles for hands
    const secondAngle = (seconds * 6) - 90; // 6 degrees per second
    const minuteAngle = (minutes * 6) + (seconds * 0.1) - 90; // 6 degrees per minute + smooth seconds
    const hourAngle = ((hours % 12) * 30) + (minutes * 0.5) - 90; // 30 degrees per hour + smooth minutes
    
    // Apply rotations
    document.getElementById('secondHand').style.transform = `rotate(${secondAngle}deg)`;
    document.getElementById('minuteHand').style.transform = `rotate(${minuteAngle}deg)`;
    document.getElementById('hourHand').style.transform = `rotate(${hourAngle}deg)`;
    
    // Update digital display
    const timeString = String(hours).padStart(2, '0') + ':' + 
                      String(minutes).padStart(2, '0') + ':' + 
                      String(seconds).padStart(2, '0');
    document.getElementById('digitalTime').textContent = timeString;
    
    // Update date
    const options = { 
        weekday: 'long',
        year: 'numeric', 
        month: 'long', 
        day: 'numeric'
    };
    const dateString = now.toLocaleDateString('he-IL', options);
    document.getElementById('dateInfo').textContent = dateString;
}

// Initialize clock when page loads
document.addEventListener('DOMContentLoaded', function() {
    updateClock();
    setInterval(updateClock, 1000);
});