import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import ViteApp from "../views/ViteApp.vue";
const Home = () => import("../views/home/Home.vue");
const Register = () => import("../views/auth/Register.vue");
const Login = () => import("../views/auth/Login.vue");
const ProjectList = () => import("../views/project/ProjectList.vue");
const ProjectDetail = () => import("../views/project/ProjectDetail.vue");
const DebugTalk = () => import("../views/httprunner/DebugTalk.vue");
const RecordApi = () => import("../views/fastrunner/api/RecordApi.vue");
const AutoTest = () => import("../views/fastrunner/case/AutoTest.vue");
const GlobalEnv = () => import("../views/variables/GlobalEnv.vue");
const ReportList = () => import("../views/reports/ReportList.vue");
const RecordConfig = () => import("../views/fastrunner/config/RecordConfig.vue");
const Tasks = () => import("../views/task/Tasks.vue");
const HostAddress = () => import("../views/variables/HostAddress.vue");
const ExecPublic = () => import("../views/components/ExecPublic.vue");

Vue.use(VueRouter);

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};

const router = new VueRouter({
  mode: "history",
  base: import.meta.env.BASE_URL,
  routes: [
    {
      path: "/vite_app",
      name: "ViteApp",
      component: ViteApp,
    },
    {
      path: "/vite_home",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/fastrunner/execpub",
      name: "ExecPublic",
      component: ExecPublic,
      meta: {
        title: "表格封装测试",
      },
    },
    {
      path: "/fastrunner/register",
      name: "Register",
      component: Register,
      meta: {
        title: "用户注册",
      },
    },
    {
      path: "/fastrunner/login",
      name: "Login",
      component: Login,
      meta: {
        title: "用户登录",
      },
    },
    {
      path: "/",
      redirect: "/fastrunner/project_list",
      meta: {
        title: "首页",
        requireAuth: true,
      },
    },
    {
      path: "/fastrunner",
      name: "Index",
      component: Home,
      redirect: "/fastrunner/project_list",
      meta: {
        title: "首页",
        requireAuth: true,
      },
      children: [
        {
          name: "ProjectList",
          path: "project_list",
          component: ProjectList,
          meta: {
            title: "项目列表",
            requireAuth: true,
          },
        },
        {
          name: "ProjectDetail",
          path: "project/:id/dashbord",
          component: ProjectDetail,
          meta: {
            title: "项目预览",
            requireAuth: true,
          },
        },
        {
          name: "DebugTalk",
          path: "debugtalk/:id",
          component: DebugTalk,
          meta: {
            title: "编辑驱动",
            requireAuth: true,
          },
        },
        {
          name: "RecordApi",
          path: "api_record/:id",
          component: RecordApi,
          meta: {
            title: "接口模板",
            requireAuth: true,
          },
        },
        {
          name: "AutoTest",
          path: "auto_test/:id",
          component: AutoTest,
          meta: {
            title: "自动化测试",
            requireAuth: true,
          },
        },
        {
          name: "RecordConfig",
          path: "record_config/:id",
          component: RecordConfig,
          meta: {
            title: "配置管理",
            requireAuth: true,
          },
        },
        {
          name: "GlobalEnv",
          path: "global_env/:id",
          component: GlobalEnv,
          meta: {
            title: "全局变量",
            requireAuth: true,
          },
        },
        {
          name: "Reports",
          path: "reports/:id",
          component: ReportList,
          meta: {
            title: "历史报告",
            requireAuth: true,
          },
        },
        {
          name: "Task",
          path: "tasks/:id",
          component: Tasks,
          meta: {
            title: "定时任务",
            requireAuth: true,
          },
        },
        {
          name: "HostIP",
          path: "host_ip/:id",
          component: HostAddress,
          meta: {
            title: "HOST配置",
            requireAuth: true,
          },
        },
      ],
    },
  ],
});

export default router;
