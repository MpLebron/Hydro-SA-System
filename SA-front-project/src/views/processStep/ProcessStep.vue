<template>
  <div>
    <!-- 运行前提示 -->
    <div style="text-align:center">
      <el-card shadow="always" style="width: 80%;margin: 2% auto;background: #f4f4f5;">
        <pre>{{getRunTips()}}</pre>
      </el-card>
      <el-button type="primary" round style="margin-top: 1% " 
                  @click="startSimulation">
        开始运行
      </el-button>
    </div>
    <!-- 运行时状态 -->
    <div v-show="paramsSample.length>0">
      <el-progress 
        :text-inside="true" :stroke-width="20" 
        :percentage="runningTip.percentage"  :format="processFormat"
        status="success" style="height: 20px;margin: 1% 5%;">
      </el-progress>

      <el-table
        :data="paramsSample" height="600"
        style="width: 90%;margin: 1% 5%;" :border="true"
        :row-class-name="tableRowClassName">
        <el-table-column 
          prop="status" label="状态">
        </el-table-column>
        <template v-for="(param,key) in paramsName" >
          <el-table-column :key="key"
            :prop="param"  :label="param">
          </el-table-column>
        </template>
      </el-table>
    </div>
    <!-- 全部运行成功 -->
    <div style="text-align:center" v-show="runningTip.percentage==100">
      <el-card shadow="always" style="width: 50%;margin: 2% auto;background: #E6A23C;">
        运行成功
      </el-card>
    </div>
    
  </div>
</template>

<script>
export default {
  name:'ProcessStep',
  props: ['SA_Project','paramsName','paramStates', 'simSetting' ,'paramsSum', 'ObservationSwitch'],
  methods:{
    // 测试
    testFunction(states){
      // 观测数据的state
      this.SA_Project.states = states
      let event = this.SA_Project.states[1].event[0]
      this.$set(event, 'url', "http://221.226.60.2:8082/data/02b4ce84-ff14-4d68-a421-06d6dda23ef7");
      this.$set(event, 'tag', "observed")
      this.$set(event, 'suffix',"txt")
      // 开关
      this.ObservationSwitch = true
      // 设置
      this.simSetting.observations = ["Flow"]
      this.simSetting.objectiveFuns = ["Nash"]
      // loading
      this.SAloading = this.$loading({
        lock: true,
        text: '正在收集全部模拟结果，计算敏感性指数（以及目标函数）',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      
      console.log(this.SA_Project)
      console.log(this.simSetting)
      // 调用运行后处理
      this.computeObjForSA()
    },

    processFormat(percentage){
      if(percentage == 0)
        return "分配任务中或初始化运行中..."
      if(percentage > 0 && percentage <100)
        return "任务完成率"+percentage.toFixed(2)+"%"
      if( percentage === 100 )
        return "全部运行成功！"
    },

    getRunTips(){
      var tip = ""
      tip += "已选参数包括："+this.paramsName.join(", ")+"；\n"
      var runTimes = 0
      switch (this.simSetting.sampleMethod) {
        case 'finite_difference_sampler':
        case 'morris_sampler':
          runTimes = this.simSetting.simTimes * (this.paramsName.length+1)
          break;
        case 'uniform_sampler':
        case 'monte_carlo_sampler':
        case 'latin_hypercube_sampler':
        case 'fast_sampler':
          runTimes = this.simSetting.simTimes
          break;
        case 'vbsa_sampler':
          runTimes = this.simSetting.simTimes * (this.paramsName.length+2)
          break;
        case 'sobol_sequence_sampler':
          runTimes = this.simSetting.simTimes * (2*this.paramsName.length+2)
          break;
        case 'extended_fast_sampler':
          runTimes = this.simSetting.simTimes * this.paramsName.length
          break;
        case 'fractional_factorial_sampler':
          runTimes = 2**(Math.ceil(Math.log2(this.paramsSum))+1)
          break;
      }
      tip += "敏感性分析方法："+this.simSetting.saMethod+"；参数采样方法："+this.simSetting.sampleMethod+"；模拟次数："+runTimes
      return tip
    },

    tableRowClassName({row, rowIndex}) {
      if (row.status == "success") {
        return 'success-row';
      } else if (row.status == "running") {
        return 'running-row';
      } else if (row.status == "waiting") {
        return 'waiting-row';
      }
      return '';
    },

    // 定义一个深拷贝函数  接收目标target参数
    deepClone(target) {
      // 定义一个变量
      let result;
      // 如果当前需要深拷贝的是一个对象的话
      if (typeof target === 'object') {
        // 如果是一个数组的话
        if (Array.isArray(target)) {
          result = []; // 将result赋值为一个数组，并且执行遍历
          for (let i in target) {
            // 递归克隆数组中的每一项
            result.push(this.deepClone(target[i]))
          }
        // 判断如果当前的值是null的话；直接赋值为null
        } else if(target===null) {
          result = null;
        // 判断如果当前的值是一个RegExp对象的话，直接赋值    
        } else if(target.constructor===RegExp){
          result = target;
        }else {
          // 否则是普通对象，直接for in循环，递归赋值对象的所有值
          result = {};
          for (let i in target) {
              result[i] = this.deepClone(target[i]);
          }
        }
      // 如果不是对象的话，就是基本数据类型，那么直接赋值
      } else {
        result = target;
      }
      // 返回最终结果
      return result;
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
      for (let i = 0; i < states.length; i++) {
        let events = states[i].event;
        let find = false;
        for (let j = 0; j < events.length; j++) {
          let event = events[j];
          if (event.eventType == "response" && event.children != undefined) {
            //拼接文件内容
            let content = "";
            let children = event.children;
            for (let k = 0; k < children.length; k++) {
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
     
      let that = this

      let formData = new FormData();
      formData.append("datafile", file);
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
        console.log("模型驱动文件上传失败，将重新尝试连接。")
        that.uploadToDataContainer(file, event);
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
            number: index,
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
                callback: action => {
                  // 需要重新发布计算任务，直至计算成功
                  console.log(index+"，invoke时失败，重新提交")
                  that.invoke(states, index)
                }
              });
              // return;
            }

            if(data.code == 0){
              var task = data.data
              that.paramsSample[index].status = "running"
              let interval = setInterval( () => {
                 that.$axios.post(
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
                    console.log(index+"，模型执行出错，重新发布计算任务")
                    clearInterval(interval);
                    // that.$alert("Some error occured when the model running! Rerun this task!", 'Error', {
                    //   type: 'error',
                    //   confirmButtonText: 'OK',
                    //   callback: action => {
                        // 需要重新发布计算任务，直至计算成功
                        that.invoke(states, index)
                    //   }
                    // });
                  } else if (data2.data.status === 2) {
                    clearInterval(interval);

                    that.paramsSample[index].status = "success"
                    let outputs = data2.data.outputdata;

                    that.runningTip.success +=1
                    // 应对出现问题重新运行，出现的异常超出问题
                    console.log(that.runningTip.success)
                    if(that.runningTip.success > that.runningTip.total){
                      that.runningTip.success = that.runningTip.total
                    }
                    that.runningTip.percentage = (that.runningTip.success/that.runningTip.total)*100

                  } else {
                    // 0 inited 或1 started 继续请求
                  }
                }).catch(function(err){
                  console.log(err)
                })
              }, 10000);
            }
          }).catch(function(err){
            console.log(err)
          })
        }
      },2000)
    },
    
    // 为计算敏感性指数准备目标函数得分
    computeObjForSA(){
      // 汇总所有需要计算目标函数的target和url
      let targets=[], urls=[]
      var states = this.SA_Project.states;
      for (let i = 0; i < states.length; i++) {
        if(states[i].name == "Observation"){
          var events = states[i].event;
          for (let j = 0; j < events.length; j++) {
            var event = events[j];
            // observation 必须是一个序列文件  输入数据
            if(event.url != undefined && event.url != ""){
              targets.push(event.eventName)
              urls.push(event.url)
            }
          }
        }
      }

      // 统一计算所有targets的目标函数用于SA
      if(this.ObservationSwitch && targets.length > 0){
        let that = this
        let interval = setInterval(() => {
          this.$axios.get(
            "/SA-back-project/simulation/compute-obj-for-sa", 
            {params:{pid:this.SA_Project.pid, targetsStr:targets.join(","), urlsStr:urls.join(",")}}
          ).then(function(response){
            var data = response.data
            if(data.code == 0){
              let scoreObjList = data.data
              if(scoreObjList != "waiting"){
                clearInterval(interval)
                that.$emit('updateScoreObj', scoreObjList)

                // 计算完目标函数，开始计算敏感性指数
                that.computeSA()
              }
            }
            else{
              console.log(data.msg)
            }
          }).catch(function(err){
            console.log(err)
          })
        },2000)
      }else{
        // 没有实测数据，无需计算目标函数，直接使用提出出来的平均值来计算敏感性指数
        this.computeSA()
      }
    },
    computeSA(){
      var that = this
      let interval = setInterval(() => {
        this.$axios.get(
          "/SA-back-project/simulation/compute-sa", {params:{pid:this.SA_Project.pid}}//this.SA_Project.pid
        ).then(function(response){
          var data = response.data
          if(data.code == 0){
            var scoreSA = data.data
            if(scoreSA != "waiting"){
              clearInterval(interval)
              that.SAloading.close();
              that.$emit('updateScoreSA', scoreSA)
              // 将这三个请求放在SA之内，可以省掉很多判断
              // 2021.10.27 目标函数的计算应该放在计算SA之前
              that.getLabels()
              that.getSimResult() 
            }
          }else{
            console.log(data.msg)
          }
        }).catch(function(err){
          console.log(err)
        })
      },5000)
      
    },
    getSimResult(){
      var that = this
      this.$axios.get(
        "/SA-back-project/simulation/sim-result", {params:{pid:this.SA_Project.pid}}//this.SA_Project.pid
      ).then(function(response){
        var data = response.data
        if(data.code == 0){
          var result = data.data
          // if(result != "waiting"){
            var simResult = result.simResult //复杂对象无法自动双向绑定
          
            // that.totalResult = result.totalResult // 二维数组也无法自动双向绑定，所以不要在子组件中对父组件变量直接赋值
            that.$emit('updateTotalResult', result.totalResult)

            that.$emit('updateSimResult', simResult)
          // }
        }else{
          console.log(data.msg)
        }
      }).catch(function(err){
        console.log(err)
      })
    },
    getLabels(){
      var that = this
      this.$axios.get(
        "/SA-back-project/simulation/labels", {params:{pid:this.SA_Project.pid}}//this.SA_Project.pid
      ).then(function(response){
        var data = response.data
        if(data.code == 0){
          var labels = data.data
          that.$emit('updateLabels', labels)
        }else{
          console.log(data.msg)
        }
      }).catch(function(err){
        console.log(err)
      })
    },
    

    // 开始采样与模拟
    startSimulation(){

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
        // 单独处理观测数据State 将已经上传数据的event记录在this.simSetting.observations 
        if(states[i].name == "Observation"){
          var obs = []
          // 2021.10.27 首先根据是否有观测数据的开关来判断
          if(this.ObservationSwitch){
            for (var k = 0; k < events.length; k++) {
              var event = events[k];
              if(event.url != undefined && event.url != ""){
                obs.push(event.eventName) 
              }
            }
          }
          this.simSetting.observations = obs
        }
      }
      // 检查参数state
      if(this.paramsName.length==0){
        this.$message.error("The parameters to be evaluated have not been selected");
        return;
      }
      for (var i = 0; i < this.paramStates.length; i++) {
        var params = this.paramStates[i].selectedParams;
        for (var j = 0; j < params.length; j++) {
          var param = params[j];
          if(parseFloat(param.table[0].left) >= parseFloat(param.table[0].right)){
            this.$message.error("The bounds of some parameters are set incorrectly");
            return;
          }
        }
      }
      // 检查模拟设置
      if(this.simSetting.simTimes == 0){
        this.$message.error("Simulation times cannot be zero");
        return;
      }

      // 参数采样
      var params = []
      for (var i = 0; i < this.paramStates.length; i++) {
        var state = this.paramStates[i];
        for (var j = 0; j < state.selectedParams.length; j++) {
          var param = state.selectedParams[j];
          params.push(param.table[0])
        }
      }
      var that = this
      var form = new FormData()
      form.append("projectId", this.SA_Project.pid)
      form.append("params", JSON.stringify(params))
      form.append("setting", JSON.stringify(this.simSetting))
      this.$axios.post(
        "/SA-back-project/simulation/sample", form
      ).then(function(response){
        var data = response.data
        if(data.code == 0){
          var samples = data.data
          that.$emit('updateParamsSet', samples)
          
          // 采样成功后 
          that.paramsSample = []
          for (let i = 0; i < samples.length; i++) {
            var set = {}
            var line = samples[i];
            for (let j = 0; j < line.length; j++) {
              set[that.paramsName[j]] = line[j]
            }
            set.status = "waiting"
            that.paramsSample.push(set)
          }
          that.runningTip.total = samples.length
          that.runningTip.success = 0
          
          that.taskNumber = 0
          that.deployTask()
          var successBatch = setInterval(()=>{
            if(that.taskNumber<that.paramsSample.length && that.runningTip.success>=that.taskNumber){
              that.deployTask()
            }
            if(that.taskNumber>=that.paramsSample.length){
              clearInterval(successBatch)
            }
          },5000)

          // // 逐组  合并参数state  生成数值与参数文件
          // for (var i = 0; i < that.paramsSample.length; i++) {
          //   // 把一组参数塞进去，不能塞到全局变量里，要塞到深拷贝的另一个对象中，防止多组之间相互影响
          //   var paramStates = that.deepClone(that.paramStates)

          //   var set = that.paramsSample[i];
          //   for (var j = 0; j < that.paramsName.length; j++) {
          //     var name = that.paramsName[j];
          //     for (var k = 0; k < paramStates.length; k++) {
          //       var params = paramStates[k].selectedParams;
          //       var m = 0
          //       for (; m < params.length; m++) {
          //         if(params[m].name == name){
          //           // that.$set(params[m],'value', set[name])
          //           // 因为在刚进页面时的mounted中，已经为这个对象设置了value属性
          //           params[m].value = set[name]
          //           break
          //         }
          //       }
          //       if(m<params.length){
          //         break
          //       }
          //     }
          //   }

          //   var states = that.deepClone(that.SA_Project.states)

          //   // 合并参数state
          //   that.mergeState(paramStates,states)
          //   // 生成数值与参数文件
          //   that.createAndUploadParamFile(states)
          //   // 等待100ms，等待文件全都上传到数据容器
          //   that.sleep(100)
          //   // 运行本次
          //   that.invoke(states, i)
          // }

          // 设置定时任务，检查所有模拟是否全部结束
          
          var success = setInterval(()=>{
            // 防止某些计算任务失败导致的success异常情况，加上第二个条件
            if(that.runningTip.success==that.runningTip.total && that.taskNumber>=that.runningTip.total){
              clearInterval(success)
              console.log("全部运行成功，开始获取全部模拟结果，计算SA，计算目标函数")

              that.SAloading = that.$loading({
                lock: true,
                text: '正在收集全部模拟结果，计算敏感性指数（以及目标函数）',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
              });
              that.computeObjForSA()
              // 系统中仅仅考虑敏感性分析，不涉及实测数据与模型校准
              // 不行啊！只做这个能得到的结论有些许薄弱，而且离应用或者实用还差一步
              // 1、在指定站点编号时，可以获得模拟结果，尝试一下以下两种情况能否区分开
              // 2、在选择实测文件时，可以计算目标函数
              // 无法获取第一种情况的信息，这个不是一个统一的event
              // 所以只能在指定站点编号，并且选择实测数据时，才能进行以下操作。。站点编号也没法检查，只能提醒

              
            }
          },5000)
        }else{
          that.$alert("Sampling failed, please check the parameter value!", 'Error', {
            type: 'error',
            confirmButtonText: 'OK',
            callback: action => {}
          });
        }
      }).catch(function(err){
        console.log(err)
      })
    },
    deployTask(){
      // 逐组 每50组一次 合并参数state  生成数值与参数文件
      // 逐组 每40组一次 合并参数state  生成数值与参数文件 2022.02.21
      for (let i = this.taskNumber; i<this.taskNumber+40 && i<this.paramsSample.length; i++) {
        // 把一组参数塞进去，不能塞到全局变量里，要塞到深拷贝的另一个对象中，防止多组之间相互影响
        var paramStates = this.deepClone(this.paramStates)

        let set = this.paramsSample[i];
        for (let j = 0; j < this.paramsName.length; j++) {
          var name = this.paramsName[j];
          for (let k = 0; k < paramStates.length; k++) {
            var params = paramStates[k].selectedParams;
            let m = 0
            for (; m < params.length; m++) {
              if(params[m].name == name){
                // this.$set(params[m],'value', set[name])
                // 因为在刚进页面时的mounted中，已经为这个对象设置了value属性
                params[m].value = set[name]
                break
              }
            }
            if(m<params.length){
              break
            }
          }
        }

        var states = this.deepClone(this.SA_Project.states)

        // 合并参数state
        this.mergeState(paramStates,states)
        // 生成数值与参数文件
        this.createAndUploadParamFile(states)
        // 运行本次
        this.invoke(states, i)
      }
      this.taskNumber += 40
    },

    sleep(millisecond) {
      return new Promise(resolve => {
        setTimeout(() => {
            resolve()
        }, millisecond)
      })
    },

  },
  mounted(){
    
  },
  data(){
    return{
      runningTip:{
        percentage:0,
        total:0,
        success:0
      },
      paramsSample: [],

      SAloading:null,

      // 当运行次数过多，比如超过一千之后，就会拥堵数据容器的上传通道，导致网络连接错误
      // 所以，设计分批次运行，那也就实现了分批次上传。每批上传50个，100个测试过，也可以，但是保险起见，50个吧。
      taskNumber:0
    }
  }
}
</script>


<style>
  .el-table .success-row {
    background: #e1f3d8 ;
  }
  .el-table .running-row {
    background: #faecd8 ;
  }
  .el-table .waiting-row {
    background: #e9e9eb ;
  }
</style>