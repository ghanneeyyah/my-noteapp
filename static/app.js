const API_URL = "/notes";
const noteList = document.getElementById("note-list");

async function fetchNotes() {
    const res = await fetch(API_URL);
    const notes = await res.json();
    noteList.innerHTML = "";

    notes.forEach(note => {
        const li = document.createElement("li");
        li.textContent = note.title + " ";

        // ✏ Edit Button
        const editBtn = document.createElement("button");
        editBtn.textContent = "✏";
        editBtn.onclick = () => {
            window.location.href = `/pad?id=${note.id}`;
        };

        // 🗑 Delete Button
        const delBtn = document.createElement("button");
        delBtn.textContent = "🗑";
        delBtn.onclick = async () => {
            await fetch(`/notes/${note.id}`, { method: "DELETE" });
            fetchNotes();
        };

        li.appendChild(editBtn);
        li.appendChild(delBtn);
        noteList.appendChild(li);
    });
}

fetchNotes();
