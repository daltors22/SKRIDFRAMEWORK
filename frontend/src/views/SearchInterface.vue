<template>
  <div>
    <!-- Barre de recherche et notifications -->
    <div class="searchbar-box">
      <h1 class="searchbar-title">Rechercher dans le contenu des partitions</h1>
    </div>

    <div v-if="showHelpToast" class="toast custom-toast align-items-center text-bg-warning border-0" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
      <div class="d-flex">
        <a href="#">
          <div class="toast-body text-center text-white">
            Aide/astuce
            <i class="bi bi-lightbulb-fill me-2"></i>
          </div>
        </a>
        <button @click="closeToast('help')" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>

    <div v-if="showMicroToast" class="toast1 custom-toast1 align-items-center text-bg border-0" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
      <div class="d-flex">
        <a href="#">
          <div class="toast-body text-center text-white">
            <p>Micro</p>
            <i class="bi bi-mic-fill"></i>
          </div>
        </a>
      </div>
    </div>

    <!-- Section de saisie musicale -->
    <div class="content-wrapper d-flex flex-column mt-5" style="align-items: center; justify-content: center;">
      <div class="search-pattern">
        <h1>Rechercher un motif musical</h1>
        <!-- Zone où la partition en cours (saisie) est affichée -->
        <div id="music-score"></div>
        <div class="clear_buttons">
          <button @click="clearAll" type="button" class="btn btn-info text-white" style="background-color: #7ab6e0;">Supprimer tout</button>
          <button @click="removeLastNote" type="button" class="btn btn-info text-white" style="background-color: #7ab6e0;">Supprimer la dernière note</button>
          <button @click="playMelody" type="button" class="btn btn-info text-white" style="background-color: #7ab6e0;">Jouer la mélodie</button>
        </div>
      </div>

      <!-- Contrôles (Volume, Octave, touches, piano, rythme) -->
      <div class="wrapper">
        <header>
          <div class="column volume-slider">
            <span>Volume</span>
            <input type="range" v-model="volume" min="0" max="1" step="any" />
          </div>
          <div class="octave-modif">
            <div class="octave-modif-bt-div">
              <button @click="changeOctave(-1)" class="btn btn-outline-secondary text-white octave-modif-bt" id="octave-minus"><span>Octave - (c)</span></button>
              <button @click="changeOctave(1)" class="btn btn-outline-secondary text-white octave-modif-bt" id="octave-plus"><span>Octave + (v)</span></button>
            </div>
            <label id="octave-lb" class="white-label">{{ octave }}</label>
          </div>
          <div class="column keys-checkbox">
            <span>Touches</span>
            <input type="checkbox" checked />
          </div>
          <div class="keyboard-config">
            <button @click="toggleKeyboardConfig" class="btn btn-secondary">
              Config clavier : {{ keyboardConfig }}
            </button>
          </div>
        </header>

        <!-- Clavier virtuel -->
        <ul class="piano-keys">
          <li v-for="key in pianoKeys" :key="key.id" :class="['key', key.color]" @mousedown="keyDown(key)" @mouseup="keyUp(key)">
            <span>{{ key.label }}<br />{{ key.key }}</span>
          </li>
        </ul>

        <!-- Boutons de modification du rythme -->
        <div class="d-flex gap-4">
          <button class="m-5" id="silence-bt">
            <span>
              <img src="/src/assets/public/silences_pics/s1.png" height="40" alt="Silence" />
              /
              <img src="/src/assets/public/silences_pics/s4.png" height="40" alt="Silence" />
              /
              <img src="/src/assets/public/silences_pics/s8.png" height="40" alt="Silence" />
              (b)
            </span>
          </button>
          <div class="rhythm-modif">
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('w')" id="whole-bt">
              <img src="/src/assets/public/notes_pics/1.png" height="50" alt="Whole" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('hd')" id="half-dotted-bt">
              <img src="/src/assets/public/notes_pics/2d.png" height="50" alt="Dotted half" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('h')" id="half-bt">
              <img src="/src/assets/public/notes_pics/2.png" height="50" alt="Half" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('qd')" id="quarter-dotted-bt">
              <img src="/src/assets/public/notes_pics/4d.png" height="50" alt="Dotted quarter" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('q')" id="quarter-bt">
              <img src="/src/assets/public/notes_pics/4.png" height="50" alt="Quarter" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('8d')" id="8th-dotted-bt">
              <img src="/src/assets/public/notes_pics/8d.png" height="50" alt="Dotted 8-th" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('8')" id="8th-bt">
              <img src="/src/assets/public/notes_pics/8.png" height="50" alt="8-th" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('16d')" id="16th-dotted-bt">
              <img src="/src/assets/public/notes_pics/16d.png" height="50" alt="Dotted 16-th" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('16')" id="16th-bt">
              <img src="/src/assets/public/notes_pics/16.png" height="50" alt="16-th" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('32d')" id="32th-dotted-bt">
              <img src="/src/assets/public/notes_pics/32d.png" height="50" alt="Dotted 32-th" />
            </button>
            <button class="rhythm-modif-bt" @click="changeLastNoteRhythm('32')" id="32th-bt">
              <img src="/src/assets/public/notes_pics/32.png" height="50" alt="32-th" />
            </button>
          </div>
        </div>
      </div>

      <!-- Options avancées -->
      <div class="flex-column" style="display: flex; justify-content: space-between; gap: 20px;">
        <div class="collections-options">
          <label for="collections">Collection dans lesquelles rechercher :</label><br />
          <select v-model="selectedCollection" id="collections" name="collections">
            <option v-for="(collection, index) in collections" :key="index" :value="collection">
              {{ collection }}
            </option>
          </select>
        </div>

        <div class="flex-column" style="display: flex; gap: 20px;">
          <h4 class="text-center">Sélectionnez le type de recherche</h4>
          <div class="flex-row" style="display: flex; gap: 40px;">
            <button @click="searchExact" id="stricte" type="button" class="btn text-white tooltip-lb" style="background-color: #7ab6e0;">Recherche exacte</button>
            <button @click="searchWithTolerance" id="modereeMelo" type="button" class="btn text-white" style="background-color: #7ab6e0;">Recherche avec tolérance<br />sur la hauteur des notes</button>
            <button @click="searchWithRhythmTolerance" id="modereeRythm" type="button" class="btn text-white" style="background-color: #7ab6e0;">Recherche avec tolérance<br />sur le rythme</button>
          </div>
        </div>

        <button @click="toggleAdvancedOptions" id="toggleButton2" class="btn btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseWidthExample" aria-expanded="false" aria-controls="collapseWidthExample">
          Options avancées
        </button>

        <div style="min-height: 120px;">
          <div class="collapse collapse-vertical" id="collapseWidthExample">
            <div class="card card-body" style="width: 300px;">
              <div class="general-options">
                <label class="tooltip-lb" id="pitch-lb">
                  <input v-model="pitchChecked" type="checkbox" />
                  Hauteur des notes
                </label><br />
                <label class="tooltip-lb" id="rhythm-lb">
                  <input v-model="rhythmChecked" type="checkbox" />
                  Rythme
                </label><br />
                <label class="tooltip-lb" id="transpose-lb">
                  <input v-model="transposeChecked" type="checkbox" />
                  Autoriser les transpositions
                </label><br />
              </div>
              <div class="fuzzy-options">
                <label class="tooltip-lb" id="pitch-dist-lb">
                  Tolérance de hauteur
                  <input v-model="pitchTolerance" type="number" min="0" step="0.5" class="nb-select" />
                </label><br />
                <label class="tooltip-lb" id="duration-dist-lb">
                  Facteur de durée
                  <input v-model="durationFactor" type="number" min="1" step="0.125" class="nb-select-large" />
                </label><br />
                <label class="tooltip-lb" id="sequencing-dist-lb">
                  Écart de durée
                  <input v-model="durationGap" type="number" min="0" step="0.125" class="nb-select-large" />
                </label><br />
                <label class="tooltip-lb" id="alpha-lb">
                  Alpha
                  <input v-model="alpha" type="number" min="0" max="100" step="5" class="nb-select" /> %
                </label>
                <hr />
                <div class="clear_buttons">
                  <button @click="searchWithAdvancedOptions" type="button" class="btn text-white send-button" style="background-color: #006485;" id="send-button">Recherche</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notifications Toast -->
      <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div v-if="toastVisible" class="toast align-items-center text-bg-white border-0" role="alert" aria-live="assertive" aria-atomic="true">
          <div class="toast-header text-white" style="background-color: #006485;">
            <strong class="me-auto">{{ toastTitle }}</strong>
            <button type="button" class="btn-close" style="background-color: white;" data-bs-dismiss="toast" aria-label="Close"></button>
          </div>
          <div class="toast-body">
            {{ toastMessage }}
          </div>
        </div>
      </div>
    </div>

    <!-- Résultats de la recherche : affichage des partitions SVG -->
    <div v-if="searchResults.length > 0" class="search-results">
      <h2>Partitions trouvées</h2>
      <div v-for="(result, index) in searchResults" :key="index" class="result-partition" :id="'partition-' + index"></div>
    </div>

    <!-- (Optionnel) Tooltip caché -->
    <div id="tooltip" class="info-note" style="display: none;"></div>
  </div>
</template>

<script>
import axios from "axios";
import Collapse from "bootstrap/js/dist/collapse";
import * as VF from "vexflow";
const { Renderer, Stave, StaveNote, Formatter, Accidental } = VF;
import { playNote, stopNote } from "../utils/audioUtils";

export default {
  data() {
    return {
      volume: 0.5,
      octave: 4,
      melody: [],
      pressedTimestamp: null,
      showHelpToast: true,
      showMicroToast: false,
      selectedCollection: "",
      collections: [],
      searchResults: [],
      pianoKeys: [
        { id: "C4", label: "DO(C)", color: "white", key: "q" },
        { id: "C#4", label: "DO#(c#)", color: "black", key: "z" },
        { id: "D4", label: "RE(D)", color: "white", key: "s" },
        { id: "D#4", label: "RE#(D#)", color: "black", key: "e" },
        { id: "E4", label: "MI(E)", color: "white", key: "d" },
        { id: "F4", label: "FA(F)", color: "white", key: "f" },
        { id: "F#4", label: "FA#(F#)", color: "black", key: "t" },
        { id: "G4", label: "SOL(G)", color: "white", key: "g" },
        { id: "G#4", label: "SOL#(G#)", color: "black", key: "y" },
        { id: "A4", label: "LA(A)", color: "white", key: "h" },
        { id: "A#4", label: "LA#(A#)", color: "black", key: "u" },
        { id: "B4", label: "SI(B)", color: "white", key: "j" },
        { id: "C5", label: "DO(C)", color: "white", key: "k" },
        { id: "C#5", label: "DO#(C#)", color: "black", key: "o" },
        { id: "D5", label: "RE(D)", color: "white", key: "l" },
        { id: "D#5", label: "RE#(D#)", color: "black", key: "p" },
        { id: "E5", label: "MI(E)", color: "white", key: "m" },
        { id: "F5", label: "FA(F)", color: "white", key: "ù" },
        { id: "F#5", label: "FA#(F#)", color: "black", key: ")" },
        { id: "G5", label: "SOL(G)", color: "white", key: "*" },
        { id: "G#5", label: "SOL#(G#)", color: "black", key: "$" },
        { id: "A5", label: "LA(A)", color: "white", key: "_" },
        { id: "A#5", label: "LA#(A#)", color: "black", key: "_" },
        { id: "B5", label: "SI(B)", color: "white", key: "_" }
      ],
      pitchChecked: true,
      rhythmChecked: true,
      transposeChecked: false,
      pitchTolerance: 0,
      durationFactor: 1,
      durationGap: 0,
      alpha: 0,
      toastVisible: false,
      toastTitle: "",
      toastMessage: "",
      keyboardConfig: "azerty",
      azertyMapping: {
        q: "C4",
        z: "C#4",
        s: "D4",
        e: "D#4",
        d: "E4",
        f: "F4",
        t: "F#4",
        g: "G4",
        y: "G#4",
        h: "A4",
        u: "A#4",
        j: "B4",
        k: "C5",
        o: "C#5",
        l: "D5",
        p: "D#5",
        m: "E5",
        "ù": "F5",
        ")": "F#5",
        "*": "G5"
      },
      qwertyMapping: {
        a: "C4",
        w: "C#4",
        s: "D4",
        e: "D#4",
        d: "E4",
        f: "F4",
        t: "F#4",
        g: "G4",
        y: "G#4",
        h: "A4",
        u: "A#4",
        j: "B4",
        k: "C5"
      },
      currentlyPlayingNotes: [],
      advancedOptionsVisible: false
    };
  },
  computed: {
    currentMapping() {
      return this.keyboardConfig === "azerty" ? this.azertyMapping : this.qwertyMapping;
    }
  },
  mounted() {
    this.initVexFlow();
    this.fetchCollections();
    document.addEventListener("keydown", this.handleGlobalKeyDown);
    document.addEventListener("keyup", this.handleGlobalKeyUp);
  },
  beforeUnmount() {
    document.removeEventListener("keydown", this.handleGlobalKeyDown);
    document.removeEventListener("keyup", this.handleGlobalKeyUp);
  },
  methods: {
    // Récupère la liste des collections depuis le backend
    async fetchCollections() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/collections", {
          headers: { Accept: "application/json" }
        });
        this.collections = response.data.authors;
      } catch (error) {
        console.error("Erreur de chargement des collections:", error);
      }
    },
    initVexFlow() {
      const div = document.getElementById("music-score");
      if (!div) {
        console.error("L'élément 'music-score' est introuvable");
        return;
      }
      this.renderer = new Renderer(div, Renderer.Backends.SVG);
      const width = 500,
        height = 200;
      this.renderer.resize(width, height);
      this.context = this.renderer.getContext();
      this.stave = new Stave(10, 40, width - 20);
      this.stave.addClef("treble").setContext(this.context).draw();
    },
    updateStaff() {
      const svg = document.querySelector("#music-score svg");
      if (svg) {
        svg.innerHTML = "";
      }
      this.stave.setContext(this.context).draw();
      if (this.melody.length > 0) {
        Formatter.FormatAndDraw(this.context, this.stave, this.melody);
      }
    },
    addNote(noteStr, duration = "q") {
      let key = noteStr.replace(/([A-G])(#?)(\d)/, (match, p1, p2, p3) => {
        return p1.toLowerCase() + (p2 ? "#" : "") + "/" + p3;
      });
      const note = new StaveNote({ keys: [key], duration: duration });
      if (noteStr.includes("#")) {
        note.addModifier(new Accidental("#"), 0);
      }
      this.melody.push(note);
      this.updateStaff();
    },
    keyDown(key) {
      if (this.currentlyPlayingNotes.length > 1) {
        console.log("Accord bloqué : trop de notes simultanées.");
        return;
      }
      this.pressedTimestamp = Date.now();
      playNote(key.id);
      this.currentlyPlayingNotes.push(key.id);
    },
    keyUp(key) {
      const elapsed = Date.now() - this.pressedTimestamp;
      this.pressedTimestamp = null;
      let duration = "q";
      if (elapsed < 150) duration = "32";
      else if (elapsed < 300) duration = "16";
      else if (elapsed < 600) duration = "8";
      else if (elapsed < 900) duration = "q";
      else if (elapsed < 1200) duration = "h";
      else duration = "w";
      stopNote(key.id);
      const index = this.currentlyPlayingNotes.indexOf(key.id);
      if (index > -1) this.currentlyPlayingNotes.splice(index, 1);
      this.addNote(key.id, duration);
    },
    changeLastNoteRhythm(newDuration) {
      if (this.melody.length === 0) {
        console.warn("Aucune note à modifier.");
        return;
      }
      const lastNote = this.melody.pop();
      const keys = lastNote.getKeys();
      let newNote;
      if (lastNote.noteType === "r") {
        newNote = new StaveNote({ keys: ["b/4"], duration: newDuration, type: "r" });
      } else {
        newNote = new StaveNote({ keys: keys, duration: newDuration, clef: "treble", auto_stem: true });
        if (keys[0].includes("#")) {
          newNote.addModifier(new Accidental("#"), 0);
        }
      }
      this.melody.push(newNote);
      this.updateStaff();
    },
    clearAll() {
      this.melody = [];
      this.updateStaff();
    },
    removeLastNote() {
      this.melody.pop();
      this.updateStaff();
    },
    playMelody() {
      console.log("Jouer la mélodie");
      // Ajoutez ici la logique pour jouer la mélodie
    },
    changeOctave(diff) {
      this.octave += diff;
      if (this.octave < 1) this.octave = 1;
      if (this.octave > 6) this.octave = 6;
    },
    searchExact() {
      this.toastVisible = true;
      this.toastTitle = "Recherche exacte";
      this.toastMessage = "Vous effectuez une recherche exacte !";
      setTimeout(() => (this.toastVisible = false), 3000);
    },
    searchWithTolerance() {
      this.toastVisible = true;
      this.toastTitle = "Recherche approchée";
      this.toastMessage = "Recherche tolérante sur la hauteur des notes.";
      setTimeout(() => (this.toastVisible = false), 3000);
    },
    searchWithRhythmTolerance() {
      this.toastVisible = true;
      this.toastTitle = "Recherche approximative";
      this.toastMessage = "Recherche tolérante sur le rythme des notes.";
      setTimeout(() => (this.toastVisible = false), 3000);
    },
    toggleAdvancedOptions() {
      this.advancedOptionsVisible = !this.advancedOptionsVisible;
      const collapseElement = document.getElementById("collapseWidthExample");
      if (!collapseElement) {
        console.error("L'élément 'collapseWidthExample' n'a pas été trouvé.");
        return;
      }
      const bsCollapse = Collapse.getInstance(collapseElement) || new Collapse(collapseElement, { toggle: false });
      this.advancedOptionsVisible ? bsCollapse.show() : bsCollapse.hide();
    },
    searchWithAdvancedOptions() {
      if (this.melody.length < 3) {
        console.error("La mélodie doit contenir au moins 3 notes pour lancer la recherche.");
        return;
      }
      const noteConditionsArray = this.melody.slice(0, 3).map((note) => {
        const key = note.getKeys()[0]; // par ex. "c/4"
        const [noteLetter, octave] = key.split("/");
        const noteClass = noteLetter.replace("#", "");
        let durValue = 8;
        if (note.duration === "16") durValue = 16;
        else if (note.duration === "32") durValue = 32;
        else if (note.duration === "w") durValue = 1;
        return { class: noteClass, octave: parseInt(octave, 10), duration: durValue };
      });
      const query = `
        MATCH (tp:TopRhythmic)-[:RHYTHMIC]->(m:Measure),
              (e0:Event)-[n0:NEXT]->(e1:Event)-[n1:NEXT]->(e2:Event),
              (e0)--(f0:Fact), (e1)--(f1:Fact), (e2)--(f2:Fact)
        WHERE tp.collection = '${this.selectedCollection}'
          AND f0.class = '${noteConditionsArray[0].class}' AND f0.octave = ${noteConditionsArray[0].octave} AND f0.dur = ${noteConditionsArray[0].duration}
          AND f1.class = '${noteConditionsArray[1].class}' AND f1.octave = ${noteConditionsArray[1].octave} AND f1.dur = ${noteConditionsArray[1].duration}
          AND f2.class = '${noteConditionsArray[2].class}' AND f2.octave = ${noteConditionsArray[2].octave} AND f2.dur = ${noteConditionsArray[2].duration}
        RETURN DISTINCT e0.source AS source, e0.start AS start
        LIMIT 10
      `.trim();
      console.log("Envoi de la requête:\n", query);
      axios
        .get("http://127.0.0.1:5000/search", {
          params: { query: query, fuzzy: true }
        })
        .then((response) => {
          console.log("Résultats de la recherche :", response.data);
          this.searchResults = response.data.results;
          this.$nextTick(() => {
            this.searchResults.forEach((result, index) => {
              this.renderPartition(index, result.source);
            });
          });
        })
        .catch((error) => {
          console.error("Erreur lors de la recherche :", error);
        });
    },

    renderPartition(index, svgUrl) {
      axios
        .get(svgUrl)
        .then((response) => {
          let svgContent = response.data;
          svgContent = this.applyGradient(svgContent);
          const container = document.getElementById("partition-" + index);
          if (container) {
            container.innerHTML = svgContent;
          }
        })
        .catch((error) => {
          console.error("Erreur lors du chargement du SVG :", error);
        });
    },
    applyGradient(svgContent) {
      // Exemple d'ajout d'un gradient linéaire.
      const gradientDef = `
        <defs>
          <linearGradient id="myGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ff0000;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#0000ff;stop-opacity:1" />
          </linearGradient>
        </defs>
      `;
      // Insère la définition du gradient juste après la balise <svg ...>
      return svgContent.replace(/(<svg[^>]*>)/, `$1${gradientDef}`);
    },
    closeToast(toastType) {
      if (toastType === "help") this.showHelpToast = false;
      else if (toastType === "micro") this.showMicroToast = false;
    },
    handleGlobalKeyDown(event) {
      const tag = event.target.tagName.toLowerCase();
      if (tag === "input" || tag === "textarea") return;
      const note = this.currentMapping[event.key];
      if (note && !event.repeat) this.keyDown({ id: note });
    },
    handleGlobalKeyUp(event) {
      const tag = event.target.tagName.toLowerCase();
      if (tag === "input" || tag === "textarea") return;
      const note = this.currentMapping[event.key];
      if (note) this.keyUp({ id: note });
    },
    toggleKeyboardConfig() {
      this.keyboardConfig = this.keyboardConfig === "azerty" ? "qwerty" : "azerty";
      console.log("Configuration du clavier :", this.keyboardConfig);
    }
  }
};
</script>

<style scoped>
.clear_buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  gap: 10px;
}
.stave_buttons {
  width: 130px;
  height: 60px;
  border-radius: 20px;
  background-color: #62aadd;
  color: #fff;
  font-size: 16px;
  text-align: center;
  border: none;
  outline: none;
  cursor: pointer;
  margin: 10px;
}
.stave_buttons:hover {
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
}
.piano-keys {
  display: flex;
}
.piano-keys .key {
  cursor: pointer;
}
.rhythm-modif button {
  width: 50px;
  height: auto;
}
.keyboard-config {
  margin-left: 20px;
}
.searchbar-box {
  background-color: white;
  color: black;
  border-bottom: 0.5px solid aqua;
}
.result-partition {
  margin: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}
</style>
