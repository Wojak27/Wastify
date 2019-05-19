<template>
  <article class="media">

    <div class="media-content">
      <div class="field">
        <p class="control">
          <textarea class="textarea" placeholder="Add a comment..." v-model="text"></textarea>
        </p>
      </div>
      <nav class="level">
        <div class="level-left">
          <div class="level-item">
            <a class="button is-info" @click="submitComment">Submit</a>
          </div>
        </div>
        <div class="level-right">
        </div>
      </nav>
    </div>
    <div class="feedback-container" v-if="feedback">{{feedback}}</div>
  </article>
</template>

<script>
import axios from 'axios'
import firebase from 'firebase'

  export default {
    name: "NewCommentBox",
    props:{ 
      postID: Number, 
      method: Function,
  },
    data() {
      return {
        feedback: null,
        text: null,
        user_email: firebase.auth().currentUser.email,
      }
    },
    methods: {
      submitComment(){
        if (this.text) {
  
          const Url = 'http://localhost:5001/add_comment/'+this.postID
          
          const comment = {
            "description": this.text,
            "authorEmail": this.user_email,
            "timestamp": Date.now(),
            "parentPostID":this.postID
          }
          this.title = null
          this.description = null
          // make the post request
          // This is how you do it:
          axios.post(Url, comment)
            .then(response => {
  
              console.log("Comment added to the database")
              this.text = null
              this.method(this.postID)
            })
            .catch(error => console.log(error))
  
          if (this.feedback) {
            feedback = null
          }
        } else {
          console.log("New Post!")
          this.feedback = "You need to write something!"
        }
      }
    },
  }
</script>