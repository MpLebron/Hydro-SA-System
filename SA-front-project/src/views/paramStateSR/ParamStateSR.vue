<template>
  <div>
    <el-row type="flex" class="state-container"
            justify="start" style="flex-wrap:wrap" >
      <div class="leftContainer">
        <div class="modelState">
          <el-button class="addParamBtn" type="primary" size="mini" icon="el-icon-plus" circle
                      @click="selectionDialogVisible=true">
          </el-button>
          <p class="state-name"> {{state.name}}</p>
          <p class="state-desc"> {{state.desc}}</p>
        </div>
      </div>
      <div class="dataContainer">

        <!-- 输入event -->
        <div class="_params-group">
          <div class="_items">
            <el-row v-for="(param,index) in selectedParams"
                    :key="index" class="_item">
              
              <!-- event名称 与 描述信息 -->
              <el-row>
                <span class="event-name"> {{param.name}} </span>
                <span class="event-desc"> {{param.desc}} </span>
              </el-row>

              <!-- 参数信息 -->
              <el-row>
                <el-table :data="param.table" border style="width: 100%">
                  <el-table-column prop="changeType" label="Type of Change">
                    <template slot-scope="scope">
                      <el-select v-model="scope.row.changeType" size="small" >
                        <el-option
                          v-for="item in options"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value">
                        </el-option>
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column label="Value">
                    <template slot-scope="scope">
                      <el-input class="model-input" size="small" v-model="scope.row.value" />
                    </template>
                  </el-table-column>
                  <el-table-column label="Operation">
                    <template slot-scope="scope">
                      <el-button size="mini" type="danger" icon="el-icon-delete" circle @click="handleDelete(scope.row.name)"></el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-row>
              
              
            </el-row>
          </div>
        </div>
      </div>
    </el-row>


    <!-- 选择参数的弹框 -->
    <el-dialog title="选择参数" width="650px" top="10vh"
      :visible.sync="selectionDialogVisible" >
      <el-transfer
        :titles="['source', 'target']"
        v-model="selectedIDs"
        :data="paramsList"
        :props="{key:'key',label:'name'}">
      </el-transfer>

      <div slot="footer" class="dialog-footer">
        <el-button @click="selectionDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmParams">Confirm</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name:"ParamStateSR",
  props: ['state'],
  methods:{
    inEventList(state) {
      return state.event.filter(value => {
        return value.eventType === "response";
      });
    },
    outEventList(state) {
      return state.event.filter(value => {
        return value.eventType === "noresponse";
      });
    },

    // 选择参数
    confirmParams(){
      this.selectionDialogVisible = false

      // 更新已选参数
      var params = []
      this.selectedIDs.forEach(key => {
        var param = this.paramsList[key]
        // 保留先前的修改
        this.state.selectedParams.forEach(p=>{
          if(p.name == param.name){
            param.table = p.table
          }
        })
        params.push(param)
      })
      this.selectedParams = params

      this.$emit('updateParamState', this.state, params, this.selectedIDs)
    },
    // 删除参数
    handleDelete(name){
      console.log(name)
      
      // 删除弹出框的变量ID
      for (let i = 0; i < this.selectedIDs.length; i++) {
        var id = this.selectedIDs[i]
        var param = this.paramsList[id]
        if(param.name == name){
          this.selectedIDs.splice(i,1)
          break
        }
      }
      // 删除参数event的变量selected
      for (let i = 0; i < this.selectedParams.length; i++) {
        var param = this.selectedParams[i]
        if(param.name == name){
          this.selectedParams.splice(i,1)
          break
        }
      }
      
      this.$emit('updateParamState', this.state, this.selectedParams, this.selectedIDs)
    },
    // 从另一个子组件 经过 父组件 更新自己
    updateFromAnother(params, selectedIDs){
      this.selectedParams = params
      this.selectedIDs = selectedIDs
    }
  },
  data(){
    return{
      selectionDialogVisible:false,

      paramsList:[],
      selectedIDs:[],
      selectedParams:[],

      options:[
        {
          value:"Replace",
          label:"Replace"
        },{
          value:"Add",
          label:"Add"
        },{
          value:"Multiply",
          label:"Multiply"
        }
      ]
    }
  },
  mounted(){
    for (let i = 0; i < this.state.event.length; i++) {
      var event = this.state.event[i];
      var p = {
        key: i,
        name: event.eventName,
        desc: event.eventDesc,
        table: event.table
      }
      this.paramsList.push(p)
    }
    
  }

}
</script>

<style scoped>
  .state-container{
    border-top: solid 1px #ebeef5;
    padding: 2rem 0;
  }
  .leftContainer{
    min-width: 215px;
    width: 23%;
    padding-right: 3%;
  }
  .modelState{
    width: 100%;
    min-width: 210px;
    border: 1px solid #cdf2bb;
    background-color:#f0f9eb;
    border-radius: 4px;
    word-wrap: break-word;
    padding-left: 5px;
    height: auto;
  }
  .state-name{
    font-size: 17px;
  }
  .state-desc{
    /* font-style: italic; */
  }
  .dataContainer{
    width:72%;
  }
  ._params-group {
    position: relative;
    padding-bottom: 1rem;
  }
  ._params-group > ._title {
    font-style: italic;
    font-size: 16px;
    padding-bottom: 10px;
    border-bottom: solid 2px #999;
  }
  /* ._params-group > ._items {
    padding: 10px 0px 6px 50px;
  } */
  ._params-group > ._items > ._item {
    padding: 7px 0;
    border-bottom: dotted 1px #999999;
  }
  .event-name{
    display: inline-block;
    font-size: 17px;
    white-space: nowrap;
    line-height: 32px;
  }
  .event-desc{
    /* font-style: italic; */
    padding-left: 10px;
    margin: 10px 0;
    font-family: Helvetica;
  }
  ._btn-group {
    margin: 2px 10px;
  }
  .addParamBtn{
    float: right;
    margin: 16px 10px 0;
  }
</style>