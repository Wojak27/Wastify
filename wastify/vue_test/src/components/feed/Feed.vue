<template>

  <div class="hello">
    <a class="button is-primary" title="Disabled button" disabled style="position:fixed; ">Disabled</a>
    <div class="content">
      <div class="center-div">
        <div class="top-container">

          <InfoBox class="animated bounceInDown" />
          <NewPost :method="getPosts" style=" width:45rem; zIndex:1" class="animated bounceInDown"/>
        </div>
        <div class="bottom-container" style="background-color:red">
          
          <div class="feed-post-container">
            <div class="loading-container">
              <p class="is-size-7 has-text-grey" v-if="loading" >Loading new posts...</p>
            </div>
            <div v-for="post in posts" :key="post.id">
            
            <BigPostBox v-if="post.imageReference != ''" />
            <PostBox :text="post.description"  :authorEmail="post.authorEmail" :timestamp="post.timestamp" style="width:31rem;" class="animated swing"/>
          </div>
          
          <BigPostBox />
          </div>
        <ProfileBar :userEmail="userEmail" style="position:fixed; margin-left : 32rem; width:45rem; zIndex:1" class="animated bounceInDown"/>
        
        </div>     
             
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
import MyPostBox from "@/components/feed/MyPostBox";
import NewPost from "@/components/feed/NewPost";
import BigPostBox from "@/components/feed/BigPostBox";
import InfoBox from "@/components/feed/InfoBox";
import axios from 'axios'
import moment from "moment"
import firebase from "firebase"
import animate from "animate.css"

export default {
  name: "Feed",
  components: {
    ProfileBar,
    Footer,
    Tiles,
    PostBox,
    NewPost,
    BigPostBox,
    InfoBox
  },
  data() {
    return {
      msg: "kjdsbnfkjsdbakfjbsdakjfbflsdaijbflkjsadbfkjsabdfklhbsadlkfhbdsalkhbfliabdhsflksdhabdsfklb dbs kjbdsakj bf ksdjb kbdsfk jbsdakjbf sdkjb kjdsba klbfdslib ilsbd ilbfsdali fbjsdil",
      posts: [],
      username: null,
      fake_description: "This is a fake description with a fake meaning created by Karol Wojtulewicz for test purpouses of his newly created, soon to be a big hit website to unite all of the people in cleaning purpouses",
      fake_email: "karol@wojtulewicz.com",
      fake_timestamp: "234567654321324",
      userEmail: firebase.auth().currentUser.email,
      loading: false,
    };
  },
  methods: {
    getPosts(){
      this.loading = true
      axios.get('http://localhost:5001/latest_posts')
      .then(response => {
        console.log(response.data)
        console.log(response.data[0])
        this.posts = []
        response.data.forEach(element => {
          var timestamp
          console.log("Timestamp")
          console.log(Date.now() - element.timestamp)
          console.log(element.timestamp)
          console.log(Date.now())
          if(Date.now() - element.timestamp < 3758207){
            timestamp = "Less than an your ago"
          }else{
            timestamp = moment(element.timestamp).format('MMMM Do YYYY, h:mm:ss a')
          }

          this.posts.push({
            id: element.id,
            description: element.description,
            authorEmail: element.authorEmail,
            timestamp: timestamp,
            imageReference: element.imageReference
          })
          console.log(element)
        });
        this.loading = false
      })
      .catch(error => console.log(error))
      },
  },
  created() {
    this.getPosts()
    
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.loading-container{
  height: 1rem;
}
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


.bottom-container{
  display: flex;
  flex-direction: row;
}
.feed-post-container{
  display: flex;
  flex-direction: column;
  padding-right: 0.5rem;
}
.center-div{
  display: flex;
  flex-direction: column;
  align-self: center;
  max-width: 45rem;
}



@media screen and (max-width: 600px) {
  .center-div{
  display: flex;
  flex-direction: column;
  align-self: center;
}
}
</style>
