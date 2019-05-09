<template>
  <div class="hello2">
    <div class="box my_map_container animated bounceInUp">
        <h3 class="is-size-3 has-text-white">Explore events</h3>
      <div class="google-map is-marginless" id="map">
      </div>
      <div class="post-area box" v-if="description">
        
        <h1 class="is-size-3" v-if="title">{{title}}</h1>
        <img src="#" id="postImageContainer" v-if="this.imageReference">
        
        <p>{{description}}</p>
        
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

export default {
  name: "GMap",
  data() {
    return {
      lat: 53,
      lng: -2,
      title: null,
      description: null,
      imageRef: null,
      eventType: null,
      authorEmail: null,
      timestamp: null
    };
  },
  mounted() {
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
              console.log(credentials.uid);
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
        },
        { maximumAge: 60000, timeout: 6000 }
      );
    } else {
      //position center by default values
      this.renderMap();
    }
  },
  methods: {
    placePostsOnMap(map){
      axios.get('http://localhost:5001/latest_posts')
      .then(response => {
        response.data.forEach(element => {
            console.log("Placing markers")
            console.log(element)
            var icon = {
                url: "http://www.newdesignfile.com/postpic/2014/07/map-icon_150412.png", // url
                scaledSize: new google.maps.Size(50, 50), // scaled size
                origin: new google.maps.Point(0,0), // origin
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
              console.log("You clicked on the marker: "+marker.get("id"));
              var id = marker.get("id")
              this.getPost(id)
            });
        });
      })
      .catch(error => console.log(error))


    },
    resetContent(){
        this.description = null
        this.authorEmail = null
        this.timestamp = null
        this.title = null
        if(this.imageReference){
          document.getElementById('postImageContainer').src='#'
          this.imageReference = null
        }
        
    },
    getPost(id){
      axios.get('http://localhost:5001/post/'+id)
      .then(response => {
        console.log("Got the post" + id)
        console.log(response.data.description)
          this.resetContent()
          var timestamp
          if(Date.now() - response.data.timestamp < 3758207){
            timestamp = "Less than an hour ago"
          }else{
            timestamp = moment(response.data.timestamp).format('MMMM Do YYYY, h:mm:ss a')
          }
          console.log(response.imageReference)
          
          this.description = response.data.description
          this.authorEmail = response.data.authorEmail
          this.timestamp = timestamp
          this.imageReference = response.data.imageReference
          this.title = response.data.title
          
          console.log(response)
          if(this.imageReference){
            var url = 'https://firebasestorage.googleapis.com/v0/b/geo-location-web-app.appspot.com/o/eventHeaderImages%2F'+this.imageReference+'?alt=media'
            this.loadImage(url)
            
          }
          
      })
      .catch(error => console.log(error))
    },
    loadImage(url){
      document.getElementById('postImageContainer').src=url
    },
    renderMap() {
      const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: this.lat, lng: this.lng },
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
              let marker = new google.maps.Marker({
                position: {
                  lat: data.geolocation.lat,
                  lng: data.geolocation.log
                },
                // icon: "https://img.icons8.com/wired/2x/map.png",
                map: map,
                title: data.user_id,
                animation: google.maps.Animation.DROP

              });
              //add click event to marker
              marker.addListener("click", () => {
                console.log("You clicked on the marker: "+marker.title);
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
.post-area{
  
}
.google-map {
  width: 100%;
  height: 90%;
  left: 0;
  position: relative;
}

.my_map_container{
  background-color: green;
  width: 50rem;
  height: 50rem;
  position: relative;
  margin: 0 auto;
  
}
@media screen and (max-width: 600px) {
  .my_map_container{
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

.map-buttons{
  margin-top:1rem;
  margin-right: 1rem;
}

</style>
