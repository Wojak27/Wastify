<template>
  <div class="box" style="margin-bottom:2rem">
  <article class="media">
    <div class="imageDiv media-left imageDivProfileNoMargin" style="background-color:red">
        <img :src="this.profileImageUrl" alt class="img-background" style="object-fit: cover; height.100%; width:100%;">
      </div>
    <div class="media-content">
      <div class="content">
        <p>
          <a class="button is-white" @click="goToUserProfile"><strong>{{authorEmail}}</strong></a>
          <br/>
          <small>{{timestamp}}</small>
          <br>
          {{text}}
        </p>
      </div>
      <nav class="level is-mobile">
        <div class="level-left">
          <a v-if="!this.isSameUser" class="button is-rounded is-info level-item" aria-label="reply" @click="messageUser">
            <span class="icon is-small">
              <i class="fas fa-reply" aria-hidden="true"></i>
            </span>
          </a>
          <a class="button level-item is-rounded" aria-label="like" @click="likePost" :id="this.post_id">
              <i class="fas fa-leaf" style="margin-right:10px"></i>{{this.likes}}
          </a>
        </div>
      </nav>
    </div>
  </article>
</div>
</template>

<script>
import "bulma/css/bulma.css";
import animate from "animate.css"
import axios from "axios"
import firebase from 'firebase'

export default {
  name: "PostBox",
  props: ['text', 'authorEmail', 'timestamp', 'title', 'user_id', 'post_id', 'authorFirebaseID'],
  data(){
    return{
      likes:0,
      isSameUser: false,
      profileImageUrl: null,
    }
  },
  methods: {
    likePost(){
      const Url = 'http://localhost:5001/like_post'

      const like = {
          "post_id": this.post_id,
          "user_id": this.user_id
        }
      axios.post(Url, like)
        .then(response => {
          this.likes = response.data
          console.log("Like added to the database")
          $('#'+this.post_id).addClass("heartBeat").addClass(" is-success")
          })
        .catch(error => console.log(error))
    },
    goToUserProfile(){
      this.$router.push({ name: "ProfilePage", params: { authorEmail: this.authorEmail } });
    },

    checkIfSameUser(){
      this.isSameUser = (this.authorEmail == firebase.auth().currentUser.email)

    },
    messageUser(){
      this.$router.push({ name: "Messenger", params: { recipientEmail: this.authorEmail } });
    },
    getLikes(){
      const Url = 'http://localhost:5001/get_likes/'+this.post_id

      axios.get(Url)
        .then(response => {
          
          this.likes = response.data
          })
        .catch(error => console.log(error))
    },
  downloadUserInfo(){
        
        const url = 'http://localhost:5001/user/id/'+this.authorFirebaseID
        axios.get(url).then(response => {
          this.profileImageUrl = response.data.profileImageRef
        }).catch(error => console.log(error))
      },
  checkIfLiked(){
    const Url = 'http://localhost:5001/has_liked'

      const content = {
        "firebase_id": this.user_id,
        "post_id": this.post_id,
      }
      axios.post(Url, content)
        .then(response => {
          if(response.data === "True"){
            $('#'+this.post_id).addClass("is-success")
          }
          })
        .catch(error => console.log(error))
  }
  },

  created() {
    this.getLikes()
    this.checkIfLiked()
    this.checkIfSameUser()
    this.downloadUserInfo()
  },
}
</script>

<style>
.imageDivProfileNoMargin {
  border-radius: 50%;
  height: 100px;
  width: 100px;
  border-color: darkblue;
  border-width: 2px;
  margin: 0 auto;
  margin-right: 2rem;
  overflow: hidden;
  align-content: center;
  background-color: red;
  position: relative;
  border-style: solid;
}
.imageDiv {
  border-radius: 50%;
  height: 100px;
  width: 100px;
  border-color: darkblue;
  border-width: 2px;
  overflow: hidden;

  position: relative;
}

.imageDiv img {
  width: 200px;
  height: 110px;
  margin: 0px 0 0 0px;
  border-width: 5px;
}
</style>
