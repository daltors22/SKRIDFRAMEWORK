import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Gestion des routes
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CDN import
import HeaderComponent from './components/HeaderComponent.vue';
import FooterComponent from './components/FooterComponent.vue';
import '/src/utils/audioUtils.js';
import '/src/assets/styles/semantic.min.css';
import '/src/assets/styles/search_interface_style.css';
import '/src/assets/scripts/paginated_results.js';
import '/src/assets/scripts/preview_scores.js';
import '/src/assets/scripts/vexflow-core.js';


const app = createApp(App);
app.use(router);
app.component('HeaderComponent', HeaderComponent);
app.component('FooterComponent', FooterComponent);
app.mount('#app');