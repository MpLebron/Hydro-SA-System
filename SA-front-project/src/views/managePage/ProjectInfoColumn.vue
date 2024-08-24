<template>
  <div id="container" v-if="project != null">
    <div class="subTitle">项目信息</div>
    <p><span>项目名称：</span>{{project.name}}</p>
    <p><span>创建日期：</span>{{new Date(project.createTime).toLocaleString()}}</p>
    <p><span>项目描述：</span>{{project.description}}</p> 

    <div class="subTitle">模型信息</div>
    <p><span>模型名称：</span>{{project.modelName}}</p>
    <p><span>模型描述：</span>{{project.modelDescription}}</p>
    <p><span>模拟目标：</span>{{project.simSetting.simTargets.toString()}}</p>
    <p><span>模型参数：</span>
      <template v-for="param in project.paramList">
        {{param.name + ": " + param.changeType + "(" + param.left + ","+ param.right + ") "}}
      </template>
    </p>

    <div class="subTitle">配置信息</div>
    <p><span>敏感性分析方法：</span>{{project.simSetting.saMethod}}</p>
    <p><span>参数采样方法：</span>{{project.simSetting.sampleMethod}}</p>
    <p><span>观测数据：</span>{{project.simSetting.observations!=null?project.simSetting.observations.toString():"无"}}</p>
    <p><span>目标函数：</span>{{project.simSetting.objectiveFuns!=null?project.simSetting.objectiveFuns.toString():"默认统计量（平均值）"}}</p>
    <p><span>模拟次数：</span>{{project.paramsSet.length}}</p>

    <div class="subTitle">敏感性分析结果</div>
    <template>
      <el-carousel style="text-align:center; margin-top:10px; background:white" indicator-position="outside" :autoplay="false" >
        <el-carousel-item v-for="item in project.scoreSA" :key="item.target">
          <div style="position: absolute;bottom:0px;right:10px;">{{item.target}}</div> 
          <img style="max-height:100%;" :src="'data:'+item.figure.contentType+';base64,'+item.figure.content.data" alt="">
        </el-carousel-item>
      </el-carousel>
    </template>
        
  </div>
</template>

<script>
export default {
  name:'ProjectInfoColumn',
  
  props: ['project'],
  data(){
    return{
    }
  },
  mounted(){

  }

}
</script>

<style>
  #container{
    padding: 20px;
    background: rgb(222, 235, 246);
    border-radius: 10px;
  }
  .subTitle{
    text-align: center;
    font-size: large;
    margin-top: 10px;
  }
  p{
    margin: 5px 0;
  }
  p span{
    font-weight: bold;
  }
</style>