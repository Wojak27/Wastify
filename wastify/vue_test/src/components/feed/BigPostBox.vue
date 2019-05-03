<template>
  <div class="box is-paddingless" style="overflow:hidden; max-width:31rem; margin-bottom: 2rem;">
    
      <div class="img-container is-paddingless">
        <figure><img src="../../assets/trash.jpg" class="img-background" alt style="object-fit: cover"></figure>
        <span>Hover</span>
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
          <i class="fas fa-location-arrow"></i>
          <i class="fas fa-leaf"></i>
          <a href="#" @click="messageUser">
            <i class="fas fa-reply" aria-hidden="true" ></i>
          </a>
          
        </div>
      </div>
      

      <div class="bottomContainer">

          <h3>This is the new post box</h3>
          <p>{{text}}</p>

      </div>
      

  </div>
</template>

<script>
import "bulma/css/bulma.css";
export default {
  name: "Post",
  props:["authorEmail", "text", "title", "likes", "authorName", "location", "imageReference"],
  data() {
    return {};
  },
  methods: {
    
    messageUser(){
      this.$router.push({ name: "Messenger", params: { recipient: this.authorEmail } });
    },
    getImageFromFirebase(){
      console.log("ImageReference: "+ this.imageReference)
    }
  },
  created() {
    this.getImageFromFirebase()
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
