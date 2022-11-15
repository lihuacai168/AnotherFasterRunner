<!--
@author Zou Tiancong
@version 创建时间：2021年4月8日 下午4:53:36
@return
————————————————
版权声明：本文为CSDN博主「邹田聪」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_37346639/article/details/115556605
 -->

<template>
  <div>
    <el-table
      size="medium"
      :data="tableData"
      :stripe="true"
      :border="false"
      :fit="true"
      :show-header="true"
      :highlight-current-row="true"
      v-loading="columObj.loading"
      :row-class-name="tableRowClassName"
      @row-click="rowClick"
    >
      <!-- 选择框是否开启，selectable控制是否单行禁用 -->
      <el-table-column
        v-if="columObj.selection"
        type="selection"
        :selectable="columObj.selectable"
        width="50px"
      />
      <!-- 普通列 -->
      <el-table-column
        v-for="(column, columIndex) in columObj.columnData"
        :key="columIndex"
        :prop="column.prop"
        :label="column.label"
        :min-width="column.width"
        :fixed="column.fixed"
        :align="column.align || 'center'"
        :sortable="column.sortable"
        :index="columIndex"
        show-overflow-tooltip
      >
        <template v-slot="{ row, $index }">
          <!-- 默认展示 -->
          <span v-if="column.text && column.editRow !== $index">{{
            row[column.prop]
          }}</span>
          <!-- 状态对象展示 -->
          <span v-if="column.status && row[column.prop]">{{
            row[column.prop].msg
          }}</span>
          <!-- 自定义内容 -->
          <span v-if="column.ownDefined">{{
            column.ownDefinedReturn(row, $index)
          }}</span>
          <!-- switch开关 -->
          <el-switch
            v-if="column.switch"
            v-model="row[column.prop]"
            :inactive-text="
              row[column.prop] ? column.openText : column.closeText
            "
            @change="switchChange(row, $index, column.prop)"
          />
          <!-- 图片展示 -->
          <el-popover trigger="hover" placement="top" popper-class="popper">
            <img v-if="column.image" :src="viewUrl + row[column.prop]" />
            <el-image
              slot="reference"
              v-if="column.image"
              :src="viewUrl + row[column.prop]"
            />
          </el-popover>

          <!-- 图片数组 -->
          <el-popover
            v-if="column.imageArr"
            trigger="hover"
            placement="top"
            popper-class="popper"
          >
            <img
              v-if="row[column.prop].length > 0"
              :src="row[column.prop][0]"
            />
            <el-image
              slot="reference"
              v-if="row[column.prop].length > 0"
              :src="row[column.prop][0]"
              :preview-src-list="row[column.prop]"
            />
          </el-popover>

          <!-- 可编辑input，仅在text默认展示类型才可编辑-->
          <el-input
            v-focus
            v-if="column.editRow === $index"
            v-model="row[column.prop]"
            @blur="editInputBlur(row, $index, column.prop, columIndex)"
          />
          <!-- 操作按钮 -->
          <span
            v-if="column.isOperation"
            v-for="(operations, index) in column.operation"
            :key="index"
          >
            <el-button
              v-if="operations.isShow(row, $index)"
              :icon="operations.icon"
              :type="operations.type"
              @click="operations.buttonClick(row, $index)"
              :style="{ color: operations.color, marginLeft: 0 }"
              :circle="operations.circle"
              size="mini"
            >
              {{ operations.label }}
            </el-button>
          </span>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <div class="page_div" :style="{ textAlign: pageObj.position || 'center' }">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :hide-on-single-page="false"
        :current-page="pageObj.pageData.page"
        :pager-count="7"
        :page-sizes="[10, 15, 20, 30, 50]"
        :page-size="pageObj.pageData.size"
        background
        layout="total, prev, pager, next, jumper, sizes"
        :total="pageObj.total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  name: "PublicTable",
  directives: {
    // 自定义指令,用于可编辑input自动获取焦点
    focus: {
      inserted: function (e) {
        e.querySelector("input").focus();
      },
    },
  },
  props: {
    tableData: {
      type: Array,
      required: true,
    },
    columObj: {
      type: Object,
      required: true,
    },
    //columObj.type(如果为""空，就不会加载多选框，或者index编号),lazy(是否支持懒加载)
    //columnData.columType(列类型,可选text(默认为普通文字模式),input(input可编辑框),switch(switch开关),image(图片),operation(操作按钮))
    //prop(参数),label(列名),width(宽度),align(对齐方式),sortable(是否支持排序)
    //如果为操作列,则需要填写需要的操作按钮,类型为Object。type(按钮样式,参考el—botton类型),label(按钮文字)icon(参考el-icon),color(字体颜色),buttonClick为点击后调用的方法名称
    pageObj: {
      type: Object,
      required: true,
    },
  },
  data() {
    let readUploadFileUrl = this.$store.state.user.readUploadFileUrl;
    return {
      viewUrl: readUploadFileUrl,
    };
  },
  methods: {
    // switchChange调用
    switchChange(row, $index, prop) {
      this.$emit("switchChange", row, $index, prop);
    },
    // 帮助点击行，获取点击的下标
    tableRowClassName({ row, rowIndex }) {
      row.rowIndex = rowIndex;
    },
    // 点击行
    rowClick(row, column, event) {
      this.$emit("rowClick", row, column, event);
    },
    // 可编辑input失去焦点
    editInputBlur(row, $index, prop, columIndex) {
      this.$emit("editInputBlur", row, $index, prop, columIndex);
    },
    // 条数变化
    handleSizeChange(e) {
      this.$emit("handleSizeChange", e);
    },
    // 页码变化
    handleCurrentChange(e) {
      this.$emit("handleCurrentChange", e);
    },
  },
};
</script>
<style lang="scss" scoped>
.el-button {
  margin: 0 6px;
}

::v-deep .el-input__inner {
  border: none;
}

::v-deep .el-image__inner {
  height: 50px;
}

// switch左边文字颜色
::v-deep .el-switch__label--left {
  color: #606266;
}

img {
  height: 400px;
}

.page_div {
  padding: 15px 0;
}
</style>
