<template>
  <div class="hello">
    <Post/>
  </div>
</template>

<script>
import Post from "@/components/Post";
export default {
  name: "Index",
  components: {
    Post
  },
  data() {
    return {
      msg: "Welcome to Your Vue.js App"
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello {
  align-content: center;
}
</style>
