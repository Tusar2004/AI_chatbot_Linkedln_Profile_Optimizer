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
    
    // Tab elements
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // AI Analysis elements
    const analyzeBtn = document.getElementById('analyze-btn');
    const profileUrlInput = document.getElementById('profile-url');
    const analysisResults = document.getElementById('analysis-results');
    const strengthsList = document.getElementById('strengths-list');
    const weaknessesList = document.getElementById('weaknesses-list');
    const suggestionsList = document.getElementById('suggestions-list');
    const profileScore = document.getElementById('profile-score');
    const scoreBar = document.getElementById('score-bar');
    const scoreComparison = document.getElementById('score-comparison');
    const exportAnalysisBtn = document.getElementById('export-analysis-btn');
    
    // Profile Score elements
    const downloadExcelBtn = document.getElementById('download-excel-btn');
    const viewChatBtn = document.getElementById('view-chat-btn');
    
    // PDF Export elements
    const generatePdfBtn = document.getElementById('generate-pdf-btn');
    
    // New elements for optimization tools
    const summaryInput = document.getElementById('summary-input');
    const summarySuggestions = document.getElementById('summary-suggestions');
    const summaryFeedback = document.getElementById('summary-feedback');
    const headlineInput = document.getElementById('headline-input');
    const analyzeHeadlineBtn = document.getElementById('analyze-headline-btn');
    const headlineResults = document.getElementById('headline-results');
    const headlineScore = document.getElementById('headline-score');
    const headlineScoreBar = document.getElementById('headline-score-bar');
    const headlineTips = document.getElementById('headline-tips');
    const targetRoleInput = document.getElementById('target-role-input');
    const findKeywordsBtn = document.getElementById('find-keywords-btn');
    const keywordResults = document.getElementById('keyword-results');
    const recommendedKeywords = document.getElementById('recommended-keywords');
    const profileTextInput = document.getElementById('profile-text-input');
    const highlightedText = document.getElementById('highlighted-text');
    const jobTitleSelect = document.getElementById('job-title-select');
    const generateHeadlineBtn = document.getElementById('generate-headline-btn');
    const generatedHeadlines = document.getElementById('generated-headlines');
    const headlineOptions = document.getElementById('headline-options');
    const regenerateHeadlinesBtn = document.getElementById('regenerate-headlines-btn');
    
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
    
    // Tab switching functionality
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            tabButtons.forEach(btn => btn.classList.remove('active', 'text-indigo-700', 'bg-indigo-50'));
            this.classList.add('active', 'text-indigo-700', 'bg-indigo-50');
            
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            
            if (tabId === 'score') {
                initProfileChart();
            }
        });
    });
    
    // Initialize profile score chart
    function initProfileChart() {
        const ctx = document.getElementById('profileChart').getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Headline', 'Summary', 'Experience', 'Education', 'Skills', 'Recommendations'],
                datasets: [{
                    label: 'Your Profile',
                    data: [85, 65, 90, 75, 70, 40],
                    backgroundColor: 'rgba(79, 70, 229, 0.2)',
                    borderColor: 'rgba(79, 70, 229, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(79, 70, 229, 1)',
                    pointRadius: 4
                }, {
                    label: 'Industry Average',
                    data: [70, 60, 80, 85, 65, 50],
                    backgroundColor: 'rgba(192, 132, 252, 0.2)',
                    borderColor: 'rgba(192, 132, 252, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(192, 132, 252, 1)',
                    pointRadius: 4
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }
    
    // Handle AI analysis
    analyzeBtn.addEventListener('click', function() {
        const profileUrl = profileUrlInput.value.trim();
        
        if (!profileUrl) {
            alert('Please enter your LinkedIn profile URL');
            return;
        }
        
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Analyzing...';
        analyzeBtn.disabled = true;
        
        setTimeout(() => {
            const analysis = {
                strengths: ["Strong keyword optimization", "Complete experience section", "Good education background"],
                weaknesses: ["Summary could be more compelling", "Need more recommendations", "Skills section needs updating"],
                suggestions: [
                    "Add 3-5 more technical skills",
                    "Include metrics in your experience descriptions",
                    "Write a more engaging summary with your unique value proposition"
                ],
                score: 78,
                comparison: "Your profile scores higher than 65% of profiles in your industry"
            };
            
            strengthsList.innerHTML = analysis.strengths.map(strength => `<li>${strength}</li>`).join('');
            weaknessesList.innerHTML = analysis.weaknesses.map(weakness => `<li>${weakness}</li>`).join('');
            suggestionsList.innerHTML = analysis.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('');
            profileScore.textContent = analysis.score;
            scoreBar.style.width = `${analysis.score}%`;
            scoreComparison.textContent = analysis.comparison;
            
            analysisResults.classList.remove('hidden');
            
            analyzeBtn.innerHTML = '<span>Analyze</span><i class="fas fa-magic ml-2"></i>';
            analyzeBtn.disabled = false;
        }, 2000);
    });
    
    // Handle Excel download
    downloadExcelBtn.addEventListener('click', function() {
        window.location.href = '/profile-score-visualization';
    });
    
    // Handle PDF generation
    generatePdfBtn.addEventListener('click', function() {
        generatePdfBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Generating...';
        generatePdfBtn.disabled = true;
        
        window.location.href = '/export-profile-pdf';
        
        setTimeout(() => {
            generatePdfBtn.innerHTML = '<span>Generate PDF Report</span><i class="fas fa-download ml-2"></i>';
            generatePdfBtn.disabled = false;
        }, 2000);
    });
    
    // Handle export analysis
    exportAnalysisBtn.addEventListener('click', function() {
        window.location.href = '/export-profile-pdf';
    });
    
    // View chat button
    viewChatBtn.addEventListener('click', function() {
        tabButtons.forEach(btn => btn.classList.remove('active', 'text-indigo-700', 'bg-indigo-50'));
        document.querySelector('[data-tab="chat"]').classList.add('active', 'text-indigo-700', 'bg-indigo-50');
        
        tabContents.forEach(content => content.classList.remove('active'));
        document.getElementById('chat').classList.add('active');
        
        userInput.focus();
    });
    
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
        
        if (soundEnabled && botVoice && !isHTML) {
            botVoice.text = message;
            window.speechSynthesis.speak(botVoice);
        }
    }
    
    // Show typing indicator
    function showTypingIndicator(type = 'chat') {
        const indicatorId = `typing-indicator-${type}`;
        if (document.getElementById(indicatorId)) return;
        
        const container = type === 'chat' ? chatMessages : document.getElementById(`${type}-results`);
        if (!container) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'flex items-start mb-3';
        typingDiv.id = indicatorId;
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
        
        container.appendChild(typingDiv);
        container.scrollTop = container.scrollHeight;
    }
    
    // Hide typing indicator
    function hideTypingIndicator(type = 'chat') {
        const indicatorId = `typing-indicator-${type}`;
        const typingIndicator = document.getElementById(indicatorId);
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
    
    // Emoji button functionality
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

    // Real-time summary suggestions
    function setupSummaryOptimizer() {
        let debounceTimer;
        const DEBOUNCE_DELAY = 1000;
        
        summaryInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            
            if (summaryInput.value.trim().length > 50) {
                debounceTimer = setTimeout(() => {
                    showTypingIndicator('summary');
                    analyzeSummary(summaryInput.value);
                }, DEBOUNCE_DELAY);
            } else {
                summarySuggestions.classList.add('hidden');
            }
        });
        
        async function analyzeSummary(text) {
            try {
                const response = await fetch('/analyze-summary', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text }),
                });
                
                const data = await response.json();
                hideTypingIndicator('summary');
                
                if (data.suggestions) {
                    summaryFeedback.innerHTML = data.suggestions.map(s => `<p class="mt-1">• ${s}</p>`).join('');
                    summarySuggestions.classList.remove('hidden');
                }
            } catch (error) {
                hideTypingIndicator('summary');
                console.error('Error analyzing summary:', error);
            }
        }
    }

    // Headline analyzer
    function setupHeadlineAnalyzer() {
        analyzeHeadlineBtn.addEventListener('click', async () => {
            const headline = headlineInput.value.trim();
            if (!headline) return;
            
            showTypingIndicator('headline');
            
            try {
                const response = await fetch('/analyze-headline', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ headline }),
                });
                
                const data = await response.json();
                hideTypingIndicator('headline');
                
                if (data.score) {
                    headlineScore.textContent = data.score;
                    headlineScoreBar.style.width = `${data.score}%`;
                    
                    headlineTips.innerHTML = data.tips.map(tip => `<div class="flex items-start">
                        <i class="fas ${tip.important ? 'fa-exclamation-circle text-red-500' : 'fa-info-circle text-blue-500'} mt-1 mr-2"></i>
                        <p>${tip.text}</p>
                    </div>`).join('');
                    
                    headlineResults.classList.remove('hidden');
                }
            } catch (error) {
                hideTypingIndicator('headline');
                console.error('Error analyzing headline:', error);
            }
        });
    }

    // Keyword highlighter
    function setupKeywordHighlighter() {
        findKeywordsBtn.addEventListener('click', async () => {
            const role = targetRoleInput.value.trim();
            if (!role) return;
            
            showTypingIndicator('keywords');
            
            try {
                const response = await fetch('/get-keywords', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ role }),
                });
                
                const data = await response.json();
                hideTypingIndicator('keywords');
                
                if (data.keywords) {
                    recommendedKeywords.innerHTML = data.keywords.map(kw => 
                        `<span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">${kw}</span>`
                    ).join('');
                    
                    keywordResults.classList.remove('hidden');
                    
                    // Setup text highlighting
                    profileTextInput.addEventListener('input', () => {
                        highlightKeywords(profileTextInput.value, data.keywords);
                    });
                }
            } catch (error) {
                hideTypingIndicator('keywords');
                console.error('Error finding keywords:', error);
            }
        });
        
        function highlightKeywords(text, keywords) {
            if (!text) {
                highlightedText.classList.add('hidden');
                return;
            }
            
            const pattern = new RegExp(`(${keywords.join('|')})`, 'gi');
            
            const highlighted = text.replace(pattern, match => 
                `<span class="bg-yellow-200 font-medium">${match}</span>`
            );
            
            highlightedText.innerHTML = highlighted;
            highlightedText.classList.remove('hidden');
        }
    }

    // Headline generator
    function setupHeadlineGenerator() {
        generateHeadlineBtn.addEventListener('click', generateHeadlines);
        regenerateHeadlinesBtn.addEventListener('click', generateHeadlines);
        
        async function generateHeadlines() {
            const jobTitle = jobTitleSelect.value;
            if (!jobTitle) return;
            
            showTypingIndicator('headline-gen');
            
            try {
                const response = await fetch('/generate-headlines', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ jobTitle }),
                });
                
                const data = await response.json();
                hideTypingIndicator('headline-gen');
                
                if (data.headlines) {
                    headlineOptions.innerHTML = data.headlines.map((hl, i) => `
                        <div class="bg-indigo-50 p-3 rounded-lg border border-indigo-100 flex justify-between items-center">
                            <p>${hl}</p>
                            <button class="copy-headline-btn text-indigo-600 hover:text-indigo-800" data-headline="${hl}">
                                <i class="fas fa-copy"></i>
                            </button>
                        </div>
                    `).join('');
                    
                    generatedHeadlines.classList.remove('hidden');
                    
                    // Add copy functionality
                    document.querySelectorAll('.copy-headline-btn').forEach(btn => {
                        btn.addEventListener('click', () => {
                            const headline = btn.getAttribute('data-headline');
                            navigator.clipboard.writeText(headline);
                            btn.innerHTML = '<i class="fas fa-check text-green-500"></i>';
                            setTimeout(() => {
                                btn.innerHTML = '<i class="fas fa-copy"></i>';
                            }, 2000);
                        });
                    });
                }
            } catch (error) {
                hideTypingIndicator('headline-gen');
                console.error('Error generating headlines:', error);
            }
        }
    }

    // Initialize all the new features
    setupSummaryOptimizer();
    setupHeadlineAnalyzer();
    setupKeywordHighlighter();
    setupHeadlineGenerator();
});
