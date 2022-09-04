<template>
<el-container><el-header style="padding: 0; height: 50px">
  <div class="nav-header">
    <img src="\static\FasterRunner\favicon.ico" alt="ico" height="35px" style="padding:0 0 5px 5px;">
      <span
        v-text="platformTitle + this.$store.state.projectName"
        style="color: white; font-size: 20px; margin-left: 10px"
      ></span>
      <el-button
          type="text"
          size="big"
          icon="el-icon-user"
          style="position: absolute; right: 60px;font-size: 16px; color: white; margin-top: 5px;"
          @click="addTasks=false"
      >{{this.$store.state.user}}
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
    </div>
</el-header></el-container>
</template>

<script>
export default {
  data() {
    return {
      platformTitle: this.$store.state.FasterRunner + "自动化测试平台",
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
  },
  name: "Header",
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
}

.right div a:hover {
  color: darkcyan;
}

.logo {
  background: white;
  height: 40px;
}

.nav-header {
  background: #01101a;
  margin: 0 auto;
  font-size: 14px;
  width: 100%;
  border-bottom: 1px solid #ddd;
  height: 49px;
  line-height: 49px;
}
</style>
