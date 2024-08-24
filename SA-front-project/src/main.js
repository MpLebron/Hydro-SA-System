// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// 引入element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)
// 引入echart
import Echarts from "echarts";
Vue.prototype.$echarts = Echarts;
// 引入axios
import axios from 'axios'
Vue.prototype.$axios = axios


// 引入qs，往后台传数据进行参数转换
import qs from 'qs'
Vue.prototype.qs = qs

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
