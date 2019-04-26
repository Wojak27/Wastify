<template>
  <div class="hello">
    <div class="content">
      <div class="center-div">
      <NewPost :newPost="getPosts"/>
        <div v-for="post in posts" :key="post.id">
          <PostBox :text="post.description" :authorEmail="post.authorEmail" :timestamp="post.timestamp"/>
        </div>
      <ProfileBar />
      
    </div>
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
import moment from "moment"

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
  methods: {
    getPosts(){
      axios.get('http://localhost:5001/latest_posts')
      .then(response => {
        console.log(response.data)
        console.log(response.data[0])
        response.data.forEach(element => {
          this.posts.push({
            id: element.id,
            description: element.description,
            authorEmail: element.authorEmail,
            timestamp: element.timestamp
          })
          console.log(element)
        });
      })
      .catch(error => console.log(error))
      }
  },
  created() {
    this.getPosts()
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.hello {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-self: center;
  text-align: center;
  padding-top: 5rem;
}

.myfooter {
  bottom: 0;
  width: 100%;
  height: 2.5rem;
}


.content{
  display: flex;
  flex-direction: row;
  align-self: center;
}

.profile-bar{
  display: flex;
  flex: 1;
  position: fixed;

}
.center-div{
  display: flex;
  flex-direction: column;
  align-self: center;
  flex: 2;
}



@media screen and (max-width: 600px) {
  .center-div{
  display: flex;
  flex-direction: column;
  align-self: center;
}
}
</style>
