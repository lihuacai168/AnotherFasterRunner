<template>
    <el-container><el-header style="padding: 0;">
        <div>
            <el-menu
                :default-active="$store.state.routerName"
                mode="horizontal"
                background-color="#01101a"
                text-color="#BFCBD9"
                active-text-color="#1dbe89"
                @select="select"
            >
                <el-menu-item>
                    <img src="\static\FasterRunner\favicon.ico" alt="ico" height="35px"/>
                    <span v-text=" platformTitle + this.$store.state.projectName" style="color: white; font-size: 16px; margin-left: 10px"></span>
                </el-menu-item>
                <el-menu-item index="ProjectList" class="menu-items">
                    <i class="iconfont">&#xe631;</i>&nbsp;首 页
                </el-menu-item>
                <el-menu-item
                    v-for="item of side_menu"
                    :index="item.url"
                    :key="item.url"
                    :disabled="$store.state.routerName === 'ProjectList'"
                ><span class="iconfont" v-html="item.code"></span>&nbsp;{{ item.name }}
                </el-menu-item>
                <el-button
                    type="text"
                    size="big"
                    icon="el-icon-user"
                    style="position: absolute; right: 60px;font-size: 16px; color: white; margin-top: 5px;"
                    @click="addTasks = false"
                    >{{ this.$store.state.user }}
                </el-button>
                <el-button
                    style="margin-left: 20px; position: absolute; right: 10px; margin-top: 10px;"
                    type="danger"
                    icon="el-icon-close"
                    title="注销"
                    size="small"
                    circle
                    @click="handleLogOut"
                >
                </el-button>
            </el-menu>
        </div>
    </el-header></el-container>
</template>

<script>
export default {
    data() {
        return {
            platformTitle: this.$store.state.FasterRunner + " API TEST",
            side_menu: [
                { name: "项目概况", url: "ProjectDetail", code: "&#xe64a;" },
                { name: "API 模板", url: "RecordApi", code: "&#xe74a;" },
                { name: "测试用例", url: "AutoTest", code: "&#xe6da;" },
                { name: "配置管理", url: "RecordConfig", code: "&#xee32;" },
                { name: "全局变量", url: "GlobalEnv", code: "&#xe692;" },
                { name: "驱动代码", url: "DebugTalk", code: "&#xe7ca;" },
                { name: "定时任务", url: "Task", code: "&#xe61e;" },
                { name: "历史报告", url: "Reports", code: "&#xe66e;" }
            ]
        };
    },
    methods: {
        handleLogOut() {
            this.$store.commit("isLogin", null);
            this.setLocalValue("token", null);
            this.setLocalValue("is_superuser", false);
            this.setLocalValue("show_hosts", false);
            this.$router.push({ name: "Login" });
        },
        select(url) {
            this.$store.commit("setRouterName", url);
            this.$router.push({ name: url });
            this.setLocalValue("routerName", url);
            let projectName = "";
            if (url !== "ProjectList") {
                projectName = this.$store.state.projectName;
            }
            this.$store.commit("setProjectName", projectName);
        }
    },
    mounted() {
        if (this.$store.state.show_hosts) {
            this.side_menu.splice(5, 0, {
                name: "Hosts管理",
                url: "HostIP",
                code: "&#xe609;"
            });
        }
    },
    name: "Header"
};
</script>

<style scoped>
.left {
    width: 180px;
    left: 20px;
    display: inline-block;
    position: fixed;
    z-index: 900;
    top: -5px;
}

.right {
    position: fixed;
    left: 300px;
    right: 0;
    top: 0;
    padding: 0 0 5px 5px;
}

.right div a:hover {
    color: darkcyan;
}

.logo {
    background: white;
    height: 40px;
}
.el-menu-item {
    padding: 0 8px;
    height: 52px;
    line-height: 52px;
}
.nav-header {
    background: #01101a;
    margin: 0 auto;
    font-size: 14px;
    width: 100%;
    border-bottom: 1px solid #ddd;
    height: 52px;
    line-height: 52px;
}
</style>
