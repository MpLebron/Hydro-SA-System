<template>
  <div>
    <div v-if="optSet.length == 0">
      没有配置观测数据，无法进行参数率定
    </div>
    <template  v-for="opt in optSet" >
      <el-divider :key="opt.target" style="width: 90%;margin: 24px auto;">最优参数组 ({{opt.target}})</el-divider>
      <!-- NSE -->
      <el-table v-if="opt.optNseSet!=undefined &&opt.optNseSet.length != 0"
        :data="opt.optNseSet"
        :key="opt.target+'nse'"
        :header-cell-style="getRowClass"
        border
        class="paramTable" style="margin: 5px auto;">
        <el-table-column
          v-for="(item,key) in nashSetName"
          :key="key"
          :prop="item"
          :label="item">
        </el-table-column>
      </el-table>
      <!-- RSquared -->
      <el-table v-if="opt.optR2Set!=undefined &&opt.optR2Set.length != 0"
        :data="opt.optR2Set"
        :key="opt.target+'r2'"
        :header-cell-style="getRowClass"
        border
        class="paramTable" style="margin: 5px auto;">
        <el-table-column
          v-for="(item,key) in r2SetName"
          :key="key"
          :prop="item"
          :label="item">
        </el-table-column>
      </el-table>
    </template>
  </div>
</template>

<script>
export default {
  name:'ParamCaResult',
  props:[ 'paramsName','paramsSet','simSetting','scoreObj' ],
  methods:{
    getRowClass() {
        return "background:#f5f7fa;color:#303133;";
    },

    loadObj(){
      // 组织表头
      let nashSetName = this.deepClone(this.paramsName)
      nashSetName.unshift("Nash")
      let r2SetName = this.deepClone(this.paramsName)
      r2SetName.unshift("RSquared")
      let logSetName = this.deepClone(this.paramsName)
      logSetName.unshift("Log")
      let drmsSetName = this.deepClone(this.paramsName)
      drmsSetName.unshift("DRMS")
      let roceSetName = this.deepClone(this.paramsName)
      roceSetName.unshift("ROCE")
      let qreSetName = this.deepClone(this.paramsName)
      qreSetName.unshift("QRE")
      let reSetName = this.deepClone(this.paramsName)
      reSetName.unshift("RE")

      this.nashSetName = nashSetName
      this.r2SetName = r2SetName
      this.logSetName=logSetName
      this.drmsSetName=drmsSetName
      this.roceSetName=roceSetName
      this.qreSetName=qreSetName
      this.reSetName=reSetName

      // 组织表内数据
      let optSet = []
      for (let j = 0; j < this.simSetting.observations.length; j++) {
        let target = this.simSetting.observations[j];

        let nashSet=[], r2Set=[], logSet=[], drmsSet=[], roceSet=[], qreSet=[], reSet=[]
        for (let i = 0; i < this.paramsSet.length; i++) {
          let set1 = this.deepClone(this.paramsSet[i])
          let set2 = this.deepClone(this.paramsSet[i])
          let set3 = this.deepClone(this.paramsSet[i])
          let set4 = this.deepClone(this.paramsSet[i])
          let set5 = this.deepClone(this.paramsSet[i])
          let set6 = this.deepClone(this.paramsSet[i])
          let set7 = this.deepClone(this.paramsSet[i])
          for (let k = 0; k < this.scoreObj.length; k++) {
            let obj = this.scoreObj[k];
            if(obj.Event == target)  {
              set1.unshift(parseFloat(obj.Nash[i].toFixed(2)))
              set2.unshift(parseFloat(obj.RSquared[i].toFixed(2)))
              set3.unshift(parseFloat(obj.Log[i].toFixed(2)))
              set4.unshift(parseFloat(obj.DRMS[i].toFixed(2)))
              set5.unshift(parseFloat(obj.ROCE[i].toFixed(2)))
              set6.unshift(parseFloat(obj.QRE[i].toFixed(2)))
              set7.unshift(parseFloat(obj.RE[i].toFixed(2)))
              break
            }
          }
          nashSet.push(set1)
          r2Set.push(set2)
          logSet.push(set3)
          drmsSet.push(set4)
          roceSet.push(set5)
          qreSet.push(set6)
          reSet.push(set7)
        }
        // 顺序不一定都是降序 没有修改完，因为这个组件打算删掉
        nashSet.sort((a,b)=>{return b[0]-a[0]})
        r2Set.sort((a,b)=>{return b[0]-a[0]})
        logSet.sort((a,b)=>{return b[0]-a[0]})
        drmsSet.sort((a,b)=>{return b[0]-a[0]})
        roceSet.sort((a,b)=>{return b[0]-a[0]})
        qreSet.sort((a,b)=>{return b[0]-a[0]})
        reSet.sort((a,b)=>{return b[0]-a[0]})

        var optNseSet = []
        var optR2Set = []
        if(nashSet.length < 10){
          // 只要排头兵
          optNseSet = nashSet.slice(0,1)
          optR2Set = r2Set.slice(0,1)
        }else if(nashSet.length < 100){
          // 要2个排头兵
          optNseSet = nashSet.slice(0,2)
          optR2Set = r2Set.slice(0,2)
        }else{
          // 要5个排头兵
          optNseSet = nashSet.slice(0,5)
          optR2Set = r2Set.slice(0,5)
        }
        var optNseDataSet = []
        var optR2DataSet = []
        for (let n = 0; n < optNseSet.length; n++) {
          var set1 = {}
          var set2 = {}
          for (let m = 0; m < nashSetName.length; m++) {
            set1[nashSetName[m]]=optNseSet[n][m]
            set2[r2SetName[m]]=optR2Set[n][m]
          }
          optNseDataSet.push(set1)
          optR2DataSet.push(set2)
        }
        optSet.push({
          target:target,
          optNseSet:optNseDataSet,
          optR2Set:optR2DataSet
        })
      }
      
      this.optSet = optSet

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
      nashSetName: [],
      r2SetName: [],
      logSetName:[],
      drmsSetName:[],
      roceSetName:[],
      qreSetName:[],
      reSetName:[],

      optSet : [],
    }
  }
}
</script>

<style scoped>

  .paramTable {
    font-family: "Times New Roman";
    width: 95%;
  }
</style>