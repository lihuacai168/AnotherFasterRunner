<template>
  <div id="app">
    <keep-alive>
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
html,
body {
  height: 100%;
  width: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
  background: #fff;
}

body {
  color: #333;
  font-family: "PingFang SC", "Helvetica Neue", Helvetica, "Hiragino Sans GB", STHeitiSC-Light, "Microsoft YaHei",
    "微软雅黑", Arial, sans-serif;
}
/* 去除table的每一条数据的下边框  */
.el-table td {
  border-bottom: none;
}
/* 去除表格的最下面一行的边框 */
.tableStyle::before {
  width: 0;
}
/* 设置表的外边框 */
.el-table {
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
