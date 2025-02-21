<template>
  <div>
    <!-- Barre de recherche -->
    <div class="searchbar-box">
      <h1 class="searchbar-title">Rechercher dans le contenu des partitions</h1>
    </div>
    
    <!-- Notification d'aide -->
    <div class="toast custom-toast align-items-center text-bg-warning border-0" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
      <div class="d-flex">
        <a href="<%= BASE_PATH %>/help"><div class="toast-body text-center text-white">
          Aide/astuce
          <i class="bi bi-lightbulb-fill me-2"></i>
        </div>
        </a>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
    
    <!-- Interface principale -->
    <div class="content-wrapper" style="align-items: center;">
      <div class="search-pattern">
        <h1>Rechercher un motif musical</h1>
        <div id="music-score"></div>
        
        <!-- Boutons de gestion des notes -->
        <div class="clear_buttons">
          <button @click="clearAll" class="btn btn-info text-white">Supprimer tout</button>
          <button @click="clearLastNote" class="btn btn-info text-white">Supprimer la dernière note</button>
          <button @click="playMelody" class="btn btn-info text-white">Jouer la mélodie</button>
        </div>
      </div>
      
      <!-- Clavier de piano -->
      <div class="wrapper">
        <header>
          <div class="column volume-slider">
            <span>Volume</span>
            <input type="range" min="0" max="1" v-model="volume" step="any">
          </div>
        </header>
        <ul class="piano-keys">
          <li v-for="key in pianoKeys" :key="key" :class="key.includes('#') ? 'key black' : 'key white'" @mousedown="playNote(key)" @mouseup="stopNote(key)">
            <span>{{ key }}</span>
          </li>
        </ul>
      </div>
      
      <!-- Options avancées -->
      <button class="btn btn-outline-secondary text-white" type="button" data-bs-toggle="collapse" data-bs-target="#bellow-keyboard">
        Options avancées
      </button>
      <div class="collapse collapse-vertical" id="bellow-keyboard">
        <div class='rhythm-modif'>
          <button v-for="note in rhythmOptions" :key="note.key" @click="changeLastNoteRhythm(note.key)">
            <img :src="note.image" height="50px">
          </button>
        </div>
      </div>
      
      <!-- Sélection de la collection -->
      <div class="collections-options">
        <label for="collections">Collection dans lesquelles rechercher :</label>
        <select id="collections" v-model="selectedCollection">
          <option v-for="collection in collections" :key="collection" :value="collection">{{ collection }}</option>
        </select>
      </div>
      
      <!-- Recherche -->
      <button @click="search" class="btn btn-outline-secondary text-white">Lancer la recherche</button>
    </div>
  </div>
</template>

<script>
import Vex from 'vexflow';
export default {
  data() {
    return {
      volume: 0.5,
      melody: [],
      selectedCollection: '',
      pianoKeys: ["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"],
      rhythmOptions: [
        { key: 'q', image: 'public/notes_pics/4.png' },
        { key: 'h', image: 'public/notes_pics/2.png' },
        { key: 'w', image: 'public/notes_pics/1.png' }
      ],
      collections: ['Bach', 'Mozart', 'Beethoven']
    };
  },
  methods: {
    playNote(note) {
      console.log(`Playing ${note}`);
    },
    stopNote(note) {
      console.log(`Stopping ${note}`);
    },
    clearAll() {
      this.melody = [];
    },
    clearLastNote() {
      this.melody.pop();
    },
    playMelody() {
      console.log("Playing melody", this.melody);
    },
    search() {
      console.log("Searching in", this.selectedCollection);
    },
    changeLastNoteRhythm(rhythm) {
      if (this.melody.length) {
        this.melody[this.melody.length - 1].rhythm = rhythm;
      }
    }
  }
};
</script>

<style scoped>
@import "@/assets/styles/search_interface_style.css";
@import "@/assets/styles/general_style.css";
.piano-keys {
  display: flex;
}
.key {
  width: 40px;
  height: 120px;
  border: 1px solid black;
  text-align: center;
  cursor: pointer;
}
.black {
  background: black;
  color: white;
}
.white {
  background: white;
}
</style>
