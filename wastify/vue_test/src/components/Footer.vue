<template>
  <footer class="footer is-clearfix">
    <div class="content has-text-centered">
      <p>
        <strong>Wastify</strong> by
        Karol Wojtulewicz.
      </p>
    </div>
    <nav class="breadcrumb has-bullet-separator" aria-label="breadcrumbs">
  <ul>
    <li><a href="#"><p class="has-text-white">Github</p></a></li>
    <li><a href="#"><p class="has-text-white">LinkedIn</p></a></li>
    <li><a href="#"><p class="has-text-white">About <strong>Wastify</strong></p></a></li>
    
  </ul>
</nav>
  </footer>
</template>
<script>
import "bulma/css/bulma.css";
export default {
  name: "Footer",
  data() {
    return {};
  }
};
</script>

<style>
.footer {
  position: relative;
  margin-top: 5rem;
  background-color: green;
  color:white;
  bottom: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
