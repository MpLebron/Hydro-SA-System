<template>
  <div>
    <el-tabs v-model="activeTabName" type="border-card" tab-position="bottom">
      <el-tab-pane v-for="(score,key) in scoreSA" :key="key" :label="score.target" :name="score.target">
        <img id="scoreFigure" :src="'data:'+score.figure.contentType+';base64,'+score.figure.content.data" alt="">
        <pre id="scoreTxt">{{score.score}}</pre>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name:'ScoreSA',
  props:[ 'simSetting', 'scoreSA' ],
  methods:{

    // 获取数据通过echarts绘图的方法，不用了，但不舍得删除
    init(){
      this.activeTabName = this.simSetting.simTargets[0]
      setTimeout(()=>{
        this.initScores()
      },0)
    },
    initScores(){
      // 基于准备好的dom，初始化echarts实例
      for(var i=0; i<this.scoreSA.length; i++){
        var score = this.scoreSA[i]
        if(score.target == this.activeTabName){

          if(this.simSetting.saMethod == 1){
            // morris Mu,μ,横向条形图,Sigma,σ,散点图
            var dom = document.getElementById(score.target)
            dom.className = "halfPane"
            var myChart1 = this.$echarts.init(dom)
            var option = {
              color:[
                '#438a5e','#96bb7c'
              ],
              title:{
                text:' Sensitivity Index (μ*)',
                subtext: score.target,
                textStyle: {
                  fontSize: 16
                },
                subtextStyle: {
                  fontSize: 12
                },
                left:'center'
              },
              grid: {
                width: '70%',
                left:'20%',
              },
              tooltip : {
                trigger: 'axis'
              },
              toolbox: {
                show : true,
                feature : {
                  dataView : {readOnly: true},
                  saveAsImage : {show: true}
                },
                orient:'vertical',
                bottom:'0',
              },
              calculable : true,
              xAxis: {
                name:'μ*',
                nameTextStyle:{ fontStyle : 'italic',fontWeight : 'bold'},
                type : 'value',
              },
              yAxis: {
                type : 'category',                    
                data : score.params
              },
              series: [
                {
                  name: 'μ*',
                  type: 'bar',
                  data: score.mu_star
                }
              ]
            }
            myChart1.setOption(option)


            var dom2 = document.getElementById(score.target+1)
            dom2.className = "halfPane"
            var myChart2 = this.$echarts.init(dom2)
            var maxMu = score.mu_star[score.mu_star.length-1]
            var maxSigma = Math.max(...score.sigma)
            var max = maxMu>maxSigma?Math.ceil(maxMu+10):Math.ceil(maxSigma+10)
            var option = {
              title:{
                text:' Sensitivity Index (σ/μ*)',
                subtext: score.target,
                textStyle: {
                  fontSize: 16
                },
                subtextStyle: {
                  fontSize: 12
                },
                left:'center'
              },
              grid: {
                width: '65%',
                left:'25%',
              },  
              legend: {
                data: score.params,
                left: '0',
                bottom : '10%',
                orient: 'vertical',
              },
              toolbox: {
                show : true,
                feature : {
                  dataView : {readOnly: true},
                  saveAsImage : {show: true}
                },
                orient:'vertical',
                bottom:'0',
              },
              calculable : true,
              xAxis: {
                name:'μ*',
                nameTextStyle:{ fontStyle : 'italic',fontWeight : 'bold'},
                type : 'value',
                max: max
              },
              yAxis: {
                name:'σ',
                nameTextStyle:{ fontStyle : 'italic',fontWeight : 'bold'},
                type : 'value',
                max: max
              },
              series: this.getSigmaMu(score, max)
            }
            myChart2.setOption(option)

          }else if(this.simSetting.saMethod == 2){
            // sobol  S1,ST,S2
            var dom = document.getElementById(score.target)
            dom.className = "wholePane"
            var myChart = this.$echarts.init(dom);
            // 绘制图表
            var option = {
              color:[
                '#438a5e','#96bb7c'
              ],
              title:{
                text:' Sensitivity Index (S1,ST)',
                subtext: score.target,
                textStyle: {
                  fontSize: 16
                },
                subtextStyle: {
                  fontSize: 12
                },
                left:'center'
              },
              tooltip : {
                trigger: 'axis'
              },
              legend: {
                data:['S1','ST'],
                bottom:'0',
              },
              toolbox: {
                show : true,
                feature : {
                  dataView : {readOnly: true},
                  saveAsImage : {show: true}
                },
                orient:'vertical',
                bottom:'0',
              },
              calculable : true,
              xAxis : [
                {
                  type : 'category',
                  data : score.params
                }
              ],
              yAxis : [
                {
                  type : 'value'
                }
              ],
              series : [
                {
                    name:'S1',
                    type:'bar',
                    data:score.S1
                },
                {
                    name:'ST',
                    type:'bar',
                    data:score.ST
                }
              ]
            }
            myChart.setOption(option);

            var dom2 = document.getElementById(score.target+1)
            dom2.className = "wholePane"
            var myChart2 = this.$echarts.init(dom2);
            // 绘制图表
            var option = {
              title:{
                text:' Sensitivity Index (S2)',
                subtext: score.target,
                textStyle: {
                  fontSize: 20
                },
                subtextStyle: {
                  fontSize: 16
                },
                left:'center'
              },
              toolbox: {
                show : true,
                feature : {
                  dataView : {readOnly: true},
                  saveAsImage : {show: true}
                },
                orient:'vertical',
                bottom:'0',
              },
              animation: false,
              grid: {
                height: '75%',
                width: '80%',
                top: '14%',
                right: "8%"
              },
              xAxis: {
                type: 'category',
                position: 'top',
                data: score.params,
                splitArea: {
                  show: true
                }
              },
              yAxis: {
                type: 'category',
                data: score.params,
                inverse: 'true',
                splitArea: {
                  show: true
                }
              },
              visualMap: {
                min: 0,
                max: 1,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '1%',
                type: 'continuous',
                color:['#527318','#899857','#dfdfdf']
              },
              series: [{
                type: 'heatmap',
                data: score.S2,
                label: {
                  show: true,
                  color:'#000'
                },
                emphasis: {
                  itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
                }
              }]
            }
            myChart2.setOption(option);
          }else if(this.simSetting.saMethod == 3 || this.simSetting.saMethod ==4){
            // eFAST fast S1,ST
            var dom = document.getElementById(score.target)
            dom.className = "wholePane"
            var myChart = this.$echarts.init(dom);
            // 绘制图表
            var option = {
              color:[
                '#438a5e','#96bb7c'
              ],
              title:{
                text:' Sensitivity Index',
                subtext: score.target,
                textStyle: {
                  fontSize: 16
                },
                subtextStyle: {
                  fontSize: 12
                },
                left:'center'
              },
              tooltip : {
                trigger: 'axis'
              },
              legend: {
                data:['S1','ST'],
                bottom:'0',
              },
              toolbox: {
                show : true,
                feature : {
                  dataView : {readOnly: true},
                  saveAsImage : {show: true}
                },
                orient:'vertical',
                bottom:'0',
              },
              calculable : true,
              xAxis : [
                {
                  type : 'category',
                  data : score.params
                }
              ],
              yAxis : [
                {
                  type : 'value'
                }
              ],
              series : [
                {
                    name:'S1',
                    type:'bar',
                    // stack:'effect',
                    data:score.S1
                },
                {
                    name:'ST',
                    type:'bar',
                    // stack:'effect',
                    data:score.ST
                }
              ]
            }
            myChart.setOption(option);
            
            var dom2 = document.getElementById(score.target+1)
            dom2.style.height = '0px'

          }

          
        }
      }
    },
    handleClick(tab, event) {
      setTimeout(()=>{
        this.initScores()
      },0)
    },
    getSigmaMu(score, max){
      var series = []
      for (let i = 0; i < score.params.length; i++) {
        var data ={
          name: score.params[i],
          type: 'scatter',
          symbolSize: 20,
          symbol: 'diamond',
          data: [[score.mu_star[i],score.sigma[i]]]
        }
        series.push(data)
      }
      if(series.length != 0){
        series[0].markLine={
          symbol:"none",
          lineStyle:{
            type : "dotted"
          },
          data: [
            [
              {
                  name: "σ/μ*=1",
                  coord: [0, 0]
              },
              {
                  coord: [max,max]
              }
            ],
            [
              {
                  name: "σ/μ*=0.5",
                  coord: [0, 0]
              },
              {
                  coord: [max,max/2]
              }
            ],
            [
              {
                  name: "σ/μ*=0.1",
                  coord: [0, 0]
              },
              {
                  coord: [max,max/10]
              }
            ],
          ]
        }
      }
      
      return series;
    },

  },
  data(){
    return{
      activeTabName:""
    }
  }
}
</script>

<style scoped>
  .halfPane{
    width: 49%;
    height: 600px;
    display: inline-block;    
    border-right: 1px dashed #909399;
    border-left: 1px dashed #909399;
  }
  .wholePane{
    width: 100%;
    height: 600px; 
    margin: 10px 0;
    border: 1px dashed #909399;
  }

  #scoreFigure{
    border: 1px dashed #909399;
    width: 60%;
    margin: 0 20%;
  }
  #scoreTxt{
    font-size: 14px;
    margin: 0 20%;
    overflow: auto;
  }
</style>
