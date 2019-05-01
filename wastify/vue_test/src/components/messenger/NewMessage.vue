<template>
  <div class="new-message">
    <form @submit.prevent="addMessage">
      <label for="new-message">New Message (Enter to add)</label>
      <input type="text" class="input is-rounded" name="new-message" v-model="newMessage">
      <p class="red-text" v-if="feedback">{{feedback}}</p>
    </form>
  </div>
</template>

<script>
import 'bulma/css/bulma.css'
import db from "@/firebase/init";
export default {
  name: "NewMessage",
  props: ["author", "recipient"],
  data() {
    return {
      newMessage: null,
      feedback: null,
      
    };
  },
  methods: {
    addMessage() {
      if (this.newMessage) {
        var chatDBReference = null
        if(this.recipient > this.author){
          chatDBReference = this.recipient+this.author
        }else{
          chatDBReference = this.author+this.recipient
        }
        console.log("Adding new message");
        db.collection("messenger").doc(chatDBReference).collection("messages")
          .add({
            content: this.newMessage,
            author: this.author,
            timestamp: Date.now()
          })
          .catch(err => {
            console.log("Error adding a message!")
            console.log(err);
            this.feedback = err.message;
          });
        // Adding a reference in the authors table
        db.collection("conversations").doc(this.author).collection("users").add({
          id:this.recipient,
          last_contacted: Date.now()
        }).catch(err => {
            console.log("Error adding a message!")
            console.log(err);
            this.feedback = err.message;
            
          });

        // Adding a reference in the recipients table
        db.collection("conversations").doc(this.recipient).collection("users").add({
          id:this.author,
          last_contacted: Date.now()
        }).catch(err => {
            console.log("Error adding a message!")
            console.log(err);
            this.feedback = err.message;
            
          });
        this.newMessage = null;
        this.feedback = null;
      } else {
        this.feedback = "You must enter a message in order to send one";
      }
    }
  }
};
</script>
