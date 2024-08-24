<template>
   <div>
    <el-tabs v-model="activeTabName" type="border-card" tab-position="bottom"  @tab-click="handleClick">
      <el-tab-pane v-for="(target,key) in simSetting.simTargets" :key="key" :label="target" :name="target">
        <div :id="target+3"  style="width: 100% ;height:600px;"></div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name:"SimResult",
  props:[ 'simSetting','simResult','labels',"scoreObj" ],
  methods:{
    init(){
      this.activeTabName = this.simSetting.simTargets[0]
      setTimeout(()=>{
        this.initResults()
      },0)
    },

    initResults(){
      // 基于准备好的dom，初始化echarts实例 
      for(var i=0; i<this.allResult.length; i++){
        var result = this.allResult[i]
        if(result.target == this.activeTabName){

          var dom = document.getElementById(result.target+3)
          var myChart = this.$echarts.init(dom);
          // 绘制图表
          var option = {
            color:[
              '#438a5e','#96bb7c','#ff5722'
            ],
            title:{
              text:' Result of Simulation',
              subtext: result.target,
              textStyle: {
                fontSize: 20
              },
              subtextStyle: {
                fontSize: 16
              },
              left:'center'
            },
            tooltip : {
              trigger: 'axis'
            },
            legend: {
              data:['min value','max value','observation'],
              bottom:'0',
            },
            toolbox: {
              show : true,
              feature : {
                dataZoom: {
                  yAxisIndex: "none"
                },
                dataView: {
                  readOnly: true
                },
                saveAsImage : {show: true}
              },
              orient:'vertical',
              bottom:'0',
            },
            calculable : true,
            
            xAxis : [
              {
                type : 'category',
                boundaryGap: false,
                data : this.labels
              }
            ],
            yAxis : [
              {
                type : 'value'
              }
            ],
            series : [
              {
                name:'max value',
                type: 'line',
                smooth: true,
                areaStyle: {
                  color:'#e3dfc8',
                  opacity:1
                },
                data:result.maxValue
              },
              {
                name:'min value',
                type: 'line',
                smooth: true,
                areaStyle: {
                    color:'#ffffff',
                    opacity:1
                },
                data:result.minValue
              },
              {
                name:'observation',
                type: 'line',
                smooth: true,
                data:result.obs
              }
            ]
          }
          myChart.setOption(option);
          
        }
      }
     
    },

    handleClick(tab, event) {
      setTimeout(()=>{
        this.initResults()
      },0)
    },

    loadData(sim_result){
      // 准备绘图数据
      for (var i = 0; i < this.simSetting.simTargets.length; i++) {
        var target = this.simSetting.simTargets[i];
        
        var data = {
          target: target,
          maxValue:[],
          minValue:[],
          obs:[]
        }
        // 最大最小模拟值
        for (var j = 0; j < sim_result.length; j++) {
          var result = sim_result[j];
          if(result.target == data.target){
            // 提取模拟结果中的最大最小值
            var maxValue = []
            var minValue = []
            for(var k=0; k<result.allValues[0].length; k++){
              var max=parseFloat(result.allValues[0][k]) 
              var min=max
              for(var h=0; h<result.allValues.length; h++){
                var value = parseFloat(result.allValues[h][k])
                if(value>max) max=value
                else if(value<min) min=value
              }
              maxValue.push(max)
              minValue.push(min)
            }
            data.maxValue = maxValue
            data.minValue = minValue
            break
          }
        }
        
        this.allResult.push(data)
      }
    },

    loadObsData(){
      // while(true){
      //   if(this.allResult.length == 0){
      //     continue
      //   }
        for (let i = 0; i < this.allResult.length; i++) {
          var data = this.allResult[i];
          // 观测值
          for (let j = 0; j < this.scoreObj.length; j++) {
            let obj = this.scoreObj[j];
            if(obj.Event == data.target){
              data.obs = obj.Observed
              break
            }
          }
        }
      //   break
      // }
      
    }

  },
  mounted() {

  },
  data() {
    return {
      allResult:[],

      activeTabName:""
    }
  }
}
</script>

<style>

</style>