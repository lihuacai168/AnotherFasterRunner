<template>
    <el-menu
        class="common-side-bar"
        :default-active="$store.state.routerName"
        background-color="#304056"
        text-color="#BFCBD9"
        active-text-color="#318DF1"
        @select="select"
    >
        <sidebar-item
            v-for="item in side_menu"
            :key="item.url"
            :item="item"
        />
    </el-menu>
</template>

<script>
import SidebarItem from "@/pages/home/components/SidebarItem.vue";

export default {
    name: "Side",
    components: {SidebarItem},
    data() {
        return {
            side_menu: [
                {name: "首页", url: "ProjectList", icon: 'el-icon-s-home'},
                {name: "项目概况", url: "ProjectDetail", icon: 'el-icon-s-cooperation'},
                {name: "API 模板", url: "RecordApi", icon: 'el-icon-s-claim'},
                {name: "测试用例", url: "AutoTest", icon: 'el-icon-s-operation'},
                {name: "配置管理", url: "RecordConfig", icon: 'el-icon-s-tools'},
                {name: "全局变量", url: "GlobalEnv", icon: 'el-icon-s-custom'},
                {name: "自定义函数", url: "DebugTalk", icon: 'el-icon-s-platform'},
                {name: "定时任务", url: "Task", icon: 'el-icon-timer'},
                {name: "历史报告", url: "Reports", icon: 'el-icon-s-data'},
                {
                    name: "Mock",
                    url: "MockServer",
                    icon: 'el-icon-s-help',
                    children: [ // 子菜单项
                        {name: "Mock 项目", url: "MockProject", icon: 'el-icon-folder-opened'},
                        {name: "Mock APIs", url: "MockAPIs", icon: 'el-icon-document-copy'},
                        {name: "Mock Log", url: "MockLog", icon: 'el-icon-data-board'}
                    ]
                }
            ]
        }
    },
    methods: {
        select(url) {
            this.$store.commit('setRouterName', url);
            this.$router.push({name: url});
            this.setLocalValue("routerName", url);
            let projectName = ''
            if (url !== 'ProjectList') {
                projectName = this.$store.state.projectName
            }
            this.$store.commit('setProjectName', projectName);
        }
    },
    mounted() {
        if (this.$store.state.show_hosts) {
            this.side_menu.splice(5, 0, {name: "Hosts管理", url: "HostIP", code: "&#xe609;"})
        }
    }
}
</script>

<style scoped>

.common-side-bar {
    position: fixed;
    top: 48px;
    border-right: 1px solid #ddd;
    height: 100%;
    width: 202px;
    background-color: #fff;
    display: inline-block;
}
</style>
