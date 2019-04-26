<template>
  <div class="chat">
    <div class="card">
      <div class="messages" v-chat-scroll>
        <div v-for="message in messages" :key="message.id" class="message-body">
          <div class="name">
            <span class="teal-text">{{ message.name}}</span>
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
        <NewMessage :name="name"/>
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
      name: "Karol"
    };
  },
  props: ["name"],
  components: {
    NewMessage
  },
  created() {
    let ref = db.collection("messages").orderBy("timestamp");

    ref.onSnapshot(snapshot => {
      snapshot.docChanges().forEach(change => {
        if (change.type == "added") {
          let doc = change.doc;
          this.messages.push({
            id: doc.id,
            name: doc.data().name,
            content: doc.data().content,
            timestamp: moment(doc.data().timestamp).format('MMMM Do YYYY, h:mm:ss a')
          });
        }
      });
    });
  }
};
</script>

<style>
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
