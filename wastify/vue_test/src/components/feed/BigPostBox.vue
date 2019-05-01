<template>
  <div class="box is-paddingless is-rounded" style="overflow:hidden">
      <div class="img-container is-paddingless">
        <img src="../../assets/trash.jpg" class="img-background" alt style="object-fit: cover">
      </div>
      <div class="header-container">
        <div class="left-div">
            Alina Kovalska<br/>
            email@email.com
        </div>
        <div class="imageDivProfileSmall">
        <img src="../../assets/profile_picture.jpg" alt class class="img-background" style="object-fit: cover;">
      </div>
      <div class="right-div">
          <i class="fas fa-location-arrow"></i>
          <i class="fas fa-leaf"></i>
          <a href="#" @click="messageUser">
            <i class="fas fa-reply" aria-hidden="true" ></i>
          </a>
          
        </div>
      </div>
      

      <div class="bottomContainer">

          <h3>This is the new post box</h3>
          <p>This is my awesome description of the problem. Right now there are no problems because the website is not done yet</p>

      </div>
      

  </div>
</template>

<script>
import "bulma/css/bulma.css";
export default {
  name: "Post",
  props:["authorEmail"],
  data() {
    return {};
  },
  methods: {
    
    messageUser(){
      this.$router.push({ name: "Messenger", params: { recipient: this.authorEmail } });
    }
  },
};
</script>

<style>
.right-div{
  /* background-color:red; */
  flex: 1;
}
.left-div{
  /* background-color:blue; */
  display: flex;
  margin-left: 1rem; 
  flex: 1;
}
.img-background{
  height: 100%;
  width: 100%;
  overflow: hidden;
  
}
.img-container{
  max-height: 12rem;
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
  height: 4rem;

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
