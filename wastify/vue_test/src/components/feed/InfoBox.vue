<template>
  <div>
    <article class="message is-primary" v-if="isOn">
      <div class="message-header">
        Info
        <button class="delete" @click="hideInfo"></button>
      </div>
      <div class="message-body">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque risus mi, tempus quis placerat ut, porta nec nulla. Vestibulum rhoncus ac ex sit amet fringilla. Nullam gravida purus diam, et dictum felis venenatis efficitur. Aenean ac eleifend lacus, in mollis lectus. Donec sodales, arcu et sollicitudin porttitor, tortor urna tempor ligula, id porttitor mi magna a neque. Donec dui urna, vehicula et sem eget, facilisis sodales sem.
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
