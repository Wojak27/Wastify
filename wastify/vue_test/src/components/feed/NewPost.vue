<template>
  <div style="padding-bottom:2rem">
    <div class="box new-post is-rounded">
      
      <textarea class="textarea post-text-field" v-model="description" placeholder="What do you want to do?"></textarea>
      
      <div class="center-container">
        <div class="left-container">
          <div class="dropdown is-hoverable">
          <div class="dropdown-trigger">
            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
              <span>Event type</span>
              <span class="icon is-small">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a href="#" class="dropdown-item" @click="selectEventType(0)">
                Trash pickup
              </a>
              <a class="dropdown-item" @click="selectEventType(1)"> 
                Sale
              </a>
            </div>
          </div>
        </div>
        <i class="fas fa-images btn-image" />
        <i class="fas fa-location-arrow btn-image"/>
        </div>

        <a @click="createPost" class="button is-primary is-inverted is-outlined submit">Submit Post</a>
        
      </div>
      <div class="create-post-button">
        
      </div>
          
        
        </div>
      
    </div>      
  </div>
</template>

<script>
import axios from "axios"
import firebase from 'firebase'

export default {
  name: "NewPost",
  props: ['newPost'],
  data(){
    return{
      description: null,
      feedback: null,
      eventType: null,
      location: null,
      imageSrc: null

    }
  },
  methods:{
    selectEventType(typeNumber){

    },
    createPost(){
      if(this.description){
        console.log("New Post1!")

        // 'http://localhost:5001/product'
        console.log(firebase.auth().currentUser.email)

        const Url = 'http://localhost:5001/post'
        // specify the object to post
        const post = {
          "description": this.description,
          "authorEmail": firebase.auth().currentUser.email,
          "lat": 0,
          "lng":0,
          "timestamp": Date.now()
        }

        // make the post request
        // This is how you do it:
        axios.post(Url,post)
        .then(response => {
          this.description = null
          //console.log(response)
          })
        .catch(error => console.log(error))

        if(feedback){
          feedback = null
        }
      }else{
        console.log("New Post!")
        this.feedback = "You need to fill in all of the fields"
      }
      this.newPost()
    }
  }
}
</script>

<style>
.new-post{
  display: flex;
  flex-direction: column;
  background-color: green;
  padding: 5px;
}
li {
  float: left;
}

.submit {
  display: flex;
  align-self: flex-end;
}

.btn-image{
  margin: 10px;
  color: white;
}

.post-text-field{
  margin-bottom:0.5rem; 
  min-width:35rem;
}
@media screen and (max-width: 600px) {
  .post-text-field{
  margin-bottom:0.5rem; 
  min-width: 10rem;
  background-color: red;
  }
}
.create-post-button{
  display: flex;
  align-self: flex-end;
}
.left-container{
  display: flex;
  flex-direction: row;
  align-self: flex-start;
}

.center-container{
  display: flex;
  flex-direction: row;
  justify-content:space-between;
}
</style>
