<template>
  <el-container style="height: 100%">
    <el-header style="background: #ffff00; padding: 0; height: 36px">
      <home-header></home-header>
    </el-header>
    <el-divider></el-divider>

    <!--            <el-aside style="width: 160px" v-show="false">-->
    <!--                <home-side></home-side>-->
    <!--            </el-aside>-->

    <el-main :style="defaultHeight">
      <router-view></router-view>
    </el-main>
    <el-footer
      style="
        background: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 24px;
        font: 0.5em sans-serif;
      "
    >
      Copyright © 2022 - 2023 . CBK QA . All Rights Reserved
    </el-footer>
  </el-container>
</template>

<script>
import HomeHeader from "./components/Header.vue";
// import HomeSide from "./components/Side.vue";

export default {
  name: "Home",
  components: {
    HomeHeader,
    // HomeSide
  },
  data() {
    return { defaultHeight: { height: "" } };
  },
  methods: {
    getHeight() {
      this.defaultHeight.height = window.innerHeight - 36 + "px";
    }
  },
  created() {
    window.addEventListener("resize", this.getHeight);
    this.getHeight();
  }
};
</script>

<style scoped>
.el-main {
  padding: 0px;
}
.el-divider--horizontal {
  margin: 0;
}
</style>
