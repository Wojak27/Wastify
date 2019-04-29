<template>
  <div class="profileDiv">
    <div class="boxProfile">
      <div class="topContainerProfile">
        <img src="../assets/trash.jpg" alt class="topImageProfile">
      </div>

      <div class="bottomContainerProfile">
        <h3>{{username}}</h3>
        <p>I like trash</p>
        <p>Tell me about your ambitions with trash!</p>
      </div>
      <div class="imageDivProfile">
        <img src="../assets/profile_picture.jpg" alt class>
      </div>
    </div>
  </div>
</template>

<script>
import firebase from 'firebase'
import "bulma/css/bulma.css";
export default {
  name: "ProfileBar",
  //props:['username'],
  data() {
    return {
      username: "Username"
    };
  },
  created() {
    //username = firebase.auth().currentUser.displayName
  },
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
  border-color: white;
  border-width: 20px;
  margin: 0 auto;
  overflow: hidden;
  align-content: center;
  position: relative;
  bottom: 500px;
}

.imageDivProfile img {
  width: 200px;
  height: 110px;
  margin: -10px 0 0 -50px;
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
