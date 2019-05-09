<template>
  <div class="box is-paddingless" style="overflow:hidden; max-width:31rem; margin-bottom: 2rem;">
    
      <div class="img-container is-paddingless">
        <figure><img :src="url" class="img-background" id="postImageContainer" alt style="object-fit: cover"></figure>

      </div>
      <div class="header-container">
        <div class="left-div">
            Alina Kovalska<br/>
            {{authorEmail}}
            
        </div>
        <div class="imageDivProfileSmall">
        <img src="../../assets/profile_picture.jpg" alt class class="img-background" style="object-fit: cover;">
      </div>
      <div class="right-div">
          
          <a href="#" @click="messageUser" class="button is-info is-fullwidth">
            <i class="fas fa-reply" aria-hidden="true" style="margin-right:10px"></i>
            Chat
          </a>
          <a class="button is-primary is-fullwidth" @click="likePost">
            <i class="fas fa-leaf" style="margin-right:10px"></i> Eco {{likes}}
          </a>
        </div>
      </div>
      

      <div class="bottomContainer">

          <h3 v-if="title">{{title}}</h3>
          <p>{{text}}</p>

      </div>
      

  </div>
</template>

<script>
import "bulma/css/bulma.css";
import firebase from "firebase";
import axios from "axios";

export default {
  name: "Post",
  props:["authorEmail", "text", "title", "authorName", "location", "imageReference", "user_id", "post_id"],
  data() {
    return {
      url: "../../assets/trash.jpg",
      likes: null
    };
  },
  methods: {
    likePost(){
      console.log("Post liked: "+ this.post_id + " username: "+this.user_id)
      const Url = 'http://localhost:5001/like_post'

      const like = {
          "post_id": this.post_id,
          "user_id": this.user_id
        }
      axios.post(Url, like)
        .then(response => {
          this.likes = response.data
          console.log("Like added to the database")
          
          })
        .catch(error => console.log(error))
    },
    getLikes(){
      const Url = 'http://localhost:5001/get_likes/'+this.post_id

      axios.get(Url)
        .then(response => {
          
          console.log("Got likes")
          console.log(response.data)
          this.likes = response.data
          })
        .catch(error => console.log(error))
    },
    messageUser(){
      this.$router.push({ name: "Messenger", params: { recipient: this.authorEmail } });
    },
    getImageFromFirebase(){
      console.log("ImageReference: "+ this.imageReference)

      this.url = 'https://firebasestorage.googleapis.com/v0/b/geo-location-web-app.appspot.com/o/eventHeaderImages%2F'+this.imageReference+'?alt=media'
      //document.getElementById('postImageContainer').src=url
    

      
    }
  },
  mounted() {
    this.getImageFromFirebase()
    this.getLikes()
  },
};
</script>

<style>
.right-div{
  /* background-color:red; */
  flex: 1;
  flex-direction:column;
}
.left-div{
  /* background-color:blue; */
  display: flex;
  margin-left: 1rem; 
  flex: 1;
}

figure img {
	-webkit-transform: scale(1.2);
	transform: scale(1.2);
	-webkit-transition: .3s ease-in-out;
	transition: .3s ease-in-out;
}

figure:hover img {
	-webkit-transform: scale(1.5);
	transform: scale(1.5);
  
}

figure:hover+span {
	bottom: 0px;
	opacity: 1;
}
.img-background{
  height: 100%;
  width: 100%;
  overflow: hidden;
  
}
.img-container{
  overflow: hidden;
  flex: 1;
  
}

.bottomContainer{
  position: relative;
  bottom: 0rem;
  padding-bottom: 1rem;
  padding-right: 1rem;
  padding-left: 1rem;
}

.post{
  margin-bottom: 10rem;
}
.header-container{
  display: flex;

}

.imageDivProfileSmall {
  border-radius: 50%;
  height: 100px;
  width: 100px;
  border-color: darkblue;
  border-width: 2px;
  margin: 0 auto;
  overflow: hidden;
  align-content: center;
  background-color: red;
  position: relative;
  bottom: 4rem;
  border-style: solid;
}

</style>
