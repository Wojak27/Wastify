<template>
  <div>
    <article class="message is-primary" v-if="isOn">
      <div class="message-header">
        Welcome to Wastify!
        <button class="delete" @click="hideInfo"></button>
      </div>
      <div class="message-body">
        This is a landing page of <strong>Wastify</strong>, a platform , where you with your friends can explore a differend opportunities of helping the world become a better place! You can set your profile picture and bio information in "My Profile". <strong>Explore</strong> new horizonts with the Explore page, where you can se the latests posts near you. You can also message people in this service, by choosing "Messenger" in the menu. <br/> We hope you will enjoy Wastify!
      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: "InfoBox",
  data(){
    return{
      isOn: true
    }
  },
  methods: {
    hideInfo(){
      this.isOn = false
    }
  },
}
</script>
<style>

</style>
