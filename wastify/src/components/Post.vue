<template>
  <div class="post">
    <div class="box">
      <div class="topContainer">
        <img src="../assets/trash.jpg" alt class="topImage">
      </div>

      <div class="bottomContainer">
        <div class="rightBottomContainer">
          <h3>Title</h3>
          <p>This is my awesome description of the problem. Right now there are no problems because the website is not done yet</p>
        </div>
      </div>
      <div class="imageDiv">
        <img src="../assets/profile_picture.jpg" alt class>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Post",
  data() {
    return {};
  }
};
</script>

<style>
.post {
}
.box {
  width: 500px;
  height: 400px;
  background-color: rgb(219, 255, 236);
  border-radius: 20px;
  border-style: solid;
  border-width: 1px;
  border-color: #53bc88;
  overflow: hidden;
}
.imageDiv {
  border-radius: 50%;
  height: 100px;
  width: 100px;
  border-color: white;
  border-width: 20px;
  margin-left: 30px;
  overflow: hidden;
  align-content: center;
  position: relative;
  bottom: 260px;
}

.imageDiv img {
  width: 200px;
  height: 110px;
  margin: -10px 0 0 -50px;
  border-width: 5px;
}
.bottomContainer {
  height: 200px;
  width: inherit;
  background-color: white;
  position: relative;
  bottom: 20px;
}
.topContainer {
  position: relative;
  background-color: red;
  height: 200px;
  top: 0px;
}
.topContainer img {
  -webkit-filter: blur(1px); /* Safari 6.0 - 9.0 */
  filter: blur(1px);
  -webkit-filter: brightness(80%);
  height: 100%;
  width: 100%;
}
.rightBottomContainer {
  position: relative;
  height: inherit;
  width: 270px;
  left: 130px;
  text-align: left;
}

.rightBottomContainer h3 {
  padding-left: 20px;
  color: black;
}
</style>
