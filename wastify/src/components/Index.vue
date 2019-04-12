<template>
  <div class="hello">
    <Tiles/>
    <PostBox/>
    <Footer/>
  </div>
</template>

<script>
import "bulma/css/bulma.css";
import Post from "@/components/Post";
import ProfileBar from "@/components/ProfileBar";
import Footer from "@/components/Footer";
import Tiles from "@/components/Tiles";
import PostBox from "@/components/PostBox";
export default {
  name: "Index",
  components: {
    Post,
    ProfileBar,
    Footer,
    Tiles,
    PostBox
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
</style>
