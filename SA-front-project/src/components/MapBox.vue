<template>
  <div>
    <div id='map'></div>

    <el-drawer
      title="研究区详情"
      custom-class="libraryDrawer"
      :visible.sync="drawer">
      
      <div id="libraryDescription" v-for="lib in selectedLibrary" :key="lib.source">
        <span class="libraryItem">模型：</span> {{lib.originModel}}<br>
        <span class="libraryItem">研究区简介：</span>{{lib.researchArea}}<br>
        <span class="libraryItem">评估参数：</span>{{lib.modelParams.join("、")}}<br>
        <span class="libraryItem">变化幅度：</span>{{lib.modelParamsRange}}<br>
        <span class="libraryItem">SA方法：</span>{{lib.saMethods}}<br>
        <span class="libraryItem">目标函数：</span>{{lib.objectiveFun}}<br>
        <span class="libraryItem">运行次数：</span>{{lib.simTimes}}<br>
        <span class="libraryItem">SA结果：</span><br>
        <span v-for="(img,index) in lib.saResults" :key="index">
          <img class="saResultImage" @click="handleImagePreview(img)" :src="'data:'+img.contentType+';base64,'+img.content.data" alt="">
        </span><br>
        
        <span class="libraryItem">文献来源：</span><a :href="lib.sourceUrl" target="_blank">{{lib.source}}</a><br>
        
        <!-- 应用到本次项目中 -->
        <div id="reuseParamsBtn">
          <el-button @click="reuseThisArticle(lib.modelParams)" size="medium" plain> 快速应用 </el-button>
        </div>
        

        <hr>
      </div>
    </el-drawer>

    <!-- 查看大图 -->
    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';
export default {
  name:"MapBox",
  data(){
    return {
      drawer:false,
      selectedLibrary:[],

      dialogVisible:false,
      dialogImageUrl:''
    }
  },
  methods:{
    // 子组件的初始化依赖于父组件的请求结果，所以只能在父组件请求成功时才可以初始化获得数据，而不可以直接写在mounted中
    initByModelName(modelName){
      console.log(modelName)
      this.$axios.get(
        "/SA-back-project/experienceLibrary/allLibraryByModel",{params:{model:modelName}}
      ).then(response=>{
        var data = response.data
        console.log(data)
        if(data.code == 0){
          this.library = data.data
          this.initMapBox()
        }
      }).catch(err=>{
        console.log(err)
      })
    },

    initMapBox(){
      mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94bWF4IiwiYSI6ImNqbnY4MHM3azA2ZmkzdnBnMThvNzRoZ28ifQ.IffqPZGkhcdPjnZ2dmSO6w';

      let map = new mapboxgl.Map({
          container: 'map',
          style: 'mapbox://styles/mapbox/satellite-v9',
          center: [105,34],
          zoom: 3,
      });
      let polygonStyle ={
        "fill-color":'#3DB2FF',
        "fill-opacity":0.5
      }

      let that = this

      map.on('load', () => {
        let geoJson = null
        for (let i = 0; i < that.library.length; i++) {
          const lib = that.library[i];
          if(!geoJson){
            geoJson = JSON.parse(lib.geoJson)
          }else{
            geoJson.features.push(...JSON.parse(lib.geoJson).features)
          }
        }
        
        map.addSource('geojson',{type:"geojson", data: geoJson==null?{}:geoJson })

        map.addLayer({
          id:'polygon',
          type:'fill',
          source:'geojson',
          layout:{},
          paint:polygonStyle,
          // filter:[]
        })
      });
      map.on('click','polygon',(e)=>{

        that.drawer = true
        that.selectedLibrary = []

        for (let i = 0; i < e.features.length; i++) {
          let name = e.features[i].properties.name
          for (let j = 0; j < that.library.length; j++) {
            const lib = that.library[j];
            if(lib.geoJsonName == name)  that.selectedLibrary.push(lib)
          }
        }

        // 尝试通过设置样式无效，所以利用JS为研究区详情抽屉设置滚动样式
        let drawer = document.getElementsByClassName('libraryDrawer')[0]
        drawer.style.overflowY = 'scroll'
      })
    },
    handleImagePreview(img) {
      this.dialogImageUrl = 'data:'+img.contentType+';base64,'+img.content.data;
      this.dialogVisible = true;
    },

    // 重用某篇文章的参数
    reuseThisArticle(modelParams){
      this.$confirm("此操作会将这篇文献中的评估参数应用到本次项目中，是否继续？","提示",{
        confirmButtonText:"确定",
        cancelButtonText:"取消",
        type:"warning"
      }).then(()=>{
        this.$emit("updataParamsFromArticle", modelParams)
        
      }).catch(()=>{

      })
    }
  },
  mounted(){
    

  }
}
</script>

<style scoped>
  @import url("https://api.mapbox.com/mapbox-gl-js/v2.0.0/mapbox-gl.css");
  #map{
    height: 600px;
    width: 100%;
  }
  #libraryDescription{
    padding: 0 20px;
  }
  .libraryItem{
    font-weight: bold;
  }
  .saResultImage{
    width: 48%;
    margin: 1%;
  }
  #reuseParamsBtn{
    text-align: right;
  }
</style>