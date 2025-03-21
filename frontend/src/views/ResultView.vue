<template>
    <div class="result-container">
      <h1 class="searchbar-title ">📜 Partition : {{ getFileName(scoreName) }}</h1>
  
      <div class="score-container">
        <!-- Affiche "Auteur" seulement si un auteur est trouvé -->
        <h2 v-if="displayedAuthor && !displayedAuthor.startsWith('Collection de')">
            🎼 Auteur indiqué : {{ displayedAuthor }}
        </h2>
        <h2 v-else-if="displayedAuthor.startsWith('Collection de')">
            📚 {{ displayedAuthor }}
        </h2>
        <hr>
        <!-- Description extraite du MEI #######  /!\v-html="formattedDescription"/!\
        Penser à sanitizer l'entrée si utilisation des données dynamiques venant d'un utilisateur ou d'une API externe -->
        <p class="description text-secondary"><span v-html="formattedDescription"></span></p>

        <!-- PRIORITÉ AU SVG STOCKÉ -->
        <div v-if="svgExists">
          <img :src="getFileUrl('svg')" alt="Partition musicale" class="score-image" />
        </div>
  
        <!-- SI PAS DE SVG, ON GÉNÈRE AVEC VEROVIO -->
        <div v-else id="notation" v-html="scoreSVG"></div>
  
        <div class="button-container">
          <button id="playMIDI" class="play-button" @click="playMIDI"><i class="fas fa-play"></i></button>
          <button id="stopMIDI" class="stop-button" @click="stopMIDI"><i class="fas fa-stop"></i></button>
          <button id="prevPage" class="prevpage-button" @click="prevPage" :disabled="currentPage === 1">Page précédente</button>
          <label>{{ currentPage }} / {{ totalPages }}</label>
          <button id="nextPage" class="nextpage-button" @click="nextPage" :disabled="currentPage === totalPages">Page suivante</button>
        </div>
      </div>
  
      <div class="right-infos">
        <h2>Fichiers associés</h2>
        <ul>
          <li><a :href="getFileUrl('mei')">Fichier MEI</a></li>
          <li><a :href="getFileUrl('mid')">Fichier MIDI</a></li>
          <li><a :href="getFileUrl('pdf')">Fichier PDF</a></li>
          <li><a :href="getFileUrl('musicxml')">Fichier MusicXML</a></li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useRoute } from "vue-router";
  import axios from "axios";
  import { computed } from "vue";

const formattedDescription = computed(() => {
    return description.value.replace(/\n/g, "<br>"); // Remplace les \n par <br>
});
  
const route = useRoute();
const author = ref(route.query.author || "");  // Collection de base
const scoreName = ref(route.query.score_name || ""); 
const scoreSVG = ref("");
const displayedAuthor = ref("");  // On ne met plus "Auteur inconnu" ici, on le calcule après
const description = ref("📜 Aucune description disponible.");
const currentPage = ref(1);
const totalPages = ref(1);
const svgExists = ref(false);
let toolkit = null;

// ✅ Vérifie si le fichier SVG existe DANS DATA
const checkSvgExists = async () => {
  try {
    const response = await axios.head(getFileUrl("svg"));
    if (response.status === 200) {
      svgExists.value = true;
      console.log("✅ SVG trouvé :", getFileUrl("svg"));
    }
  } catch (error) {
    console.log("❌ Aucun fichier SVG trouvé, on utilisera Verovio.");
  }
};

// ✅ Récupère les METADONNÉES du fichier MEI (Auteur + Description)
const fetchMeiMetadata = async () => {
  try {
    const response = await axios.get(getFileUrl("mei"));
    const meiData = response.data;

    // ✅ Parse l'XML du MEI
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(meiData, "text/xml");

    // ✅ Récupérer l'auteur du MEI
    const authorElem = xmlDoc.querySelector('pgHead > rend[halign="right"]');

    if (authorElem) {
      displayedAuthor.value = authorElem.textContent.trim();
    } else {
      displayedAuthor.value = `Collection de ${author.value}`; // 🟢 Fallback sur la collection
      console.log("⚠️ Auteur introuvable dans le MEI. Utilisation de la collection :", displayedAuthor.value);
    }

    // ✅ Récupérer la description
    const descriptionElems = xmlDoc.querySelectorAll('pgHead > rend[halign="center"], pgHead > rend[halign="right"], pgHead > rend[valign="top"]');
    // VOIR CONDITIONS D'AFFICHAGE -> pour plus ou moins de données.
    if (descriptionElems.length > 0) {
    // On transforme NodeList en tableau et on map chaque texte
    const descriptions = Array.from(descriptionElems).map(elem => elem.textContent.trim());

    console.log("📜 Descriptions extraites :", descriptions); // ✅ Log pour vérifier
    
    // Concatène avec un double saut de ligne "\n\n"
    description.value = descriptions.join("\n\n");
    } else {
        description.value = "📜 Aucune description disponible.";
    }

    console.log("✍️ Auteur affiché :", displayedAuthor.value);
    console.log("📜 Description extraite :", description.value);
  } catch (error) {
    console.error("❌ Erreur lors du chargement du fichier MEI :", error);
  }
};

  
  // ✅ Charge la partition en SVG ou MEI
  const fetchScore = async () => {
    if (svgExists.value) return; // ⚠️ Ne pas utiliser Verovio si le SVG existe !
  
    try {
      const response = await axios.get(getFileUrl("mei"));
      const meiData = response.data;
  
      toolkit = new verovio.toolkit();
      toolkit.loadData(meiData);
      totalPages.value = toolkit.getPageCount();
      scoreSVG.value = toolkit.renderToSVG(currentPage.value);
    } catch (error) {
      console.error("❌ Erreur lors du chargement de la partition avec Verovio:", error);
    }
  };
  
  // ✅ Génère les URLs propres des fichiers
  const getFileUrl = (type) => {
    return `http://127.0.0.1:5000/files/data/${author.value.replace(/\s+/g, "-")}/${type}/${getFileName(scoreName.value).replace(".mei", `.${type}`)}`;
  };
  
  // ✅ Extrait uniquement le nom du fichier sans extension
  const getFileName = (path) => {
    if (!path || typeof path !== "string") return "Partition inconnue";
    return path.split("/").pop();
  };
  
  // ✅ Gestion des pages pour Verovio
  const nextPage = () => {
    if (toolkit && currentPage.value < totalPages.value) {
      currentPage.value++;
      scoreSVG.value = toolkit.renderToSVG(currentPage.value);
    }
  };
  const prevPage = () => {
    if (toolkit && currentPage.value > 1) {
      currentPage.value--;
      scoreSVG.value = toolkit.renderToSVG(currentPage.value);
    }
  };
  
  // ✅ Charge toutes les données au montage
  onMounted(async () => {
    await checkSvgExists(); // ⚠️ Vérifie d'abord le SVG
    await fetchMeiMetadata(); // Récupère l'auteur + description
    await fetchScore(); // ✅ Charge la partition (SVG ou Verovio)
  });
  </script>
  
  <style scoped>
  .result-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin-top: 50px;
  }
  
  .score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80%;
  }
  
  .score-image {
    max-width: 100%;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .button-container {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .right-infos {
    margin-top: 20px;
    text-align: left;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  ul li {
    margin: 5px 0;
  }
  
  #notation {
    width: 100%;
    text-align: center;
  }
  </style>
  