<template>
  <div class="layout">
    <main>
      <router-view></router-view> <!-- 子路由在这里渲染 -->
    </main>
  </div>
</template>

<script>
export default {
  name: 'CommonLayout',
  // ...
};
</script>
