<template>
  <div id="app">
    <Navbar/>
    <router-view/>
    <!---<Footer v-if="isFooterOn"/>-->
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default {
  name: "App",
  data(){
    return{
      isFooterOn: true,
    }
  },
  components: {
    Navbar,
    Footer
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: 100%;
  bottom: 0px;
}

.myfooter {
  top: auto;
  bottom: 0px;
}
</style>
