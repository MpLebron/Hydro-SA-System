<template>
  <div>
    <Header/>

    <div id="projectsContainer">

      <el-page-header id="pageHeader" @back="goBack" content="项目管理页面"></el-page-header>

      <el-table
        :data="projectList"
        height="600"
        border
        style="width: 100%"
        @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          width="40">
        </el-table-column>
        <el-table-column
          label="项目名称"
          width="130"
          sortable
          :sort-by="['createTime']">
          <template slot-scope="scope">
            <div>{{scope.row.name}}</div> 
            <div style="font-size:smaller; color:#aaa">{{new Date(scope.row.createTime).toLocaleString()}}</div>
          </template>
        </el-table-column>
        <el-table-column
          prop="description"
          label="项目描述">
        </el-table-column>
        <el-table-column
          prop="modelName"
          label="模型名称"
          width="130"
          :filters="modelNames"
          :filter-method="filterByModelName">
        </el-table-column>
        <el-table-column
          label="评估参数"
          width="200">
          <template slot-scope="scope">
            <div v-for="param in scope.row.paramList" :key="param.name">
              {{param.name + ": " + param.changeType + "(" + param.left + ","+ param.right + ")"}}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="SA+采样方法+目标函数"
          width="200"
          :filters="saMethods"
          :filter-method="filterBySAMethod">
          <template slot-scope="scope">
            <div>SA方法: {{scope.row.simSetting.saMethod}}</div> 
            <div>采样方法: {{scope.row.simSetting.sampleMethod}}</div> 
            <div>目标函数: {{scope.row.simSetting.objectiveFuns!=null?scope.row.simSetting.objectiveFuns.toString():"默认统计量（平均值）"}}</div> 
          </template>
        </el-table-column>
        <el-table-column
          label="模拟次数"
          width="80">
          <template slot-scope="scope">
            {{scope.row.paramsSet.length}}
          </template>
        </el-table-column>
        <el-table-column 
          label="SA结果"
          width="250">
          <template slot-scope="scope">
            <el-carousel height="200px" direction="vertical" :autoplay="false" >
              <el-carousel-item v-for="item in scope.row.scoreSA" :key="item.target">
                <div style="text-align:center; bottom:0">{{item.target}}</div> 
                <img style="max-height:180px" :src="'data:'+item.figure.contentType+';base64,'+item.figure.content.data" alt="">
              </el-carousel-item>
            </el-carousel>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="50">
          <template slot-scope="scope">
            <div>
              <el-button disabled @click="editProject(scope.row.pid)" type="primary" icon="el-icon-edit" circle size="small" ></el-button>
            </div>
            <div style="margin-top:10px">
              <el-button disabled @click="deleteProject(scope.row.pid)" type="danger" icon="el-icon-delete" circle size="small" ></el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 进入项目对比页面 -->
      <div id="enterBtns">
        <el-button id="convergenceEnter" type="primary" plain @click="turnToConvergencePage">收敛性检验</el-button>
        <el-button id="credibilityEnter" type="primary" plain @click="turnToCredibilityPage">可信度检验</el-button>
      </div>
    </div>


    <Footer/>
  </div>
</template>

<script>
import Header from "../../components/Header.vue"
import Footer from "../../components/Footer.vue"
export default {
  components:{Header, Footer},
  data(){
    return{
      projectList:[],
      modelNames:[],
      saMethods:[],
      projectsSelection:[]
    }
  },
  methods:{
    goBack(){
      this.$router.back()
    },
    modifyCarouselBtns(){
      setTimeout(()=>{
        let carouselBtns = document.getElementsByClassName("el-carousel__button")
        for (let i = 0; i < carouselBtns.length; i++) {
          carouselBtns[i].style.backgroundColor = "#aaa"
        }
      },0)
    },

    // 可以进入比较页面的条件是
    // 1、收敛性检验：相同模型 （相同研究区） 相同参数与调整范围 相同SA方法 不同模拟次数  （括号内不可控）
    turnToConvergencePage(){
      // 检查前提条件
      if(this.projectsSelection.length !=2){
        alert("请选择两个项目")
        return
      }else if(this.projectsSelection[0].md5 != this.projectsSelection[1].md5){
        alert("请选择使用相同模型的两次项目")
        return
      }else if(!this.checkParamList(this.projectsSelection[0].paramList, this.projectsSelection[1].paramList)){
        alert("请选择具有相同参数与调整范围的两次项目")
        return
      }else if(this.projectsSelection[0].simSetting.saMethod != this.projectsSelection[1].simSetting.saMethod){
        alert("请选择具有相同SA方法的两次项目")
        return
      }
      // 验证通过
      this.$notify({
        title: '成功',
        message: '进入收敛性检验页！',
        type: 'success'
      });

      this.$router.push({name:"ConvergencePage",params:{projects:this.projectsSelection}})

    },
    // 2、可信度检验：相同模型 （相同研究区） 相同参数与调整范围 不同SA方法 （都达到收敛） （括号内不可控）
    turnToCredibilityPage(){
      // 检查前提条件
      if(this.projectsSelection.length !=2){
        alert("请选择两个项目")
        return
      }else if(this.projectsSelection[0].md5 != this.projectsSelection[1].md5){
        alert("请选择使用相同模型的两次项目")
        return
      }else if(!this.checkParamList(this.projectsSelection[0].paramList, this.projectsSelection[1].paramList)){
        alert("请选择具有相同参数与调整范围的两次项目")
        return
      }else if(this.projectsSelection[0].simSetting.saMethod == this.projectsSelection[1].simSetting.saMethod){
        alert("请选择具有不同SA方法的两次项目")
        return
      }
      // 验证通过
      this.$notify({
        title: '成功',
        message: '进入可信度检验页！',
        type: 'success'
      });

      
      this.$router.push({name:"CredibilityPage",params:{projects:this.projectsSelection}})

    },
    checkParamList(paramList1, paramList2){
      if(paramList1.length != paramList2.length)
        return false

      for (let i = 0; i < paramList1.length; i++) {
        const param1 = paramList1[i];
        let flag = false
        for (let j = 0; j < paramList2.length; j++) {
          const param2 = paramList2[j];
          // 参数名相同
          if(param1.name === param2.name){
            // 参数调整方式与范围相同
            if(param1.changeType===param2.changeType && param1.left===param2.left && param1.right===param2.right){
              flag = true
              break
            }else{
              return false
            }
          }
        }
        if(!flag)
          return false
      }

      return true
    },

    // 筛选相关函数
    initFilterData(){
      for (let i = 0; i < this.projectList.length; i++) {
        const project = this.projectList[i];
        this.modelNames.push({
          text:project.modelName,
          value:project.modelName
        })
        this.saMethods.push({
          text:project.simSetting.saMethod,
          value:project.simSetting.saMethod
        })
      }

      this.modelNames = this.modelNames.filter((item, index, arr)=>{
        return arr.findIndex(el=>el.value==item.value) === index
      })
      this.saMethods = this.saMethods.filter((item, index, arr)=>{
        return arr.findIndex(el=>el.value==item.value) === index
      })
    },
    filterByModelName(value, row, column){
      const property = column["property"]
      return row[property] === value
    },
    filterBySAMethod(value, row, column){
      return row.simSetting.saMethod === value
    },
    handleSelectionChange(val) {
      this.projectsSelection = val;
    },
    
    // 编辑和删除项目
    editProject(pid){
      // this.$router.push({name:"SAPage",params:{pid:pid}})
    },
    deleteProject(pid){

    }
  },
  mounted(){
    let that = this
    // 获取所有运行成功的项目
    this.$axios.get(
      '/SA-back-project/project/getAllProjects'
    ).then(response => {
      let data = response.data
      if(data.code == 0){
        that.projectList = data.data
        that.modifyCarouselBtns()
        that.initFilterData()
      }
    }).catch(reason => {
      console.log(reason)
    })
  }
}
</script>

<style scoped>
  #projectsContainer{
    width: 90%;
    margin: auto;
    min-height: 500px;
  }
  #pageHeader{
    margin: 20px 0;
  }
  #enterBtns{
    text-align: center;
    margin-top: 20px;
  }
</style>