<template>
  <div ref="editor" class="main" :style="style"></div>
</template>

<script>
// import * as monaco from "monaco-editor";
import * as monaco from "monaco-editor/esm/vs/editor/editor.api";
import createSqlCompleter from "./util/sql-completion";
import createJavascriptCompleter from "./util/javascript-completion";
import createPythonCompleter from "./util/python-completion";
import registerLanguage from "./util/log-language";

const global = {};

const getHints = (model) => {
  let id = model.id.substring(6);
  return (global[id] && global[id].hints) || [];
};
monaco.languages.registerCompletionItemProvider("sql", createSqlCompleter(getHints));
monaco.languages.registerCompletionItemProvider("javascript", createJavascriptCompleter(getHints));
monaco.languages.registerCompletionItemProvider("python", createPythonCompleter(getHints));
registerLanguage(monaco);
/**
 * monaco options
 * https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.istandaloneeditorconstructionoptions.html
 */
export default {
  props: {
    options: {
      type: Object,
      default() {
        return {};
      },
    },
    value: { type: String, required: true },
    language: { type: String, default: "javascript" },
    theme: { type: String, default: "vs-dark" }, // vs, hc-black
    hints: {
      type: Array,
      default() {
        return [];
      },
    },
    width: { type: [String, Number], default: "100%" },
    height: { type: [String, Number], default: "100%" },
    highlighted: {
      type: Array,
      default: () => [
        {
          number: 0,
          class: "",
        },
      ],
    },
    changeThrottle: { type: Number, default: 0 },
  },
  name: "BaseMonacoEditor",
  data() {
    return {
      editorInstance: null,
      defaultOptions: {
        theme: this.theme,
        fontSize: 14,
      },
    };
  },
  watch: {
    value() {
      if (this.value !== this.editorInstance.getValue()) {
        this.editorInstance.setValue(this.value);
      }
    },
  },
  mounted() {
    this.initEditor();
    global[this.editorInstance._id] = this;
    window.addEventListener("resize", this.layout);
  },
  destroyed() {
    this.editorInstance.dispose();
    global[this.editorInstance._id] = null;
    window.removeEventListener("resize", this.layout);
  },
  methods: {
    layout() {
      this.editorInstance.layout();
    },
    undo() {
      this.editorInstance.trigger("anyString", "undo");
      this.onValueChange();
    },
    redo() {
      this.editorInstance.trigger("anyString", "redo");
      this.onValueChange();
    },
    getOptions() {
      let props = { value: this.value };
      this.language !== undefined && (props.language = this.language);
      return Object.assign({}, this.defaultOptions, this.options, props);
    },
    onValueChange() {
      this.$emit("codeChange", this.editorInstance);
    },
    initEditor() {
      this.MonacoEnvironment = {
        getWorkerUrl: function () {
          return "./editor.worker.bundle.js";
        },
      };

      this.editorInstance = monaco.editor.create(this.$refs.editor, this.getOptions());
      this.editorInstance.onContextMenu((e) => {
        this.$emit("contextmenu", e);
      });
      this.editorInstance.onDidChangeModelContent(() => {
        this.onValueChange();
      });
      this.editorInstance.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_S, () => {
        this.$emit("save");
      });
    },
  },
  computed: {
    style() {
      const { width, height } = this;
      const fixedWidth = width.toString().indexOf("%") !== -1 ? width : `${width}px`;
      const fixedHeight = height.toString().indexOf("%") !== -1 ? height : `${height}px`;
      return {
        width: fixedWidth,
        height: fixedHeight,
      };
    },
  },
};
</script>

<style scoped>
.main /deep/ .view-lines * {
  font-family: Consolas, "Courier New", monospace !important;
}
</style>
