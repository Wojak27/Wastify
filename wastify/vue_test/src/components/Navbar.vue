<template>
  <div class="navbar is-fixed-top" role="navigation">
    <nav aria-label="dropdown navigation">
      <div class="navbar-menu nav-container">
        <ul class="navbar-start logo left">
          <router-link :to="{name: 'Feed'}">
            <img src="../assets/logo.png" alt="Wastify" class="logo">
            <span>Wastify</span>
          </router-link>
        </ul>

        <ul class="navbar-end field right">
          <li class="navbar-item">
            <router-link :to="{name: 'Signup'}" v-if="!user">Signup</router-link>
          </li>
          <li class="navbar-item">
            <router-link :to="{name: 'Login'}" v-if="!user">Login</router-link>
          </li>
          <li v-if="user" class="navbar-item">
            <router-link :to="{name: 'Map'}" v-if="user">Map</router-link>
          </li>

          <li v-if="user" class="navbar-item">
            
          </li>
          <li v-if="user" class="navbar-item">


    <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link" href="https://bulma.io/documentation/overview/start/">
          
        </a>
        <div class="navbar-dropdown is-boxed">
          <router-link class="navbar-item" :to="{name: 'Map'}" v-if="user">Map</router-link>
          <router-link class="navbar-item" :to="{name: 'Feed'}" v-if="user">Feed</router-link>
          <router-link class="navbar-item" :to="{name: 'Messenger'}" v-if="user">Messenger</router-link>
          <router-link class="navbar-item" :to="{name: 'ProfilePage'}" v-if="user">Profile</router-link>
          
          <hr class="navbar-divider">
          <a class="navbar-item" href="" @click="logout">
            Logout
          </a>
        </div>
  </div>
          </li>
        </ul>
        
      </div>
    </nav>
  </div>
</template>

<script>
import firebase from "firebase";
import "bulma/css/bulma.css";
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
  padding-left: 1rem;
  align-self: baseline;
}

ul.right {
  padding-right: 5rem;
}

ul.left {
  padding-left: 5rem;
}
.nav-container{
  margin: auto;
  max-width: 60rem;
}

</style>
