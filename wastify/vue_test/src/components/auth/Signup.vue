<template>
 <section class="hero is-fullheight my-section">
  <div class="signup container box  animated bounceInUp">
    <form @submit.prevent="signup" class="card-panel">
      <h2 class="center deep-purple-text">Signup</h2>
      <div class="field">
        <label for="alias">Username:</label>
        <input type="text" name="alias" v-model="alias"
        class="input is-rounded">
      </div>
      <div class="field">
        <label for="email">Email:</label>
        <input type="email" name="email" v-model="email"
        class="input is-rounded">
      </div>

      <div class="field">
        <label for="password">Password:</label>
        <input type="password" name="password" v-model="password"
        class="input is-rounded">
      </div>
      <div class="field">
        <label for="password">Repeat password:</label>
        <input type="password" 
        class="input is-rounded"
        name="repeated_password" v-model="repeatedPassword">
      </div>
      <p class="red-text center" v-if="feedback">{{feedback}}</p>
      <div class="field center">
        <button class="button is-rounded">Signup</button><br>
        or...
      </div>
      </form>
      <div class="field g-signin2" data-onsuccess="onSignIn">
        
        <button class="button is-rounded"><img src="https://developers.google.com/identity/images/g-logo.png" class="googleImage"> Sign in with Google</button>
      </div>
      <div class="g-signin2" data-onsuccess="onSignIn"></div>


  </div>
 </section>
</template>
<script>
import slugify from "slugify";
import db from "@/firebase/init";
import firebase from "firebase";
import axios from "axios";
import animate from "animate.css"

export default {
  name: "Signup",
  data() {
    return {
      email: null,
      password: null,
      repeatedPassword: null,
      alias: null,
      feedback: null,
      slug: null
    };
  },
  methods: {
    logout() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.$router.push({ name: "Login" });
        });
    },
    createUserinRefDatabase(){
        console.log("New User created!")
        
        console.log(firebase.auth().currentUser.email)
        console.log(firebase.auth().currentUser.user_id)
        console.log(firebase.auth().currentUser.displayName)
        console.log(Date.now())

        var user = firebase.auth().currentUser

        var username = this.alias;
        var email = user.email;
        var uid = user.uid;

        const Url = 'http://localhost:5001/user/create/'
        // specify the object to post
        const new_user = {
          "firebase_id": uid,
          "username": username,
          "emailAddress": email,
          "creation_time": Date.now()
        }

        // make the post request
        // This is how you do it:
        axios.post(Url,new_user)
        .then(response => {
          this.description = null
            console.log("Response from the database")
            console.log(response)
          })
        .catch(error => console.log(error))

        if(feedback){
          feedback = null
        }
      
    },
    signup() {
      if (this.alias && this.email && this.password && this.repeatedPassword) {
        this.slug = slugify(this.alias, {
          replacement: "-",
          remove: /[$*_+~.()'"!\-:@]/g,
          lower: true
        });
        let ref = db.collection("users").doc(this.slug);
        ref.get().then(doc => {
          if (doc.exists) {
            this.feedback = "This username is already taken!";
          } else {
            if (this.repeatedPassword !== this.password) {
              this.feedback = "You need to repeat your password!";
            } else {
              firebase
                .auth()
                .createUserWithEmailAndPassword(this.email, this.password)
                .then(cred => {
                  // cred.user to get a user


                  // creating this new user in the firebase database
                  ref
                    .set({
                      alias: this.alias,
                      geolocation: null,
                      user_id: cred.user.uid
                    })
                    .then(() => {
                      console.log("Pushing to Feed")
                      this.$router.push({ name: "Feed" });
                    });

                  //creating a new user in the local database
                  this.createUserinRefDatabase()
                  
                  this.feedback = null;
                  this.alias = null;
                  this.password = null;
                  this.repeatedPassword = null;
                  this.email = null;
                })
                .catch(error => {
                  console.log(error);
                  this.feedback = error.message;
                });
            }
          }
        });
        console.log(this.slug);
        this.feedback = null;
      } else {
        this.feedback = "You must enter a all fields";
      }
    },
    onSignIn(googleUser) {
        // Useful data for your client-side scripts:
        var profile = googleUser.getBasicProfile();
        console.log("ID: " + profile.getId()); // Don't send this directly to your server!
        console.log('Full Name: ' + profile.getName());
        console.log('Given Name: ' + profile.getGivenName());
        console.log('Family Name: ' + profile.getFamilyName());
        console.log("Image URL: " + profile.getImageUrl());
        console.log("Email: " + profile.getEmail());

        // The ID token you need to pass to your backend:
        var id_token = googleUser.getAuthResponse().id_token;
        console.log("ID Token: " + id_token);
      }

  }
};
</script>

<style>

.my-section{
  background-color: white;
  background-image: url("http://www.broward.org/GoGreen/Municipalities/PublishingImages/468457117%20-%20handprint.jpg");
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  background-position: 50% 50%;
}

.signup {
  max-width: 400px;
  margin-top: 15rem;
}
.signup h2 {
  font-size: 2.4em;
}
.signup .field {
  margin-bottom: 16px;
}
.googleImage{
  height: 20px;
}
</style>
