<template>
  <div class="box" style="margin-bottom:2rem">
  <article class="media">
    <div class="imageDiv media-left imageDivProfileNoMargin" style="background-color:red">
        <img src="../../assets/profile_picture.jpg" alt class="img-background" style="
  object-fit: cover; height.100%; width:100%;">
      </div>
    <div class="media-content">
      <div class="content">
        <p>
          <a class="button is-white" @click="goToUserProfile"><strong>{{authorEmail}}</strong></a>
          <br/>
          <small>{{timestamp}}</small>
          <br>
          <strong v-if="title">{{title}}</strong>
          <br>
          
          {{text}}
        </p>
      </div>
      <nav class="level is-mobile">
        <div class="level-left">
          <a class="level-item" aria-label="reply" @click="messageUser">
            <span class="icon is-small">
              <i class="fas fa-reply" aria-hidden="true"></i>
            </span>
          </a>
          <a class="level-item" aria-label="like">
            <span class="icon is-small">
              <i class="fas fa-heart" aria-hidden="true"></i>
            </span>
          </a>
        </div>
      </nav>
    </div>
  </article>
</div>
</template>

<script>
import "bulma/css/bulma.css";

export default {
  name: "PostBox",
  props: ['text', 'authorEmail', 'timestamp', 'title'],
  data(){
    return{

    }
  },
  methods: {
    goToUserProfile(){
      this.$router.push({ name: "ProfilePage", params: { authorEmail: this.authorEmail } });
    },
    messageUser(){
      this.$router.push({ name: "Messenger", params: { recipient: this.authorEmail } });
    }
  },
  created() {
    console.log(this.authorEmail)
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
