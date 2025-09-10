
/**
 * Updates the current timestamp and date display elements with real-time values.
 * This function is called repeatedly by the timer to create a live clock.
 */
function task() {
    var timestamp = new Date();
    document.getElementById('cur_timestamp').innerHTML = Math.round(timestamp / 1000);
    document.getElementById('cur_date').innerHTML = timestamp2date(timestamp);
}

/**
 * Starts a timer that updates the display every second to show real-time values.
 * Creates a live clock by calling task() function at 1-second intervals.
 */
function showTime() {
    setInterval("task();", 1000)
}

/**
 * Converts a timestamp to a formatted date string.
 * @param {number|Date} timestamp - The timestamp to convert (milliseconds since epoch or Date object)
 * @returns {string} Formatted date string in YYYY-MM-DD HH:MM:SS format
 */
function timestamp2date(timestamp) {
    // Padding array for zero-padding single digit numbers (0-9)
    var paddin = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'];
    var date = new Date(timestamp);
    
    // Extract and format year
    Y = date.getFullYear() + '-';
    
    // Extract and format month (getMonth() returns 0-11, so add 1)
    M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
    
    // Extract and format day with zero-padding if needed
    D = date.getDate();
    if (D < 10) D = paddin[parseInt(D)];
    D = D + ' ';
    
    // Extract hours, minutes, and seconds
    h = date.getHours() + ':';
    m = date.getMinutes() + ':';
    s = date.getSeconds();
    
    // Zero-pad seconds if single digit
    if (s < 10) s = paddin[parseInt(s)];
    
    return Y + M + D + h + m + s;
}

/**
 * Handles bidirectional conversion between timestamps and date strings.
 * Provides conversion functionality for the user interface form elements.
 * @param {number} t - Conversion direction flag (1 = timestamp to date, other = date to timestamp)
 */
function gen(t) {
    try {
        if (t == 1) {
            // Convert timestamp to date string
            document.getElementById('beijing_time_1').value = timestamp2date(parseInt(document.getElementById('timestamp_1').value) * 1000);
        }
        else {
            // Convert date string to timestamp
            document.getElementById('timestamp_2').value = Math.round(Date.parse(document.getElementById('beijing_time_2').value) / 1000);
        }
    }
    catch (err) {
        // Handle invalid input with user-friendly error message
        alert('Invalid Input!');
    }
}

// Initialize the application
task(); // Set initial timestamp and date values
document.getElementById('change').innerHTML = ' = <B>Date String</B>:  '; // Update UI label
showTime(); // Start the real-time clock

// Set up initial form values with current timestamp
var timestamp = new Date();

// Pre-fill timestamp input field with current Unix timestamp
document.getElementById('timestamp_1').value = Math.round(timestamp / 1000);

// Pre-fill date input field with current formatted date
document.getElementById('beijing_time_2').value = timestamp2date(timestamp);
