<template>
  <div id="app">
    <HeaderComponent />
    <div class="main-content">
      <p></p>
      <PaginatedResults />
      <router-view></router-view> <!-- Contenu de la page -->
    </div>
    <FooterComponent />
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    // Calcule la hauteur du navbar
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    // Applique dynamiquement un padding-top au contenu pour qu'il ne soit pas masqué sous le navbar
    document.querySelector('.main-content').style.top = `${navbarHeight}px`;
  },
  
  
};
</script>

<style>

body {
  padding: 0;
  margin: 0;
  overflow-x: hidden;
  padding-top: 0; /* Ajuste en fonction de la hauteur de la navbar */
}
nav {
  background-color: #006485;

}
.container-main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.searchbar-box {
  margin-top: 80px;
  width: 100% !important;
  justify-content: center;
  align-items: center;
  display: flex;
}
.main-content {
  display: block;
}

</style>