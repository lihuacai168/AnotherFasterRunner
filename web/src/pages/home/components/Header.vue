<template>
    <div>
        <div class="nav-header">
            <span v-text="platformTitle + this.$store.state.projectName"
                  style="color: white; font-size: 25px; margin-left: 10px">
            </span>
            <span class="right">
                <div style="float: right; color: #d9d9d9; margin-right: 100px">
                    <a :href="githubURL" style="padding-left: 10px; color: white;" target="_blank">
                        <span style="font-size: large" >GitHub</span>
                    </a>
                    <a :href="docURL" style="padding-left: 10px; margin-right: 10px; color: white;" target="_blank">
                        <span style="font-size: large"  >项目文档</span>
                    </a>
                    <i class="iconfont">&#xe61c;</i>
                    <span v-text="this.$store.state.user" style="padding-left: 5px; font-size: large"></span>
                    <a style="padding-left: 10px; font-size: large" @click="handleLogOut">注销</a>
                </div>
            </span>
        </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      platformTitle: this.$store.state.FasterRunner + '自动化测试平台'
    }
  },
  computed: {
    githubURL() {
      return 'https://github.com/lihuacai168/AnotherFasterRunner'
    },
    docURL() {
      return 'https://www.yuque.com/lihuacai/fasterunner/cn5ncg'
    }
  },
  methods: {
    handleLogOut() {
      this.$store.commit('isLogin', null)
      this.setLocalValue('token', null)
      this.setLocalValue('is_superuser', false)
      this.setLocalValue('show_hosts', false)
      this.$router.push({name: 'Login'})
    }
  },
  name: 'Header'
}
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
    background: #242f42;
    margin: 0 auto;
    font-size: 14px;
    width: 100%;
    border-bottom: 1px solid #ddd;
    height: 49px;
    line-height: 49px;
}
</style>
