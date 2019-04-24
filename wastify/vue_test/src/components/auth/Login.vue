<template>
  <div class="box login container">
    <form @submit.prevent="login" class="card-panel">
      <h2 class="center deep-purple-text"> {{login_text}}</h2>
      <div class="field">

        <div class="control has-icons-left has-icons-right">

  <input class="input is-rounded" name="email" v-model="email" type="email" placeholder="Email">
  <span class="icon is-small is-left">
    <i class="fas fa-envelope"></i>
  </span>

</div>
      </div>

      <div class="field">
        <div class="control">

<p class="control has-icons-left">
    <input class="input is-rounded" type="password" 
    name="password"
            v-model="password"
            placeholder="Password">
    <span class="icon is-small is-left">
      <i class="fas fa-lock"></i>
    </span>
  </p>
        </div>

        
      </div>
      <p class="red-text center" v-if="feedback">{{feedback}}</p>
      <div class="field">
        <button class="button is-rounded">Login</button>
      </div>
      <p>
        or...
      </p>
      <div class="field">
        
        <button class="button is-rounded" @click="loginWithGoogle"><img src="https://developers.google.com/identity/images/g-logo.png" class="googleImage"> Sign in with Google</button>
      </div>
    </form>
  </div>
</template>

<script>
import firebase from 'firebase'
import 'bulma/css/bulma.css'
import axios from 'axios'
import request from 'request'

export default {
  name: 'Login',
  data() {
    return {
      email: null,
      password: null,
      feedback: null,
      ROOT_API: process.env.ROOT_API,
      login_text: "Login"
    };
  },
  methods: {
    login() {
      if (this.email && this.password) {
        firebase
          .auth()
          .signInWithEmailAndPassword(this.email, this.password)
          .then(credentials => {
            console.log(credentials.user);
            this.$router.push({ name: "Feed" });
          })
          .catch(error => {
            this.feedback = error.message;
          });
        this.feedback = null;
      } else {
        this.feedback = "Please fill in both fields";
      }
    },
    loginWithGoogle(){
      function newLoginHappened(user){
        if(user){
          //user signed in
        }else{
          console.log("provider")
          var provider = new firebase.auth.GoogleAuthProvider()
          firebase.auth().signInWithRedirect(provider)
        }
      }
      
      firebase.auth().onAuthStateChanged(newLoginHappened)
    },
    logout() {
      firebase.auth().signOut();
    },
    checkConnection(){
      //fetch(':5001/books').then((response)=>{console.log(response)}).then(json => {
      //  console.log(json)
      //})
      var bodyText
      const request = require('request');
      request('http://localhost:5001/app', function (error, response, body) {
        console.error('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the HTML for the Google homepage.
        bodyText = body
        console.log(typeof(bodyText))
        self.login_text = bodyText
      });
      


    },
    changeTitleText(){
      self.login_text = "Hello World"
      console.log(self.login_text)
    }
  },
  created() {
    this.logout()
    this.checkConnection()
  },
  mounted() {
    this.checkConnection()
  },
};
</script>

<style>
.login {
  max-width: 400px;
  margin-top: 60px;
}

.login h2 {
  font-size: 2.4em;
}
.login .field {
  margin-bottom: 16px;
}

.googleImage{
  height: 20px;
}
</style>
