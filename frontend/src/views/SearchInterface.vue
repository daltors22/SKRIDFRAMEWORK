<template>
  <div class="search-interface">
    <h1 class="searchbar-title">Rechercher dans le contenu des partitions</h1>
    
    <!-- Portée musicale -->
    <div id="music-score"></div>
    
    <!-- Piano interactif -->
    <PianoKeyboard @noteOn="handleNoteOn" @noteOff="handleNoteOff" />

    <!-- AJOUTER L'OPTION HIDE/SHOW -- ## Paramètres de recherche avancés ##
    <div class="search-controls">

      <div class="options">
        <label><input type="checkbox" v-model="searchOptions.pitch" /> Hauteur des notes</label>
        <label><input type="checkbox" v-model="searchOptions.rhythm" /> Rythme</label>
        <label><input type="checkbox" v-model="searchOptions.transpose" /> Autoriser transposition</label>
      </div>
      
      <div class="search-parameters d-flex flex-column">
        <label>Distance de hauteur : <input type="number" v-model.number="searchOptions.pitchDist" min="0" step="0.5"></label>
        <label>Facteur de durée : <input type="number" v-model.number="searchOptions.durationFactor" min="0.5" step="0.1"></label>
        <label>Écart de durée : <input type="number" v-model.number="searchOptions.durationGap" min="0" step="0.01"></label>
        <label>Alpha (score min) : <input type="number" v-model.number="searchOptions.alpha" min="0" max="100" step="5"></label>
      </div>
      
    </div>
    -->
    <!-- Sélection de la collection (choix unique) -->
    <div class="collections-container">
      <label class="collection-label">Collection à rechercher :</label>
      <div class="collections-menu">
        <button 
          v-for="(author, index) in authors" 
          :key="index" 
          class="btn collection-item"
          :class="{ 'active': author === selectedAuthor }"
          @click="selectCollection(author)"
        >
          {{ author }}
        </button>
      </div>
    </div>
    <hr>
    <div class="preset-buttons">
        <button @click="applyPreset('stricte')" :class="{ active: activePreset === 'stricte' }">Recherche exacte</button>
        <button @click="applyPreset('modereeMelo')" :class="{ active: activePreset === 'modereeMelo' }">Recherche tolérante (mélodie)</button>
        <button @click="applyPreset('modereeRythm')" :class="{ active: activePreset === 'modereeRythm' }">Recherche tolérante (rythme)</button>
    </div>
    <br>
    <button @click="search" class="search-button">Lancer la recherche</button>

    <div v-if="results.length > 0" class="results-container">
      <h2>Résultats :</h2>
      <ul>
        <li v-for="result in results" :key="result.id">{{ result.title }} - Score : {{ result.score }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import PianoKeyboard from '@/components/PianoKeyboard.vue';
import axios from 'axios';
import { Renderer, Stave, Formatter, StaveNote } from 'vexflow';

export default {
  components: { PianoKeyboard },
  data() {
    return {
      activePreset: 'stricte',
      searchOptions: {
        pitch: true,
        rhythm: true,
        transpose: false,
        pitchDist: 0,
        durationFactor: 1,
        durationGap: 0,
        alpha: 0,
      },
      authors: [],  // 📌 Liste des collections récupérées depuis l'API
      selectedAuthor: "", // 📌 Collection sélectionnée
      results: [],
      melody: [],
      renderer: null,
      context: null,
      stave: null,
    };
  },
  methods: {
    async fetchAuthors() {
      try {
        console.log("📡 Récupération des collections...");
        const response = await axios.get("http://127.0.0.1:5000/collections", {
          headers: { Accept: "application/json" }
        });

        this.authors = response.data.authors;
        console.log("✅ Collections chargées :", this.authors);

        // 📌 Pré-sélectionner la première collection si disponible
        if (this.authors.length > 0) {
          this.selectCollection(this.authors[0]);
        }
      } catch (error) {
        console.error("❌ Erreur de chargement des collections:", error);
      }
    },

    selectCollection(author) {
      this.selectedAuthor = author;
      console.log("📌 Collection sélectionnée :", this.selectedAuthor);
    },

    applyPreset(preset) {
      this.activePreset = preset;
      const presets = {
        stricte: { pitchDist: 0, durationFactor: 1, durationGap: 0, alpha: 0, pitch: true, rhythm: true, transpose: false },
        modereeMelo: { pitchDist: 3, durationFactor: 1.5, durationGap: 0, alpha: 50, pitch: true, rhythm: true, transpose: true },
        modereeRythm: { pitchDist: 1, durationFactor: 4, durationGap: 0.0625, alpha: 50, pitch: true, rhythm: true, transpose: true },
      };
      Object.assign(this.searchOptions, presets[preset]);
    },

    async search() {
      if (!this.melody.length) {
        alert('Ajoutez des notes avant de rechercher !');
        return;
      }
      const data = {
        notes: this.melody,
        ...this.searchOptions,
        collection: this.selectedAuthor,
      };
      try {
        const response = await axios.post('http://127.0.0.1:5000/search', data);
        this.results = response.data.results;
      } catch (error) {
        console.error('Erreur lors de la recherche', error);
      }
    },

    initVexflow() {
      this.renderer = new Renderer(document.getElementById('music-score'), Renderer.Backends.SVG);
      this.context = this.renderer.getContext();
      this.stave = new Stave(10, 40, 400);
      this.stave.addClef('treble').setContext(this.context).draw();
    },
  },

  mounted() {
    this.fetchAuthors();
    this.initVexflow();
  },
};
</script>

<style scoped>
.search-interface {
  text-align: center;
  padding: 20px;
}

.preset-buttons button {
  margin: 5px;
  padding: 10px;
  border: none;
  cursor: pointer;
}

.preset-buttons button.active {
  background-color: #007bff;
  color: white;
}

.search-button {
  margin-top: 10px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.collections-container {
  margin-top: 15px;
}

.collections-menu {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.collection-item {
  background-color: #f8f9fa;
  border: 1px solid #ccc;
  padding: 8px 15px;
  cursor: pointer;
}

.collection-item.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}
</style>

