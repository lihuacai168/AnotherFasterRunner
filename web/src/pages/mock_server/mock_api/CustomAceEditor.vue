// CustomAceEditor.vue

<template>
    <ace-editor
        ref="aceEditor"
        :value="value"
        @input="onInput"
        @init="editorInit"
        lang="python"
        theme="github"
        width="100%"
        :height="codeHeight"
    ></ace-editor>
</template>

<script>
import Editor from 'vue2-ace-editor';

export default {
    components: {
        'ace-editor': Editor
    },
    props: ['value'],
    methods: {
        onInput(value) {
            this.$emit('input', value);
        },
        editorInit() {
            require('brace/ext/language_tools');
            require('brace/mode/python');
            require('brace/theme/dracula');
            const editor = this.$refs.aceEditor.editor;  // 获取编辑器对象
            editor.setOptions({
                enableBasicAutocompletion: true,  // 启用基本自动补全
                enableSnippets: true,  // 启用代码段
                enableLiveAutocompletion: true, // 启用实时自动补全
                autoScrollEditorIntoView: true,
            });
        },
    },
    computed: {
        codeHeight() {
            return window.screen.height - 648;
        }
    }
};
</script>
