<template>
  <div class="code-mirror-div">
    <div class="tool-bar">
      <span>请选择主题</span>

      <el-select v-model="cmTheme" placeholder="请选择" size="small" style="width: 150px">
        <el-option v-for="item in cmThemeOptions" :key="item" :label="item" :value="item"></el-option>
      </el-select>

      <span style="margin-left: 10px">请选择编辑模式</span>

      <el-select
        v-model="cmEditorMode"
        placeholder="请选择"
        size="small"
        style="width: 150px"
        @change="onEditorModeChange"
      >
        <el-option v-for="item in cmEditorModeOptions" :key="item" :label="item" :value="item"></el-option>
      </el-select>

      <el-button type="primary" size="small" style="margin-left: 10x" @click="setStyle">修改样式</el-button>

      <el-button type="primary" size="small" style="margin-left: 10x" @click="getValue">获取内容</el-button>

      <el-button type="primary" size="small" style="margin-left: 10x" @click="setValue">修改内容</el-button>
    </div>

    <code-mirror-editor
      ref="cmEditor"
      :cmTheme="cmTheme"
      :cmMode="cmMode"
      :autoFormatJson="autoFormatJson"
      :jsonIndentation="jsonIndentation"
    ></code-mirror-editor>
  </div>
</template>

<script>
// 使用时需要根据CodeMirrorEditor.vue的实际存放路径，调整from后面的组件路径，以便正确引用

import CodeMirrorEditor from "./CodeMirror.vue";

export default {
  components: {
    CodeMirrorEditor,
  },
  data() {
    return {
      cmTheme: "default", // codeMirror主题 // codeMirror主题选项
      cmThemeOptions: [
        "default",
        "3024-day",
        "3024-night",
        "abcdef",
        "ambiance",
        "ayu-dark",
        "ayu-mirage",
        "base16-dark",
        "base16-light",
        "bespin",
        "blackboard",
        "cobalt",
        "colorforth",
        "darcula",
        "dracula",
        "duotone-dark",
        "duotone-light",
        "eclipse",
        "elegant",
        "erlang-dark",
        "gruvbox-dark",
        "hopscotch",
        "icecoder",
        "idea",
        "isotope",
        "lesser-dark",
        "liquibyte",
        "lucario",
        "material",
        "material-darker",
        "material-palenight",
        "material-ocean",
        "mbo",
        "mdn-like",
        "midnight",
        "monokai",
        "moxer",
        "neat",
        "neo",
        "night",
        "nord",
        "oceanic-next",
        "panda-syntax",
        "paraiso-dark",
        "paraiso-light",
        "pastel-on-dark",
        "railscasts",
        "rubyblue",
        "seti",
        "shadowfox",
        "solarized dark",
        "solarized light",
        "the-matrix",
        "tomorrow-night-bright",
        "tomorrow-night-eighties",
        "ttcn",
        "twilight",
        "vibrant-ink",
        "xq-dark",
        "xq-light",
        "yeti",
        "yonce",
        "zenburn",
      ],

      cmEditorMode: "default", // 编辑模式 // 编辑模式选项
      cmEditorModeOptions: ["default", "json", "sql", "javascript", "css", "xml", "html", "yaml", "markdown", "python"],

      cmMode: "application/json", //codeMirror模式
      jsonIndentation: 2, // json编辑模式下，json格式化缩进 支持字符或数字，最大不超过10，默认缩进2个空格
      autoFormatJson: true, // json编辑模式下，输入框失去焦点时是否自动格式化，true 开启， false 关闭
    };
  },

  methods: {
    // 切换编辑模式事件处理函数

    onEditorModeChange(value) {
      switch (value) {
        case "json":
          this.cmMode = "application/json";
          break;
        case "sql":
          this.cmMode = "sql";
          break;
        case "javascript":
          this.cmMode = "javascript";
          break;
        case "xml":
          this.cmMode = "xml";
          break;
        case "css":
          this.cmMode = "css";
          break;
        case "html":
          this.cmMode = "htmlmixed";
          break;
        case "yaml":
          this.cmMode = "yaml";
          break;
        case "markdown":
          this.cmMode = "markdown";
          break;
        case "python":
          this.cmMode = "python";
          break;
        default:
          this.cmMode = "application/json";
      }
    }, // 修改样式（不推荐，建议参考<style>中的样式，提前配置好样式）

    setStyle() {
      let styleStr =
        "position: absolute; top: 80px; left: 50px; right: 200px; bottom: 20px; padding: 2px; height: auto;";
      this.$refs.cmEditor.setStyle(styleStr);
    }, //获取内容

    getValue() {
      let content = this.$refs.cmEditor.getValue();
      console.log(content);
    }, //修改内容

    setValue() {
      let jsonValue = {
        name: "laiyu",
        addr: "广东省深圳市",
        other: "nothing",
        tel: "168888888",
        intro: [{ item1: "item1" }],
      };

      this.$refs.cmEditor.setValue(JSON.stringify(jsonValue));
    },
  },
};
</script>

<style>
.CodeMirror {
  position: absolute;
  top: 80px;
  left: 2px;
  right: 5px;
  bottom: 0px;
  padding: 2px;
  height: auto;
  overflow-y: auto;
}
</style>

<style lang="scss" scoped>
.code-mirror-div {
  position: absolute;
  top: 0px;
  left: 2px;
  right: 5px;
  bottom: 0px;
  padding: 2px;
  .tool-bar {
    top: 20px;
    margin: 30px 2px 0px 20px;
  }
}
</style>
