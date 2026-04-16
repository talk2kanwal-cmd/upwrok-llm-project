document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadStatus = document.getElementById('upload-status');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    
    let selectedFile = null;

    // File Upload Handlers
    dropZone.addEventListener('click', () => fileInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        selectedFile = file;
        dropZone.querySelector('p').textContent = file.name;
    }

    uploadBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            uploadStatus.textContent = 'Please select a file first.';
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Uploading...';
        uploadStatus.textContent = '';

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            
            if (res.ok) {
                uploadStatus.innerHTML = `<span style="color: #10b981;">Success! Ingested into ${data.chunks_created} chunks.</span>`;
                dropZone.querySelector('p').textContent = 'Drag & drop or click to upload';
                selectedFile = null;
                fileInput.value = '';
            } else {
                uploadStatus.innerHTML = `<span style="color: #ef4444;">Error: ${data.detail || 'Upload failed'}</span>`;
            }
        } catch (err) {
            uploadStatus.innerHTML = `<span style="color: #ef4444;">Connection error.</span>`;
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload Document';
        }
    });

    // Chat Handlers
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        chatInput.value = '';
        
        const typingId = appendTypingIndicator();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text })
            });
            
            removeElement(typingId);
            
            if (res.ok) {
                const data = await res.json();
                appendMessage('bot', data.response, data.context_sources);
            } else {
                appendMessage('bot', 'Error: Unable to reach the server.');
            }
        } catch (err) {
            removeElement(typingId);
            appendMessage('bot', 'Network error or server is down.');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function appendMessage(role, text, sources = []) {
        const div = document.createElement('div');
        div.className = `message msg-${role}`;
        
        div.textContent = text; 
        
        if (sources && sources.length > 0 && sources[0] !== 'Unknown') {
            const sourcesDiv = document.createElement('span');
            sourcesDiv.className = 'msg-sources';
            sourcesDiv.textContent = `Sources: ${sources.join(', ')}`;
            div.appendChild(sourcesDiv);
        }
        
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.className = 'message msg-bot';
        div.id = id;
        div.innerHTML = '<span class="material-icons" style="animation: pulse 1s infinite; font-size: 1rem;">more_horiz</span>';
        chatMessages.appendChild(div);
        scrollToBottom();
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
