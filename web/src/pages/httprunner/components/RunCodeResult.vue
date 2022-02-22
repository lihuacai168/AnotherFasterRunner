<template>
    <MonacoEditor
        :height="codeHeight"
        language="text"
        :code="msg"
        :options="options"
    >
    </MonacoEditor>
</template>

<script>
import MonacoEditor from 'vue-monaco-editor'

export default {
    components: {
        MonacoEditor
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
    name: "DebugResult",
    computed: {
        codeHeight() {
            return window.screen.height
        }
    },
}
</script>

<style scoped>

</style>
