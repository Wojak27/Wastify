<template>
  <div class="hello">
    <Tiles/>
  </div>
</template>

<script>
import "bulma/css/bulma.css";
import ProfileBar from "@/components/ProfileBar";
import Footer from "@/components/Footer";
import Tiles from "@/components/Tiles";
export default {
  name: "Index",
  components: {
    ProfileBar,
    Footer,
    Tiles
  },
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.hello {
  justify-content: center;
  display: inline-block;
  text-align: center;
}

.myfooter {
  bottom: 0;
  width: 100%;
  height: 2.5rem;
}
</style>
