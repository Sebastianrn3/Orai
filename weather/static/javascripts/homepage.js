const titleInput = document.querySelector("#titleInput");
const noteInput = document.querySelector("#noteInput");
const cancelBtn = document.querySelector("#cancelBtn");
const container = document.querySelector(".noteContainer");
const noteBackgroundColors = ["#0d8f6362", "#0d5f8f62", "#3521a562"];
let notes = localStorage.getItem("notes") ? JSON.parse(localStorage.getItem("notes")) : [];

function storageSave(){
    localStorage.setItem("notes", JSON.stringify(notes))
};

noteReloader();

function noteReloader(){
    while(container.firstChild){container.removeChild(container.firstChild);}
    notes.forEach(createNoteElement);
}
function createNoteElement(note, id){
    const div = document.createElement("div");
    div.style.backgroundColor = noteBackgroundColors[Math.floor(Math.random()*noteBackgroundColors.length)];
    div.style.textDecoration = note.finished ? "line-through" : "";
    div.addEventListener("click", () => {
        div.style.textDecoration = note.finished ? "" : "line-through";
        note.finished = !note.finished;
        storageSave();
    });
    const titleElement = document.createElement("h3");
    titleElement.textContent = note.title ? note.title : `Note ${id+1}`;
    titleElement.style.color = note.title ? "rgba(6, 0, 82, 0.83)" : "rgba(0, 0, 0, 0.14)";

    const noteTextElement = document.createElement("p");
    noteTextElement.textContent = note.noteText;

    const deleteBtn = document.createElement("div");
    deleteBtn.textContent = "🗑️";
    deleteBtn.addEventListener("click", (event) => {
        event.stopPropagation();
        notes.splice(id, 1);
        storageSave();
        noteReloader();
    });

    div.append(titleElement, noteTextElement, deleteBtn)
    container.prepend(div);
}

document.querySelector("form").addEventListener("submit", (event)=>{
    event.preventDefault();
    if(noteInput.value.trim() === ""){return noteInput.style.backgroundColor = "rgb(247, 154, 154)";}
    const newNote = {
        title: titleInput.value,
        noteText: noteInput.value,
        id: notes.length,
        finished: false
    };
    createNoteElement(newNote, newNote.id);
    notes.push(newNote);
    storageSave();
    noteInput.value = "";
    titleInput.value = "";
});
noteInput.addEventListener("focus", () => {
    noteInput.style.backgroundColor = "white";
    titleInput.hidden = false;
    cancelBtn.hidden = false;
});
cancelBtn.addEventListener("click", (event) => {
    event.preventDefault();
    noteInput.value = "";
    titleInput.value = "";
    titleInput.hidden = true;
    cancelBtn.hidden = true;
});