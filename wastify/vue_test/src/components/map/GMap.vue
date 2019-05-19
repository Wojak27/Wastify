<template>
  <div class="hello2">
    <div class="box my_map_container animated bounceInUp">
      <h3 class="is-size-3 has-text-white">Explore events near you</h3>
      <div class="google-map is-marginless" id="map">
      </div>
      <div class="post-area box" v-if="description">
  
        <h1 class="is-size-3" v-if="title">{{title}}</h1>
        <div class="image-container-gmap">
          <img :src="this.imageUrl" id="postImageContainer" v-if="this.imageReference" @error="handleError">
        </div>
        
        <br>
        <div class="under-image-container">
          <div class="header-container">
            <div class="left-div">
              <p class="is-size-7">{{authorEmail}}</p>
              <p class="is-size-7">{{timestamp}}</p>
  
            </div>
            <div class="imageDivProfileSmall">
              <img :src="profileImageUrl" alt class class="img-background" style="object-fit: cover;">
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
  
          <p>{{description}}</p>
        </div>
  
        <br>
        <hr>
        <p class="is-size-5"><strong>Comments:</strong></p>
  
        <div class="comments-div" v-for="(comment, index) in comments" :key="index">
          <CommentBox :comment="comment" />
  
          <hr>
        </div>
        <NewCommentBox :method="getFreshComments" :postID='post_id' v-if="post_id" />
      </div>
  
    </div>
  
  </div>
</template>

<script>
  import firebase from "firebase";
  import "bulma/css/bulma.css";
  import db from "@/firebase/init";
  import axios from "axios";
  import moment from "moment"
  import NewCommentBox from "@/components/map/NewCommentBox"
  import CommentBox from "@/components/map/CommentBox"
  
  export default {
    name: "GMap",
    components: {
      NewCommentBox,
      CommentBox
    },
    props: ['selectedPostID'],
    data() {
      return {
        lat: 53,
        lng: -2,
        title: null,
        description: null,
        imageReference: null,
        eventType: null,
        authorEmail: null,
        timestamp: null,
        imageUrl: "http://moritzdentalcare.com/wp-content/uploads/2016/10/orionthemes-placeholder-image.png",
        comments: [],
        post_id: null,
        likes: 0,
        isSameUser: false,
        user_id: firebase.auth().currentUser.uid,
        profileImageUrl: null
      };
    },
    mounted() {
      this.getUserPositionOnMap()
      this.downloadUserInfo()
    },
    methods: {
      handleError(e){
        // I have no clue why downloading an image from the firebase does not work...
        console.log("Handle image error")
        console.log(e)
        console.log("image ref: "+ this.imageReference)
        this.imageUrl = "http://moritzdentalcare.com/wp-content/uploads/2016/10/orionthemes-placeholder-image.png"
        setTimeout(function(){ this.imageUrl = 'https://firebasestorage.googleapis.com/v0/b/geo-location-web-app.appspot.com/o/eventHeaderImages%2F' + this.imageReference + '?alt=media' }, 3000);
        
      
      },
      downloadUserInfo(){
        
        const url = 'http://localhost:5001/user/id/'+this.user_id
        axios.get(url).then(response => {
          this.profileImageUrl = response.data.profileImageRef
        }).catch(error => console.log(error))
      },
      likePost() {
        console.log("Post liked: " + this.post_id + " username: " + this.user_id)
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
            console.log("Response data:")
            console.log(response.data)
            if (response.data === "True") {
              $('#' + this.post_id).addClass("is-success")
            }
          })
          .catch(error => console.log(error))
      },
      getLikes() {
        const Url = 'http://localhost:5001/get_likes/' + this.post_id
  
        axios.get(Url)
          .then(response => {
  
            console.log(response.data)
            this.likes = response.data
          })
          .catch(error => console.log(error))
      },
      checkIfSameUser() {
        console.log("check if same user " + this.authorEmail + " " + (this.authorEmail == firebase.auth().currentUser.email))
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
  
      getUserPositionOnMap() {
  
        //get current user
        let credentials = firebase.auth().currentUser;
        this.renderMap();
        //get user geolocation
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            pos => {
              this.lat = pos.coords.latitude;
              this.lng = pos.coords.longitude;
              db.collection("users")
                .where("user_id", "==", credentials.uid)
                .get()
                .then(snapshot => {
                  console.log("Saving geolocation");
                  snapshot.forEach(doc => {
                    console.log(doc.id);
                    db.collection("users")
                      .doc(doc.id)
                      .update({
                        geolocation: {
                          lat: pos.coords.latitude,
                          log: pos.coords.longitude
                        }
                      });
                  });
                });
              this.renderMap();
            },
            err => {
              console.log("Render map error")
              console.log(err.message);
            }, {
              maximumAge: 60000,
              timeout: 6000
            }
          );
        } else {
          //position center by default values
          this.renderMap();
        }
      },
      placePostsOnMap(map) {
        axios.get('http://localhost:5001/latest_posts')
          .then(response => {
            // for selecting a marker programatically 
            // when the user clicks on the post
            var selectedMarker = null
            response.data.forEach(element => {
              var icon = {
                url: "http://www.newdesignfile.com/postpic/2014/07/map-icon_150412.png", // url
                scaledSize: new google.maps.Size(50, 50), // scaled size
                origin: new google.maps.Point(0, 0), // origin
                anchor: new google.maps.Point(0, 0) // anchor
              };
              let marker = new google.maps.Marker({
                position: {
                  lat: element.lat,
                  lng: element.lng
                },
                icon: icon,
                map: map,
                title: element.description,
  
  
              });
              marker.set("id", element.id);
              //add click event to marker
              marker.addListener("click", () => {
                this.title = marker.getTitle()
                console.log("You clicked on the marker: " + marker.get("id"));
                var id = marker.get("id")
                this.getPost(id)
              });
              console.log("Selected post id")
              console.log(this.selectedPostID)
              if (this.selectedPostID && element.id == this.selectedPostID) {
                selectedMarker = marker
              }
            });
            if (selectedMarker) {
              google.maps.event.trigger(selectedMarker, 'click')
            }
  
          })
          .catch(error => console.log(error))
  
  
      },
      resetContent() {
        this.description = null
        this.authorEmail = null
        this.timestamp = null
        this.comments = []
        this.title = null
        if (this.imageReference) {
          document.getElementById('postImageContainer').src = '#'
          this.imageReference = null
        }
  
      },
      getPost(id) {

        axios.get('http://localhost:5001/post/' + id)
          .then(response => {
            console.log("Got the post" + id)
            console.log(response.data.description)
            this.resetContent()
            var timestamp
            if (Date.now() - response.data.timestamp < 3758207) {
              timestamp = "Less than an hour ago"
            } else {
              timestamp = moment(response.data.timestamp).format('MMMM Do YYYY, h:mm:ss a')
            }
            console.log(response.imageReference)
  
            this.description = response.data.description
            this.authorEmail = response.data.authorEmail
            this.timestamp = timestamp
            this.imageReference = response.data.imageReference
            this.title = response.data.title
  
            console.log(response)
            if (this.imageReference) {
              this.imageUrl = 'https://firebasestorage.googleapis.com/v0/b/geo-location-web-app.appspot.com/o/eventHeaderImages%2F' + this.imageReference + '?alt=media'
  
            }
            console.log("Image url: " + this.imageUrl)
            this.post_id = id
            this.getFreshComments(id)
            this.getLikes()
            this.checkIfLiked()
            this.checkIfSameUser()
          })
          .catch(error => console.log(error))
  
      },
      getFreshComments(id) {
        this.comments = []
        this.getComments(id)
      },
      getComments(id) {
        axios.get('http://localhost:5001/get_comments/' + id)
          .then(response => {
            if(this.comments.length != 0){
              return
            }
            response.data.forEach(element => {
              var timestamp
              if (Date.now() - element.timestamp < 3758207) {
                timestamp = "Less than an hour ago"
              } else {
                timestamp = moment(element.timestamp).format('MMMM Do YYYY, h:mm:ss a')
              }
              console.log(element.imageReference)
              this.comments.push({
                id: element.id,
                description: element.description,
                authorEmail: element.authorEmail,
                timestamp: timestamp,
              })
              console.log(element)
            });
  
          })
          .catch(error => console.log(error))
      },
      renderMap() {
        const map = new google.maps.Map(document.getElementById("map"), {
          center: {
            lat: this.lat,
            lng: this.lng
          },
          zoom: 6,
          maxZoom: 15,
          minZoom: 3,
          streetViewControl: false
        });
  
        db.collection("users")
          .get()
          .then(users => {
            users.docs.forEach(doc => {
              let data = doc.data();
              if (data.geolocation) {
                //has geolocaiton
                console.log(data.user_id);
                var icon = {
                  url: "https://cmxpv89733.i.lithium.com/t5/image/serverpage/image-id/165436i36DCE8AF5DF64A5A/image-size/large?v=1.0&px=999", // url for the icon
                  scaledSize: new google.maps.Size(50, 50), // scaled size
                  origin: new google.maps.Point(0, 0), // origin
                  anchor: new google.maps.Point(0, 0) // anchor
                };
                let marker = new google.maps.Marker({
  
                  position: {
                    lat: data.geolocation.lat,
                    lng: data.geolocation.log
                  },
                  // icon: "https://img.icons8.com/wired/2x/map.png",
                  map: map,
                  title: data.user_id,
                  animation: google.maps.Animation.DROP,
                  icon: icon,
  
                });
                //add click event to marker
                marker.addListener("click", () => {
                  console.log("You clicked on the marker: " + marker.title);
                });
              }
            });
          });
        this.placePostsOnMap(map)
      }
    }
  };
</script>

<style>
  
  .google-map {
    width: 100%;
    height: 90%;
    left: 0;
    position: relative;
  }
  
  .image-container-gmap{
    min-height: 10rem;
    background-image: url("https://media3.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif");
    background-repeat: no-repeat;
    background-position: center;
  }
  .my_map_container {
    background-color: green;
    width: 50rem;
    height: 50rem;
    position: relative;
    margin: 0 auto;
  }
  
  @media screen and (max-width: 600px) {
    .my_map_container {
      background-color: green;
      width: 100%;
      height: 20rem;
      position: relative;
      margin: 0 auto;
    }
  }
  
  .hello2 {
    margin-top: 5rem;
  }
  
  .map-buttons {
    margin-top: 1rem;
    margin-right: 1rem;
  }
</style>
