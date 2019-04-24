<template>
  <div>
    <div class="box new-post is-rounded">
      
      <textarea class="textarea" v-model="description" style="margin-bottom:0.5rem; min-width:35rem;" placeholder="What do you want to do?"></textarea>
      <ul>

        <li>
          <div class="dropdown is-hoverable">
          <div class="dropdown-trigger">
            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
              <span>Event type</span>
              <span class="icon is-small">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a href="#" class="dropdown-item" @click="selectEventType(0)">
                Trash pickup
              </a>
              <a class="dropdown-item" @click="selectEventType(1)"> 
                Sale
              </a>
            </div>
          </div>
        </div>
        </li>
        <li><i class="fas fa-images btn-image" /></li>
        <li><i class="fas fa-location-arrow btn-image"/></li>
        <li class="submit"><a class="button is-primary is-inverted is-outlined">Submit Post</a></li>
        
      </ul>
      
    </div>      

    <!-- Old new post -->
    <form @submit.prevent="createPost" class="card-panel">
      <h2 class="center deep-purple-text"> Create new product</h2>
      <div class="field">
        <label for="name">Name:</label>
        <input type="text" name="name" v-model="name"
        placeholder="Write the name of the product">
      </div>

      <div class="field">
        <label for="description" class="label">Description</label>
        <div class="control">
          <input
            type="text"
            name="description"
            v-model="description"
            class="input"
            placeholder="Write the description of the product"
          >
        </div>
      </div>
      <div class="field">
        <label for="price" class="label">Price</label>
        <div class="control">
          <input
            type="number"
            name="price"
            v-model="price"
            class="input"
            placeholder="Write the price of the product"
          >
        </div>
      </div>
      <div class="field">
        <label for="qty" class="label">Quantity</label>
        <div class="control">
          <input
            type="number"
            name="qty"
            v-model="qty"
            class="input"
            placeholder="Write the quantity of the product"
          >
        </div>
      </div>
      <p class="red-text center" v-if="feedback">{{feedback}}</p>
      <div class="field">
        <button class="btn deep-purple">Post</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: "NewPost",
  data(){
    return{
      name: null,
      description: null,
      price: null,
      qty: null,
      feedback: null,
      eventType: null,
      location: null,
      imageSrc: null

    }
  },
  methods:{
    selectEventType(typeNumber){

    },
    createPost(){
      if(this.name && this.description && this.price && this.qty){
        console.log("New Post1!")

        // 'http://localhost:5001/product'

        const Url = 'http://localhost:5001/product'
        // specify the object to post
        const post = {
          "name": this.name,
          "description": this.description,
          "price": this.price,
          "qty": this.qty
        }

        // make the post request
        // This is how you do it:
        axios.post(Url,post)
        .then(response => console.log(response))
        .catch(error => console.log(error))

        if(feedback){
          feedback = null
        }
      }else{
        console.log("New Post!")
        this.feedback = "You need to fill in all of the fields"
      }
    }
  }
}
</script>

<style>
.new-post{
  background-color: green;
  padding: 5px;
  padding-bottom: 40px;
}
li {
  float: left;
}

li .submit {
  float: right;
}

li .btn-image{
  margin: 10px;
  color: white;
}
</style>
