<template>
  <div>
    <Header/>
    <div id="CredibilityContainer">
      <el-page-header id="pageHeader" @back="goBack" content="可信度检验页面"></el-page-header>

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
            <el-select v-model="var1" placeholder="请选择">
              <el-option
                v-for="item in variables1"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
            <el-select v-model="var2" placeholder="请选择">
              <el-option
                v-for="item in variables2"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>

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
      targetSimilarity:[],

      variables1:[],
      var1:'',
      variables2:[],
      var2:'',
    }
  },
  methods:{
    goBack(){
      this.$router.back()
    },
    computeSimilarity(){
      this.targetSimilarity = []
      // 分target计算两次项目SA结果的相似性，需要指定用于比较的coreVariable
      // scoreSA.score记录有需要用于比较的字段，都是以一维数组存储
      // 计算标准，var1和var2的包含程度、排序差异 M*50% + num(diff)/num(allParam)*50% abc acb，相似度=1-0.5-2/3
      let scores1 = this.parseScoreSA(this.projects[0].scoreSA)
      let scores2 = this.parseScoreSA(this.projects[1].scoreSA)
      let targets = this.projects[0].simSetting.simTargets
      // 因为同一个模型的target顺序是一致的，所以直接按照顺序来计算就ok
      for (let i = 0; i < scores1.length; i++) {
        const s1 = scores1[i]
        const s2 = scores2[i]
        let similarity = 0
        // 对两个score进行排序，比较顺序
        let map1 = s1[this.var1].map((value,index)=>{return {param:this.projects[0].paramList[index].name, value:value}})
        let map2 = s2[this.var2].map((value,index)=>{return {param:this.projects[0].paramList[index].name, value:value}})
        // 降序
        map1.sort((a,b)=>{return b.value-a.value})
        map2.sort((a,b)=>{return b.value-a.value})
        // 为防止不敏感参数的干扰，应只选择一定分数以上的参数，例如大于0.1
        let newMap1 = map1.slice(0,map1.findIndex(a=>a.value<0.1))
        let newMap2 = map2.slice(0,map2.findIndex(a=>a.value<0.1))
        // 先计算前一半
        let mlen1 = newMap1.length,
            mlen2 = newMap2.length,
            pnums = 0,//参数个数
            firstHalf
        if (mlen1<mlen2) {
          for (let i = 0; i < mlen1; i++) {
            let param = newMap1[i].param
            if(newMap2.findIndex(a=>a.param===param)){
              pnums++
            }
          }
        }else{
          for (let i = 0; i < mlen2; i++) {
            let param = newMap2[i].param
            if(newMap1.findIndex(a=>a.param===param)){
              pnums++
            }
          }
        }
        firstHalf = (pnums/mlen1)*0.5
        // 再计算后一半
        let minLen = mlen1<mlen2 ? mlen1:mlen2,
            snum = 0, // 顺序相同的参数数量
            secondHalf
        for (let j = 0; j < minLen; j++) {
          const t1 = newMap1[j].param;
          const t2 = newMap2[j].param;
          if(t1 != t2){
            snum++
          }
        }
        secondHalf = (snum/minLen)*0.5
        similarity = (1 - firstHalf - secondHalf).toFixed(3)

        this.targetSimilarity.push({
          target: targets[i],
          similarity: similarity
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
    // 初始化用于比较的核心变量
    initVariables(){
      let project = this.projects[0];
      let score = project.scoreSA[0].score
      let lines = score.includes("\r\n") ? score.split("\r\n"):score.split("\n")
      let index = lines.findIndex((line)=>{return line.startsWith("coreVariables")})
      let coreVariables = lines[index].split(": ")[1].split("\t")
      this.variables1 = coreVariables
      this.var1 = coreVariables[0]

      project = this.projects[1];
      score = project.scoreSA[0].score
      lines = score.includes("\r\n") ? score.split("\r\n"):score.split("\n")
      index = lines.findIndex((line)=>{return line.startsWith("coreVariables")})
      coreVariables = lines[index].split(": ")[1].split("\t")
      this.variables2 = coreVariables
      this.var2 = coreVariables[0]
    }
  },
  mounted(){
    this.projects = this.$route.params.projects
    this.initVariables()
  }

}
</script>

<style scoped>
  #CredibilityContainer{
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
  .el-select{
    margin-top: 5px;
  }
</style>