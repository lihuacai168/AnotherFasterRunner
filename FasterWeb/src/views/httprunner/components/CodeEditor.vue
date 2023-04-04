<template>
  <codemirror
    ref="cmEditor"
    :value="code"
    :options="cmOptions"
    @ready="onCmReady"
    @focus="onCmFocus"
    @input="onCmCodeChange"
  />
</template>

<script>
import codemirror from "vue-codemirror";
import "codemirror/mode/javascript/javascript.js";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/cobalt.css";
import "codemirror/mode/python/python.js";
import "codemirror/addon/hint/show-hint.css";

require("codemirror/addon/hint/javascript-hint");

export default {
  name: "CodeEditor",
  components: {
    codemirror,
  },
  data() {
    return {
      code: "const a = 1",
      cmOptions: {
        tabSize: 4,
        mode: "javascript",
        theme: "cobalt",
        lineNumbers: true,
        line: true,
        // more CodeMirror options...
      },
    };
  },
  methods: {
    onCmReady(cm) {
      console.log("the editor is readied!", cm);
      cm.on("keypress", () => {
        cm.showHint();
      });
    },
    onCmFocus(cm) {
      console.log("the editor is focused!", cm);
    },
    onCmCodeChange(newCode) {
      console.log("this is new code", newCode);
      this.code = newCode;
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
