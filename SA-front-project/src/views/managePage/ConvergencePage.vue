<template>
  <div>
    <Header/>
    <div id="convergenceContainer">
      <el-page-header id="pageHeader" @back="goBack" content="收敛性检验页面"></el-page-header>

      <el-row :gutter="20">
        <el-col :span="10">
          <ProjectInfoColumn :project="projects[0]" />
        </el-col>
        <el-col :span="10">
          <ProjectInfoColumn :project="projects[1]" />
        </el-col>
        <el-col :span="4">
          <div id="btnContainer">
            <el-button id="similarityBtn" type="primary" plain @click="computeSimilarity">计算相似性</el-button>
          
            <div v-for="target in targetSimilarity" :key="target.target">
              <p><span>{{target.target}}: </span>{{target.similarity}}</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <Footer/>
  </div>
</template>

<script>
import Header from "../../components/Header.vue"
import Footer from "../../components/Footer.vue"
import ProjectInfoColumn from "@/views/managePage/ProjectInfoColumn.vue"
export default {
  components:{Header, Footer, ProjectInfoColumn},
  data(){
    return{
      projects:[],
      targetSimilarity:[]
    }
  },
  methods:{
    goBack(){
      this.$router.back()
    },

    computeSimilarity(){
      this.targetSimilarity = []
      // 分target计算两次项目SA结果的相似性
      // scoreSA.score记录有需要用于比较的字段，都是以一维数组存储
      // 计算标准，1-average((ai-bi)/min(ai,bi))
      let scores1 = this.parseScoreSA(this.projects[0].scoreSA)
      let scores2 = this.parseScoreSA(this.projects[1].scoreSA)
      // 因为同一个模型的target顺序是一致的，所以直接按照顺序来计算就ok
      let similaritys = []
      for (let i = 0; i < scores1.length; i++) {
        const s1 = scores1[i]
        const s2 = scores2[i]
        let similarity = 0
        // 计算每个参数的平均相似度
        for (const key in s1) {
          let similar = 0
          // 计算单个数组的平均相似度
          let nums = 0 // 计数，大于0.1的个数
          for (let j = 0; j < s1[key].length; j++) {
            const ele1 = s1[key][j]
            const ele2 = s2[key][j]
            // 为防止不敏感参数的干扰，应只选择一定分数以上的参数，例如大于0.1
            if(ele1>=0.1 || ele2>=0.1){
              nums++
              similar += this.getSimilar(ele1, ele2)
            }
          }
          similar = similar/nums
          similarity += similar
        }
        similarity = (1 - similarity/Object.keys(s1).length).toFixed(3)
        similaritys.push(similarity)
      }
      
      // 开始合并target及其相似度
      let targets = this.projects[0].simSetting.simTargets
      for (let i = 0; i < targets.length; i++) {
        const t = targets[i];
        this.targetSimilarity.push({
          target: t,
          similarity: similaritys[i]
        })
      }

    },
    parseScoreSA(scoreSA){
      let scoreArr = []
      for (let i = 0; i < scoreSA.length; i++) {
        const score = scoreSA[i];
        let scoreCoreObj =  this.parseScore(score.score)
        scoreArr.push(scoreCoreObj)
      }

      return scoreArr
    },
    parseScore(score){
      let obj = {}

      let lines = score.includes("\r\n") ? score.split("\r\n"):score.split("\n")
      // 找到用于比较的参数
      let index = lines.findIndex((line)=>{return line.startsWith("coreVariables")})
      let coreVariables = lines[index].split(": ")[1].split("\t")
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        let vary = line.split(": ")[0]
        if(coreVariables.includes(vary)){
          let values = line.split(": ")[1].split("\t")
          obj[vary] = values.map((value)=>parseFloat(value))
        }
      }

      return obj
    },
    getSimilar(ele1, ele2){
      // 防止除以0
      if(ele1-ele2 < 1e-5)
        return 0
      else if(Math.abs(ele1)<1e-5 || Math.abs(ele2)<1e-5)
        return 1
      else{
        let s = ele1>ele2 ? (ele1-ele2)/Math.abs(ele2) : (ele2-ele1)/Math.abs(ele1)
        return s<1 ? s:1
      }
    }
  },
  mounted(){
    this.projects = this.$route.params.projects
  }

}
</script>

<style scoped>
  #convergenceContainer{
    width: 80%;
    margin: auto;
  }
  #pageHeader{
    margin: 20px 0;
  }
  #btnContainer{
    background:rgb(226, 240, 217);
    padding: 20px;
    border-radius: 10px;
  }
  #similarityBtn{
    display: block;
    margin: auto;
  }
</style>