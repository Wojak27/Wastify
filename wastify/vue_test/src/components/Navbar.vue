<template>
  <div class="navbar">
    <nav>
      <img src="../assets/logo.png" alt="Wastify" class="logo">
      <span>Wastify</span>
      <input
        type="text"
        name="search"
        id
        class="searchField"
        placeholder="What are you looking for?"
      >
      <i class="fas fa-heart"></i>
      <i class="fas fa-comment-dots"></i>
      <i class="fas fa-ellipsis-h"></i>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {};
  }
};
</script>

<style>
.navbar nav {
  padding: 0 0px;
  background-color: #53bc88;
  height: 50px;
  border-radius: 0px 0px 20px 20px;
  align-content: center;
  top: 0px;
  position: fixed;
  width: 100%;
  left: 0px;
  vertical-align: bottom;
  margin: 0 auto;
  padding: 10;
  display: -moz-inline-box;
}
.navbar span {
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  font-size: 30px;
  left: 20px;
  color: #fff;
}

input.searchField {
  width: 500px;
  border-radius: 8px;
  height: 25px;
  align-content: center;
  background-color: white;
  font-size: 15px;
}

.logo {
  height: 40px;
  left: 0px;
  align-self: baseline;
}
</style>
