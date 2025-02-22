<template>
    <div class="piano-container">
      <div class="options-supp-container d-flex gap-2">
        <button class="btn btn-primary">Supprimer tout</button>
        <button class="btn btn-primary">Supprimer la dernière note</button>
        <button class="btn btn-primary">Jouer la mélodie</button>
      </div>
      <hr>
      <div class="octave-container d-flex gap-1">
        <button class="btn btn-outline-secondary">Octave -</button>
        <button class="btn btn-outline-secondary">Octave +</button>
      </div>
      <div class="piano">
        <div
          v-for="(key, index) in keys"
          :key="index"
          :class="['key', key.isBlack ? 'black' : 'white']"
          @mousedown="playNote(key.note)"
          @mouseup="stopNote(key.note)"
          @mouseleave="stopNote(key.note)"
        >
          <span v-if="!key.isBlack" class="note-label">{{ key.note }}</span>
        </div>
      </div>
      <!-- 🎼 Figures de notes sous le clavier -->
        <div class="notes-container">
        <div 
            v-for="(note, index) in notesPics" 
            :key="index" 
            class="note-button"
            @click="selectNoteFigure(note.pics)"
        >
            <img :src="getNoteImage(note.pics)" :alt="note.pics" class="note-img" />
            <!--<span class="note-label">{{ note.pics }}</span>-->
        </div>
        </div>
        <hr>
    </div>
  </template>
  
  <script>
  import { playNote, stopNote } from '@/utils/audioUtils';
  
  export default {
    name: 'PianoKeyboard',
    data() {
      return {
        keys: [
          { note: 'C4', isBlack: false },
          { note: 'C#4', isBlack: true },
          { note: 'D4', isBlack: false },
          { note: 'D#4', isBlack: true },
          { note: 'E4', isBlack: false },
          { note: 'F4', isBlack: false },
          { note: 'F#4', isBlack: true },
          { note: 'G4', isBlack: false },
          { note: 'G#4', isBlack: true },
          { note: 'A4', isBlack: false },
          { note: 'A#4', isBlack: true },
          { note: 'B4', isBlack: false },
          { note: 'C5', isBlack: false },
          // NEXT OCTAVE
          { note: 'C#5', isBlack: true },
          { note: 'D5', isBlack: false },
          { note: 'D#5', isBlack: true },
          { note: 'E5', isBlack: false },
          { note: 'F5', isBlack: false },
          { note: 'F#5', isBlack: true },
          { note: 'G5', isBlack: false },
          { note: 'G#5', isBlack: true },
          { note: 'A5', isBlack: false },
          { note: 'A#5', isBlack: true },
          { note: 'B6', isBlack: false },
          
        ],
        notesPics: [
            { pics: '1', label: 'Ronde' },
            { pics: '2', label: 'Blanche' },
            { pics: '2d', label: 'Blanche pointée' },
            { pics: '4', label: 'Noire' },
            { pics: '4d', label: 'Noire pointée' },
            { pics: '8', label: 'Croche' },
            { pics: '8d', label: 'Croche pointée' },
            { pics: '16', label: 'Double croche' },
            { pics: '16d', label: 'Double croche pointée' },
            { pics: '32', label: 'Triple croche' },
            { pics: '32d', label: 'Triple croche pointée' },
        ],
      };
    },
    methods: {
      playNote(note) {
        playNote(note);
      },
      stopNote(note) {
        stopNote(note);
      },
      selectNoteFigure(note) {
        console.log("🎼 Figure de note sélectionnée :", note);
      },
      getNoteImage(note) {
        return new URL(`/src/assets/public/notes_pics/${note}.png`, import.meta.url).href;
      },
    },
  };
  </script>
  
  <style scoped>
  .piano-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    flex-direction: column !important;
    margin-left: 0%;
  }
  
  .piano {
    display: flex;
    border-radius: 10px;
    background-color: #222;
    padding: 30px;
  }
  
  .key {
    width: 50px;
    height: 170px;
    border: 1px solid black;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    position: relative;
    user-select: none;
  }
  
  .white {
    background-color: white;
  }
  
  .black {
    background-color: black;
    height: 100px;
    width: 30px;
    margin-left: -15px;
    margin-right: -15px;
    z-index: 1;
    color: white !important;
  }
  
  .note-label {
    font-size: 14px;
    color: black;
    position: absolute;
    bottom: 5px;
  }
  /* 🎼 Figures de notes sous le clavier */
    .notes-container {
    background-color: #222;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 5px;
    padding: 5px;
    border-radius: 0px 0px 5px 5px;
    }
    .note-button {
    width: 50px;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: white;
    border: 1px solid black;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .note-button:hover {
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    }
    .note-img {
    width: auto;
    height: 50px;
    }
    .octave-container {
        background-color: #222;
        padding: 5px;
        border-radius: 5px 5px 0px 0px;
    }
  </style>
  