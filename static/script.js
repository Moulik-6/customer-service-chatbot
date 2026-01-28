// Get DOM elements
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');
const sendButton = document.getElementById('sendButton');

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Disable send button while processing
    sendButton.disabled = true;
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    try {
        // Send message to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        typingIndicator.remove();
        
        // Add bot response to chat
        addMessage(data.response, 'bot');
        
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        
        // Provide more specific error messages
        let errorMessage = 'Sorry, I encountered an error. Please try again.';
        if (!navigator.onLine) {
            errorMessage = 'No internet connection. Please check your network and try again.';
        } else if (error.message.includes('Network')) {
            errorMessage = 'Unable to reach the server. Please try again later.';
        }
        
        addMessage(errorMessage, 'bot');
    } finally {
        // Re-enable send button
        sendButton.disabled = false;
        userInput.focus();
    }
});

// Function to add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${escapeHtml(text)}`;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to add typing indicator
function addTypingIndicator() {
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'message bot-message';
    indicatorDiv.id = 'typingIndicator';
    
    const indicatorContent = document.createElement('div');
    indicatorContent.className = 'typing-indicator';
    indicatorContent.innerHTML = '<span></span><span></span><span></span>';
    
    indicatorDiv.appendChild(indicatorContent);
    chatMessages.appendChild(indicatorDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return indicatorDiv;
}

// Helper function to get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});
