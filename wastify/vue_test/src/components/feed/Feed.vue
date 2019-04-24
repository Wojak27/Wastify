<template>
  <div class="hello">
    <NewPost/>
    <div v-for="post in posts" :key="post.id">
      <PostBox :text="post.description" :authorEmail="post.authorEmail"/>
    </div>
    
  </div>
</template>

<script>
import "bulma/css/bulma.css";
import ProfileBar from "@/components/ProfileBar";
import Footer from "@/components/Footer";
import Tiles from "@/components/Tiles";
import PostBox from "@/components/feed/PostBox";
import NewPost from "@/components/feed/NewPost";
import axios from 'axios'
export default {
  name: "Feed",
  components: {
    ProfileBar,
    Footer,
    Tiles,
    PostBox,
    NewPost
  },
  data() {
    return {
      msg: "kjdsbnfkjsdbakfjbsdakjfbflsdaijbflkjsadbfkjsabdfklhbsadlkfhbdsalkhbfliabdhsflksdhabdsfklb dbs kjbdsakj bf ksdjb kbdsfk jbsdakjbf sdkjb kjdsba klbfdslib ilsbd ilbfsdali fbjsdil",
      posts: []
    };
  },
  created() {
    console.log("Hello")

    axios.get('http://localhost:5001/post')
    .then(response => {
      console.log(response.data)
      console.log(response.data[0])
      response.data.forEach(element => {
        this.posts.push({
          id: element.id,
          description: element.description,
          authorEmail: element.authorEmail
        })
        console.log(element)
      });
    })
    .catch(error => console.log(error))
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.hello {
  justify-content: center;
  display: inline-block;
  text-align: center;
  padding-top: 5rem;
  max-width: 45rem;
}

.myfooter {
  bottom: 0;
  width: 100%;
  height: 2.5rem;
}
</style>
