<template>
  <div class="map">
    <div class="google-map" id="map"></div>
  </div>
</template>

<script>
import firebase from "firebase";
import db from "@/firebase/init";
export default {
  name: "GMap",
  data() {
    return {
      lat: 53,
      lng: -2
    };
  },
  mounted() {
    //get current user
    let credentials = firebase.auth().currentUser;
    console.log(credentials);
    console.log(credentials.uid);

    //find the user record

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
          console.log(err);
        },
        { maximumAge: 60000, timeout: 3000 }
      );
    } else {
      //position center by default values
      this.renderMap();
    }
  },
  methods: {
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
            console.log("setting pins");
            console.log(data);
            if (data.geolocation) {
              //has geolocaiton
              console.log(data.user_id);
              let marker = new google.maps.Marker({
                position: {
                  lat: data.geolocation.lat,
                  lng: data.geolocation.log
                },
                map: map,
                title: data.user_id
              });
              //add click event to marker
              marker.addListener("click", () => {
                console.log(doc.id);
              });
            }
          });
        });
    }
  }
};
</script>

<style>
.google-map {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
