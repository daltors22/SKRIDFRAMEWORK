const audioFiles = {
    C4: new Audio('/sounds/C4.mp3'),
    'C#4': new Audio('/sounds/Csharp4.mp3'),
    D4: new Audio('/sounds/D4.mp3'),
    'D#4': new Audio('/sounds/Dsharp4.mp3'),
    E4: new Audio('/sounds/E4.mp3'),
    F4: new Audio('/sounds/F4.mp3'),
    'F#4': new Audio('/sounds/Fsharp4.mp3'),
    G4: new Audio('/sounds/G4.mp3'),
    'G#4': new Audio('/sounds/Gsharp4.mp3'),
    A4: new Audio('/sounds/A4.mp3'),
    'A#4': new Audio('/sounds/Asharp4.mp3'),
    B4: new Audio('/sounds/B4.mp3'),
    C5: new Audio('/sounds/C5.mp3'),
  };
  
  export function playNote(note) {
    if (audioFiles[note]) {
      audioFiles[note].currentTime = 0;
      audioFiles[note].play();
    }
  }
  
  export function stopNote(note) {
    if (audioFiles[note]) {
      audioFiles[note].pause();
      audioFiles[note].currentTime = 0;
    }
  }