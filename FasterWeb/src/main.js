import Vue from "vue";
import { createPinia, PiniaVuePlugin } from "pinia";
import ElementUI from "element-ui";
import VJsoneditor from "v-jsoneditor";
import VueClipboard from "vue-clipboard2";
import echarts from "echarts";
import VueApexCharts from "vue-apexcharts";
import "element-ui/lib/theme-chalk/index.css";
import "./assets/theme/index.css";
import "./assets/styles/iconfont.css";
import "./assets/styles/swagger.css";
import "./assets/styles/tree.css";
import "./assets/styles/home.css";
import "./assets/styles/reports.css";
import * as api from "./restful/api";
import store from "./stores";
import { datetimeObj2str, timestamp2time } from "./util/format.js";

import App from "./App.vue";
import router from "./router";

// import "./assets/main.css";

Vue.use(PiniaVuePlugin);
Vue.use(ElementUI);
Vue.use(VJsoneditor);
Vue.use(VueClipboard);
Vue.use(VueApexCharts);
Vue.config.productionTip = false;
Vue.prototype.$api = api;
Vue.prototype.$echarts = echarts;
Vue.prototype.setLocalValue = function (name, value) {
  if (window.localStorage) {
    localStorage.setItem(name, value);
  } else {
    alert("This browser does NOT support localStorage");
  }
};
Vue.prototype.getLocalValue = function (name) {
  const value = localStorage.getItem(name);
  if (value) {
    // localStorage只能存字符串，布尔类型需要转换
    if (value === "false" || value === "true") {
      return eval(value);
    }
    return value;
  } else {
    return "";
  }
};
Vue.prototype.getViewportSize = function () {
  return {
    width:
      window.innerWidth ||
      document.documentElement.clientWidth ||
      document.body.clientWidth,
    height:
      window.innerHeight ||
      document.documentElement.clientHeight ||
      document.body.clientHeight,
  };
};
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  setTimeout(() => {
    if (to.meta.title) {
      document.title = to.meta.title;
    }
    if (to.meta.requireAuth) {
      if (store.state.token !== "") {
        next();
      } else {
        next({ name: "Login" });
      }
    } else {
      next();
    }
  });
});

Vue.component("ApexCharts", VueApexCharts);
Vue.filter("datetimeFormat", datetimeObj2str);
Vue.filter("timestampToTime", timestamp2time);

new Vue({
  el: "#app",
  router,
  store,
  pinia: createPinia(),
  render: (h) => h(App),

  components: { App },
  template: "<App/>",
  created() {
    if (this.getLocalValue("token") === null) {
      this.setLocalValue("token", "");
    }
    if (this.getLocalValue("user") === null) {
      this.setLocalValue("user", "");
    }
    if (this.getLocalValue("routerName") === null) {
      this.setLocalValue("routerName", "ProjectList");
    }

    if (this.getLocalValue("is_superuser") === null) {
      this.setLocalValue("is_superuser", false);
    }
    if (this.getLocalValue("show_hosts") === null) {
      this.setLocalValue("show_hosts", false);
    }
    this.$store.commit("isLogin", this.getLocalValue("token"));
    this.$store.commit("setUser", this.getLocalValue("user"));
    this.$store.commit("setRouterName", this.getLocalValue("routerName"));
    this.$store.commit("setIsSuperuser", this.getLocalValue("is_superuser"));
    this.$store.commit("setShowHots", this.getLocalValue("show_hosts"));
  },
}).$mount("#app");
