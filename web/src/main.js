// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import VueClipboard from 'vue-clipboard2'
import echarts from 'echarts'
import VueApexCharts from 'vue-apexcharts'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import 'styles/iconfont.css'
import 'styles/swagger.css'
import 'styles/tree.css'
import 'styles/home.css'
import 'styles/reports.css'
import * as api from './restful/api'
import store from './store'
import {datetimeObj2str, timestamp2time} from './util/format.js'
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.prototype.$api = api
Vue.prototype.$echarts = echarts
Vue.use(VueClipboard)
Vue.use(VueApexCharts)

import Editor from 'vue2-ace-editor'
Vue.component('ace-editor', Editor)
Vue.component('ApexCharts', VueApexCharts)

Vue.filter('datetimeFormat', datetimeObj2str)

Vue.filter('timestampToTime', timestamp2time)

Vue.prototype.setLocalValue = function(name, value) {
  if (window.localStorage) {
    localStorage.setItem(name, value)
  } else {
    alert('This browser does NOT support localStorage')
  }
}
Vue.prototype.getLocalValue = function(name) {
  const value = localStorage.getItem(name)
  if (value) {
    // localStorage只能存字符串，布尔类型需要转换
    if (value === 'false' || value === 'true') {
      return eval(value)
    }
    return value
  } else {
    return ''
  }
}

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  setTimeout((res) => {
    if (to.meta.title) {
      document.title = to.meta.title
    }

    if (to.meta.requireAuth) {
      if (store.state.token !== '') {
        next()
      } else {
        next({
          name: 'Login'
        })
      }
    } else {
      next()
    }
  })
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>',
  created() {
    if (this.getLocalValue('token') === null) {
      this.setLocalValue('token', '')
    }
    if (this.getLocalValue('user') === null) {
      this.setLocalValue('user', '')
    }
    if (this.getLocalValue('routerName') === null) {
      this.setLocalValue('routerName', 'ProjectList')
    }

    if (this.getLocalValue('is_superuser') === null) {
      this.setLocalValue('is_superuser', false)
    }
    if (this.getLocalValue('show_hosts') === null) {
      this.setLocalValue('show_hosts', false)
    }
    this.$store.commit('isLogin', this.getLocalValue('token'))
    this.$store.commit('setUser', this.getLocalValue('user'))
    this.$store.commit('setRouterName', this.getLocalValue('routerName'))
    this.$store.commit('setIsSuperuser', this.getLocalValue('is_superuser'))
    this.$store.commit('setShowHots', this.getLocalValue('show_hosts'))
  }
})
