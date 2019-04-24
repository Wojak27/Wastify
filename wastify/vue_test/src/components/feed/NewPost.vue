<template>
  <div style="padding-bottom:2rem">
    <div class="box new-post is-rounded">
      
      <textarea class="textarea" v-model="description" style="margin-bottom:0.5rem; min-width:35rem;" placeholder="What do you want to do?"></textarea>
      <ul>

        <li>
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
        </li>
        <li><i class="fas fa-images btn-image" /></li>
        <li><i class="fas fa-location-arrow btn-image"/></li>
        <li class="submit"><a @click="createPost" class="button is-primary is-inverted is-outlined">Submit Post</a></li>
        
      </ul>
      
    </div>      
  </div>
</template>

<script>
import axios from "axios"
import firebase from 'firebase'

export default {
  name: "NewPost",
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
          "authorEmail": firebase.auth().currentUser.email
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
    }
  }
}
</script>

<style>
.new-post{
  background-color: green;
  padding: 5px;
  padding-bottom: 40px;
}
li {
  float: left;
}

li .submit {
  float: right;
}

li .btn-image{
  margin: 10px;
  color: white;
}
</style>
