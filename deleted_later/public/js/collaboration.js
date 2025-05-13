// Initialize Socket.IO connection
const socket = io();

// Current user's role
let currentRole = '';

// Function to set user role
function setUserRole(role) {
    currentRole = role;
    socket.emit('role-join', { role });
}

// Function to handle document updates
function updateDocument(content, documentId) {
    socket.emit('document-update', {
        role: currentRole,
        content,
        documentId
    });
}

// Listen for document updates from other users
socket.on('document-updated', (data) => {
    const { role, content, documentId } = data;
    
    // Update the UI based on the role and content
    updateUI(role, content, documentId);
});

// Listen for role-specific updates
socket.on('sdet-update', (data) => {
    if (currentRole === 'test-lead' || currentRole === 'product-owner') {
        // Show SDET's changes to Test Lead and Product Owner
        showSDETChanges(data);
    }
});

socket.on('test-lead-update', (data) => {
    if (currentRole === 'product-owner') {
        // Show Test Lead's changes to Product Owner
        showTestLeadChanges(data);
    }
});

// UI update functions
function updateUI(role, content, documentId) {
    const documentElement = document.getElementById(documentId);
    if (documentElement) {
        documentElement.innerHTML = content;
        // Add visual indicator for real-time updates
        documentElement.classList.add('updated');
        setTimeout(() => {
            documentElement.classList.remove('updated');
        }, 1000);
    }
}

function showSDETChanges(data) {
    // Implement UI to show SDET's changes
    const changesContainer = document.getElementById('sdet-changes');
    if (changesContainer) {
        changesContainer.innerHTML = `
            <div class="change-item">
                <h4>SDET Changes</h4>
                <p>${data.content}</p>
                <button onclick="acceptChanges('${data.documentId}')">Accept</button>
                <button onclick="rejectChanges('${data.documentId}')">Reject</button>
            </div>
        `;
    }
}

function showTestLeadChanges(data) {
    // Implement UI to show Test Lead's changes
    const changesContainer = document.getElementById('test-lead-changes');
    if (changesContainer) {
        changesContainer.innerHTML = `
            <div class="change-item">
                <h4>Test Lead Changes</h4>
                <p>${data.content}</p>
                <button onclick="acceptChanges('${data.documentId}')">Accept</button>
                <button onclick="rejectChanges('${data.documentId}')">Reject</button>
            </div>
        `;
    }
}

// Change acceptance/rejection handlers
function acceptChanges(documentId) {
    socket.emit('accept-changes', { documentId, role: currentRole });
}

function rejectChanges(documentId) {
    socket.emit('reject-changes', { documentId, role: currentRole });
} 