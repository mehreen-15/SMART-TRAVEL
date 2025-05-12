/**
 * Analytics Dashboard JavaScript
 * 
 * This script handles the real-time updates and visualizations
 * for the analytics dashboard in the Smart Travel admin interface.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts and data tables
    initializeCharts();
    initializeDataTables();
    
    // Initialize WebSocket connections
    initializeWebSockets();
    
    // Set up refresh buttons
    document.querySelectorAll('.refresh-panel').forEach(button => {
        button.addEventListener('click', function() {
            const panelId = this.getAttribute('data-panel');
            refreshPanel(panelId);
        });
    });
    
    // Set up auto-refresh
    setAutoRefresh();
});

/**
 * Initialize Chart.js charts for the dashboard
 */
function initializeCharts() {
    // User Activity Chart
    if (document.getElementById('userActivityChart')) {
        const ctx = document.getElementById('userActivityChart').getContext('2d');
        
        window.userActivityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: getLast24Hours(),
                datasets: [{
                    label: 'User Activity',
                    data: getRandomData(24), // This will be replaced with real data
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Activity Count'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                }
            }
        });
    }
    
    // Booking Chart
    if (document.getElementById('bookingChart')) {
        const ctx = document.getElementById('bookingChart').getContext('2d');
        
        window.bookingChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: getLast7Days(),
                datasets: [{
                    label: 'Hotel Bookings',
                    data: getRandomData(7), // This will be replaced with real data
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }, {
                    label: 'Transportation Bookings',
                    data: getRandomData(7), // This will be replaced with real data
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Booking Count'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Day'
                        }
                    }
                }
            }
        });
    }
    
    // Popular Destinations Chart
    if (document.getElementById('popularDestinationsChart')) {
        const ctx = document.getElementById('popularDestinationsChart').getContext('2d');
        
        // This will be replaced with real data
        const destinations = ['Paris', 'Tokyo', 'New York', 'London', 'Rome'];
        
        window.popularDestinationsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: destinations,
                datasets: [{
                    data: getRandomData(destinations.length),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
    
    // Revenue Chart
    if (document.getElementById('revenueChart')) {
        const ctx = document.getElementById('revenueChart').getContext('2d');
        
        window.revenueChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: getLast12Months(),
                datasets: [{
                    label: 'Monthly Revenue',
                    data: getRandomRevenue(12), // This will be replaced with real data
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.raw.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        },
                        title: {
                            display: true,
                            text: 'Revenue (USD)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    }
                }
            }
        });
    }
}

/**
 * Initialize DataTables for tabular data
 */
function initializeDataTables() {
    const tables = ['#userActivityTable', '#recentBookingsTable', '#recentPaymentsTable'];
    
    tables.forEach(tableId => {
        if (document.querySelector(tableId)) {
            $(tableId).DataTable({
                pageLength: 5,
                lengthMenu: [5, 10, 25, 50],
                dom: 'Bfrtip',
                buttons: ['copy', 'csv', 'excel', 'pdf'],
                responsive: true
            });
        }
    });
}

/**
 * Initialize WebSocket connections for real-time updates
 */
function initializeWebSockets() {
    if (document.getElementById('user-activity-feed')) {
        const userActivitySocket = createUserActivitySocket(function(data) {
            updateUserActivityFeed(data.message);
            updateUserActivityChart(data.message);
        });
        userActivitySocket.connect();
    }
    
    if (document.getElementById('booking-updates-feed')) {
        const bookingUpdatesSocket = createBookingUpdatesSocket(function(data) {
            updateBookingFeed(data);
            updateBookingChart(data);
        });
        bookingUpdatesSocket.connect();
    }
}

/**
 * Update user activity feed with new data
 */
function updateUserActivityFeed(activityData) {
    const feed = document.getElementById('user-activity-feed');
    if (!feed) return;
    
    const timestamp = new Date(activityData.timestamp).toLocaleTimeString();
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';
    activityItem.innerHTML = `
        <span class="time">${timestamp}</span>
        <span class="user">${activityData.username}</span>
        <span class="action">${activityData.action}</span>
        <span class="page">${activityData.page}</span>
    `;
    
    // Add to the top of the feed
    feed.insertBefore(activityItem, feed.firstChild);
    
    // Limit the number of items
    if (feed.children.length > 50) {
        feed.removeChild(feed.lastChild);
    }
    
    // Flash the new item
    activityItem.classList.add('highlight');
    setTimeout(() => {
        activityItem.classList.remove('highlight');
    }, 2000);
}

/**
 * Update user activity chart with new data
 */
function updateUserActivityChart(activityData) {
    if (!window.userActivityChart) return;
    
    const hour = new Date(activityData.timestamp).getHours();
    
    // Find the index for the current hour
    const hourIndex = window.userActivityChart.data.labels.indexOf(`${hour}:00`);
    
    if (hourIndex !== -1) {
        // Increment the count for this hour
        window.userActivityChart.data.datasets[0].data[hourIndex]++;
        window.userActivityChart.update();
    }
}

/**
 * Update booking feed with new data
 */
function updateBookingFeed(bookingData) {
    const feed = document.getElementById('booking-updates-feed');
    if (!feed) return;
    
    const timestamp = new Date(bookingData.timestamp).toLocaleTimeString();
    const bookingItem = document.createElement('div');
    bookingItem.className = 'booking-item';
    
    let statusClass = 'status-pending';
    if (bookingData.status === 'confirmed') statusClass = 'status-confirmed';
    if (bookingData.status === 'cancelled') statusClass = 'status-cancelled';
    
    bookingItem.innerHTML = `
        <span class="time">${timestamp}</span>
        <span class="booking-id">Booking #${bookingData.booking_id}</span>
        <span class="status ${statusClass}">${bookingData.status}</span>
        <span class="message">${bookingData.message}</span>
    `;
    
    // Add to the top of the feed
    feed.insertBefore(bookingItem, feed.firstChild);
    
    // Limit the number of items
    if (feed.children.length > 50) {
        feed.removeChild(feed.lastChild);
    }
    
    // Flash the new item
    bookingItem.classList.add('highlight');
    setTimeout(() => {
        bookingItem.classList.remove('highlight');
    }, 2000);
}

/**
 * Update booking chart with new data
 */
function updateBookingChart(bookingData) {
    if (!window.bookingChart) return;
    
    // Logic to update the booking chart based on new data
    // This is a simplified example - in a real app, you'd have more complex logic
    const today = new Date().toLocaleDateString('en-US', { weekday: 'short' });
    
    // Find the index for today
    const todayIndex = window.bookingChart.data.labels.indexOf(today);
    
    if (todayIndex !== -1) {
        // Increment the appropriate dataset based on booking type
        if (bookingData.message.includes('hotel')) {
            window.bookingChart.data.datasets[0].data[todayIndex]++;
        } else if (bookingData.message.includes('transportation')) {
            window.bookingChart.data.datasets[1].data[todayIndex]++;
        }
        window.bookingChart.update();
    }
}

/**
 * Helper function to get labels for the last 24 hours
 */
function getLast24Hours() {
    const hours = [];
    for (let i = 0; i < 24; i++) {
        hours.push(`${i}:00`);
    }
    return hours;
}

/**
 * Helper function to get labels for the last 7 days
 */
function getLast7Days() {
    const days = [];
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    
    const date = new Date();
    for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(date.getDate() - i);
        days.push(dayNames[d.getDay()]);
    }
    
    return days;
}

/**
 * Helper function to get labels for the last 12 months
 */
function getLast12Months() {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const months = [];
    
    const date = new Date();
    const currentMonth = date.getMonth();
    
    for (let i = 11; i >= 0; i--) {
        const monthIndex = (currentMonth - i + 12) % 12;
        months.push(monthNames[monthIndex]);
    }
    
    return months;
}

/**
 * Helper function to generate random data for testing
 */
function getRandomData(count) {
    const data = [];
    for (let i = 0; i < count; i++) {
        data.push(Math.floor(Math.random() * 50) + 10);
    }
    return data;
}

/**
 * Helper function to generate random revenue data for testing
 */
function getRandomRevenue(count) {
    const data = [];
    for (let i = 0; i < count; i++) {
        data.push(Math.floor(Math.random() * 50000) + 10000);
    }
    return data;
}

/**
 * Refresh a specific panel by fetching updated data
 */
function refreshPanel(panelId) {
    // Show loading indicator
    const panel = document.getElementById(panelId);
    if (!panel) return;
    
    panel.classList.add('loading');
    
    // Fetch updated data
    fetch(`/api/analytics/${panelId}`)
        .then(response => response.json())
        .then(data => {
            updatePanelData(panelId, data);
            panel.classList.remove('loading');
        })
        .catch(error => {
            console.error('Error refreshing panel:', error);
            panel.classList.remove('loading');
        });
}

/**
 * Update panel data based on API response
 */
function updatePanelData(panelId, data) {
    switch (panelId) {
        case 'user-activity':
            // Update user activity chart and table
            if (window.userActivityChart && data.chartData) {
                window.userActivityChart.data = data.chartData;
                window.userActivityChart.update();
            }
            
            if (data.tableData) {
                updateTable('#userActivityTable', data.tableData);
            }
            break;
            
        case 'bookings':
            // Update bookings chart and table
            if (window.bookingChart && data.chartData) {
                window.bookingChart.data = data.chartData;
                window.bookingChart.update();
            }
            
            if (data.tableData) {
                updateTable('#recentBookingsTable', data.tableData);
            }
            break;
            
        case 'destinations':
            // Update destinations chart
            if (window.popularDestinationsChart && data.chartData) {
                window.popularDestinationsChart.data = data.chartData;
                window.popularDestinationsChart.update();
            }
            break;
            
        case 'revenue':
            // Update revenue chart
            if (window.revenueChart && data.chartData) {
                window.revenueChart.data = data.chartData;
                window.revenueChart.update();
            }
            
            if (data.tableData) {
                updateTable('#recentPaymentsTable', data.tableData);
            }
            break;
    }
}

/**
 * Update a DataTable with new data
 */
function updateTable(tableSelector, data) {
    const table = $(tableSelector).DataTable();
    table.clear();
    table.rows.add(data);
    table.draw();
}

/**
 * Set up auto-refresh for panels
 */
function setAutoRefresh() {
    const panels = [
        { id: 'user-activity', interval: 60000 }, // 1 minute
        { id: 'bookings', interval: 120000 },     // 2 minutes
        { id: 'destinations', interval: 300000 }, // 5 minutes
        { id: 'revenue', interval: 300000 }       // 5 minutes
    ];
    
    panels.forEach(panel => {
        setInterval(() => {
            refreshPanel(panel.id);
        }, panel.interval);
    });
} 