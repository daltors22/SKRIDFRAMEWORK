// utils/audioUtils.js

const audioFiles = {
  "C4": new Audio('./src/assets/acoustic_grand_piano-mp3/C4.mp3'),
  "C#4": new Audio('./src/assets/acoustic_grand_piano-mp3/Db4.mp3'),
  "D4": new Audio('./src/assets/acoustic_grand_piano-mp3/D4.mp3'),
  "D#4": new Audio('./src/assets/acoustic_grand_piano-mp3/Eb4.mp3'),
  "E4": new Audio('./src/assets/acoustic_grand_piano-mp3/E4.mp3'),
  "F4": new Audio('./src/assets/acoustic_grand_piano-mp3/F4.mp3'),
  "F#4": new Audio('./src/assets/acoustic_grand_piano-mp3/Gb4.mp3'),
  "G4": new Audio('./src/assets/acoustic_grand_piano-mp3/G4.mp3'),
  "G#4": new Audio('./src/assets/acoustic_grand_piano-mp3/Ab4.mp3'),
  "A4": new Audio('./src/assets/acoustic_grand_piano-mp3/A4.mp3'),
  "A#4": new Audio('./src/assets/acoustic_grand_piano-mp3/Bb4.mp3'),
  "B4": new Audio('./src/assets/acoustic_grand_piano-mp3/B4.mp3'),
  "C5": new Audio('./src/assets/acoustic_grand_piano-mp3/C5.mp3'),
  "C#5": new Audio('./src/assets/acoustic_grand_piano-mp3/Db5.mp3'),
  "D5": new Audio('./src/assets/acoustic_grand_piano-mp3/D5.mp3'),
  "D#5": new Audio('./src/assets/acoustic_grand_piano-mp3/Eb5.mp3'),
  "E5": new Audio('./src/assets/acoustic_grand_piano-mp3/E5.mp3'),
  "F5": new Audio('./src/assets/acoustic_grand_piano-mp3/F5.mp3'),
  "F#5": new Audio('./src/assets/acoustic_grand_piano-mp3/Gb5.mp3'),
  "G5": new Audio('./src/assets/acoustic_grand_piano-mp3/G5.mp3'),
  "G#5": new Audio('./src/assets/acoustic_grand_piano-mp3/Ab5.mp3'),
  "A5": new Audio('./src/assets/acoustic_grand_piano-mp3/A5.mp3'),
  "A#5": new Audio('./src/assets/acoustic_grand_piano-mp3/Bb5.mp3'),
  "B5": new Audio('./src/assets/acoustic_grand_piano-mp3/B5.mp3')
};

console.log("Audio mapping:", audioFiles);

export function playNote(note) {
  console.log("playNote appelé pour la note:", note);
  if (audioFiles[note]) {
    audioFiles[note].currentTime = 0;
    audioFiles[note].play().catch((err) => {
      console.error("Erreur lors de la lecture de la note", note, err);
    });
  } else {
    console.warn("Note non trouvée dans le mapping:", note);
  }
}

export function stopNote(note) {
  if (audioFiles[note]) {
    audioFiles[note].pause();
    audioFiles[note].currentTime = 0;
  }
}
