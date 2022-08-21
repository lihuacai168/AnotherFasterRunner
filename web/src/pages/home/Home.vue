<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <home-header></home-header>
        </el-header>

        <el-container>
            <el-aside style="width: 160px">
                <home-side></home-side>
            </el-aside>

            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>


</template>

<script>
import HomeHeader from './components/Header'
import HomeSide from './components/Side'

export default {
    name: "Home",
    components: {
        HomeHeader,
        HomeSide
    }

}
</script>

<style scoped>
.el-main {
    padding: 0px;
}

</style>
