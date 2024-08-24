<template>
  <div>
    <Header />
    <div class="saContainer">
      <el-page-header id="pageHeader" @back="goBack" :content="SA_Project.name+' | '+SA_Project.modelName"></el-page-header>

      <!-- <h2>{{SA_Project.modelName}}</h2> -->
      <el-divider></el-divider>
      
      <el-steps :active="activeStep" simple style="margin:10px 0;"> 
        <el-step title="模拟准备" icon="el-icon-s-tools" @click.native="turnPreparation"></el-step>
        <el-step title="模拟过程" icon="el-icon-menu" @click.native="turnProcess"></el-step>
        <el-step title="模拟结果" icon="el-icon-s-data" @click.native="turnResult"></el-step>
        <!-- <el-step title="单次模拟" icon="el-icon-s-operation" @click.native="turnSingleRun"></el-step> -->
      </el-steps>
      
      <!-- 模拟准备 -->
      <el-tabs tab-position="left" type="border-card" v-show="preparationStep">
        <el-tab-pane label="模拟探索">
          <MapBox ref="mapbox"
                  @updataParamsFromArticle="updataParamsFromArticle"></MapBox>
        </el-tab-pane>
        <el-tab-pane label="配置数据">
          <el-collapse v-model="expandDataStates">
            <template v-for="(state,index) in SA_Project.states"  >
              <el-collapse-item  :name="index" :key="index"  v-if="state.type=='basic' && state.name!='Observation' && state.name!='Result'" >
                <template slot="title">
                  <span style="margin: auto;font-size: 16px;">{{state.name+': '+state.desc}}</span>
                </template>
                <DataState :state="state"
                          @updateDataState="updateDataState" />
              </el-collapse-item>
            </template>
          </el-collapse>
          <div class="observationSwitch">
            <el-switch
              v-model="ObservationSwitch"
              @change="changeObservationSwitch"
              active-text="Observation"
              inactive-text="No Observation">
            </el-switch>
          </div>
          <el-collapse v-model="expandObsStates" v-if="ObservationSwitch">
            <template v-for="(state,index) in SA_Project.states"  >
              <el-collapse-item  :name="index" :key="index"  v-if="state.name=='Observation'" >
                <template slot="title">
                  <span style="margin: auto;font-size: 16px;">{{state.name+': '+state.desc}}</span>
                </template>
                <DataState :state="state"
                          @updateDataState="updateDataState" />
              </el-collapse-item>
            </template>
          </el-collapse>
          
          <!-- <template v-for="(state,index) in SA_Project.states" >
            <div :key="index">
              <DataState :state="state" />
            </div>
          </template> -->
        </el-tab-pane>
        <el-tab-pane label="选择参数">
          <template v-for="(state,index) in SA_Project.paramStates">
            <div :key="index">
              <ParamState :ref="'paramState'+index"
                          :state="state"
                          @updateParamState="updateParamState" />
            </div>
          </template>
        </el-tab-pane>
        <el-tab-pane label="设置条件">
          <SimSetting :simSetting="simSetting"
                      :paramsSum="paramsSum"
                      :ObservationSwitch="ObservationSwitch" />
        </el-tab-pane>
      </el-tabs>

      <!-- 模拟过程 -->
      <el-card v-show="processStep">
        <ProcessStep ref="processStep" 
                    :SA_Project="SA_Project"  
                    :paramsName="paramsName" 
                    :paramStates="SA_Project.paramStates"
                    :simSetting="simSetting"
                    :paramsSum="paramsSum"
                    :ObservationSwitch="ObservationSwitch"
                    @updateParamsSet="updateParamsSet"
                    @updateScoreSA="updateScoreSA"
                    @updateSimResult="updateSimResult"
                    @updateTotalResult="updateTotalResult"
                    @updateLabels="updateLabels"
                    @updateScoreObj="updateScoreObj"  />
      </el-card >

      <!-- 模拟结果 -->
      <!-- <el-card v-show="resultStep">
        <ScoreSA  ref="scoreSA"
                  :simSetting="simSetting"
                  :scoreSA="scoreSA" />
      </el-card> -->
      <el-tabs tab-position="left" type="border-card" v-show="resultStep" @tab-click="clickResultTabs">
        <el-tab-pane label="模拟结果">
          <SimResult  ref="simResult"
                      :simSetting="simSetting"
                      :simResult="simResult"
                      :labels="labels"
                      :scoreObj="scoreObj" />
        </el-tab-pane>
        <el-tab-pane label="定性SA结果">
          <ScoreSAQual ref="scoreSAQual"
                      :simSetting="simSetting" 
                      :paramsName="paramsName" 
                      :paramsSet="paramsSet"
                      :simResult="simResult" 
                      :totalResult="totalResult" />
        </el-tab-pane>
        <el-tab-pane label="定量SA结果">
          <ScoreSA  ref="scoreSA"
                    :simSetting="simSetting"
                    :scoreSA="scoreSA" />
        </el-tab-pane>
        <!-- <el-tab-pane label="参数率定结果">
          <ParamCaResult ref="paramCaResult" 
                        :paramsName="paramsName" 
                        :paramsSet="paramsSet"
                        :simSetting="simSetting"
                        :scoreObj="scoreObj"  />
        </el-tab-pane> -->
      </el-tabs>

      <!-- 单次模拟 暂未提供该功能 -->
      <el-tabs tab-position="left" type="border-card" v-show="singleRunStep">
        <el-tab-pane label="模拟准备">
          <el-collapse v-model="expandDataStatesSR">
            <template v-for="(state,index) in SA_Project.states"  >
              <el-collapse-item  :name="index" :key="index"  v-if="state.type=='basic' && state.name!='Observation' && state.name!='Result'" >
                <template slot="title">
                  <span style="margin: auto;font-size: 16px;">{{state.name+': '+state.desc}}</span>
                </template>
                <DataState :state="state"
                          @updateDataState="updateDataState" />
              </el-collapse-item>
            </template>
          </el-collapse>
          <el-collapse v-model="expandParamStatesSR">
            <template v-for="(state,index) in SA_Project.paramStates">
              <el-collapse-item  :name="index" :key="index" >
                <template slot="title">
                  <span style="margin: auto;font-size: 16px;">{{state.name+': '+state.desc}}</span>
                </template>
                <ParamStateSR :ref="'paramStateSR'+index"
                            :state="state"
                            @updateParamState="updateParamState" />
              </el-collapse-item>
            </template>
          </el-collapse>
          <el-collapse v-model="expandResultStatesSR">
            <template v-for="(state,index) in SA_Project.states"  >
              <el-collapse-item  :name="index" :key="index"  v-if="state.name =='Result'" >
                <template slot="title">
                  <span style="margin: auto;font-size: 16px;">{{state.name+': '+state.desc}}</span>
                </template>
                <DataState :state="state"
                          @updateDataState="updateDataState" />
              </el-collapse-item>
            </template>
          </el-collapse>
          <div class="observationSwitch">
            <el-switch
              v-model="ObservationSwitch"
              @change="changeObservationSwitch"
              active-text="Observation"
              inactive-text="No Observation">
            </el-switch>
          </div>
          <el-collapse v-model="expandObsStates" v-if="ObservationSwitch">
            <template v-for="(state,index) in SA_Project.states"  >
              <el-collapse-item  :name="index" :key="index"  v-if="state.name=='Observation'" >
                <template slot="title">
                  <span style="margin: auto;font-size: 16px;">{{state.name+': '+state.desc}}</span>
                </template>
                <DataState :state="state"
                          @updateDataState="updateDataState" />
              </el-collapse-item>
            </template>
          </el-collapse>
          <div style="text-align:right">
            <el-button type="primary" round style="margin: 1% " 
                        @click="startSingleSimulation">
              开始运行
            </el-button>
          </div>
        </el-tab-pane>
        <el-tab-pane label="模拟结果">
          单词模拟结果 以及 评价指标得分
        </el-tab-pane>
        
      </el-tabs>


    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '../../components/Header'
import Footer from '../../components/Footer'
import MapBox from '../../components/MapBox'
import DataState from '../dataState/dataState'
import ParamState from '../paramState/ParamState'
import SimSetting from '../simSetting/SimSetting'
import ProcessStep from '../processStep/ProcessStep'
import ScoreSA from '../scoreSA/ScoreSA'
import ScoreSAQual from '../scoreSAQual/ScoreSAQual'
import ParamCaResult from '../paramCaResult/ParamCaReult'
import SimResult from '../simResult/SimResult'
import ParamStateSR from '../paramStateSR/ParamStateSR'

export default {
  components:{ Header, Footer, MapBox, DataState, ParamState, SimSetting, ProcessStep, ScoreSA, ScoreSAQual, ParamCaResult, SimResult, ParamStateSR },
  methods: {
    
    goBack(){
      this.$router.back()
    },

    turnPreparation(){
      this.activeStep = 0
      this.preparationStep = true
      this.processStep = false
      this.resultStep =false
      this.singleRunStep = false
    },
    turnProcess(){
      this.activeStep = 1
      this.preparationStep = false
      this.processStep = true
      this.resultStep =false
      this.singleRunStep = false
    },
    turnResult(){
      this.activeStep = 2
      this.preparationStep = false
      this.processStep = false
      this.resultStep =true 
      this.singleRunStep = false
      this.$refs.simResult.init()
    },
    turnSingleRun(){
      this.activeStep = 3
      this.preparationStep = false
      this.processStep = false
      this.resultStep =false
      this.singleRunStep = true
    },

    changeObservationSwitch(e){
      if(e){
        this.$message({
          showClose: true,
          message: '请注意设置观测数据对应的站点编号，系统无法统一检测。'
        });
      }
    },

    // 更新模型数据页面 暂时没用了
    updateDataState(state){
      for (let i = 0; i < this.SA_Project.states.length; i++) {
        var oldState = this.SA_Project.states[i];
        if(oldState.name == state.name){
          oldState = state
          break
        }
      }
    },
    // 更新模型参数页面
    updateParamState(state, params, selectedIDs){
      this.paramsName = []
      let i = 0
      for (; i < this.SA_Project.paramStates.length; i++) {
        var oldState = this.SA_Project.paramStates[i];
        if(oldState.name == state.name){
          oldState.selectedParams = params
        }
        // 汇总参数名称
        for (let j = 0; j < oldState.selectedParams.length; j++) {
          var param = oldState.selectedParams[j];
          this.paramsName.push(param.name)
        }
        break
      }
      // 计算参数总数
      this.paramsSum = this.paramsName.length
      // 因为有两个地方都用到了参数State，所以要更新另一个子组件的变量
      this.$refs["paramState"+i][0].updateFromAnother(params, selectedIDs)
      this.$refs["paramStateSR"+i][0].updateFromAnother(params, selectedIDs)
    },
    // 重用某篇文章的参数
    updataParamsFromArticle(modelParams){
      
      for (let i = 0; i < this.SA_Project.paramStates.length; i++) {
        // 挨个检查哪个state的哪几个在这篇文章里，并记录下来
        let selectedIDs=[],params=[]
        const state = this.SA_Project.paramStates[i];
        for (let j = 0; j < state.event.length; j++) {
          const event = state.event[j];
          for (let k = 0; k < modelParams.length; k++) {
            const param = modelParams[k];
            if(event.eventName === param){
              let p = {
                key: j,
                name: event.eventName,
                desc: event.eventDesc,
                table: event.table
              }
              params.push(p)
              selectedIDs.push(j)
            }
          }
        }
        if(selectedIDs.length){
          this.$refs["paramState"+i][0].updateFromAnother(params, selectedIDs)
          this.$refs["paramStateSR"+i][0].updateFromAnother(params, selectedIDs)
        }
      }
      
    },
    // 更新采样的参数组
    updateParamsSet(result){
      this.paramsSet = result
    },
    // 更新SA结果
    updateScoreSA(result){
      this.scoreSA = result
    },
    // 更新模拟结果
    updateSimResult(result){
      this.simResult = result
      // 更新SimResult子组件中的模拟数据
      this.$refs.simResult.loadData(result)
      // 更新SimResult子组件中的观测数据
      this.$refs.simResult.loadObsData()
    },
    // 更新total模拟结果
    updateTotalResult(result){
      this.totalResult = result
    },
    updateLabels(result){
      this.labels = result
    },
    updateScoreObj(result){
      this.scoreObj = result
      // 更新ParamCaResult子组件中的目标函数得分 
      // this.$refs.paramCaResult.loadObj()
      // SA整个运行完成，删除存储在数据容器的模拟结果

      // 先不删了，数据容器的这个接口老有问题 2022.02.23
      // this.clearSASimResult()
    },

    // 参数率定进行的N组模拟会对数据容器存储带来很大压力，所以模拟完需要将所有模拟结果进行清除
    clearSASimResult(){
      this.$axios.delete(
        "/SA-back-project/simulation/clear-sa-sim-result",{params:{pid:this.SA_Project.pid}}
      ).then(res => {
        console.log(res)
      })
    },
    
    clickResultTabs(tab){
      console.log(tab.label);
      if(tab.label == "定量SA结果"){
        this.$refs.scoreSA.init()
      }
    },
    
    sortByMu(score){
      var len = score.mu_star.length;
      var minIndex, temp;
      for(var i = 0; i < len - 1; i++) {
          minIndex = i;
          for(var j = i + 1; j < len; j++) {
              if(parseFloat(score.mu_star[j]) < parseFloat(score.mu_star[minIndex])) {     // 寻找最小的数
                  minIndex = j;                 // 将最小数的索引保存
              }
          }
          temp = score.mu_star[i];
          score.mu_star[i] = score.mu_star[minIndex];
          score.mu_star[minIndex] = temp;

          temp = score.params[i];
          score.params[i] = score.params[minIndex];
          score.params[minIndex] = temp;

          temp = score.sigma[i];
          score.sigma[i] = score.sigma[minIndex];
          score.sigma[minIndex] = temp;
      }
      return score;
    },

    startSingleSimulation(){
      // 检查数据state
      var states = this.SA_Project.states;
      for (var i = 0; i < states.length; i++) {
        var events = states[i].event;
        for (var j = 0; j < events.length; j++) {
          var event = events[j];
          if (event.eventType == "response" && event.optional == false) {
            // 输入数值
            if(event.children != undefined){
              for (var k = 0; k < event.children.length; k++) {
                var child = event.children[k];
                if (child.value == undefined || child.value.trim() == "") {
                  this.$message.error("Some input data are not set");
                  return;
                }
              }
            }
            // 输入数据
            else{
              if(event.url == undefined || event.url == ""){
                this.$message.error("Some input data are not set");
                return;
              }
            }
          }
        }
      }      
     

      // 合并参数state
      this.mergeState(this.SA_Project.paramStates,states)
      // 生成数值与参数文件
      this.createAndUploadParamFile(states)
      // 运行本次
      this.invoke(states, i)
    },
    // 将参数state插入到总states中
    mergeState(paramStates,states){
      // 遍历参数state
      for (var i = 0; i < paramStates.length; i++) {
        var state = paramStates[i];
        for (var j = 0; j < state.selectedParams.length; j++) {
          var param = state.selectedParams[j];
          // 遍历总states
          for (var k = 0; k < states.length; k++) {
            if(states[k].type == "group"){
              var events = states[k].event;
              var m = 0
              for (; m < events.length; m++) {
                if(param.name == events[m].eventName){
                  // 更新到event地children中
                  for (var n = 0; n < events[m].children.length; n++) {
                    var child = events[m].children[n];
                    if(child.eventName == "Operation")  this.$set(child,"value",param.table[0].changeType)
                    else if(child.eventName == "Value") this.$set(child,"value",param.value)
                  }
                  break
                }
              }
              if(m<events.length) break
            }
          }
        }
      }
    },
    // 生成数值与参数文件
    createAndUploadParamFile: async function(states){
      for (var i = 0; i < states.length; i++) {
        let events = states[i].event;
        let find = false;
        for (var j = 0; j < events.length; j++) {
          let event = events[j];
          if (event.eventType == "response" && event.children != undefined) {
            //拼接文件内容
            let content = "";
            let children = event.children;
            for (var k = 0; k < children.length; k++) {
              let child = children[k];
              if (child.value === undefined || (typeof(child.value)=='string' && child.value.trim() === '') ) {
                continue;
              }else {
                content += "<XDO name=\"" + child.eventName + "\" kernelType=\"" + child.eventType.toLowerCase() + "\" value=\"" + child.value + "\" /> ";
              }
            }
            if (content === "") {
              continue;
            }else {
              content = "<Dataset> " + content + " </Dataset>";
            }

            //生成文件
            let file = new File([content], event.eventName + '.xml', {
                type: 'text/plain',
            });
            //上传文件
            await this.uploadToDataContainer(file, event);
          }
        }
      }
    },
    uploadToDataContainer:async function(file, event) {
      var that = this

      let formData = new FormData();
      formData.append("datafile", file);
      // formData.append("datafile", configFile);
      formData.append("name", event.eventName);
      formData.append("userId", "1565916523@qq.com"); // 系统没有用户概念，暂时传到固定的用户名下
      formData.append("serverNode", "china");
      formData.append("origination", "SA_Project");

      await this.$axios.post(
        "/SA-back-project/dataManager/uploadMutiFiles",formData
      ).then(function(response){
        var data = response.data
        if (data.code == 0) {
          let file=data.data;
          file.suffix="xml";
          file.tag=event.eventName;

          let ipAndPort = file.ipAndPort
          that.$set(event, 'url', "http://" + ipAndPort + "/data/" + file.id);
          that.$set(event, 'tag', file.tag)
          that.$set(event, 'suffix', file.suffix)
        }
      }).catch(function(err){
        console.log(err)
      })
    },
    // 检查数据是否准备好
    checkReady(states){
      var prepared = true
      for (var i = 0; i < states.length; i++) {
        let events = states[i].event;
        for (var j = 0; j < events.length; j++) {
          //判断参数文件是否已经上传
          if (events[j].eventType == "response") {

            let children = events[j].children;
            if (children === undefined) {
              continue;
            }
            else {
              let hasFile = false;
              for (var k = 0; k < children.length; k++) {
                if (children[k].value != undefined && children[k].value.trim() != "") {
                  hasFile = true;
                  break;
                }
              }
              if (hasFile) {
                if (events[j].url == undefined) {
                  prepared = false;
                  break;
                }
              }
            }
          }
        }
        if (!prepared) {
            break;
        }
      }
      return prepared
    },
    invoke(states, index){
      var that = this
      var prepare = setInterval(()=>{
        // 检查数据有没有准备好
        var prepared = that.checkReady(states)
        
        // 准备好了，开始发送运行请求
        if(prepared){
          console.log(states)
          console.log("-------------YESYES----------------")
          clearInterval(prepare)

          let json = {
            oid: that.SA_Project.oid,
            pid: that.SA_Project.md5,
            projectId: that.SA_Project.pid,
            inputs: []
          };

          try {
            states.forEach(state => {
              let statename = state.name;
              state.event.forEach(el => {
                let event = el.eventName;
                let tag = el.tag;
                let url = el.url;
                let suffix = el.suffix;
                let templateId = el.externalId;
                if(templateId!=null) templateId=templateId.toLowerCase();
                let children = el.children;
                if (el.eventType == "response") {
                  if (el.optional) {
                    if (url === null || url === undefined) {

                    }else{
                      json.inputs.push({
                        statename,
                        event,
                        url,
                        tag,
                        suffix,
                        templateId,
                        children
                      });
                    }
                  }else{
                    if(url === null || url === undefined) {
                      this.$message.error("Some input data are not provided");
                      throw new Error("Some input data are not provided");
                    }
                    json.inputs.push({
                      statename,
                      event,
                      url,
                      tag,
                      suffix,
                      templateId,
                      children
                    });
                  }
                }
              });
            });
          } catch (e) {
            return;
          }

          that.$axios.post(
            "/SA-back-project/simulation/invoke", json
          ).then(function(response){
            var data = response.data
            if (data.code == -1) {
              that.$alert(data.msg, 'Error', {
                type: 'error',
                confirmButtonText: 'OK',
                callback: action => {}
              });
              return;
            }
            if (data.code == -2) {
              that.$alert(data.msg, 'Error', {
                type: 'error',
                confirmButtonText: 'OK',
                callback: action => {}
              });
              return;
            }

            if(data.code == 0){
              var task = data.data
              let interval = setInterval(async () => {
                await that.$axios.post(
                  "/SA-back-project/simulation/single-sim-result",
                  JSON.stringify(task),{headers: {"Content-Type": "application/json"}}
                ).then(function(response2){
                  var data2 = response2.data
                  if (data2.code === -1) {
                    clearInterval(interval);
                    that.$alert(data2.msg, 'Error', {
                      type: 'error',
                      confirmButtonText: 'OK',
                      callback: action => { }
                    });
                  }
                  if (data2.data.status === -1) {
                    clearInterval(interval);
                    that.$alert("Some error occured when the model running!", 'Error', {
                      type: 'error',
                      confirmButtonText: 'OK',
                      callback: action => {}
                    });
                  } else if (data2.data.status === 2) {
                    clearInterval(interval);

                    let outputs = data2.data.outputdata;
                    console.log(outputs)
                  } else {
                  }
                }).catch(function(err){
                  console.log(err)
                })
              }, 5000);
            }
          }).catch(function(err){
            console.log(err)
          })
        }
      },2000)
    },
  },
  data() {
    return {

      SA_Project:{
        // 项目ID
        pid:'',
        name:'',
        description:'',
      
        // 模型ID
        oid:'',
        md5:'',
        modelName:'',
        modelDescription:'',

        mdl:'',
        mdlJson:{},

        states:[],
        paramStates:[],
      },
      expandObsStates:[],
      expandDataStates:[0],
      expandDataStatesSR:[0],
      expandParamStatesSR:[],
      expandResultStatesSR:[],
      // 参数嵌套太深，会影响父子组件的绑定
      paramsSum:0,
      paramsName:[],
      paramsSet:[],
      simSetting:{
        saMethod: "morris",
        sampleMethod:"morris_sampler",
        simTimes: 0,
        simTargets: [],
        observations: [],
        objectiveFuns:[]
      },
      scoreSA:[],
      simResult:[],
      totalResult:[],
      labels:[],
      scoreObj:[],

      // 观测数据开关
      ObservationSwitch:false,

      activeStep:0,
      preparationStep:true,
      processStep:false,
      resultStep:false,
      singleRunStep:false,

    }
  },
  mounted(){
    // 测试
    // var pid = "ae2a1cac-b6e0-45fe-82a7-f30d36c41213"

    var that = this
    var pid = that.$route.params.pid
    this.$axios.get(
      "/SA-back-project/project/getByPid", {params:{pid:pid}}
    ).then(function(response){
      var data = response.data
      if(data.code == 0){
        var project = data.data
        that.SA_Project = project
        console.log(that.SA_Project)
        
        that.SA_Project.paramStates = []
        that.SA_Project.states = that.SA_Project.mdlJson.mdl.states

        var states = that.SA_Project.states;
        for (var i = 0; i < states.length; i++) {
          var state = states[i];
          
          // 整理输入数据（数值）和参数State
          for (var j = 0; j < state.event.length; j++) {
            if (state.event[j].data != undefined && state.event[j].eventType == "response") {
              let nodes = state.event[j].data[0].nodes;
              let refName = state.event[j].data[0].text.toLowerCase();
              if (state.event[j].data[0].externalId != undefined) {
                state.event[j].externalId = state.event[j].data[0].externalId;
              }

              if (nodes != undefined && refName != "grid" && refName != "table" && refName != "shapes") {
                let children = [];
                for (var k = 0; k < nodes.length; k++) {
                  let node = nodes[k];
                  let child = {};
                  child.eventId = node.text;
                  child.eventName = node.text;
                  child.eventDesc = node.desc;
                  child.eventType = node.dataType;

                  child.child = true;
                  children.push(child);
                }
                that.SA_Project.states[i].event[j].children = children;
              }
              else {
                that.SA_Project.states[i].event[j].data[0].nodes = undefined;
              }

            }
          }

          // 单独整理参数State
          if(state.type == "group"){
            for (var k = 0; k < state.event.length; k++) {
              var event = state.event[k];
              var table = []
              var element = {}
              element.name = event.eventName
              element.changeType = "Multiply"
              element.left = -0.2
              element.right = 0.2
              element.value = ""
              table.push(element)
              event.table = table
            }
            
            state.selectedParams = []

            that.SA_Project.paramStates.push(state)
          }

          // 单独整理simTarget Observation-State
          if(state.name == "Observation"){
            var obs = []
            for (var k = 0; k < state.event.length; k++) {
              obs.push(state.event[k].eventName) 
            }
            that.simSetting.simTargets = obs
          }
            
        }

        // 根据模型名称初始化mapbox
        that.$refs.mapbox.initByModelName(that.SA_Project.modelName)

        // 测试
        // that.$refs.processStep.testFunction(that.SA_Project.states)
      }
    }).catch(function(err){
      console.log(err)
    })
  }
}
</script>

<style scoped>
  #pageHeader{
    margin: 20px 0;
  }
  .saContainer{
    width: 80%;
    margin: auto;
    min-height: 500px;
  }
  .observationSwitch{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 10px;
  }
</style>
<style>
  .el-collapse-item__header{
    background-color: #FAFAFA;
  }
  .el-collapse-item__arrow{
    margin-left:5px;
    margin-right:15px;
  }
  .el-collapse-item__content{
    padding-bottom: 0;
  }
</style>