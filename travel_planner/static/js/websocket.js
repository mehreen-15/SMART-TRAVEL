/**
 * WebSocket Communication Module
 * 
 * This module handles WebSocket connections for real-time updates
 * in the travel planner application.
 */

// Create a class for handling WebSocket connections
class WebSocketManager {
    constructor(url, onMessageCallback, debug = false) {
        this.url = url;
        this.socket = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 2000; // Starting with 2 seconds
        this.onMessageCallback = onMessageCallback;
        this.debug = debug;
        
        // Bind methods to this instance
        this.connect = this.connect.bind(this);
        this.disconnect = this.disconnect.bind(this);
        this.reconnect = this.reconnect.bind(this);
        this.sendMessage = this.sendMessage.bind(this);
        this.onOpen = this.onOpen.bind(this);
        this.onClose = this.onClose.bind(this);
        this.onMessage = this.onMessage.bind(this);
        this.onError = this.onError.bind(this);
    }
    
    // Connect to the WebSocket server
    connect() {
        if (this.socket && this.socket.readyState !== WebSocket.CLOSED) {
            this.log('WebSocket is already open or connecting');
            return;
        }
        
        try {
            this.log(`Connecting to ${this.url}`);
            this.socket = new WebSocket(this.url);
            
            // Set up event handlers
            this.socket.onopen = this.onOpen;
            this.socket.onclose = this.onClose;
            this.socket.onmessage = this.onMessage;
            this.socket.onerror = this.onError;
        } catch (error) {
            this.log('WebSocket connection error:', error);
            this.reconnect();
        }
    }
    
    // Disconnect from the WebSocket server
    disconnect() {
        if (this.socket) {
            this.log('Disconnecting WebSocket');
            this.socket.close();
            this.socket = null;
            this.connected = false;
        }
    }
    
    // Reconnect to the WebSocket server with exponential backoff
    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.log('Maximum reconnect attempts reached. Giving up.');
            return;
        }
        
        // Exponential backoff: 2s, 4s, 8s, 16s, 32s
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
        this.reconnectAttempts++;
        
        this.log(`Reconnecting in ${delay / 1000} seconds... (Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        
        setTimeout(() => {
            this.log('Attempting to reconnect...');
            this.connect();
        }, delay);
    }
    
    // Send a message to the WebSocket server
    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.log('Sending message:', message);
            this.socket.send(JSON.stringify(message));
            return true;
        } else {
            this.log('Cannot send message, socket is not open');
            return false;
        }
    }
    
    // Handle WebSocket open event
    onOpen(event) {
        this.connected = true;
        this.reconnectAttempts = 0;
        this.log('WebSocket connection established');
        
        // Dispatch a custom event
        document.dispatchEvent(new CustomEvent('websocket-connected', {
            detail: { url: this.url }
        }));
    }
    
    // Handle WebSocket close event
    onClose(event) {
        this.connected = false;
        this.log(`WebSocket connection closed: ${event.code} ${event.reason}`);
        
        // Attempt to reconnect if the close was unexpected
        if (event.code !== 1000) { // 1000 is normal closure
            this.reconnect();
        }
        
        // Dispatch a custom event
        document.dispatchEvent(new CustomEvent('websocket-disconnected', {
            detail: { code: event.code, reason: event.reason }
        }));
    }
    
    // Handle WebSocket message event
    onMessage(event) {
        try {
            const data = JSON.parse(event.data);
            this.log('Received message:', data);
            
            // Call the provided callback with the parsed data
            if (this.onMessageCallback && typeof this.onMessageCallback === 'function') {
                this.onMessageCallback(data);
            }
            
            // Dispatch a custom event with the data
            document.dispatchEvent(new CustomEvent('websocket-message', {
                detail: { data }
            }));
        } catch (error) {
            this.log('Error parsing message:', error);
        }
    }
    
    // Handle WebSocket error event
    onError(event) {
        this.log('WebSocket error:', event);
        
        // Dispatch a custom event
        document.dispatchEvent(new CustomEvent('websocket-error', {
            detail: { error: event }
        }));
    }
    
    // Logging utility, only logs if debug is true
    log(...args) {
        if (this.debug) {
            console.log('[WebSocketManager]', ...args);
        }
    }
}

// Create specific managers for different WebSocket connections

// 1. User Activity WebSocket
function createUserActivitySocket(callback) {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const host = window.location.host;
    const url = `${protocol}${host}/ws/user_activity/`;
    
    return new WebSocketManager(url, callback, true);
}

// 2. Booking Updates WebSocket
function createBookingUpdatesSocket(callback) {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const host = window.location.host;
    const url = `${protocol}${host}/ws/booking_updates/`;
    
    return new WebSocketManager(url, callback, true);
}

// Example usage:
/*
document.addEventListener('DOMContentLoaded', function() {
    // For user activity (in admin dashboard)
    if (document.getElementById('user-activity-feed')) {
        const userActivitySocket = createUserActivitySocket(function(data) {
            // Handle incoming user activity data
            console.log('User activity update:', data);
            // Update UI with the new data
        });
        userActivitySocket.connect();
    }
    
    // For booking updates (in admin dashboard or user booking page)
    if (document.getElementById('booking-updates-feed')) {
        const bookingUpdatesSocket = createBookingUpdatesSocket(function(data) {
            // Handle incoming booking update data
            console.log('Booking update:', data);
            // Update UI with the new data
        });
        bookingUpdatesSocket.connect();
    }
});
*/ 