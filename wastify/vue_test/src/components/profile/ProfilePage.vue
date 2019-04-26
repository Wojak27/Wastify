<template>
  <div class="hello">
      
      <div class="centered-content">
        
        <div class="header-div">
          <div class="profile-image">
            <img src="https://amp.businessinsider.com/images/5899ffcf6e09a897008b5c04-750-750.jpg" alt="">
          </div>
          <div class="name-text">
            <p class="is-size-3">Karol Wojtulewicz</p>  
          </div>
          
        </div>
        
      </div>
      
  </div>
</template>
<script>
import "bulma/css/bulma.css";
export default {
  name: "ProfilePage",
  data(){
    return{

    }
  }
}
</script>

<style>
.hello {
  padding-top: 5rem;
  background-color:yellow;
  padding-bottom: 2rem;
}

.centered-content{
  width: 45rem;
  margin-top: 20rem;
  height: 100rem;
  background-color: red;
  align-self: center;
}

@media screen and (max-width: 600px) {
  .centered-content{
  min-width: 20rem;
  margin-top: 10rem;
  height: 100rem;
  align-self: center;
}
}
.header-div{
  background-color: lightblue;
  height: 10rem;
  display: flex;

}
.profile-image{
  display: flex;
  flex:1;
}

.name-text{
  display: flex;
  flex:4;
}

.parallax {
  /* The image used */
  background-image: url('../../assets/trash.jpg');

  /* Full height */
  height: 100%; 

  /* Create the parallax scrolling effect */
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

</style>
