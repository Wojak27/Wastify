<template>
  <div class="hello2">
    <div class="box my_map_container animated bounceInUp">
        <i class="is-large">Add an event</i>
      <div class="google-map is-marginless" id="map">
      </div>
      <span class="button is-info map-buttons is-rounded"><i class="fas fa-map-pin" style="margin-right:5px"></i>   Mark and Create an Event</span>
      <span class="button is-primary map-buttons is-rounded"><i class="fas fa-location-arrow" style="margin-right:5px"></i>    Create Event With this Position</span>
      <div class="post-area box" v-if="title">
        {{title}}
      </div>
    
    </div>
    
  </div>
</template>

<script>
import firebase from "firebase";
import "bulma/css/bulma.css";
import db from "@/firebase/init";
import axios from "axios";


export default {
  name: "GMap",
  data() {
    return {
      lat: 53,
      lng: -2,
      posts:[],
      title: null
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
            //add click event to marker
            marker.addListener("click", () => {
              this.title = marker.getTitle()
              console.log("You clicked on the marker: "+this.title);
              
            });
        });
      })
      .catch(error => console.log(error))


    },
    renderMap() {
      const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: this.lat, lng: this.lng },
        zoom: 6,
        maxZoom: 15,
        minZoom: 3,
        streetViewControl: false
      });

      // custom marker icon
      var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
      var icons = {
        parking: {
          icon: iconBase + 'parking_lot_maps.png'
        },
        library: {
          icon: iconBase + 'library_maps.png'
        },
        info: {
          icon: iconBase + 'info-i_maps.png'
        }
      };


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
