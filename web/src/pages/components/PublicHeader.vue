<template>
  <div>
    <el-aside width="200px">
      <el-menu
        default-active="1"
        background-color="#545c64"
        text-color="#fff"
        :unique-opened="true"
        active-text-color="#ffd04b"
      >
        <div v-for="(item, index) in list2" :key="index">
          <el-submenu v-if="item.children && item.children.length" :index="item.path" :key="item.path">
            <template slot="title"
              ><img :src="item.icon" alt="" /><span>{{ item.name }}</span></template
            >
            <template v-for="itemChild in item.children">
              <el-menu-item
                :index="itemChild.path"
                :key="itemChild.path"
                @click="changeurl(itemChild.path, itemChild.name)"
              >
                <img :src="childrenIndex == itemChild.name ? itemChild.active : itemChild.icon" alt="" />
                <span slot="title">{{ itemChild.name }}</span>
              </el-menu-item>
            </template>
          </el-submenu>
          <el-menu-item v-else :index="item.path" :key="item.name" @click="changeurl2(item.path, item.name)">
            <img :src="childrenIndex == item.name ? item.active : item.icon" alt="" />
            <span slot="title">{{ item.name }}</span>
          </el-menu-item>
        </div>
      </el-menu>
    </el-aside>
  </div>
</template>
<script>
export default {
  data() {
    return {
      childrenIndex: "",
      list2: [
        {
          path: "/4",
          name: "导航一",
          // icon:'el-icon-menu'
          icon: import("../assets/image/menu6_4.png"),
          active: import("../assets/image/menu6_4_c.png")
        },
        {
          path: "/5",
          name: "导航二",
          // icon:'el-icon-menu'
          icon: import("../assets/image/menu6_c.png"),
          children: [
            {
              path: "/54",
              name: "导航2-1-1",
              icon: import("../assets/image/menu13_c.png"),
              active: import("../assets/image/menu13.png")
            },
            {
              path: "/55",
              name: "导航3-1-2",
              icon: import("../assets/image/menu12_c.png"),
              active: import("../assets/image/menu12.png")
            }
          ]
        },
        {
          path: "/6",
          name: "导航三",
          // icon: "el-icon-menu",
          icon: import("../assets/image/menu6_c.png"),
          children: [
            {
              path: "/57",
              name: "导航4-1-1",
              icon: import("../assets/image/icon/1.png"),
              active: import("../assets/image/icon/2.png")
            },
            {
              path: "/58",
              name: "导航4-1-2",
              icon: import("../assets/image/icon/3.png"),
              active: import("../assets/image/icon/4.png")
            }
          ]
        },
        {
          path: "/47",
          name: "导航四",
          // icon:'el-icon-menu'
          icon: import("../assets/image/icon/5.png"),
          active: import("../assets/image/icon/6.png")
        }
      ]
    };
  },
  methods: {
    changeurl(a, b) {
      this.childrenIndex = b;
      console.log(a);
      console.log(b);
      console.log(this.childrenIndex);
    },
    changeurl2(c, d) {
      console.log(c);
      console.log(d);
      this.childrenIndex = d;
    }
  }
};
</script>
<style scoped>
.el-submenu__title {
  background: url(../assets/image/left_menu.png) no-repeat !important;
}

.el-menu-item.is-active {
  background: url(../assets/image/left_menu_c.png) no-repeat;
}

.el-menu-item {
  height: 58px;
  line-height: 39px;
  align: center;
  color: #fff;
  margin-top: 10px;
  background: url(../assets/image/left_menu.png) no-repeat;
}

.el-submenu .el-menu-item.is-active {
  background: url(../assets/image/mb2.png) no-repeat;
}

.el-submenu .el-menu-item {
  width: 180px;
  height: 33px;
  line-height: 33px;
  background: url(../assets/image/children-bg.png) no-repeat;
}
</style>
