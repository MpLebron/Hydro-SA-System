<template>
  <div class="header">
    <!-- <img src="./static/images/OpenGMS.png" @click="openOpenGMSHome" class="OpenGMS-image" /> -->
    <img src="../assets/OpenGMS.png" @click="openOpenGMSHome" class="OpenGMS-image" />
  </div>
</template>

<script>
export default {
  name:'Header',
  methods:{
    openOpenGMSHome() {
      window.location.href = "http://geomodeling.njnu.edu.cn/home"
    },
  },
  data(){
    return{
      ogmsUrl:'./static/images/OpenGMS.png'
    }
  }
}
</script>

<style>
  .header{
    background-color: #000;
    text-align: center;
    height: 62px;
    margin-bottom: 40px;
  }
  
  .OpenGMS-image {
    float: left;
    margin: 8px 20px;
    height: 46px;
  }
  .OpenGMS-image:hover {
    cursor: pointer;
  }
</style>