<template>
  <div>
    <Header/>
    <div id="mapAndFormContainer">

      <el-page-header id="pageHeader" @back="goBack" content="知识库贡献页面"></el-page-header>

      <el-row :gutter="20">
        <!-- 地图 -->
        <el-col id="mapContainer" :span="16">
          <div id="contributeMap"></div>
          <!-- 图层控制 -->
          <div id="layerControlContainer">
            <el-button type="text" id="layerControlBtn" icon="el-icon-s-home"
              circle 
              v-show="layerControlEnter" 
              @click="layerControl=!layerControl; layerControlEnter=!layerControlEnter; layerControlTitle=!layerControlTitle">
            </el-button>

            <el-button type="text" id="layerControlTitle" 
              v-show="layerControlTitle"
              @click="layerControl=!layerControl; layerControlEnter=!layerControlEnter; layerControlTitle=!layerControlTitle">
              图层管理
            </el-button>
            <el-collapse-transition>
              <div id="layerControl" v-show="layerControl">
                <div id="basinTitle">全球流域</div>
                <el-radio-group v-model="basinData" @change="changeBasinData">
                  <el-radio :label="4">level 04</el-radio><br>
                  <el-radio :label="5">level 05</el-radio><br>
                  <el-radio :label="6">level 06</el-radio><br>
                  <el-radio :label="7">level 07</el-radio>
                </el-radio-group><br>
                <hr>
                <el-checkbox v-model="provincalData" @change="changeProvinceData">省级边界</el-checkbox>
              </div>
            </el-collapse-transition>
          </div>
        </el-col>
        
        <!-- 表单 -->
        <el-col :span="8">
          <el-form label-width="100px" :model="newLibrary" :rules="formRules" ref="ruleForm">
            <el-form-item label="模型" prop="model">
              <el-select v-model="newLibrary.originModel" size="medium" class="modelSelectStyle" placeholder="请选择原始模型" @change="changeOriginModel">
                <div v-for="model in allOriginModel" :key="model">
                  <el-option :label="model" :value="model"></el-option>
                </div>
              </el-select>
              <el-select v-model="newLibrary.model" size="medium" class="modelSelectStyle" placeholder="请选择计算模型" @change="changeComputableModel">
                <div v-for="model in allModel" :key="model">
                  <el-option :label="model" :value="model"></el-option>
                </div>
              </el-select>
            </el-form-item>
            <el-form-item label="研究区简介" prop="researchArea">
              <el-input type="textarea" size="medium" v-model="newLibrary.researchArea"></el-input>
            </el-form-item>
            <el-form-item label="评估参数" prop="modelParams">
              <!-- 可多选，不可新建 -->
              <el-select
                v-model="newLibrary.modelParams"
                size="medium"
                class="paramSelectStyle"
                multiple
                filterable
                collapse-tags
                clearable 
                default-first-option
                placeholder="请选择评估参数">
                <!-- 分组展示参数  -->
                <el-option-group
                  v-for="group in modelParamsGroup"
                  :key="group.label"
                  :label="group.label">
                  <el-option
                    v-for="item in group.params"
                    :key="item"
                    :label="item"
                    :value="item">
                  </el-option>
                </el-option-group>
              </el-select>
            </el-form-item>
            <el-form-item label="变化幅度">
              <el-input v-model="newLibrary.modelParamsRange" size="medium"></el-input>
            </el-form-item>
            <el-form-item label="SA方法" prop="saMethods">
              <el-input v-model="newLibrary.saMethods" size="medium"></el-input>
            </el-form-item>
            <el-form-item label="目标函数">
              <el-input v-model="newLibrary.objectiveFun" size="medium"></el-input>
            </el-form-item>
            <el-form-item label="运行次数">
              <el-input v-model="newLibrary.simTimes" size="medium"></el-input>
            </el-form-item>
            <el-form-item label="SA结果">
              <el-upload
                action="#"
                list-type="text"
                accept="image/png, image/jpeg"
                :auto-upload="false"
                :file-list="saResultsFile"
                :on-change="selectResult">
                <el-button id="resultUploadBtn" size="small" icon="el-icon-upload" circle></el-button>
              </el-upload>
            </el-form-item>
            <el-form-item label="文献来源" prop="source">
              <el-input type="textarea" v-model="newLibrary.source" size="medium"></el-input>
              <el-input v-model="newLibrary.sourceUrl" size="medium" placeholder="文献链接"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button id="submitBtn" @click="submitLibrary" size="medium" plain>提交</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
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
      modelList:[],
      
      layerControlEnter:true,
      layerControlTitle:false,
      layerControl:false,

      // 矢量瓦片数据
      map:{},
      basinId:"basin_global_lev04",
      basinData:4,
      provincalData:false,

      formRules:{
        model:[{required:true, message:'请选择原始模型和计算模型', trigger:'change'}],
        researchArea:[{required:true, message:'请输入研究区简介', trigger:'change'}],
        modelParams:[{required:true, message:'请选择评估参数', trigger:'change'}],
        saMethods:[{required:true, message:'请输入所应用的SA方法', trigger:'change'}],
        source:[{required:true, message:'请输入文献来源和链接', trigger:'change'}]
      },
      allOriginModel:[],
      allModel:[],
      modelParamsGroup:[],

      saResultsFile:[],
      selectedFeature:null,
      newLibrary:{
        saved:false,
        originModel:'',
        model:'',
        researchArea:'',
        modelParams:[],
        modelParamsRange:'',
        saMethods:'',
        objectiveFun:'',
        simTimes:'',
        saResults:[],
        source:'',
        sourceUrl:'',
        geoJson:{},
        geoJsonName:''
      }
    }
  },
  methods:{
    goBack(){
      if(!this.newLibrary.saved){
        this.$confirm('检测到未保存的内容，是否在离开页面前保存修改？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '保存',
          cancelButtonText: '放弃修改'
        }).then(() => {
          this.submitLibrary()
          if(this.newLibrary.saved) this.$router.back()
        }).catch(action => {
          if(action === 'cancel') this.$router.back()
        });
      }else{
        this.$router.back()
      }
    },

    initMapBox(){
      mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94bWF4IiwiYSI6ImNqbnY4MHM3azA2ZmkzdnBnMThvNzRoZ28ifQ.IffqPZGkhcdPjnZ2dmSO6w';

      this.map = new mapboxgl.Map({
          container: 'contributeMap',
          style: 'mapbox://styles/mapbox/satellite-v9',
          center: [105,34],
          zoom: 3,
      });
      let polygonStyle ={
        "fill-color":'#3DB2FF',
        "fill-opacity":0.3,
        "fill-outline-color":"#0f0"
      }
      var that = this
      this.map.on("load", function(){

        // 全球省级边界数据
        that.map.addSource("gadm_province",{
          "type": "vector",
          "scheme":"tms",
          "tiles": ["http://172.21.212.43:8080/geoserver/gwc/service/tms/1.0.0/zhangshuo%3Agadm_province@EPSG%3A900913@pbf/{z}/{x}/{y}.pbf"],
          "minzoom": 1,
          "maxzoom": 14
        })

        // 4级全球流域数据
        that.map.addSource(that.basinId,{
          "type": "vector",
          "scheme":"tms",
          "tiles": ["http://172.21.212.43:8080/geoserver/gwc/service/tms/1.0.0/zhangshuo%3Abasin_global_lev04@EPSG%3A900913@pbf/{z}/{x}/{y}.pbf"],
          "minzoom": 1,
          "maxzoom": 14
        })
        that.map.addLayer({
          "id": that.basinId,
          "type": "fill",
          "source": that.basinId,
          "source-layer": that.basinId,
          "paint": polygonStyle
        });

      })

      this.map.on('click',that.basinId,(e)=>{
        let name = e.features[0].id
        that.map.setPaintProperty(that.basinId,'fill-opacity',[
            'match',//匹配模式
            ['get','OBJECTID'],//匹配的属性值名称，id，可以从feature的属性得到
            name, //要匹配的值
            0.8,
            0.3 
        ])
        that.selectedFeature = e.features[0]
      })

    },
    initModelInfo(){
      for (let i = 0; i < this.modelList.length; i++) {
        const model = this.modelList[i];
        this.allOriginModel.push(model.originModel)
      }
      this.allOriginModel = this.allOriginModel.filter((item,index,arr)=>{
        return arr.indexOf(item) === index
      })
    },

    // 切换原始模型、计算模型
    changeOriginModel(val){
      this.allModel = []
      this.newLibrary.model = ''
      for (let i = 0; i < this.modelList.length; i++) {
        const model = this.modelList[i];
        if(model.originModel == val)  this.allModel.push(model.name)
      }
    },
    changeComputableModel(val){
      this.modelParamsGroup = []
      for (let i = 0; i < this.modelList.length; i++) {
        const model = this.modelList[i];
        if(model.name == val){
          // 从计算模型的state中抽取出模型参数
          let states = model.mdlJson.mdl.states
          for (let j = 0; j < states.length; j++) {
            const state = states[j];
            if(state.type == "group"){
              let group = {
                label:state.name,
                params:state.event.map(item=>item.eventName)
              }
              this.modelParamsGroup.push(group)
            }
          }
          break
        }
      }
    },

    // 切换流域数据、省级边界数据
    changeBasinData(){
      let basinId = "basin_global_lev0" + this.basinData
      // 删除图层
      this.map.removeLayer(this.basinId)
      this.selectedFeature = null // 清空已选要素

      // 添加数据源，生成图层
      this.basinId = basinId
      if(!this.map.getSource(this.basinId)){
        this.map.addSource(this.basinId,{
          "type": "vector",
          "scheme":"tms",
          "tiles": ["http://172.21.212.43:8080/geoserver/gwc/service/tms/1.0.0/zhangshuo%3A"+this.basinId+"@EPSG%3A900913@pbf/{z}/{x}/{y}.pbf"],
          "minzoom": 1,
          "maxzoom": 14
        })
      } 
      let polygonStyle ={
        "fill-color":'#3DB2FF',
        "fill-opacity":0.3,
        "fill-outline-color":"#0f0"
      }
      this.map.addLayer({
        "id": this.basinId,
        "type": "fill",
        "source": this.basinId,
        "source-layer": this.basinId,
        "paint": polygonStyle
      });
      if(this.provincalData){
        this.map.moveLayer(this.basinId, "gadm_province")
      }
      
      // 绑定点击事件
      var that = this
      this.map.on('click',that.basinId,(e)=>{
        let name = e.features[0].id
        that.map.setPaintProperty(that.basinId,'fill-opacity',[
            'match',//匹配模式
            ['get','OBJECTID'],//匹配的属性值名称，id，可以从feature的属性得到
            name, //要匹配的值
            0.8,
            0.3
        ])
        that.selectedFeature = e.features[0]
      })
    },
    changeProvinceData(){
      if(this.provincalData){
        let provincePolygonStyle ={
          "fill-color":'rgba(0, 0, 0, 0)',
          "fill-outline-color":"#f00"
        }
        this.map.addLayer({
          "id": "gadm_province",
          "type": "fill",
          "source": "gadm_province",
          "source-layer": "gadm_province",
          "paint": provincePolygonStyle
        });
      }else{
        this.map.removeLayer("gadm_province")
      }

      
    },

    selectResult(file, fileList){
      
      // 判断有没有重名文件  而且file-list绑定的变量无法自动更新，只能用于展示
      let index = fileList.findIndex(f => file.name === f.name)
      if(index == fileList.length-1){
        this.saResultsFile = fileList
      }else{ 
        this.saResultsFile = fileList.splice(0,fileList.length-1)
      }
      
    },

    submitLibrary(){
      this.$refs["ruleForm"].validate((valid) => {
        if (valid) {
          console.log(this.newLibrary)
          // 判断是否选择了流域
          if(this.selectedFeature != null){
            this.convertToGeoJson()

            let formData = new FormData()
            // formdata的value只能接收File和String两种类型
            formData.append("library", JSON.stringify(this.newLibrary))
            let files = this.getFileList()
            for (let i = 0; i < files.length; i++) {
              const f = files[i];
              formData.append("files", f)
            }
            let that = this
            this.$axios({
              method:"post",
              url:'/SA-back-project/experienceLibrary/contribute',
              data:formData,
              headers:{
                'Content-Type':'multipart/form-data'
              }
            }).then(function(response){
              var data = response.data
              if(data.code == 0){
                that.newLibrary.saved = true
              }
              that.$notify({
                title: '上传成功',
                type:"success",
                message:"感谢您的支持!"
              })
            }).catch(function(err){
              console.log(err)
            })

          }else{
            this.$message({
              type:"warning",
              message:"请选择文献中的研究区域！"
            })
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },

    // 生成选中流域的GeoJson
    convertToGeoJson(){
      let name = "lev0" + this.basinData + "-" + this.selectedFeature.id
      let coordinates = this.selectedFeature.geometry.coordinates
      let geoJson = {
        "type": "FeatureCollection",
        "name": name,
        "crs": {
          "type": "name",
          "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
          }
        },
        "features": [
          {
            "type": "Feature",
            "properties": {
              "name": name
            },
            "geometry": {
              "type": "MultiPolygon",
              "coordinates":[coordinates]
            }
          }
        ]
      }
      this.newLibrary.geoJsonName = name
      this.newLibrary.geoJson = JSON.stringify(geoJson) 
    },
    // 将结果文件提取到newlibrary中
    getFileList(){
      let results = this.saResultsFile.map(el=>el.raw)
      return results
    }
  },
  mounted(){
    this.$axios.get(
      '/SA-back-project/computableModel/allModel'
    ).then(response=>{
      var data = response.data
      if(data.code == 0){
        this.initMapBox()
        this.modelList = data.data
        this.initModelInfo()
      }
    }).catch(err=>{
      console.log(err)
    })
  }
}
</script>

<style>
@import url("https://api.mapbox.com/mapbox-gl-js/v2.0.0/mapbox-gl.css");
#pageHeader{
  margin: 20px 0;
}
#mapAndFormContainer{
  width: 80%;
  margin: auto;
}
#mapContainer{
  position: relative;
}
#contributeMap{
  float: left;
  width: 100%;
  height: 600px;
}
#layerControlContainer{
  position:absolute;
  float: left;
  margin: 10px;
}
#layerControlBtn{
  background-color: aliceblue;
  padding: 5px;
  font-size: 20px;
}
#layerControlTitle{
  width: 110px;
  text-align: center;
  background-color: black;
  border-radius: unset;
  color: white;
  margin: 0;
  padding: 10px 0;
}
#layerControl{
  width: 90px;
  background-color: rgb(255 255 255 / 80%);
  padding: 10px;
}
#basinTitle{
  font-size: 14px;
  font-weight: bold;
  margin: 5px 0;
}
.modelSelectStyle{
  width: 49%;
}
.paramSelectStyle{
  width: 100%;
}

#resultUploadBtn{
  padding: 5px;
  font-size: 20px;
}
.el-upload-list{
  display: flex;
  flex-wrap: wrap;
}
.el-upload-list__item {
  width: 50%;
}
.el-upload-list__item:first-child{
  margin-top: 5px;
}
#submitBtn{
  float: right;
}
</style>