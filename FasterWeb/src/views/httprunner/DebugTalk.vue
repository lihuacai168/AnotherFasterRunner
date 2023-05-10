<template>
  <div>
    <div class="nav-api-header" style="padding: 10px 0 0 10px">
      <el-button type="success" size="small" icon="el-icon-circle-check" @click="handleConfirm">点击保存</el-button>
      <el-button icon="el-icon-caret-right" type="info" size="small" style="margin-left: 5px" @click="handleRunCode">
        在线运行
      </el-button>
      <!-- <el-button type="text" size="small" @click="isBaseMonacoShow = true">打开Monaco</el-button> -->
      <el-button type="text" size="small" @click="isCodemirror = true">打开Codemirror</el-button>
    </div>
    <div>
      <BaseMonacoEditor
        ref="editor"
        :height="codeHeight"
        language="python"
        :code="code.code"
        :value="code.code"
        :options="options"
        @mounted="onMounted"
        @codeChange="onCodeChange"
        @save="handleConfirm"
        :key="timeStamp"
      >
      </BaseMonacoEditor>

      <el-drawer
        size="50%"
        style="margin-top: 85px"
        :height="codeHeight"
        :destroy-on-close="true"
        :with-header="false"
        :modal="false"
        :visible.sync="isShowDebug"
      >
        <RunCodeResult :msg="resp.msg"></RunCodeResult>
      </el-drawer>
      <el-drawer
        size="50%"
        style="margin-top: 85px"
        :height="codeHeight"
        :destroy-on-close="true"
        :with-header="false"
        :modal="false"
        :visible.sync="isCodemirror"
        ><CodeEditor :code="code.code"></CodeEditor>
      </el-drawer>
      <!-- <el-dialog :visible.sync="isBaseMonacoShow" width="70%">
        <MonacoEditor
          ref="editor"
          :height="codeHeight"
          language="python"
          :code="code.code"
          :value="code.code"
          :options="options"
          @mounted="onMounted"
          @codeChange="onCodeChange"
          :key="timeStamp"
        >
        </MonacoEditor>
      </el-dialog> -->
    </div>
  </div>
</template>

<script>
import MonacoEditor from "../monaco-editor/MonacoEditor.vue";
import RunCodeResult from "./components/RunCodeResult.vue";
import BaseMonacoEditor from "../monaco-editor/BaseMonacoEditor.vue";
import CodeEditor from "../components/CodeMirrorEditor.vue";

export default {
  components: {
    // MonacoEditor,
    RunCodeResult,
    BaseMonacoEditor,
    CodeEditor,
  },
  data() {
    return {
      timeStamp: "",
      isShowDebug: false,
      isCodemirror: false,
      // isBaseMonacoShow: false,
      options: {
        selectOnLineNumbers: false,
      },
      code: {
        code: "",
        id: "",
      },
      resp: {
        msg: "",
      },
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
      this.$api.updateDebugtalk(this.code).then(() => {
        this.getDebugTalk();
        this.$message.success("代码保存成功");
      });
    },
    getDebugTalk() {
      this.$api.getDebugtalk(this.$route.params.id).then((res) => {
        this.code = res;
      });
    },
  },
  watch: {
    code() {
      this.timeStamp = new Date().getTime();
    },
    resp() {
      this.isShowDebug = true;
    },
  },

  computed: {
    codeHeight() {
      return window.innerHeight - 110;
    },
  },

  mounted() {
    this.getDebugTalk();
  },
};
</script>

<style scoped></style>
