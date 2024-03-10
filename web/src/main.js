// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import VueClipboard from 'vue-clipboard2'
// import echarts from 'echarts'
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
// Vue.prototype.$echarts = echarts
Vue.use(VueClipboard)
Vue.use(VueApexCharts)

Vue.component('ApexCharts', VueApexCharts)

Vue.filter('datetimeFormat', datetimeObj2str)

Vue.filter('timestampToTime', timestamp2time)

Vue.prototype.setLocalValue = function (name, value) {
    if (window.localStorage) {
        localStorage.setItem(name, value)
    } else {
        alert('This browser does NOT support localStorage')
    }
}
Vue.prototype.getLocalValue = function (name) {
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


// register component and loading directive
import ElDataTable from '@femessage/el-data-table'
import ElFormRenderer from '@femessage/el-form-renderer'
import {
    Button,
    Dialog,
    Form,
    FormItem,
    Loading,
    Pagination,
    Table,
    TableColumn,
    Message,
    MessageBox
} from 'element-ui'

Vue.use(Button)
Vue.use(Dialog)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Loading.directive)
Vue.use(Pagination)
Vue.use(Table)
Vue.use(TableColumn)
Vue.component('el-form-renderer', ElFormRenderer)
Vue.component('el-data-table', ElDataTable)
// to show confirm before delete
Vue.prototype.$confirm = MessageBox.confirm
// show tips
Vue.prototype.$message = Message
// if the table component cannot access `this.$axios`, it cannot send request
import axios from 'axios'
// 创建axios实例
const service = axios.create({
    // 可以在这里设置基础URL和其他配置
});

// 请求拦截器
service.interceptors.request.use(
    config => {
        config.headers.Authorization = store.state.token;
        // 确保URL以斜杠结尾
        if (!config.url.endsWith('/')) {
            config.url += '/';
        }
        // 返回修改后的请求配置
        return config;
    },
    error => {
        // 请求错误处理
        return Promise.reject(error);
    }
);
Vue.prototype.$axios = service

router.beforeEach((to, from, next) => {
    /* 路由发生变化修改页面title */
    setTimeout((res) => {
        if (to.meta.title) {
            document.title = to.meta.title
        }

        if (to.meta.requireAuth) {
            if (store.state.token !== '') {
                if (to.name === 'HomeRedirect' || to.name === 'Login') {
                    next({name: 'ProjectList'});
                } else {
                    next();
                }
            } else {
                next({
                    name: 'Login'
                });
            }
        } else {
            // 如果已经登录了，重新登录时，跳转到项目首页
            if (store.state.token !== '' && store.state.token !== null && store.state.token !== 'null' && to.name === 'Login') {
                next({name: 'ProjectList'});
            } else {
                next();
            }
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
