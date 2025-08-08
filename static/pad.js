const form = document.getElementById("note-form");
const API_URL = "/notes/";

// If editing, load note data
const urlParams = new URLSearchParams(window.location.search);
const noteId = urlParams.get("id");

if (noteId) {
    fetch(`/notes/`)
        .then(res => res.json())
        .then(notes => {
            const note = notes.find(n => n.id == noteId);
            if (note) {
                document.getElementById("title").value = note.title;
                document.getElementById("note-content").value = note.content;
            }
        });
}

form.onsubmit = async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const content = document.getElementById("note-content").value;

    if (noteId) {
        // Update
        await fetch(`/notes/${noteId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, content })
        });
    } else {
        // Create
        await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, content })
        });
    }

    window.location.href = "/";
};
