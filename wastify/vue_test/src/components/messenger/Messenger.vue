<template>
  <div class="chat">
    <div class="body-messages-div">
      <div class="left-messages-div box is-paddingless">
        <div>
          <div class="friend-body" v-for="(friend, index) in friends" :key="index">
            <a
              class="button is-small"
              style="width:100%"
              @click="loadConversation(friend)"
            >{{friend}}</a>
          </div>
        </div>
      </div>
      <div class="card box center-messages-div">
        <div class="messages" v-chat-scroll="{smooth: true}" style="overflow:scroll;">
          <div class="nofrineds" v-if="!hasFriends">You don't have any friends yet!</div>
          <div
            v-for="message in messages"
            :key="message.id"
            style="display: flex; width:100%;"
            class="message-body"
          >
            <div
              class="author-message-body box"
              v-if="message.author == author"
              style="background-color:lightgreen; width:100%"
            >
              <div class="name">
                <span class="teal-text">You</span>
              </div>
              <div class="time-message">
                <div class="my-message">
                  <p class="is-size-5">{{message.content}}</p>
                </div>
                <div class="time">
                  <p class="is-size-7">{{message.timestamp}}</p>
                </div>
              </div>
            </div>
            <div
              class="friend-message-body box"
              v-if="message.author != author"
              style="background-color:lightblue; width:100%"
            >
              <div class="name">
                <span class="teal-text">{{ message.author}}</span>
              </div>
              <div class="time-message">
                <div class="my-message">
                  <p class="is-size-5">{{message.content}}</p>
                </div>
                <div class="time">
                  <p class="is-size-7">{{message.timestamp}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="new-message">
          <NewMessage :author="author" :recipientEmail="this.recipient"/>
        </div>
      </div>
      <div class="right-messages-div">You are messaging {{this.recipient}}</div>
    </div>
  </div>
</template>

<script>
import NewMessage from "@/components/messenger/NewMessage";
import MessageBox from "@/components/messenger/MessageBox";
import db from "@/firebase/init";
import firebase from "firebase";
import moment from "moment";
export default {
  name: "Messenger",
  data() {
    return {
      messages: [],
      author: firebase.auth().currentUser.email,
      friends: [],
      recipient: null,
      hasFriends: true
    };
  },
  props: ["recipientEmail"],
  components: {
    NewMessage,
    MessageBox
  },
  methods: {
    createChatBox(friendEmail) {
      this.messages = [];
      var chatDBReference = null;
      if (friendEmail > this.author) {
        chatDBReference = friendEmail + this.author;
      } else {
        chatDBReference = this.author + friendEmail;
      }
      let ref = db
        .collection("messenger")
        .doc(chatDBReference)
        .collection("messages")
        .orderBy("timestamp");

      ref.onSnapshot(snapshot => {
        snapshot.docChanges().forEach(change => {
          if (change.type == "added") {
            let doc = change.doc;
            this.messages.push({
              id: doc.id,
              author: doc.data().author,
              content: doc.data().content,
              timestamp: moment(doc.data().timestamp).format(
                "MMMM Do YYYY, h:mm:ss a"
              )
            });
          }
        });
      });
    },
    loadConversation(friend) {
      console.log("Load conversation " + friend);
      this.createChatBox(friend);
      this.recipient = friend;
    },
    createFriendsList() {
      let ref = db
        .collection("conversations")
        .doc(this.author)
        .collection("users")
        .orderBy("last_contacted");
      console.log("ref");
      console.log(ref);

      ref.onSnapshot(snapshot => {
        console.log(snapshot);
        snapshot.docChanges().forEach(change => {
          console.log("conversations " + change.type);
          if (change.type == "added") {
            let doc = change.doc;
            console.log("New change!");
            console.log(!this.friends.includes(doc.data().id));
            console.log(this.friends);
            console.log(doc.data().id);
            if (!this.friends.includes(doc.data().id)) {
              this.friends.unshift(doc.data().id);
            }
          }
        });
        this.setRecipient();
      });
    },
    setRecipient() {
      console.log("recipientEmail");
      console.log(this.recipientEmail);
      if (this.recipientEmail) {
        console.log("has rec");
        this.recipient = this.recipientEmail;
        this.loadConversation(this.recipient);
      } else if (this.friends.length == 0) {
        this.hasFriends = false;
        console.log("No frineds yet!");
      } else {
        console.log(this.friends);
        this.recipient = this.friends[0];
        this.loadConversation(this.recipient);
      }
    }
  },
  created() {
    this.createFriendsList();
  }
};
</script>

<style>
.body-messages-div {
  position: fixed;
  height: 97vh;
  display: flex;
  align-self: center;
  width: 100%;
}

.friend-body {
  width: 15rem;
}
.left-messages-div {
  display: flex;
  flex: 1;
}
.right-messages-div {
  display: flex;
  flex: 2;
}
.chat h2 {
  font-size: 2.6em;
  margin-bottom: 40px;
}

.chat span {
  font-size: 1.4em;
}
.chat .time {
  font-size: 1.2em;
}
.chat {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: bottom;
  align-items: bottom;
  height: auto;
}
.new-message {
  width: 100%;
}

@media screen and (max-width: 600px) {
  .new-message {
    width: 100%;
  }
}

.messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  flex: 6;
}

.messages::-webkit-scrollbar-track {
  background: #ddd;
}
.messages::-webkit-scrollbar-thumb {
  background: #aaa;
}
.messages::-webkit-scrollbar {
  width: 3px;
}

.time {
  display: flex;
  padding: 0.1rem;
  flex: 1;
  justify-content: flex-end;
  align-items: flex-end;
}

.name {
  display: flex;
  align-self: flex-start;
  flex: 1;
}

.message-body {
  display: flex;
  width: 100%;
}
.my-message {
  flex: 2;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  padding: 10px;
}
.time-message {
  flex: 5;
  display: flex;
  flex-direction: column;
}
.card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

@media screen and (max-width: 600px) {
  .message-body {
    display: flex;
    width: 100%;
    border-top: #000;
  }
}

.center-messages-div {
  display: flex;
  flex: 5;
}
</style>
