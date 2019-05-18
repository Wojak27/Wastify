<template>
  <article class="media">
    <div class="media-content">
      <div class="content">
        <p>
          <strong>{{comment.authorEmail}}</strong> <small>{{comment.timestamp}}</small>
          <br> {{comment.description}}
        </p>
      </div>
  
    </div>
  </article>
</template>

<script>
  export default {
    name: "CommentBox",
    props:['comment'],
    data() {
      return {
  
      }
    }
  }
</script>