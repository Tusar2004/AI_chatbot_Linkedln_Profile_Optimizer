document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const quickButtons = document.querySelectorAll('.quick-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const soundBtn = document.getElementById('sound-btn');
    const emojiBtn = document.getElementById('emoji-btn');
    const instructionsToggle = document.getElementById('instructions-toggle');
    const instructionsContent = document.getElementById('instructions-content');
    const instructionsIcon = document.getElementById('instructions-icon');
    
    let soundEnabled = true;
    let speechRecognition;
    let botVoice = null;
    
    // Initialize speech synthesis
    function initVoice() {
        if ('speechSynthesis' in window) {
            botVoice = new SpeechSynthesisUtterance();
            botVoice.rate = 1;
            botVoice.pitch = 0.9;
            botVoice.volume = 1;
            
            // Set a pleasant voice if available
            const voices = window.speechSynthesis.getVoices();
            const preferredVoices = voices.filter(v => v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Zira'));
            if (preferredVoices.length > 0) {
                botVoice.voice = preferredVoices[0];
            }
        }
    }
    
    // Initialize speech recognition
    function initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            speechRecognition = new webkitSpeechRecognition();
            speechRecognition.continuous = false;
            speechRecognition.interimResults = false;
            speechRecognition.lang = 'en-US';
            
            speechRecognition.onstart = function() {
                voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
                addSystemMessage("Listening... Speak now");
            };
            
            speechRecognition.onerror = function(event) {
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
                addSystemMessage("Voice input failed. Please try again.");
            };
            
            speechRecognition.onend = function() {
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            };
            
            speechRecognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                userInput.value = transcript;
                chatForm.dispatchEvent(new Event('submit'));
            };
        } else {
            voiceBtn.style.display = 'none';
        }
    }
    
    // Toggle instructions panel
    instructionsToggle.addEventListener('click', function() {
        instructionsContent.classList.toggle('hidden');
        instructionsIcon.classList.toggle('rotate-180');
    });
    
    // Add system message to chat
    function addSystemMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex justify-center';
        messageDiv.innerHTML = `
            <div class="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">
                ${message}
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Add user message to chat
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start justify-end';
        messageDiv.innerHTML = `
            <div class="bg-gradient-to-r from-blue-500 to-teal-400 text-white rounded-lg p-3 max-w-xs md:max-w-md shadow-sm">
                <p>${message}</p>
            </div>
            <div class="w-8 h-8 rounded-full user-avatar flex items-center justify-center ml-2 shadow-sm">
                <i class="fas fa-user text-white"></i>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Add bot message to chat
    function addBotMessage(message, isHTML = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start';
        
        if (isHTML) {
            messageDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bot-avatar flex items-center justify-center mr-2 shadow-sm">
                    <i class="fas fa-robot text-white"></i>
                </div>
                <div class="bg-indigo-50 rounded-lg p-3 max-w-xs md:max-w-md shadow-sm">
                    ${message}
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bot-avatar flex items-center justify-center mr-2 shadow-sm">
                    <i class="fas fa-robot text-white"></i>
                </div>
                <div class="bg-indigo-50 rounded-lg p-3 max-w-xs md:max-w-md shadow-sm">
                    <p>${message}</p>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Speak the message if sound is enabled and it's not HTML
        if (soundEnabled && botVoice && !isHTML) {
            botVoice.text = message;
            window.speechSynthesis.speak(botVoice);
        }
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'flex items-start';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full bot-avatar flex items-center justify-center mr-2">
                <i class="fas fa-robot text-white"></i>
            </div>
            <div class="bg-indigo-50 rounded-lg p-3 max-w-xs md:max-w-md">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 rounded-full bg-indigo-400 animate-bounce"></div>
                    <div class="w-2 h-2 rounded-full bg-indigo-400 animate-bounce delay-100"></div>
                    <div class="w-2 h-2 rounded-full bg-indigo-400 animate-bounce delay-200"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Handle voice button click
    voiceBtn.addEventListener('click', function() {
        if (speechRecognition) {
            try {
                speechRecognition.start();
            } catch (error) {
                addSystemMessage("Voice recognition not available. Please check your microphone permissions.");
            }
        } else {
            addSystemMessage("Voice recognition not supported in your browser.");
        }
    });
    
    // Handle sound button click
    soundBtn.addEventListener('click', function() {
        soundEnabled = !soundEnabled;
        if (soundEnabled) {
            soundBtn.innerHTML = '<i class="fas fa-volume-up text-white"></i>';
            addSystemMessage("Sound enabled");
        } else {
            soundBtn.innerHTML = '<i class="fas fa-volume-mute text-white"></i>';
            addSystemMessage("Sound muted");
        }
    });
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (message) {
            addUserMessage(message);
            userInput.value = '';
            
            showTypingIndicator();
            
            try {
                // Special case for greeting to trigger voice introduction
                if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
                    setTimeout(() => {
                        hideTypingIndicator();
                        const greeting = "Hello! I'm Linky, your LinkedIn optimization assistant. How can I help you optimize your profile today?";
                        addBotMessage(greeting);
                        
                        if (soundEnabled && botVoice) {
                            botVoice.text = greeting;
                            window.speechSynthesis.speak(botVoice);
                        }
                    }, 1500);
                    return;
                }
                
                // Send message to backend
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });
                
                const data = await response.json();
                hideTypingIndicator();
                
                if (data.html) {
                    addBotMessage(data.response, true);
                } else {
                    addBotMessage(data.response);
                }
            } catch (error) {
                hideTypingIndicator();
                addBotMessage("Sorry, I'm having trouble connecting to the server. Please try again later.");
                console.error('Error:', error);
            }
        }
    });
    
    // Quick buttons functionality
    quickButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            let message = '';
            
            switch(button.textContent.trim()) {
                case 'API Help':
                    message = "How can I integrate LinkedIn API with my project?";
                    break;
                case 'Keywords':
                    message = "What keywords should I use in my LinkedIn profile for digital marketing?";
                    break;
                case 'Profile Score':
                    message = "How can I check my LinkedIn profile completeness score?";
                    break;
                case 'Content Ideas':
                    message = "Can you suggest some LinkedIn post ideas for software developers?";
                    break;
                case 'Connection Tips':
                    message = "What are some effective ways to grow my LinkedIn connections?";
                    break;
                default:
                    message = button.textContent;
            }
            
            userInput.value = message;
            chatForm.dispatchEvent(new Event('submit'));
        });
    });
    
    // Emoji button functionality (placeholder)
    emojiBtn.addEventListener('click', function() {
        addSystemMessage("Emoji picker coming soon!");
    });
    
    // Auto-focus input on page load
    userInput.focus();
    
    // Initialize voice features when voices are loaded
    window.speechSynthesis.onvoiceschanged = function() {
        initVoice();
    };
    initVoice();
    initSpeechRecognition();
    
    // Welcome animation
    setTimeout(() => {
        document.querySelector('header').classList.remove('pulse');
    }, 3000);
});