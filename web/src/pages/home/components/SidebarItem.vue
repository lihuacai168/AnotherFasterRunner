<template>
    <div>
        <el-menu-item
            v-if="!item.children"
            :index="item.url"
            :disabled="isDisabled"
        >
            <i :class="item.icon"></i>&nbsp;{{ item.name }}

        </el-menu-item>
        <el-submenu
            v-else
            :index="item.url"
        >
            <template slot="title">
                    <i :class="item.icon"></i>&nbsp;{{ item.name }}
            </template>
            <sidebar-item
                v-for="child in item.children"
                :key="child.url"
                :item="child"
            />
        </el-submenu>
    </div>
</template>

<script>
export default {
    name: 'SidebarItem',
    props: ['item'],
    computed: {
        isDisabled() {
            const routerName = this.$store.state.routerName;
            // 适当调整路径逻辑以匹配你的需求
            const pathCondition = this.$route.path === '/fastrunner/project_list';
            // 根据你的全局状态或路由条件设置 disabled 状态
            return routerName === 'ProjectList' || pathCondition;
        }
    },
    components: {
        SidebarItem: () => import('./SidebarItem') // 注意递归引用自身
    }
};
</script>
