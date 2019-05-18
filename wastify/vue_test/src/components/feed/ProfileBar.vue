<template>
  <div class="profileDiv">
    <div class="boxProfile" >
      <div class="topContainerProfile">
        <img src="https://images.unsplash.com/photo-1528920304568-7aa06b3dda8b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80" alt class="topImageProfile" style="object-fit: cover;">
      </div>

      <div class="bottomContainerProfile" >
        <a class="button is-white" @click="goToUserProfile">{{userEmail}}</a>
        <p>{{motto}}</p>
        <h2 class="is-size-5">You have written: {{postNumber}} posts</h2>
      </div>
      <div class="imageDivProfile">
        <img src="../../assets/profile_picture.jpg" alt class style="object-fit: cover;">
      </div>
      
    </div>
  </div>
</template>

<script>
import firebase from 'firebase'
import "bulma/css/bulma.css";
import axios from "axios";

export default {
  name: "ProfileBar",
  props:['userEmail', 'postNumber'],
  data() {
    return {
      motto: "I like trash, tell me about your ambitions with trash!",
      user_id: firebase.auth().currentUser.uid,
    };
  },
  methods: {
    goToUserProfile(){
      this.$router.push({ name: "ProfilePage", params: { authorEmail: this.userEmail } });
    }
  }
};
</script>

<style scoped>
.profileDiv {
  top: 2 rem;
}
.boxProfile {
  width: 13rem;
  height: 600px;
  margin: 0px 0px 0px 0;
  background-color: rgb(219, 255, 236);
  border-radius: 10px;
  border-style: solid;
  border-width: 1px;
  border-color: #53bc88;
  overflow: hidden;
  position: relative;
}
.imageDivProfile {
  border-radius: 50%;
  height: 100px;
  width: 100px;
  border-color: lightcyan;
  border-width: 2px;
  border-style: solid;
  margin: 0 auto;
  overflow: hidden;
  align-content: center;
  position: relative;
  bottom: 500px;
}

.imageDivProfile img {
  width: 200px;
  height: 110px;
  margin: 0px 0 0 0px;
  border-width: 5px;
}
.bottomContainerProfile {
  height: 400px;
  padding-top: 20px;
  width: inherit;
  background-color: white;
  position: relative;
  bottom: 20px;
}
.topContainerProfile {
  position: relative;
  background-color: red;
  height: 200px;
  top: 0px;
  border-style: solid;
  border-color: green;
}
.topContainerProfile img {
  -webkit-filter: blur(1px); /* Safari 6.0 - 9.0 */
  filter: blur(1px);
  -webkit-filter: brightness(80%);
  height: 100%;
  width: 100%;
}

.rightBottomContainerProfile h3 {
  padding-left: 20px;
  color: black;
}
</style>
