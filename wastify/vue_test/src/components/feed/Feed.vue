<template>
  <div class="hello">
    <div class="content">
      <div class="center-div">
        <div class="top-container">
          <!--<InfoBox class="animated" />-->
          <div id="newpost_div">
            <NewPost :method="getFreshPosts" style=" width:45rem; zIndex:1" class="animated"/>
          </div>
        </div>
        <div class="bottom-container">
          
          <div class="feed-post-container">
            
            <div v-for="post in posts" :key="post.id">
            
            <BigPostBox v-if="post.imageReference != ''" :text="post.description" :authorEmail="post.authorEmail" :user_id="user_id" :post_id="post.id" :timestamp="post.timestamp" :title="post.title" :imageReference="post.imageReference" :url="post.imageURL"  :authorFirebaseID="post.authorFirebaseID"/>
            <PostBox style="width:31rem;" class="animated swing" v-if="post.imageReference == ''"
                      :text="post.description"  :authorEmail="post.authorEmail" :timestamp="post.timestamp" :title="post.title" :user_id="user_id" :post_id="post.id" :authorFirebaseID="post.authorFirebaseID"/>
            
          </div>
          <div id="sentinel" v-if="hasMorePosts">
            <a class="button is-rounded is-loading"></a>
          </div>
          <div class="loading-container" v-if="!hasMorePosts" style="margin-bottom:5rem">
              No more posts
            </div>
          
          
          </div>
        <ProfileBar  id="profile-bar-css" :userEmail="userEmail" :postNumber="postNumber" class="animated profile-bar" />
        
        </div>     
             
      </div>
    </div>
  </div>
</template>

<script>
import "bulma/css/bulma.css";
import ProfileBar from "@/components/feed/ProfileBar";
import Footer from "@/components/Footer";
import Tiles from "@/components/Tiles";
import PostBox from "@/components/feed/PostBox";
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
      socket: null,
      hasMorePosts: true,
      counter: 0,
      user_id: firebase.auth().currentUser.uid,
      postNumber: 0
    };
  },
  methods: {
    getFreshPosts(){
      console.log("resetting")
      this.counter = 0
      this.posts = []
      this.getUserPostNumber()
      this.hasMorePosts = true
      
    },
    getPosts(){
      this.loading = true
      axios.get('http://localhost:5001/latest_posts/'+this.counter*5)
      .then(response => {
        
        if(response.data[0]){
          this.counter +=1
          response.data.forEach(element => {
          var timestamp
          if(Date.now() - element.timestamp < 3758207){
            timestamp = "Less than an hour ago"
          }else{
            timestamp = moment(element.timestamp).format('MMMM Do YYYY, h:mm:ss a')
          }
          console.log(element.imageReference)
          this.posts.push({
            id: element.id,
            description: element.description,
            authorEmail: element.authorEmail,
            authorFirebaseID: element.authorFirebaseID,
            timestamp: timestamp,
            imageReference: element.imageReference,
            title: element.title,
            imageURL: 'https://firebasestorage.googleapis.com/v0/b/geo-location-web-app.appspot.com/o/eventHeaderImages%2F'+element.imageReference+'?alt=media'
          })
          console.log(element)
        });
        if(response.data.length < 5){
          this.hasMorePosts = false
        }
        }else{
          this.hasMorePosts = false
        }
        
        this.loading = false
      })
      .catch(error => console.log(error))
      },
      getUserPostNumber(){
        const Url = 'http://localhost:5001/get_post_number/'+this.user_id

        axios.get(Url)
          .then(response => {
            
            this.postNumber = response.data
            })
          .catch(error => console.log(error))
      },
      
  },
  mounted() {
    
    // Setting up all of the intersecion observers
    var sentinel = document.querySelector('#sentinel')

    var intersectionObserver = new IntersectionObserver(entries =>{
      // if intersection ratio is 0, the sentinel is out of view
      // and we do not need to do anything
      if(entries[0].intersectionRatio <= 0){
        return;
      }
      console.log("triggered")
      this.getPosts()
    })
    intersectionObserver.observe(sentinel)

    //Profile bar follows with
    
    var newpostBoxSentinel = document.querySelector('#newpost_div')

    var intersectionObserverNewPostBox = new IntersectionObserver(entries =>{
      // When the new post div is in view,
      // let the profile bar's position be absolute
      // and fixed otherwise
      if(entries[0].intersectionRatio <= 0){
          $('#profile-bar-css').css('position', 'fixed').css('top', '3rem');
        }else{
          $('#profile-bar-css').css('position', 'absolute').css('top', 'auto');
        }
      return
    })
    intersectionObserverNewPostBox.observe(newpostBoxSentinel)
  },
  created() {
    this.getUserPostNumber()
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
  position: absolute; 
  margin-left : 32rem; 
  z-index:1;

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
