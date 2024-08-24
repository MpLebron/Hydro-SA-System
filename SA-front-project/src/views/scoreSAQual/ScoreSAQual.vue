<template>
  <div>
    <el-tabs v-model="activeTabName" type="border-card" tab-position="bottom">
      <el-tab-pane  label="单参数" name="singleParam">
        <el-select v-model="singleParam" @change="refreshSingleChart" clearable size="small" placeholder="请选择参数" class="singleSelect">
          <el-option
            v-for="item in paramsName"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <el-select v-model="singleParamTarget" @change="refreshSingleChart" clearable size="small"  placeholder="请选择模拟目标" class="singleSelect">
          <el-option
            v-for="item in simSetting.simTargets"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <div id="singleParamCanvas" class="wholePane"></div>
      </el-tab-pane>

      <el-tab-pane  label="双参数" name="doubleParam">
        <el-select v-model="doubleParamH" @change="refreshBoubleChart" clearable size="small"  placeholder="请选择横轴参数" class="doubleSelect">
          <el-option
            v-for="item in paramsName"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <el-select v-model="doubleParamV" @change="refreshBoubleChart" clearable size="small"  placeholder="请选择纵轴参数" class="doubleSelect">
          <el-option
            v-for="item in paramsName"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <el-select v-model="doubleParamTarget" @change="refreshBoubleChart" clearable size="small"  placeholder="请选择模拟目标" class="doubleSelect">
          <el-option
            v-for="item in simSetting.simTargets"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <div id="doubleParamCanvas" class="wholePane"></div>
      </el-tab-pane>

      <el-tab-pane  label="全参数" name="allParam">
        <el-select v-model="allParamTarget" @change="refreshAllParamChart" clearable size="small"  placeholder="请选择模拟目标" class="allSelect">
          <el-option
            v-for="item in simSetting.simTargets"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <div id="allParamCanvas" class="wholePane"></div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name:'ScoreSAQual',
  props:[ 'simSetting','paramsName', 'paramsSet', 'simResult', 'totalResult' ],
  methods:{

    refreshSingleChart(){
      if(this.singleParam=="" || this.singleParamTarget==""){
        return
      }
      // 根据 this.singleParam 抽取需要展示的数据 [参数值，模拟值] 
      var paramVals = []
      for (let i = 0; i < this.paramsName.length; i++) {
        var pn = this.paramsName[i];
        if(pn == this.singleParam ){
          for (let j = 0; j < this.paramsSet.length; j++) {
            paramVals.push(this.paramsSet[j][i]);
          }
          break
        }
      }
      // 模拟值 需要从 res_total_output.dat 这个文件中获取
      var resultVals = []
      for (var i = 0; i < this.simSetting.simTargets.length; i++) {
        var target = this.simSetting.simTargets[i]
        if(target == this.singleParamTarget){
          resultVals = this.totalResult[i]
          break
        }
      }

      // 组合成绘图需要的数据
      var data = []
      for (let i = 0; i < paramVals.length; i++) {
        data.push([paramVals[i],resultVals[i]])
        
      }

      var chartDom = document.getElementById('singleParamCanvas');
      var myChart = this.$echarts.init(chartDom);
      var option;
      option = {
          color:['#67c23a'],
          xAxis: {
              type:"value",
              name:this.singleParam,
              nameLocation:'center',
              nameGap:20,
              nameTextStyle:{
                  fontWeight : 'bold',
                  fontSize:16
              }
          },
          yAxis: {
              type:"value",
              name:this.singleParamTarget,
              nameLocation:'center',
              nameGap:25,
              nameTextStyle:{
                  fontWeight : 'bold',
                  fontSize:16
              }
          },
          tooltip: {
              padding: 10,
              borderColor: '#838383',
              borderWidth: 1,
              formatter: function(param){
                  return param.dimensionNames[0] + ": " +param.value[0] + "<br>"
                  + param.dimensionNames[1] + ": " +param.value[1]
              }
          },
          series: [{
            symbolSize: 8,
            data: data,
            type: 'scatter',
            dimensions: [this.singleParam, this.singleParamTarget]
          }]
      };

      option && myChart.setOption(option);

    },

    refreshBoubleChart(){
      if(this.doubleParamH==""||this.doubleParamV==""||this.doubleParamTarget==""){
        return
      }
      
      // 根据 this.doubleParamH doubleParamV  抽取需要展示的数据 [参数值，参数值，模拟值] 
      var paramHVals = []
      var paramVVals = []
      for (let i = 0; i < this.paramsName.length; i++) {
        var pn = this.paramsName[i];
        if(pn == this.doubleParamH ){
          for (let j = 0; j < this.paramsSet.length; j++) {
            paramHVals.push(this.paramsSet[j][i]);
          }
        }
        if(pn == this.doubleParamV ){
          for (let j = 0; j < this.paramsSet.length; j++) {
            paramVVals.push(this.paramsSet[j][i]);
          }
        }
      }
      // 模拟值 需要从 res_total_output.dat 这个文件中获取
      var resultVals = []
      for (var i = 0; i < this.simSetting.simTargets.length; i++) {
        var target = this.simSetting.simTargets[i]
        if(target == this.doubleParamTarget){
          resultVals = this.totalResult[i]
          break
        }
      }

      // 组合成绘图需要的数据
      var data = []
      for (let i = 0; i < paramHVals.length; i++) {
        data.push([paramHVals[i],paramVVals[i],resultVals[i]])
      }
      var min = function(resultVals){
        var minVal = resultVals[0]
        for (let i = 1; i < resultVals.length; i++) {
          if(resultVals[i] < minVal)
            minVal = resultVals[i]
        }
        return Math.floor(minVal)
      }
      var max = function(resultVals){
        var maxVal = resultVals[0]
        for (let i = 1; i < resultVals.length; i++) {
          if(resultVals[i] > maxVal)
            maxVal = resultVals[i]
        }
        return Math.ceil(maxVal)
      }

      var chartDom = document.getElementById('doubleParamCanvas');
      var myChart = this.$echarts.init(chartDom);
      var option;
      
      option = {
          xAxis: {
            type:"value",
            name:this.doubleParamH,
            nameLocation:'center',
            nameGap:20,
            nameTextStyle:{
                fontWeight : 'bold',
                fontSize:16
            }
          },
          yAxis: {
            type:"value",
            name:this.doubleParamV,
            nameLocation:'center',
            nameGap:25,
            nameTextStyle:{
                fontWeight : 'bold',
                fontSize:16
            }
          },
          tooltip: {
            padding: 10,
            borderColor: '#838383',
            borderWidth: 1,
            formatter: function(param){
                return param.dimensionNames[0] + ": " +param.value[0] + "<br>"
                + param.dimensionNames[1] + ": " +param.value[1] + "<br>"
                + param.dimensionNames[2] + ": " +param.value[2]
            }
          },
          visualMap: {
            min: min(resultVals),
            max: max(resultVals),
            inRange: {
                color:["#2c7bb6","#abd9e9","#ffffbb","#fdac63", "#d7191c"]
            },
            right:"2%",
            bottom:"10%",
            text:[this.doubleParamTarget.substr(0,4)]
          },
          series: [{
            symbolSize: 8,
            data:data,
            type: 'scatter',
            dimensions: [this.doubleParamH, this.doubleParamV, this.doubleParamTarget]
          }]
      };

      option && myChart.setOption(option);
    },

    refreshAllParamChart(){
      if(this.allParamTarget==""){
        return
      }
      // 获取各组参数的取值
      var paramVals = this.deepClone(this.paramsSet)

      // 跟Target好像没有关系，就按照本Target模拟值中前10%
      var resultVals = []
      for (var i = 0; i < this.simSetting.simTargets.length; i++) {
        var target = this.simSetting.simTargets[i]
        if(target == this.allParamTarget){
          resultVals = this.totalResult[i]
          break
        }
      }
      
      // 组合成绘图需要的数据
      var data = []
      for (let i = 0; i < paramVals.length; i++) {
        paramVals[i].push(resultVals[i])
        data.push(paramVals[i])
      }
      var inedx = paramVals[0].length -1
      // 二维数组排序  倒序
      data.sort(function(a,b){
        if(a[inedx]<b[inedx]){
            return 1;
        }
        if(a[inedx]>b[inedx]){
          return -1;
        }
        return 0;
      })
      
      var top = Math.ceil(data.length * 0.1)
      var topData = data.slice(0, top)
      var otherData = data.slice(top)

      var chartDom = document.getElementById('allParamCanvas');
      var myChart = this.$echarts.init(chartDom);
      var option;

      var parallelAxis = []
      for (let i = 0; i < this.paramsName.length; i++) {
        var param = this.paramsName[i]
        parallelAxis.push({dim: i, name: param},)
      }

      option = {
        parallelAxis: parallelAxis,
        parallel: {
          parallelAxisDefault: {
            type: 'value',
            name: '参数平行坐标图',
            nameLocation: 'start',
            nameTextStyle: {
                color: '#000',
                fontSize: 12
            },
            axisLine: {
                lineStyle: {
                    color: '#aaa'
                }
            },
            axisTick: {
                lineStyle: {
                    color: '#777'
                }
            },
            splitLine: {
                show: false
            },
            axisLabel: {
                color: '#aaa'
            }
          }
        },
        series: [
          {
            type: 'parallel',
            lineStyle: {
                color:'#000',
                type:'dashed',
                width: 0.5,
            },
            data: otherData
          },
          {
            type: 'parallel',
            lineStyle: {
                color:'#F00',
                type:'solid',
                width: 1,
            },
            data: topData
          }
        ]
      };

      option && myChart.setOption(option);
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
  },
  data(){
    return{
      activeTabName:"singleParam",

      singleParam:'',
      singleParamTarget:'',
      
      options:['a','b','c','d','e'],

      doubleParamH:'',
      doubleParamV:'',
      doubleParamTarget:'',

      allParamTarget:''
    }
  }
}
</script>

<style scoped>
  .singleSelect{
    width: 49%;
  }
  .doubleSelect{
    width: 32.5%;
  }
  .allSelect{
    width: 100%;
  }
  
  .wholePane{
    width: 100%;
    height: 560px; 
    margin: 10px 0;
    border: 1px dashed #909399;
  }
</style>
