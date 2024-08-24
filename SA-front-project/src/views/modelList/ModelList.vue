<template>
  <div> 
    <Header />
    <div id="modelListContainer">
      <el-row>
        <el-col :span="18"><span id="topicTitle">敏感性分析专题</span></el-col>
        <el-col :span="3"><el-button id="libraryEnter" type="primary" plain @click="turnToLibraryPage">知识库</el-button></el-col>
        <el-col :span="3"><el-button id="projecEnter" type="primary" plain @click="turnToProjectManagePage">项目库</el-button></el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row :gutter="20">
        <el-col :span="6"  v-for="(model,key) in modelList" :key="key">
          <el-card shadow="hover"  :body-style="{ padding: '0px' }">
            <img src="http://geomodeling.njnu.edu.cn/static/modelItem/5299fa74-0d3a-4cd5-a005-d2613b0b51f9.jpg" class="image">
            <div style="padding: 14px;">
              <span>{{model.name}}</span>
              <div class="bottom clearfix">
                <el-button type="text" @click="createProject(model)" class="button">新建项目</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
        <!-- 上传模型页面 -->
        <el-col :span="6" >
          <el-card shadow="hover"  :body-style="{ padding: '0px' }">
            <img src="http://geomodeling.njnu.edu.cn/static/theme//00e92d1e-1d91-4612-89eb-373507b78bf0.jpg" class="image">
            <div style="padding: 14px;">
              <span>New Model</span>
              <div class="bottom clearfix">
                <el-button type="text" @click="contributeModel()" class="button">贡献模型</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <Footer />

    <el-dialog
      title="新建SA项目"
      :visible.sync="newProjectDialog"
      width="30%"
      center>
      <el-form label-position="top" label-width="80px" :rules="rules"  :model="SA_Project"  size="small">
        <el-form-item label="名称" prop="name">
          <el-input v-model="SA_Project.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="SA_Project.description"></el-input>
        </el-form-item>
        <el-form-item style="text-align:center">
          <el-button @click="newProjectDialog = false">取 消</el-button>
          <el-button type="primary" @click="turnToSAPage">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import Header from '../../components/Header'
import Footer from '../../components/Footer'
export default {
  components:{ Header, Footer },
  data(){
    return{
      modelList:[],
      newProjectDialog:false,

      SA_Project:{
        // 模型ID
        oid:'',
        name:'',
        description:'',
      },
      rules: {
        name: [
          { required: true, message: '请输入活动名称', trigger: 'blur' },
        ]
      }
    }
  },
  methods:{
    createProject(model){
      this.SA_Project.oid = model.oid
      this.SA_Project.name = "SA_" + model.name

      this.newProjectDialog = true
    },
    contributeModel(){
      this.$router.push({name:"ModelContribute"})
    },
    turnToSAPage(){
      this.newProjectDialog = false

      var that = this
      this.$axios.post(
        "/SA-back-project/project/create",this.SA_Project
      ).then(function(response){
        var data = response.data
        if(data.code == 0){
          var pid = data.data 
          that.$router.push({name:"SAPage",params:{pid:pid}})
        }
      })
      .catch(function(err){
        console.log(err)
      })
    },

    turnToLibraryPage(){
      this.$router.push({name:"LibraryPage"})
    },

    turnToProjectManagePage(){
      this.$router.push({name:"ProjectManagePage"})
    }
  },
  mounted(){
    var that = this

    this.$axios.get(
      '/SA-back-project/computableModel/allModel'
    ).then((response) => {
      var data = response.data
      if(data.code == 0){
        that.modelList = data.data
      }
    })
    .catch((error) => {
      console.log(error);
    });
  }
}
</script>

<style scoped>
  #modelListContainer{
    width: 80%;
    margin: auto;
    min-height: 500px;
  }
  #topicTitle{
    font-size: 2em;
    font-weight: bold;
  }
  #libraryEnter{
    float: right;
    /* margin: 0 20px; */
    font-size: 1.2em;
    font-weight: bold;
  }
  #projecEnter{
    float: right;
    margin: 0 10px;
    font-size: 1.2em;
    font-weight: bold;
  }
  .cardContanier{
    width: 30%;
    margin: 1% 1.5%;
    float: left;
  } 
  .image {
    width: 100%;
    height: 150px;
    display: block;
  }
  
  .el-col-6 {
    padding-bottom: 10px;
  }

</style>