from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/style", StaticFiles(directory="style"), name="style")


templates = Jinja2Templates(directory="templates")

class Note(BaseModel):
    id: int
    title: str
    content: str

class NoteCreate(BaseModel):
    title: str
    content: str

class UpdateNote(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

note_list: List[Note] = []
next_id: int = 1

# Serve frontend
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pad")
def read_pad(request: Request):
    return templates.TemplateResponse("pad.html", {"request": request})

# Create note
@app.post("/notes/")
def create_notes(note: NoteCreate):
    global next_id
    new_note = Note(id=next_id, title=note.title, content=note.content)
    note_list.append(new_note)
    next_id += 1
    return {"message": "Note added successfully!", "note": new_note}

# Get notes
@app.get("/notes/", response_model=List[Note])
def get_notes(content: Optional[str] = None):
    if content:
        return [note for note in note_list if content.lower() in note.content.lower()]
    return note_list

# Update note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: UpdateNote):
    for index, note in enumerate(note_list):
        if note.id == note_id:
            if updated_note.title is not None:
                note.title = updated_note.title
            if updated_note.content is not None:
                note.content = updated_note.content
            note_list[index] = note
            return {"message": "Note updated", "note": note}
    return {"error": "Note not found"}

# Delete note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(note_list):
        if note.id == note_id:
            deleted = note_list.pop(index)
            return {"message": "Note deleted", "note": deleted}
    return {"error": "Note not found"}
