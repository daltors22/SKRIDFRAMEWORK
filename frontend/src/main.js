import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Gestion des routes
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CDN import
import HeaderComponent from './components/HeaderComponent.vue';
import FooterComponent from './components/FooterComponent.vue';

const app = createApp(App);
app.use(router);
app.component('HeaderComponent', HeaderComponent);
app.component('FooterComponent', FooterComponent);
app.mount('#app');