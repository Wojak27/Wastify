import Vue from "vue";
import Router from "vue-router";
import Feed from "@/components/feed/Feed";
import Signup from "@/components/auth/Signup";
import Login from "@/components/auth/Login";
import Messenger from "@/components/messenger/Messenger";
import GMap from "@/components/map/GMap";
import NewPost from "@/components/feed/NewPost";
import firebase from "firebase";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "Feed",
      component: Feed,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/map",
      name: "Map",
      component: GMap,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/messenger",
      name: "Messenger",
      component: Messenger,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/signup",
      name: "Signup",
      component: Signup
    },
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: "/new_post",
      name: "NewPost",
      component: NewPost
    }
  ]
});

router.beforeEach((to, from, next) => {
  //check to see if the route requires auth
  if (to.matched.some(rec => rec.meta.requiresAuth)) {
    //check auth state of the user
    let user = firebase.auth().currentUser;
    if (user) {
      //user signed in, proceed to the route
      next();
    } else {
      //no user signed in, redirect to login
      next({ name: "Login" });
    }
  } else {
    next();
  }
});

export default router;
