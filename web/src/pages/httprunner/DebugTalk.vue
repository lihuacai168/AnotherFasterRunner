<template>
    <el-container>
        <el-header style="background-color: #F7F7F7;; padding: 0; height: 50px;">
            <div style="padding-top: 10px; margin-left: 10px; ">
                <el-row>
                    <el-col :span="15">
                        <el-button
                            type="primary"
                            size="small"
                            icon="el-icon-circle-check-outline"
                            @click="handleConfirm"
                            round
                        >
                            点击保存
                        </el-button>

                        <el-button
                            icon="el-icon-caret-right"
                            type="info"
                            size="small"
                            @click="handleRunCode"
                            round
                        >
                            在线运行
                        </el-button>
                    </el-col>
                </el-row>
            </div>

        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px">
                <el-row>
                    <el-col :span="24">
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

                    </el-col>

                    <el-col :span="14">
                        <el-drawer
                            style="margin-top: 100px"
                            :height="codeHeight"
                            :destroy-on-close="true"
                            :with-header="false"
                            :modal="false"
                            v-model:visible="isShowDebug"
                        >
                            <RunCodeResult :msg="resp.msg"></RunCodeResult>
                        </el-drawer>

                    </el-col>

                </el-row>

            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import MonacoEditor from 'vue-monaco-editor'
import RunCodeResult from './components/RunCodeResult'
import BaseMonacoEditor from '../monaco-editor/BaseMonacoEditor'

export default {
  components: {
    MonacoEditor,
    RunCodeResult,
    BaseMonacoEditor
  },
  data() {
    return {
      timeStamp: '',
      isShowDebug: false,
      options: {
        selectOnLineNumbers: false
      },
      code: {
        code: '',
        id: ''
      },
      resp: {
        msg: ''
      }
    }
  },
  name: 'DebugTalk',
  methods: {
    onMounted(editor) {
      this.editor = editor
    },
    onCodeChange(editor) {
      this.code.code = editor.getValue()
      // editor.trigger('随便写点儿啥', 'editor.action.triggerSuggest', {});
    },
    handleRunCode() {
      this.resp.msg = ''
      this.$api.runDebugtalk(this.code).then(resp => {
        this.resp = resp
      })
    },
    handleConfirm() {
      this.$api.updateDebugtalk(this.code).then(resp => {
        this.getDebugTalk()
        this.$message.success('代码保存成功')
      })
    },
    getDebugTalk() {
      this.$api.getDebugtalk(this.$route.params.id).then(res => {
        this.code = res
      })
    }
  },
  watch: {
    code() {
      this.timeStamp = (new Date()).getTime()
    },
    resp() {
      this.isShowDebug = true
    }
  },

  computed: {

    codeHeight() {
      return window.screen.height - 248
    }
  },

  mounted() {
    this.getDebugTalk()
  }
}
</script>

<style scoped>

</style>
