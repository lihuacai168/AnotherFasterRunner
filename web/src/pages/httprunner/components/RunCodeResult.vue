<template>
    <ace-editor
        :value="msg"
        @init="editorInit"
        lang="python"
        theme="dracula"
        width="100%"
        :height="codeHeight"
    ></ace-editor>
</template>

<script>

import Editor from "vue2-ace-editor";

export default {
    components: {
      'ace-editor': Editor
  },
  props: {
    msg: {
      require: true
    }
  },
  data() {
    return {
      timeStamp: '',
      options: {
        selectOnLineNumbers: false
      },
      minimap: {
        enabled: false
      }
    }
  },
  name: 'DebugResult',
  methods: {
    editorInit: function() {
      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/text')
      require('brace/theme/dracula')
    }
  },

  computed: {
    codeHeight() {
      return window.screen.height
    }
  }
}
</script>

<style scoped></style>
