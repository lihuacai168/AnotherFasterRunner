<template>
  <div>
    <div style="height: 48px; padding: 5px 10px; background: #f7f7f7">
      <el-button type="primary" size="small" icon="el-icon-circle-check" @click="handleConfirm"> 点击保存 </el-button>
      <el-button icon="el-icon-caret-right" type="info" size="small" style="margin-left: 0" @click="handleRunCode">
        在线运行
      </el-button>
      <el-button type="text" @click="table = true">嵌套表格的演示Drawer</el-button>
      <el-drawer title="示例表格代码!" :visible.sync="table" direction="rtl" size="50%">
        <el-table :data="gridData">
          <el-table-column property="date" label="日期" width="150"></el-table-column>
          <el-table-column property="name" label="姓名" width="200"></el-table-column>
          <el-table-column property="address" label="地址"></el-table-column>
        </el-table>
      </el-drawer>
    </div>
    <div>
      <MonacoEditor
        ref="editor"
        :height="codeHeight"
        language="python"
        :code="code.code"
        :options="options"
        @mounted="onMounted"
        @codeChange="onCodeChange"
        :key="timeStamp"
      >
      </MonacoEditor>

      <el-drawer
        style="margin-top: 86px"
        :height="codeHeight"
        :destroy-on-close="true"
        :with-header="false"
        :modal="false"
        :visible.sync="isShowDebug"
      >
        <RunCodeResult :msg="resp.msg"></RunCodeResult>
      </el-drawer>
    </div>
  </div>
</template>

<script>
import MonacoEditor from "../monaco-editor/MonacoEditor.vue";
import RunCodeResult from "./components/RunCodeResult.vue";
import BaseMonacoEditor from "../monaco-editor/BaseMonacoEditor";

export default {
  components: {
    MonacoEditor,
    RunCodeResult
    // BaseMonacoEditor
  },
  data() {
    return {
      timeStamp: "",
      isShowDebug: false,
      options: { selectOnLineNumbers: false },
      code: { code: "", id: "" },
      resp: { msg: "" },
      table: false,
      gridData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄"
        }
      ]
    };
  },
  name: "DebugTalk",
  methods: {
    onMounted(editor) {
      this.editor = editor;
    },
    onCodeChange(editor) {
      this.code.code = editor.getValue();
      // editor.trigger('随便写点儿啥', 'editor.action.triggerSuggest', {});
    },
    handleRunCode() {
      this.resp.msg = "";
      this.$api.runDebugtalk(this.code).then((resp) => {
        this.resp = resp;
      });
    },
    handleConfirm() {
      this.$api.updateDebugtalk(this.code).then((resp) => {
        this.getDebugTalk();
        this.$message.success("代码保存成功");
      });
    },
    getDebugTalk() {
      this.$api.getDebugtalk(this.$route.params.id).then((res) => {
        this.code = res;
      });
    }
  },
  watch: {
    code() {
      this.timeStamp = new Date().getTime();
    },
    resp() {
      this.isShowDebug = true;
    }
  },

  computed: {
    codeHeight() {
      return window.innerHeight - 100;
    }
  },

  mounted() {
    this.getDebugTalk();
  }
};
</script>

<style scoped></style>
