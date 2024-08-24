<template>
  <div>
    <Header />

    <div id="modelContainer">
        
        <el-page-header id="pageHeader" @back="goBack" content="模型贡献页面"></el-page-header>

        <el-row :gutter="20">
          <!-- 地图 -->
          <el-col id="imageContainer" :span="10">
            <el-image :src="imageUrl" fit="contain"></el-image>

            <el-upload
              class="upload-demo"
              action="">
              <el-button disabled size="small" plain>点击上传</el-button>
            </el-upload>
          </el-col>
          
          <!-- 表单 -->
          <el-col :span="14">
            <el-form label-width="100px" :model="modelService">

              <el-form-item label="模型名称" prop="name">
                <el-input v-model="modelService.name" size="medium"></el-input>
              </el-form-item>
              <el-form-item label="基本描述" prop="description">
                <el-input type="textarea" size="medium" v-model="modelService.description"></el-input>
              </el-form-item>
              <el-form-item label="服务标识" prop="md5">
                <el-input v-model="modelService.md5" size="medium"></el-input>
              </el-form-item>
              <el-form-item label="模型描述文档" prop="mdl">
                <el-input type="textarea" size="medium" v-model="modelService.mdl"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button disabled id="submitBtn" @click="submitModelService" size="medium" plain>提交</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

    </div>

    <Footer id="modelListFooter"  />

  </div>
</template>

<script>
import Header from '../../components/Header'
import Footer from '../../components/Footer'
export default {
  components:{ Header, Footer },
  data(){
    return{
      imageUrl: 'http://geomodeling.njnu.edu.cn/static/theme//00e92d1e-1d91-4612-89eb-373507b78bf0.jpg',
      
      modelService:{
        name:'',
        description:'',
        md5:'',
        mdl:'',
        image:{}
      }
    }
  },
  methods:{
    goBack(){
      this.$router.back()
    },
    submitModelService(){
      // todo
    }
  }

}
</script>

<style scoped>
  #pageHeader{
    margin: 20px 0;
  }
  #modelContainer{
    width: 70%;
    margin: auto;
    min-height: 500px;
  }
</style>