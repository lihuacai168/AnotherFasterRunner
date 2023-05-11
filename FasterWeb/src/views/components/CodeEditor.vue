<template>
  <div class="codeMirror">
    <codemirror
      ref="cmEditor"
      :value="code"
      :options="cmOptions"
      @ready="onCmReady"
      @focus="onCmFocus"
      @input="onCmCodeChange"
    />
  </div>
</template>

<script>
import { codemirror } from "vue-codemirror";
import "codemirror/mode/javascript/javascript.js";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/panda-syntax.css";
import "codemirror/theme/idea.css";
import "codemirror/theme/darcula.css";
import "codemirror/mode/python/python.js";

import "codemirror/addon/hint/show-hint";
import "codemirror/addon/hint/show-hint.css";
import "codemirror/addon/hint/javascript-hint";

export default {
  props: {
    code: { type: String, required: true },
    theme: { type: String, default: "darcula" },
    mode: { type: String, default: "python" },
  },
  name: "CodeEditor",
  components: {
    codemirror,
  },
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        mode: this.mode,
        theme: this.theme,
        lineNumbers: true,
        line: true,
        // more CodeMirror options...
      },
    };
  },
  methods: {
    onCmReady(cm) {
      cm.on("keypress", () => {
        // cm.showHint();
      });
    },
    onCmFocus(cm) {},
    onCmCodeChange(newCode) {
      this.$emit("codeChange", newCode);
    },
  },
  computed: {
    codemirror() {
      return this.$refs.cmEditor.codemirror;
    },
  },
  mounted() {
    // console.log('the current CodeMirror instance object:', this.$refs.cmEditor.codemirror)
    // you can use this.codemirror to do something...
  },
};
</script>

<style lang="scss">
.codeMirror {
  .CodeMirror {
    // overscroll-y: scroll !important;
    height: auto !important;
  }
}
</style>
