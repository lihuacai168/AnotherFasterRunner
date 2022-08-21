import Vue from "vue";
import Router from "vue-router";
import Home from "@/pages/home/Home";
import Register from "@/pages/auth/Register";
import Login from "@/pages/auth/Login";
import ProjectList from "@/pages/project/ProjectList";
import ProjectDetail from "@/pages/project/ProjectDetail";
import DebugTalk from "@/pages/httprunner/DebugTalk";
import RecordApi from "@/pages/fastrunner/api/RecordApi";
import AutoTest from "@/pages/fastrunner/case/AutoTest";
import GlobalEnv from "@/pages/variables/GlobalEnv";
import ReportList from "@/pages/reports/ReportList";
import RecordConfig from "@/pages/fastrunner/config/RecordConfig";
import Tasks from "@/pages/task/Tasks";
import HostAddress from "@/pages/variables/HostAddress";

Vue.use(Router);

export default new Router({
    mode: "history",
    routes: [
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
            name: "Index",
            component: Home,
            meta: {
                title: "首页",
                requireAuth: true,
            },
        },
        {
            path: "/fastrunner",
            name: "Index",
            component: Home,
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
