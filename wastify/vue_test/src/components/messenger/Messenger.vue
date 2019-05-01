<template>
  <div class="chat">
    <div class="center-messages-div">
      <div class="left-messages-div box">
        <div v-chat-scroll>
          <div class="friend-body" v-for="(recipient, index) in recipients" :key="index">
            
            <a class="button is-small" style="width:100%">{{recipient}}</a>
          </div>
        </div>
      </div>
      <div class="card box">
        <div class="messages" v-chat-scroll>
          <div v-for="message in messages" :key="message.id" class="message-body">
            <div class="name">
              <span class="teal-text">{{ message.author}}</span>
            </div>
            <div class="time-message">
              <div class="my-message">
                <p class="is-size-5">
                  {{message.content}}
                </p>
          </div>
            <div class="time">
              <p class="is-size-7"> 
                {{message.timestamp}}
              </p>
              
          </div>
            </div>
            </div>
        </div>
        <div class="new-message">
          <NewMessage :author="author" :recipient="recipient"/>
        </div>
        You are messaging {{recipient}}
      </div>
    </div>
    
  </div>
</template>

<script>
import NewMessage from "@/components/messenger/NewMessage";
import db from "@/firebase/init";
import firebase from "firebase";
import moment from "moment"
export default {
  name: "Messenger",
  data() {
    return {
      messages: [],
      author: firebase.auth().currentUser.email,
      recipients: ["Antek Szadaj","Tabea Schrot","Lenny Johansson","Daniel Wassing"]
    };
  },
  props: ["recipient"],
  components: {
    NewMessage
  },
  methods: {
    createChatBox(){
      var chatDBReference = null
        if(this.recipient > this.author){
          chatDBReference = this.recipient+this.author
        }else{
          chatDBReference = this.author+this.recipient
        }
    let ref = db.collection("messenger").doc(chatDBReference).collection("messages").orderBy("timestamp");

    ref.onSnapshot(snapshot => {
      snapshot.docChanges().forEach(change => {
        if (change.type == "added") {
          let doc = change.doc;
          this.messages.push({
            id: doc.id,
            author: doc.data().author,
            content: doc.data().content,
            timestamp: moment(doc.data().timestamp).format('MMMM Do YYYY, h:mm:ss a')
          });
        }
      });
    });
    },
    createFriendsList(){

      let ref = db.collection("conversations").doc(this.author).collection("users").orderBy("timestamp");

      ref.onSnapshot(snapshot => {
        snapshot.docChanges().forEach(change => {
          if (change.type == "added") {
            let doc = change.doc;
            this.messages.push({
              id: doc.id,
              author: doc.data().author,
              content: doc.data().content,
              timestamp: moment(doc.data().timestamp).format('MMMM Do YYYY, h:mm:ss a')
            });
          }
        });
      });
    }
  },
  created() {
    this.createChatBox();
    this.createFriendsList();
  }
};
</script>

<style>
.center-messages-div{
  height: 40rem;
  display: flex;
  align-self: center;

}

.friend-body{
  width: 15rem;
}
.left-messages-div{
  display: flex;
  background-color: red;
  flex: 1;
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
.chat{
  margin-top:4rem;
  display: flex;
  flex-direction: column;
  justify-content: bottom;
  align-items: bottom;
  height:auto;
}
.new-message{
  width: 45rem;
}

@media screen and (max-width: 600px) {
  .new-message{
  width: 100%;
  }
}

.messages{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 40rem;
  overflow: auto;
  flex: 3;
}


.messages::-webkit-scrollbar-track{
  background: #ddd;
}
.messages::-webkit-scrollbar-thumb{
  background: #aaa;
}
.messages::-webkit-scrollbar{
  width: 3px;
}

.card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

}

.message-body{
  display: flex;
  width: 45rem;
  justify-content: space-between;
  border-top: #000;
}

@media screen and (max-width: 600px) {
  .message-body{
  display: flex;
  width: 100%;
  border-top: #000;
}
}

.my-message{
  flex: 2;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  padding: 10px;
}
.time{
  display: flex;
  padding: 0.1rem;
  flex: 1;
  justify-content: flex-end;
  align-items: flex-end;
}
.name{
  display: flex;
  align-self: flex-start;
  flex: 1;
}

.time-message{
  flex:5;
  display: flex;
  flex-direction: column;
}
</style>
