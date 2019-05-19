<template>
  <div class="box is-paddingless" style="overflow:hidden; max-width:31rem; margin-bottom: 2rem;">
  
    <div class="img-container is-paddingless" @click="showOnMap">
      <figure><img :src="url" class="img-background" id="postImageContainer" alt style="object-fit: cover"></figure>
  
    </div>
    <div class="header-container">
      <div class="left-div">
        <a href="#" @click="goToUserProfile"><p class="is-size-7">{{authorEmail}}</p></a>
        <p class="is-size-7">{{timestamp}}</p>
  
      </div>
      <div class="imageDivProfileSmall">
        <img :src="this.profileImageUrl" alt class class="img-background" style="object-fit: cover;">
      </div>
      <div class="right-div">
  
        <a href="#" @click="messageUser" class="button is-fullwidth is-info is-rounded" v-if="!this.isSameUser">
          <i class="fas fa-reply" aria-hidden="true" style="margin-right:10px"></i> Message
        </a>
        <a class="button is-fullwidth is-rounded" @click="likePost" :id="this.post_id">
          <i class="fas fa-leaf" style="margin-right:10px;"></i> Eco {{likes}}
        </a>
  
      </div>
    </div>
  
  
    <div class="bottomContainer">
      <a href="#" @click="showOnMap">
        <h3 v-if="title">{{title}}</h3>
      </a>
  
      <p>{{text}}</p>
      <span class="tag is-link is-normal is-rounded"><i class="fas fa-comment-dots" style="margin-right:0.5rem;"></i>{{commentsNumber}} Comments</span>
    </div>
  
  
  </div>
</template>

<script>
  import "bulma/css/bulma.css";
  import firebase from "firebase";
  import axios from "axios";
  
  export default {
    name: "BigPostBox",
    props: ["authorEmail", "timestamp", "text", "title", "authorName", "location", "imageReference", "authorFirebaseID", "user_id", "post_id"],
    data() {
      return {
        url: "../../assets/trash.jpg",
        likes: 0,
        isSameUser: false,
        commentsNumber: 0,
        profileImageUrl: null,
      };
    },
    methods: {
      likePost() {
        const Url = 'http://localhost:5001/like_post'
  
        const like = {
          "post_id": this.post_id,
          "user_id": this.user_id
        }
        axios.post(Url, like)
          .then(response => {
            this.likes = response.data
            console.log("Like added to the database")
            $('#' + this.post_id).addClass("heartBeat").addClass("is-success")
          })
          .catch(error => console.log(error))
      },
      checkIfLiked() {
        const Url = 'http://localhost:5001/has_liked'
  
        const content = {
          "firebase_id": this.user_id,
          "post_id": this.post_id,
        }
        axios.post(Url, content)
          .then(response => {
            if (response.data === "True") {
              $('#' + this.post_id).addClass("is-success")
            }
          })
          .catch(error => console.log(error))
      },
      downloadUserInfo(){
        
        const url = 'http://localhost:5001/user/id/'+this.authorFirebaseID
        axios.get(url).then(response => {
          this.profileImageUrl = response.data.profileImageRef
        }).catch(error => console.log(error))
      },
      getLikes() {
        const Url = 'http://localhost:5001/get_likes/' + this.post_id
  
        axios.get(Url)
          .then(response => {
  
            this.likes = response.data
          })
          .catch(error => console.log(error))
      },
      checkIfSameUser() {
        this.isSameUser = (this.authorEmail == firebase.auth().currentUser.email)
  
      },
      messageUser() {
        this.$router.push({
          name: "Messenger",
          params: {
            recipientEmail: this.authorEmail
          }
        });
      },
      showOnMap() {
        this.$router.push({
          name: "Map",
          params: {
            selectedPostID: this.post_id
          }
        });
      },
  
      goToUserProfile() {
        this.$router.push({
          name: "ProfilePage",
          params: {
            authorEmail: this.authorEmail
          }
        });
      },
      getCommentsNum() {
        const Url = 'http://localhost:5001/get_comments_num/' + this.post_id
  
        axios.get(Url)
          .then(response => {
  
            this.commentsNumber = response.data
          })
          .catch(error => console.log(error))
      },
      getImageFromFirebase() {
  
        this.url = 'https://firebasestorage.googleapis.com/v0/b/geo-location-web-app.appspot.com/o/eventHeaderImages%2F' + this.imageReference + '?alt=media'
        //document.getElementById('postImageContainer').src=url
  
  
  
      }
    },
    mounted() {
      this.getImageFromFirebase()
      this.getLikes()
      this.checkIfLiked()
      this.checkIfSameUser()
      this.getCommentsNum()
      this.downloadUserInfo()
    },
  };
</script>

<style>
  .right-div {
    /* background-color:red; */
    flex: 1;
    flex-direction: column;
    padding: 1rem;
  }
  
  .left-div {
    /* background-color:blue; */
    display: flex;
    padding: 1rem;
    flex-direction: column;
    flex: 1;
  }
  
  a {
    color: #000000;
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
  
  .img-background {
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  
  .img-container {
    overflow: hidden;
    flex: 1;
    min-height: 10rem;
    cursor: pointer;
    background-image: url("https://media3.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif");
    background-repeat: no-repeat;
    background-position: center;
  }
  
  .bottomContainer {
    position: relative;
    bottom: 0rem;
    padding-bottom: 1rem;
    padding-right: 1rem;
    padding-left: 1rem;
  }
  
  .post {
    margin-bottom: 10rem;
  }
  
  .header-container {
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
