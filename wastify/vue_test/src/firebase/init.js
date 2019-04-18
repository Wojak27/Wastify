import firebase from "firebase";

// Initialize Firebase
var config = {
  apiKey: "AIzaSyAw_51y0MhDUaMCv6RXSG0eNDmU4pyy248",
  authDomain: "geo-location-web-app.firebaseapp.com",
  databaseURL: "https://geo-location-web-app.firebaseio.com",
  projectId: "geo-location-web-app",
  storageBucket: "geo-location-web-app.appspot.com",
  messagingSenderId: "808972368583"
};
const firebaseApp = firebase.initializeApp(config);

export default firebaseApp.firestore();
