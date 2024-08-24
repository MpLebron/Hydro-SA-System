<template>
  <div>
    <Header />
    <div id="mapAndTableContainer">
      
      <el-page-header id="pageHeader" @back="goBack" content="知识库浏览页面"></el-page-header>

      <!-- 贡献知识库 -->
      <el-button id="contributeEnter" type="primary" plain @click="turnToContributePage">贡献知识条目</el-button>
      <!-- 地图 -->
      <div class="sonContainer">
        <h2 class="title">MAP</h2> 
        <div id="browseMap"></div>
        <el-drawer
          title="研究区详情"
          custom-class="libraryDrawer"
          :visible.sync="drawer">
          
          <div id="libraryDescription" v-for="lib in selectedLibrary" :key="lib.id">
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
            
            <hr>
          </div>
        </el-drawer>
        <!-- 查看大图 -->
        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
      </div>
      <!-- 列表 -->
      <div class="sonContainer">
        <h2 class="title">TABLE</h2> 
        <template>
          <el-table
            id="browseTable"
            :data="library"
            height="600"
            border
            style="width: 100%">
            <el-table-column
              type="index"
              width="30">
            </el-table-column>
            <el-table-column
              prop="originModel"
              label="模型"
              width="100"
              :filters="modelsName"
              :filter-method="filterByModel">
            </el-table-column>
            <el-table-column
              prop="researchArea"
              label="研究区简介">
            </el-table-column>
            <el-table-column
              prop="modelParams"
              label="评估参数"
              width="200">
              <template slot-scope="scope">
                {{scope.row.modelParams.join("、")}}
              </template>
            </el-table-column>
            <el-table-column
              prop="modelParamsRange"
              label="变化幅度"
              width="100">
            </el-table-column>
            <el-table-column
              prop="saMethods"
              label="SA方法"
              width="100">
            </el-table-column>
            <el-table-column
              prop="objectiveFun"
              label="目标函数"
              width="100">
            </el-table-column>
            <el-table-column
              prop="simTimes"
              label="运行次数"
              width="100">
            </el-table-column>
            <el-table-column
              prop="saResults"
              label="SA结果"
              width="100">
              <template slot-scope="scope">
                <span v-for="img in scope.row.saResults" :key="img.name">
                  <img class="saResultImageTable"  @click="handleImagePreview(img)" :src="'data:'+img.contentType+';base64,'+img.content.data" alt="">
                </span>
              </template>
            </el-table-column>
            <el-table-column
              prop="source"
              label="文献来源"
              width="150">
            </el-table-column>
          </el-table>
        </template>
      </div>

      
    </div>
    
    <Footer />
  </div>
</template>

<script>
import Header from '../../components/Header'
import Footer from '../../components/Footer'
import mapboxgl from 'mapbox-gl';
export default {
  components:{Header, Footer},
  data(){
    return{
      library:[],
      modelsName:[],
      
      drawer:false,
      selectedLibrary:[],

      dialogVisible:false,
      dialogImageUrl:''
    }
  },
  methods:{
    goBack(){
      this.$router.back()
    },

    initMapBox(){
      mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94bWF4IiwiYSI6ImNqbnY4MHM3azA2ZmkzdnBnMThvNzRoZ28ifQ.IffqPZGkhcdPjnZ2dmSO6w';

      let map = new mapboxgl.Map({
          container: 'browseMap',
          style: 'mapbox://styles/mapbox/satellite-v9',
          center: [105,34],
          zoom: 3,
      });
      let polygonStyle ={
        "fill-color":'#3DB2FF',
        "fill-opacity":0.5,
        "fill-outline-color":"#0f0"
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
    initModelsName(){
      for (let i = 0; i < this.library.length; i++) {
        const lib = this.library[i];
        this.modelsName.push({
          text:lib.originModel,
          value:lib.originModel
        })
      }
      this.modelsName = this.modelsName.filter((item, index, arr)=>{
        return arr.findIndex(el=>el.value==item.value) === index
      })
    },
    filterByModel(value, row, column){
      const property = column["property"]
      return row[property] === value
    },

    handleImagePreview(img) {
      this.dialogImageUrl = 'data:'+img.contentType+';base64,'+img.content.data;
      this.dialogVisible = true;
    },

    turnToContributePage(){
      this.$router.push({name:'LibraryContributePage'})
    }
  },
  mounted(){
    
    this.$axios.get(
      "/SA-back-project/experienceLibrary/allLibrary"
    ).then(response=>{
      var data = response.data
      if(data.code == 0){
        this.library = data.data
        this.initMapBox()
        this.initModelsName()
      }
    }).catch(err=>{
      console.log(err)
    })
  }

}
</script>

<style scoped>
  @import url("https://api.mapbox.com/mapbox-gl-js/v2.0.0/mapbox-gl.css");
  #pageHeader{
    margin: 20px 0;
  }
  #contributeEnter{
    float: right;
  }
  #browseMap{
    height: 600px;
    width: 100%;
    box-shadow: 2px 4px 6px #aaa;
  }
  #browseTable{
    box-shadow: 2px 4px 6px #aaa;
  }
  #mapAndTableContainer{
    width: 80%;
    margin: auto;
  }
  .sonContainer{
    margin: 10px 0;
  }
  .title{
    text-align: center;
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

  .saResultImageTable{
    width: 100%;
  }

</style>