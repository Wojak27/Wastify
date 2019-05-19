<template>
  <section class="hero is-fullheight my-section">
    <div class="hello">
      <div class="centered-content box animated bounceInUp">
        <div class="top-div">
          <div class="top-left-div">
            <p class="is-size-6 has-text-white">{{ authorEmail }}</p>
          </div>
          <div class="imageDivProfileBig">
            <img src="../../assets/profile_picture.jpg" alt class="img-background" style="object-fit: cover;">
          </div>
          <div class="top-right-div">
            <a class="button is-primary" @click="messageUser" v-if="isNotTheUser">
              <span class="icon">
                      <i class="fas fa-envelope"></i>
                    </span>
              <span>Message</span>
            </a>
            <div class="file" v-if="!isNotTheUser">
              <label class="file-label">
                  <input class="file-input" type="file" name="resume" value="upload" @change="changeProfileImage">
                  <span class="file-cta">
                    <span class="file-icon">
                      <i class="fas fa-images"></i>
                    </span>
                    <span class="file-label">
                      Change profile image
                    </span>
                  </span>
                </label>
            </div>
            <div class="file" v-if="!isNotTheUser">
              <label class="file-label">
                  <input class="file-input" type="file" name="resume" value="upload" @change="changeBackgroundImage">
                  <span class="file-cta">
                    <span class="file-icon">
                      <i class="fas fa-images"></i>
                    </span>
                    <span class="file-label">
                      Change background
                    </span>
                  </span>
                </label>
            </div>
          </div>
        </div>
  
        <div class="header-div">
          <div class="name-text box">
            <h1 class="is-size-3">My Motto:</h1>
  
            <div class="horizontal-div">
              <p class="is-size-6" v-if="!this.editing" style="width:100%">{{motto}}</p>
              <input type="text" v-if="this.editing" style="width:100%" v-model="motto">
              <a class="button" @click="handleEdit">{{this.edit_button_title}}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import "bulma/css/bulma.css";
  import firebase from "firebase";
  import animate from "animate.css";
  import axios from "axios";

  export default {
    name: "ProfilePage",
    props: ["authorEmail"],
    data() {
      return {
        isNotTheUser: null,
        editing: false,
        edit_button_title: "Edit",
        motto: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis, voluptatibus.",
        userID: firebase.auth().currentUser.uid,
      };
    },
    methods: {
      messageUser() {
        this.$router.push({
          name: "Messenger",
          params: {
            recipientEmail: this.authorEmail
          }
        });
      },
      handleEdit() {
        this.editing = !this.editing;
        if (this.edit_button_title == "Edit") {
          this.edit_button_title = "Done";
        } else if (this.edit_button_title == "Done") {
          this.edit_button_title == "Edit";
          this.handleMottoChange()
        }
      },
      handleMottoChange(){
        const url = 'http://localhost:5001/user/update_user_motto/'+this.userID

        const motto = {
          "motto": this.motto
        }

      axios.put(url, motto)
        .then(response => {
          console.log("Updating the motto successful")
          console.log(response.data)
          })
        .catch(error => console.log(error))
      },
      downloadUserInfo(){
        const url = 'http://localhost:5001/user/id/'+this.userID
        axios.get(url).then(response => {
          this.motto = response.data.motto
        }).catch(error => console.log(error))
      },
      changeProfileImage() {
        console.log("change Profile image");
      },
      changeBackgroundImage() {
        console.log("change Background image");
      }
    },
    created() {
      if (!this.authorEmail) {
        this.authorEmail = firebase.auth().currentUser.email;
      }
      console.log(this.authorEmail);
      this.isNotTheUser = this.authorEmail != firebase.auth().currentUser.email;
      this.downloadUserInfo()
    }
  };
</script>

<style scoped>
  .hello {
    padding-top: 5rem;
    padding-bottom: 2rem;
  }
  
  .img-background {
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  
  .horizontal-div {
    display: flex;
    flex-direction: row;
  }
  
  .top-div {
    display: flex;
    flex: 1;
  }
  
  .top-right-div {
    display: flex;
    flex: 1;
    flex-direction: column;
    /* background-color: red; */
    justify-content: center;
  }
  
  .top-left-div {
    display: flex;
    flex: 1;
    /* background-color: red; */
    justify-content: center;
    align-items: center;
  }
  
  .centered-content {
    width: 45rem;
    margin-top: 20rem;
    background-color: green;
    align-self: center;
  }
  
  .imageDivProfileBig img {
    border-radius: 50%;
    height: 250px;
    width: 250px;
    border-color: lightcyan;
    border-width: 2px;
    border-style: solid;
    margin: 0 auto;
    overflow: hidden;
    align-content: center;
    background-color: red;
    position: relative;
    bottom: 4rem;
  }
  
  .imageDivProfileBig img:hover {
    border-color: yellow;
    border-width: 4px;
    cursor: pointer;
  }
  
  .imageDivProfile {
    height: 250px;
    width: 250px;
  }
  
  @media screen and (max-width: 600px) {
    .centered-content {
      min-width: 20rem;
      margin-top: 10rem;
      height: 100rem;
      align-self: center;
    }
  }
  
  .header-div {
    background-color: lightblue;
    height: 10rem;
    display: flex;
  }
  
  .hello {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-self: center;
    text-align: center;
    padding-top: 5rem;
  }
  
  .profile-image {
    display: flex;
    flex: 1;
  }
  
  .name-text {
    display: flex;
    flex-direction: column;
    flex: 4;
  }
  
  .parallax {
    /* The image used */
    background-image: url("../../assets/trash.jpg");
    /* Full height */
    height: 100%;
    /* Create the parallax scrolling effect */
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
  }
  
  .my-section {
    background-color: white;
    background-image: url("https://images.unsplash.com/photo-1528920304568-7aa06b3dda8b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    background-position: 50% 50%;
  }
</style>
