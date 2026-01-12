const API_URL = '/api/v1/notes';
let currentNotes = [];

// DOM Elements
const notesGrid = document.getElementById('notesGrid');
const searchInput = document.getElementById('searchInput');
const modalOverlay = document.getElementById('modalOverlay');
const noteForm = document.getElementById('noteForm');
const modalTitle = document.getElementById('modalTitle');

// Initial Load
document.addEventListener('DOMContentLoaded', fetchNotes);

// Event Listeners
searchInput.addEventListener('input', debounce((e) => fetchNotes(e.target.value), 300));

function openModal(mode = 'create', note = null) {
    modalOverlay.style.display = 'flex';
    if (mode === 'edit' && note) {
        modalTitle.textContent = 'Edit Note';
        document.getElementById('noteId').value = note.id;
        document.getElementById('title').value = note.title;
        document.getElementById('subject').value = note.subject;
        document.getElementById('student').value = note.student_name;
        document.getElementById('content').value = note.content;
        document.getElementById('tags').value = note.tags.join(', ');
    } else {
        modalTitle.textContent = 'New Note';
        noteForm.reset();
        document.getElementById('noteId').value = '';
    }
}

function closeModal() {
    modalOverlay.style.display = 'none';
}

// Close modal on outside click
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
});

// Fetch Notes
async function fetchNotes(search = '') {
    try {
        let url = `${API_URL}/?page_size=100`;
        if (search) url += `&search=${search}`;
        
        const response = await fetch(url);
        const data = await response.json();
        currentNotes = data.notes;
        renderNotes(currentNotes);
    } catch (error) {
        console.error('Error fetching notes:', error);
        notesGrid.innerHTML = '<div class="loading">Failed to load notes. Please try again.</div>';
    }
}

// Render Notes
function renderNotes(notes) {
    if (notes.length === 0) {
        notesGrid.innerHTML = '<div class="loading">No notes found. Create one to get started!</div>';
        return;
    }

    notesGrid.innerHTML = notes.map(note => `
        <div class="note-card">
            <div class="note-actions">
                <button class="btn-icon" onclick="editNote(${note.id})" title="Edit">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                </button>
                <button class="btn-icon delete" onclick="deleteNote(${note.id})" title="Delete">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
            </div>
            <div class="note-header">
                <h3 class="note-title">${escapeHtml(note.title)}</h3>
            </div>
            <div class="note-meta">
                <span>📚 ${escapeHtml(note.subject)}</span>
                <span>👤 ${escapeHtml(note.student_name)}</span>
            </div>
            <p class="note-content">${escapeHtml(note.content)}</p>
            <div class="tags">
                ${note.tags.map(tag => `<span class="tag">#${escapeHtml(tag)}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// Handle Form Submit
noteForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const noteId = document.getElementById('noteId').value;
    const formData = {
        title: document.getElementById('title').value,
        subject: document.getElementById('subject').value,
        student_name: document.getElementById('student').value,
        content: document.getElementById('content').value,
        tags: document.getElementById('tags').value.split(',').map(t => t.trim()).filter(t => t)
    };

    try {
        const url = noteId ? `${API_URL}/${noteId}` : API_URL + '/';
        const method = noteId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            closeModal();
            fetchNotes();
        } else {
            alert('Error saving note');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
    }
});

// Edit Note Helper
function editNote(id) {
    const note = currentNotes.find(n => n.id === id);
    if (note) openModal('edit', note);
}

// Delete Note
async function deleteNote(id) {
    if (!confirm('Are you sure you want to delete this note?')) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        if (response.ok) fetchNotes();
    } catch (error) {
        console.error('Error deleting note:', error);
    }
}

// Utility: Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Utility: Escape HTML
function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
