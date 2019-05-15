<template>
  <div class="message-body">
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
</template>
<script>
export default {
  name: "MessageBox",
  props: ["message"],
  data() {
    return {};
  }
};
</script>

<style>
</style>
