<template>
  <div class="signup container box">
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
      <div class="field center">
        <button class="button is-rounded" @click="loginWithGoogle"><img src="https://developers.google.com/identity/images/g-logo.png" class="googleImage"> Sign up with Google</button>
      </div>
      </form>
  </div>
</template>
<script>
import slugify from "slugify";
import db from "@/firebase/init";
import firebase from "firebase";

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

                  ref
                    .set({
                      alias: this.alias,
                      geolocation: null,
                      user_id: cred.user.uid
                    })
                    .then(() => {
                      this.$router.push({ name: "Feed" });
                    });
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
    created() {
      this.logout();
    }
  }
};
</script>

<style>
.signup {
  max-width: 400px;
  margin-top: 60px;
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
