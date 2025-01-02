// Select DOM elements
const textInput = document.querySelector('.textInput');
const sendButton = document.querySelector('.ui-btn');
const chatContainer = document.querySelector('.chat');

// Helper function to create chat bubbles
function createChatBubble(role, message) {
  const chatSection = document.createElement('div');
  chatSection.classList.add(`${role}-section`);

  const avatar = document.createElement('div');
  avatar.classList.add(`${role}-avatar`);
  avatar.textContent = role === 'user' ? 'You:' : 'Anna:';

  const messageDiv = document.createElement('div');
  messageDiv.classList.add(`${role}-message`);
  messageDiv.textContent = message;

  chatSection.appendChild(avatar);
  chatSection.appendChild(messageDiv);

  return chatSection;
}

// Function to handle sending messages
async function sendMessage() {
  const userMessage = textInput.value.trim();
  if (!userMessage) return;

  // Add user's message to the chat
  const userBubble = createChatBubble('user', userMessage);
  chatContainer.appendChild(userBubble);
  textInput.value = '';

  // Scroll to the bottom of the chat container
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    // Send the message to the backend
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) throw new Error('Failed to fetch AI response.');

    const data = await response.json();
    const aiMessage = data.reply;

    // Add AI's response to the chat
    const aiBubble = createChatBubble('ai', aiMessage);
    chatContainer.appendChild(aiBubble);

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch (error) {
    console.error('Error:', error);
    const errorBubble = createChatBubble('ai', 'Sorry, something went wrong. Please try again later.');
    chatContainer.appendChild(errorBubble);
  }
}

// Add event listeners
sendButton.addEventListener('click', sendMessage);
textInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    sendMessage();
  }
});
