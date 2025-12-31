/**
 * Vibella Frontend JavaScript
 * Handles user interactions, image upload, and API communication
 * FIXED: Properly converts image to base64 for backend
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const loading = document.getElementById('loading');
const imageInput = document.getElementById('imageInput');

// Global variable to store selected image as base64
let selectedImageBase64 = null;

/**
 * Handle image file selection and convert to base64
 */
imageInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    
    if (!file) {
        selectedImageBase64 = null;
        return;
    }
    
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        alert('Please select a valid image file (JPEG, PNG, or WebP)');
        imageInput.value = '';
        return;
    }
    
    // Validate file size (max 5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('Image size should be less than 5MB');
        imageInput.value = '';
        return;
    }
    
    // Convert image to base64
    console.log('📸 Converting image to base64...');
    try {
        selectedImageBase64 = await fileToBase64(file);
        console.log(`✅ Image converted: ${selectedImageBase64.substring(0, 50)}...`);
        
        // Show visual feedback that image is selected
        userInput.placeholder = '📸 Image selected! Add a message or just send...';
    } catch (error) {
        console.error('❌ Error converting image:', error);
        alert('Failed to process image. Please try again.');
        imageInput.value = '';
        selectedImageBase64 = null;
    }
});

/**
 * Convert File to base64 data URI
 */
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result); // Returns "data:image/jpeg;base64,..."
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

/**
 * Send message with optional image to backend
 */
async function sendMessage() {
    const message = userInput.value.trim();
    const hasImage = selectedImageBase64 !== null;

    // Need either message or image
    if (!message && !hasImage) {
        return;
    }

    // Default message if only image provided
    const finalMessage = message || 'Generate caption, hashtags, and song suggestions for this image';

    // Visual feedback
    sendBtn.classList.add('sending');
    
    // Display user message
    if (message) {
        addMessage(message, 'user');
    }
    if (hasImage) {
        addMessage('🖼️ Image attached', 'user');
    }

    // Clear inputs
    userInput.value = '';
    userInput.style.height = 'auto';
    userInput.placeholder = 'Type your vision here...';
    
    // Store image data before clearing
    const imageToSend = selectedImageBase64;
    
    // Clear image selection
    imageInput.value = '';
    selectedImageBase64 = null;

    // Disable send button and show loading
    sendBtn.disabled = true;
    loading.style.display = 'block';

    try {
        // Prepare request body with base64 image
        const requestBody = {
            message: finalMessage
        };
        
        // Add image if present (as base64 string)
        if (imageToSend) {
            requestBody.image = imageToSend; // This is already "data:image/jpeg;base64,..."
            console.log('📤 Sending request with image...');
        }

        console.log('📤 Sending to backend:', {
            message: finalMessage.substring(0, 50) + '...',
            hasImage: !!imageToSend
        });

        // Send POST request to backend (JSON format, not FormData!)
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        console.log('📥 Response status:', response.status);

        // Check if request was successful
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        // Parse JSON response
        const data = await response.json();
        console.log('✅ Got response from AI');

        // Display AI response
        addMessage(data.response, 'bot');

    } catch (error) {
        // Handle errors gracefully
        console.error('❌ Error:', error);
        addMessage(
            "⚠️ Surge detected! Connection issue. Make sure the backend is running and try again.",
            'bot'
        );
    } finally {
        // Re-enable send button and hide loading
        sendBtn.disabled = false;
        sendBtn.classList.remove('sending');
        loading.style.display = 'none';
    }
}

/**
 * Add message to chat interface
 * @param {string} text - Message text
 * @param {string} sender - 'user' or 'bot'
 */
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    messageDiv.innerHTML = `
        <div class="message-content">
            ${formatMessage(text)}
        </div>
    `;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Format message text (preserve line breaks, highlight keywords)
 * @param {string} text - Raw message text
 * @returns {string} - Formatted HTML
 */
function formatMessage(text) {
    let formatted = text.replace(/\n/g, '<br>');
    formatted = formatted.replace(
        /\b(Caption|Hashtags|Song Suggestions|Mood):/g,
        '<strong style="color:var(--neon-cyan)">$1:</strong>'
    );
    return formatted;
}

/**
 * Auto-resize textarea as user types
 */
userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
});

/**
 * Handle Enter key press in textarea
 */
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

/**
 * Check backend connection on page load
 */
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (!response.ok) {
            throw new Error('Backend not responding');
        }
        console.log('✅ Connected to Vibella backend');
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        addMessage(
            "⚠️ Could not connect to backend. Please make sure it's running on http://localhost:8000",
            'bot'
        );
    }
});