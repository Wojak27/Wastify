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
  data() {
    return {
      newMessage: null,
      feedback: null,
      name: "Karol"
    };
  },
  methods: {
    addMessage() {
      if (this.newMessage) {
        console.log("Adding new message");
        db.collection("messages")
          .add({
            content: this.newMessage,
            name: this.name,
            timestamp: Date.now()
          })
          .catch(err => {
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
