<template>
  <div style="padding-bottom:2rem">
    <div class="box new-post is-rounded">
      <a class="delete is-large" style="position:absolute; z-index:1;" v-if="hasChoosenFile" @click="deleteImage"></a>
      <img v-if="hasChoosenFile" id="blah" src="#" alt="your image">
      <div class="control">
        <input v-if="!isPost" class="input is-primary" type="text" placeholder="Title" v-model="title">
      </div>
      <textarea class="textarea post-text-field" v-model="description" placeholder="What do you want to do?"></textarea>
      <div class="control date-time" v-if="!isPost">
        <VueCtkDateTimePicker v-model="date" />
      </div>
      <div class="center-container">
        <div class="left-container">
          <div class="dropdown is-hoverable">
            <div class="dropdown-trigger">
              <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
                <span>{{eventType}}</span>
                <span class="icon is-small">
                  <i class="fas fa-angle-down" aria-hidden="true"></i>
                </span>
              </button>
            </div>
            <div class="dropdown-menu" id="dropdown-menu" role="menu">
              <div class="dropdown-content">
                <a href="#" class="dropdown-item" @click="selectEventType(0)">
                  Post
                </a>
                <a href="#" class="dropdown-item" @click="selectEventType(1)">
                  Trash pickup
                </a>
                <a class="dropdown-item" @click="selectEventType(2)"> 
                  Sale
                </a>
              </div>
            </div>
          </div>
  
          <div class="file" v-if="!hasChoosenFile && !isPost">
            <label class="file-label">
              <input class="file-input" type="file" name="resume" value="upload" @change="gotAnImage">
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-images"></i>
                </span>
                <span class="file-label">
                  Pick an image
                </span>
              </span>
            </label>
          </div>
  
          <a class="button is-link" title="Disabled button" @click="addCurrentLocationToPost" v-if="!lat && !isPost">
            <span class="icon">
              <i class="fas fa-location-arrow btn-image"/>
            </span>
            <span>Add current location</span>
  
          </a>
          <a class="button is-danger" title="Disabled button" @click="removeLocation" v-if="lat">
            <span class="icon">
              <i class="fas fa-location-arrow btn-image"/>
            </span>
            <span>Remove location</span>
  
          </a>
  
  
        </div>
  
        <a @click="createPost" class="button is-primary is-inverted is-outlined submit">Submit Post</a>
  
      </div>
      <p class="has-text-danger" v-if="feedback">{{feedback}}</p>
  
    </div>
  
  </div>
</template>

<script>
  import axios from "axios"
  import firebase from 'firebase'
  import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
  import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
  
  export default {
    name: "NewPost",
    props: {
      method: {
        type: Function
      },
    },
    components: {
      VueCtkDateTimePicker
    },
    data() {
      return {
        title: null,
        description: null,
        feedback: null,
        eventType: null,
        lat: null,
        lng: null,
        imageSrc: null,
        hasChoosenFile: null,
        eventType: "Post",
        isPost: true,
        date: new Date(),
        fileName: "https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
  
  
      }
    },
    methods: {
      selectEventType(typeNumber) {
        this.isPost = false
        if (typeNumber == 0) {
          this.isPost = true
          this.eventType = "Post"
        } else if (typeNumber == 1) {
          this.eventType = "Trash pickup"
        } else if (typeNumber == 2) {
          this.eventType = "Sale"
        }
      },
      removeLocation() {
        this.lat = null
        this.lng = null
      },
      addCurrentLocationToPost() {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            pos => {
              this.lat = pos.coords.latitude;
              this.lng = pos.coords.longitude;
  
            },
            err => {
              console.log("Getting position error")
              console.log(err.message);
            }, {
              maximumAge: 60000,
              timeout: 10000
            }
          );
        }
      },
      deleteImage() {
        this.hasChoosenFile = null
      },
      createPost() {

        if(!this.isPost && (!this.title || !this.description || !this.lat || !this.hasChoosenFile)){
          this.feedback = "You need to fill in all of the fields, current location and image to create an event!"
        }
        else if(this.isPost && !this.description){
          this.feedback = "You need to fill in all of the fields"
        }
        else{
          console.log(firebase.auth().currentUser.email)
  
          const Url = 'http://localhost:5001/post'
          // specify the object to post
  
          //randomize some input
          var min = 0;
          var max = 50;
          var randomLat = Math.random() * (+max - +min) + +min;
          var randomLng = Math.random() * (+max - +min) + +min;
          var imageReference
          if (this.hasChoosenFile) {
            imageReference = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
            this.uploadImageToFireStorage(imageReference)
          } else {
            imageReference = ""
          }

          /////////////////////////// remove for production
          var latitude = randomLat
          var longitude = randomLng
          // set the random coordinates
          if(!this.isPost){
            latitude = this.lat
            longitude = this.lng
          }
          ///////////////////////////
          const post = {
            "title": this.eventType + ": " + this.title,
            "description": this.description,
            "authorEmail": firebase.auth().currentUser.email,
            "lat": latitude,
            "lng": longitude,
            "timestamp": Date.now(),
            "imageReference": imageReference,
            "timeOfTheEvent": this.date
          }
          this.title = null
          this.hasChoosenFile = null
          this.description = null
          // make the post request
          // This is how you do it:
          axios.post(Url, post)
            .then(response => {
  
              console.log("Posting added to the database")
              this.method()
  
            })
            .catch(error => console.log(error))
  
          this.feedback = null
        }
  
      },
      gotAnImage(event) {
        console.log("Got an image! " + event.target.files[0])
        this.hasChoosenFile = event.target.files[0]
        var reader = new FileReader();
  
        reader.onload = function(e) {
          console.log("on load")
          $('#blah').attr('src', e.target.result);
          document.getElementById('blah').src = e.target.result
        }
  
        reader.readAsDataURL(event.target.files[0]);
  
      },
      uploadImageToFireStorage(firebaseReference) {
        console.log(firebaseReference)
  
        var storageRef = firebase.storage().ref('eventHeaderImages/' + firebaseReference)
        storageRef.put(this.hasChoosenFile)
      }
    }
  
  }
</script>

<style>
  .new-post {
    display: flex;
    flex-direction: column;
    background-color: green;
    padding: 5px;
  }
  
  li {
    float: left;
  }
  
  .date-time {
    display: flex;
    flex-direction: row;
    margin: 5px;
  }
  
  .submit {
    display: flex;
    align-self: flex-end;
  }
  
  .btn-image {
    margin: 10px;
    color: white;
  }
  
  .post-text-field {
    margin-bottom: 0.5rem;
    min-width: 35rem;
  }
  
  @media screen and (max-width: 600px) {
    .post-text-field {
      margin-bottom: 0.5rem;
      min-width: 10rem;
      background-color: red;
    }
  }
  
  .left-container {
    display: flex;
    flex-direction: row;
    align-self: flex-start;
  }
  
  .center-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
</style>
