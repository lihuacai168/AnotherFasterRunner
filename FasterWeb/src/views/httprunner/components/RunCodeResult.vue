<template>
  <!-- <MonacoEditor :height="codeHeight" language="text" :code="msg" :options="options"> </MonacoEditor> -->
  <MonacoEditor :mode="mode" :code="msg" :theme="theme"> </MonacoEditor>
</template>

<script>
// import MonacoEditor from "../../monaco-editor/MonacoEditor.vue";
import MonacoEditor from "../../components/CodeEditor.vue";

export default {
  components: {
    MonacoEditor,
  },
  props: {
    msg: { require: true },
  },
  data() {
    return {
      timeStamp: "",
      theme: "idea",
      mode: "text",
      options: {
        selectOnLineNumbers: false,
      },
      minimap: {
        enabled: false,
      },
    };
  },
  name: "DebugResult",
  computed: {
    codeHeight() {
      return window.screen.height;
    },
  },
};
</script>

<style scoped></style>
