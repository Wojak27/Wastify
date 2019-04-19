<template>
  <div class="login container">
    <form @submit.prevent="login" class="card-panel">
      <h2 class="center deep-purple-text">Login</h2>
      <div class="field">
        <label for="email">Email:</label>
        <input type="email" name="email" v-model="email">
      </div>

      <div class="field">
        <label for="password" class="label">Password:</label>
        <div class="control">
          <input
            type="password"
            name="password"
            v-model="password"
            class="input"
            placeholder="e.g Alex Smith"
          >
        </div>
      </div>
      <p class="red-text center" v-if="feedback">{{feedback}}</p>
      <div class="field">
        <button class="btn deep-purple">Login</button>
      </div>
    </form>
  </div>
</template>

<script>
import firebase from "firebase";
import "bulma/css/bulma.css";

export default {
  name: "Login",
  data() {
    return {
      email: null,
      password: null,
      feedback: null
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
            this.$router.push({ name: "Index" });
          })
          .catch(error => {
            this.feedback = error.message;
          });
        this.feedback = null;
      } else {
        this.feedback = "Please fill in both fields";
      }
    },
    logout() {
      firebase.auth().signOut();
    }
  },
  created() {
    this.logout();
  }
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
</style>
