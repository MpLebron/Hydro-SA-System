<template>
  <el-form  :model="simSetting" label-width="20%">

    <el-form-item label="敏感性分析方法">
      <el-select @change="changeSAMethod" v-model="simSetting.saMethod" size="small">
        <el-option-group
          v-for="group in saMethodGroup"
          :key="group.label"
          :label="group.label">
          <el-option
            v-for="item in group.saMethod"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-option-group>
      </el-select>
    </el-form-item>

    <el-form-item label="参数采样方法">
      <el-select @change="changeSampleMethod" v-model="simSetting.sampleMethod" size="small">
        <el-option
          v-for="item in sampleMethods"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="模拟次数" prop="simTimes">
      <div v-if="simSetting.sampleMethod=='finite_difference_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="0"></el-input-number>
        <span> * ({{paramsSum}} + 1) = {{simSetting.simTimes * (paramsSum+1)}}</span>
      </div>
      <div v-else-if="simSetting.sampleMethod=='uniform_sampler' || simSetting.sampleMethod=='monte_carlo_sampler' || simSetting.sampleMethod=='latin_hypercube_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="0"></el-input-number>
      </div>
      <div v-else-if="simSetting.sampleMethod=='morris_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="0"></el-input-number>
        <span> * ({{paramsSum}} + 1) = {{simSetting.simTimes * (paramsSum+1)}}</span>
      </div>
      <div v-else-if="simSetting.sampleMethod=='vbsa_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="0"></el-input-number>
        <span> * ({{paramsSum}}+ 2)  = {{simSetting.simTimes * (paramsSum+2)}}</span>
      </div>
      <div v-else-if="simSetting.sampleMethod=='sobol_sequence_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="0"></el-input-number>
        <span> * (2 * {{paramsSum}}+ 2)  = {{simSetting.simTimes * (2*paramsSum+2)}}</span>
      </div>
      <div v-else-if="simSetting.sampleMethod=='fast_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="65"></el-input-number>
      </div>
      <div v-else-if="simSetting.sampleMethod=='extended_fast_sampler'">
        <el-input-number v-model="simSetting.simTimes" controls-position="right" size="small" :min="66"></el-input-number>
        <span> * {{paramsSum}} = {{simSetting.simTimes * paramsSum}}</span>
      </div>
      <div v-else-if="simSetting.sampleMethod=='fractional_factorial_sampler'">
        <span> {{2**(Math.ceil(Math.log2(paramsSum))+1)}}</span>
      </div>
      <div v-else>请选择敏感性分析方法和参数采样方法</div>

    </el-form-item>

    <el-form-item label="目标函数" v-if="ObservationSwitch">
      <el-checkbox-group v-model="simSetting.objectiveFuns">
        <el-checkbox v-for="obj in objFuns" :label="obj" :key="obj">{{obj}}</el-checkbox>
      </el-checkbox-group>
    </el-form-item>

    <el-divider></el-divider>
    <!-- 用于展示SA方法与采样方法的文本信息，后面完善 -->
    

    <div id="methodDesc">
      <el-row :gutter="20">
        <el-col :span="10">
          <div>
            <el-carousel :autoplay='false' arrow="always">
              <el-carousel-item >
                <img class="criteria" :src="saUrl" />
              </el-carousel-item>
              <el-carousel-item >
                <img class="criteria" :src="funUrl" />
              </el-carousel-item>
            </el-carousel>
          </div>
        </el-col>
        <el-col :span="14">
          <div>
            <p><span class="methodTitle">敏感性分析方法：</span>{{saMethodInfo}}</p>
            <p><span class="methodTitle">参数采样方法：</span>{{sampleMethodInfo}}</p>
            <p><span class="methodTitle">目标函数含义：</span>{{objFunsInfo}}</p>
          </div>
        </el-col>
      </el-row>
      
    </div>
    
  </el-form>
</template>

<script>

export default {
  name: "SimSetting",
  props: ['simSetting','paramsSum','ObservationSwitch'],
  data(){
    return{
      sampleMethods:[],
      objFuns:['Nash','RSquared','Log','DRMS','ROCE','QRE','RE'],

      saUrl:'../static/images/SAmethods.png',
      funUrl:'../static/images/ObjectiveFuns.png',
        
      saMethodInfo:'Morris，Morris在1991年提出的元效应方法，也被称为Morris方法或EET法或Morris-OAT法，是一种定性筛选参数敏感性的方法。',
      sampleMethodInfo:'Morris的采样方法是特定的，样本量 = T*(G+1)  T:轨迹数N  G:分组数，没有就是D（参数量）',
      objFunsInfo:`Nash效率系数：用于评价实测值与模拟值两个序列的吻合程度；确定性系数R^2：用于评价实测值与模拟值两个序列的吻合程度；
                  实测和模拟流量的LOG函数：侧重于小流量值的拟合误差；实测和模拟流量的DRMS函数：侧重于大流量值的拟合误差；
                  径流系数误差ROCE：强调模拟过程整体的拟合精度；洪峰相对误差Qre：用于评价洪峰模拟误差；水量相对误差RE。`
      
    }
  },
  created(){
    this.saMethodGroup = [
      {
        label:"基于导数的全局方法",
        saMethod:[{label:'DGSM',value:'dgsm'}]
      },
      {
        label:"定性筛选法",
        saMethod:[{label:'Morris',value:'morris'}]
      },
      {
        label:"区域敏感性分析",
        saMethod:[{label:'RSA',value:'rsa'}]
      },
      {
        label:"基于方差的方法",
        saMethod:[{label:'VBSA',value:'vbsa'},{label:'Sobol',value:'sobol'},{label:'FAST',value:'fast'},{label:'RBD-FAST',value:'rbd_fast'},{label:'eFAST',value:'extended_fast'}]
      },
      {
        label:"基于密度的方法",
        saMethod:[{label:'Delta',value:'delta'},{label:'PAWN',value:'pawn'}]
      },
      {
        label:'其他方法',
        saMethod:[{label:'Fractional Factorial',value:'fractional_factorial'}]
      }        
    ]
    this.sampleMethodGroup = [
      {
        saMethod:'dgsm',
        sampleMethods:[{
          label:'Finite Difference Sampler',
          value:'finite_difference_sampler',
          rule:'N*(D+1)'
        }]
      },
      {
        saMethod:'rsa',
        sampleMethods:[{
          label:'Uniform Sampler',
          value:'uniform_sampler',
          rule:'N'
        },{
          label:'Monto Carlo Sampler',
          value:'monte_carlo_sampler',
          rule:'N'
        },{
          label:'Latin Hypercube Sampler',
          value:'latin_hypercube_sampler',
          rule:'N'
        }]
      },
      {
        saMethod:'morris',
        sampleMethods:[{
          label:'Morris Sampler',
          value:'morris_sampler',
          rule:'N*(D+1)'
        }]
      },
      {
        saMethod:'vbsa',
        sampleMethods:[{
          label:'VBSA Sampler',
          value:'vbsa_sampler',
          rule:'N*(D+2)'
        }]
      },
      {
        saMethod:'sobol',
        sampleMethods:[{
          label:'Sobol Sampler',
          value:'sobol_sequence_sampler',
          rule:'N*(2D+2)'
        }]
      },
      {
        saMethod:'fast',
        sampleMethods:[{
          label:'FAST Sampler',
          value:'fast_sampler',
          rule:'N  N > 64'
        }]
      },
      {
        saMethod:'rbd_fast',
        sampleMethods:[{
          label:'Uniform Sampler',
          value:'uniform_sampler',
          rule:'N'
        },{
          label:'Monte Carlo Sampler',
          value:'monte_carlo_sampler',
          rule:'N'
        },{
          label:'Latin Hypercube Sampler',
          value:'latin_hypercube_sampler',
          rule:'N'
        }]
      },
      {
        saMethod:'extended_fast',
        sampleMethods:[{
          label:'Extended FAST Sampler',
          value:'extended_fast_sampler',
          rule:'N*D  N > 64'
        }]
      },
      {
        saMethod:'delta',
        sampleMethods:[{
          label:'Uniform Sampler',
          value:'uniform_sampler',
          rule:'N'
        },{
          label:'Monte Carlo Sampler',
          value:'monte_carlo_sampler',
          rule:'N'
        },{
          label:'Latin Hypercube Sampler',
          value:'latin_hypercube_sampler',
          rule:'N'
        }]
      },
      {
        saMethod:'pawn',
        sampleMethods:[{
          label:'Uniform Sampler',
          value:'uniform_sampler',
          rule:'N'
        },{
          label:'Monte Carlo Sampler',
          value:'monte_carlo_sampler',
          rule:'N'
        },{
          label:'Latin Hypercube Sampler',
          value:'latin_hypercube_sampler',
          rule:'N'
        }]
      },
      {
        saMethod:'fractional_factorial',
        sampleMethods:[{
          label:'Fractional Factorial Sampler',
          value:'fractional_factorial_sampler',
          rule:'2^([log2 D]+1)'
        }]
      },
    ]
    this.saMethodDesc = [
      {
        saMethod:'dgsm',
        description:'DGSM，与微分分析法相似，利用一阶偏导数来评估每个参数的敏感性，计算成本较低，但是只能提供局部敏感性信息。'
      },
      {
        saMethod:'morris',
        description:'Morris，Morris在1991年提出的元效应方法，也被称为Morris方法或EET法或Morris-OAT法，是一种定性筛选参数敏感性的方法。'
      },
      {
        saMethod:'rsa',
        description:'RSA，区域敏感性分析方法，是Young等于1980年左右提出的一种重要的全局敏感性分析方法，借助累积分布函数计算参数敏感性。'
      },
      {
        saMethod:'vbsa',
        description:`VBSA，基于方差的敏感性分析方法，与Sobol'方法相似，但只能输出一阶和全阶敏感性指数，无法分析参数之间的相互关系。`
      },
      {
        saMethod:'sobol',
        description:`Sobol',是基于方差类方法中最早出现的一个方法，可以输出一阶、二阶和全阶的敏感性指数，但需要相当大的样本量来支持以上敏感性指标的计算。`
      },
      {
        saMethod:'fast',
        description:'FAST，傅里叶振幅灵敏度检验法，理论来源于傅里叶变换和方差分析方法，可用于计算一阶敏感性指标。'
      },
      {
        saMethod:'rbd_fast',
        description:'RBD-FAST，由随机平衡设计与FAST方法耦合而成，可用于计算一阶敏感性指标，但大大减少了模型计算需求。'
      },
      {
        saMethod:'extended_fast',
        description:`eFAST，扩展傅里叶振幅灵敏度检验法，由Saltelli提出的一种基于方差的全局方法，它集成了FAST法和Sobol法的优点。`
      },
      {
        saMethod:'delta',
        description:'Delta，δ矩独立测度方法，该类方法不再仅仅使用模型输出分布的特定矩来表达不确定性，而是关注模型输出的整个概率密度函数。'
      },
      {
        saMethod:'pawn',
        description:'PAWN，是由Pianosi等人提出的一种新的矩独立全局敏感性分析方法，该方法为了简化数值实现，使用累积分布函数（CDF）代替了概率密度函数（PDF）。'
      },
      {
        saMethod:'fractional_factorial',
        description:'Fractional Factorial，部分析因分析法。'
      }
    ]
    this.sampleMethodDesc = [
      {
        sampleMethod:'uniform_sampler',
        description:'均匀采样，样本量 = 预设运行次数'
      },
      {
        sampleMethod:'monte_carlo_sampler',
        description:'蒙特卡罗采样，样本量 = 预设运行次数'
      },
      {
        sampleMethod:'latin_hypercube_sampler',
        description:'拉丁超立方体采样，样本量 = 预设运行次数'
      },
      {
        sampleMethod:'fractional_factorial_sampler',
        description:'部分析因分析法的特定采样方法，样本量 = 2^([log2 D]+1)  D是参数量'
      },
      {
        sampleMethod:'finite_difference_sampler',
        description:'DGSM的特定采样方法，样本量 = N*(D+1) D是参数量'
      },
      {
        sampleMethod:'morris_sampler',
        description:'Morris的特定采样方法，样本量 = T*(G+1)  T:轨迹数N  G:分组数，没有就是D（参数量）'
      },
      {
        sampleMethod:'vbsa_sampler',
        description:'VBSA的特定采样方法，样本量 = N*(D+2)  D是参数量'
      },
      {
        sampleMethod:'sobol_sequence_sampler',
        description:`Sobol'的特定采样方法，样本量 = N*(D+2) | N*(2D+2)  D是参数量，N 应该是2的幂次方`
      },
      {
        sampleMethod:'fast_sampler',
        description:'FAST的特定采样方法，样本量 = N  N > 64'
      },
      {
        sampleMethod:'extended_fast_sampler',
        description:'eFAST的特定采样方法，样本量 = N*D  D是参数量  N > 64'
      }
    ]
  },
  methods:{
    changeSAMethod(value){
      this.simSetting.sampleMethod = ''
      for (let i = 0; i < this.sampleMethodGroup.length; i++) {
        const group = this.sampleMethodGroup[i];
        if(group.saMethod === value){
          this.sampleMethods = group.sampleMethods
          break
        }
      }

      // 更新描述
      for (let i = 0; i < this.saMethodDesc.length; i++) {
        const method = this.saMethodDesc[i];
        if(method.saMethod == value){
          this.saMethodInfo = method.description
          break
        }
      }
      this.sampleMethodInfo=""
    },

    changeSampleMethod(value){
      // 更新描述
      for (let i = 0; i < this.sampleMethodDesc.length; i++) {
        const method = this.sampleMethodDesc[i];
        if(method.sampleMethod == value){
          this.sampleMethodInfo = method.description
          break
        }
      }
    }
  }
}
</script>

<style scoped>
#methodDesc{
  padding: 0 10% 0 5%;
  font-size: 14px;
}
.criteria{
  /* height: 100%; */
  width: 100%;
}
.methodTitle{
  font-weight: bold;
}
</style>