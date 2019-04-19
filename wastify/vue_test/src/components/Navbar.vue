<template>
  <div class="navbar">
    <nav>
      <div class="container">
        <ul class="left">
          <router-link :to="{name: 'Index'}" class="brand-logo left">
            <img src="../assets/logo.png" alt="Wastify" class="logo">
            <span>Wastify</span>
          </router-link>
        </ul>

        <ul class="right">
          <li>
            <router-link :to="{name: 'Signup'}" v-if="!user">Signup</router-link>
          </li>
          <li>
            <router-link :to="{name: 'Login'}" v-if="!user">Login</router-link>
          </li>
          <li v-if="user">
            <router-link :to="{name: 'Map'}" v-if="user">Map</router-link>
          </li>
          <li v-if="user">
            <router-link :to="{name: 'Messenger'}" v-if="user">Messeges</router-link>
          </li>
          <li v-if="user">
            <a>{{user.email}}</a>
          </li>
          <li v-if="user">
            <a @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
import firebase from "firebase";
export default {
  name: "Navbar",
  data() {
    return {
      user: null
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
    }
  },
  created() {
    let user = firebase.auth().currentUser;
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        //user is logged in
        this.user = user;
      } else {
        //user is not logged in
        this.user = null;
      }
    });
  }
};
</script>

<style>
.navbar nav {
  padding: 0 0px;
  background-color: #53bc88;
  height: 50px;
  border-radius: 0px 0px 20px 20px;
  align-content: center;
  top: 0px;
  position: fixed;
  width: 100%;
  left: 0px;
  vertical-align: bottom;
  margin: 0 auto;
  padding: 10;
  display: -moz-inline-box;
}
.navbar span {
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  font-size: 30px;
  left: 20px;
  color: #fff;
}

input.searchField {
  width: 500px;
  border-radius: 8px;
  height: 25px;
  align-content: center;
  background-color: white;
  font-size: 15px;
}

.logo {
  height: 40px;
  left: 0px;
  align-self: baseline;
}
</style>
