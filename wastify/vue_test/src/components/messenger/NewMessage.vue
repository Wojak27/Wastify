<template>
  <div class="new-message">
    <form @submit.prevent="addMessage">
      <label for="new-message">New Message (Enter to add)</label>
      <input type="text" class="input is-rounded" name="new-message" v-model="newMessage" placeholder="Be the first one to say hello!">
      <p class="red-text" v-if="feedback">{{feedback}}</p>
    </form>
  </div>
</template>

<script>
import "bulma/css/bulma.css";
import db from "@/firebase/init";
export default {
  name: "NewMessage",
  props: ["author", "recipientEmail"],
  data() {
    return {
      newMessage: null,
      feedback: null
    };
  },
  methods: {
    addMessage() {
      if (this.newMessage) {
        var chatDBReference = null;
        if (this.recipientEmail > this.author) {
          chatDBReference = this.recipientEmail + this.author;
        } else {
          chatDBReference = this.author + this.recipientEmail;
        }
        console.log("Adding new message");
        db.collection("messenger")
          .doc(chatDBReference)
          .collection("messages")
          .add({
            content: this.newMessage,
            author: this.author,
            timestamp: Date.now()
          }).then(response=>console.log("Success adding a message!"))
          .catch(err => {
            console.log("Error adding a message!");
            console.log(err);
            this.feedback = err.message;
          });
        // Adding a reference in the authors table
        db.collection("conversations")
          .doc(this.author)
          .collection("users")
          .add({
            id: this.recipientEmail,
            last_contacted: Date.now(),
            test: "this is a test"
          }).then(response=> console.log("Success adding a conversation author!"))
          .catch(err => {
            console.log("Error adding a message!");
            console.log(err);
            this.feedback = err.message;
          });

        // Adding a reference in the recipientEmails table
        db.collection("conversations")
          .doc(this.recipientEmail)
          .collection("users")
          .add({
            id: this.author,
            last_contacted: Date.now()
          }).then(response=> console.log("Success adding a conversation recipientEmail!"))
          .catch(err => {
            console.log("Error adding a message!");
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

<style>

</style>
