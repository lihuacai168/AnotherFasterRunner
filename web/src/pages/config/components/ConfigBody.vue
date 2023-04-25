<template>
    <div style="margin-left: 10px">
        <div style="margin-top: 10px">
            <el-input
                style="width: 600px"
                placeholder="请输入配置名称"
                v-model="name"
                clearable
            >
                <template v-slot:prepend>配置信息录入</template>

                <el-button
                    slot="append"
                    type="success"
                    plain
                    @click="save = !save"
                >Save
                </el-button>
            </el-input>
        </div>
        <div>
            <el-input
                class="input-with-select"
                placeholder="请输入 base_url 地址"
                v-model="baseUrl"
                clearable
            >
                <template v-slot:prepend>配置请求地址</template>
            </el-input>
        </div>

        <div class="request">
            <el-tabs
                v-model="activeTag"
                style="margin-left: 20px"
            >
                <el-tab-pane label="Header" name="first">
                    <headers
                        :save="save"
                        v-on:header="handleHeader"
                        :header="response ? response.body.header: [] ">
                    </headers>
                </el-tab-pane>

                <el-tab-pane label="Request" name="second">
                    <request
                        :save="save"
                        v-on:request="handleRequest"
                        :request="response ? response.body.request: []"
                    >
                    </request>
                </el-tab-pane>

                <el-tab-pane label="Variables" name="third">
                    <variables
                        :save="save"
                        v-on:variables="handleVariables"
                        :variables="response ? response.body.variables : []"
                    >

                    </variables>
                </el-tab-pane>

                <el-tab-pane label="Hooks" name="fourth">
                    <hooks
                        :save="save"
                        v-on:hooks="handleHooks"
                        :hooks="response ? response.body.hooks: []"
                    >
                    </hooks>
                </el-tab-pane>

                <el-tab-pane label="Parameters" name="five">
                    <parameters
                        :save="save"
                        v-on:parameters="handleParameters"
                        :parameters="response ? response.body.parameters: []"
                    >
                    </parameters>
                </el-tab-pane>

            </el-tabs>
        </div>
    </div>

</template>

<script>
import Headers from '../../../httprunner/components/Headers'
import Request from '../../../httprunner/components/Request'
import Variables from '../../../httprunner/components/Variables'
import Hooks from '../../../httprunner/components/Hooks'
import Parameters from '../../../httprunner/components/Parameters'

export default {
  components: {
    Headers,
    Request,
    Variables,
    Hooks,
    Parameters
  },

  props: {
    project: {
      require: false
    },
    response: {
      require: false
    }
  },

  watch: {
    response: function() {
      this.name = this.response.body.name
      this.baseUrl = this.response.body.base_url
      this.id = this.response.id
    }
  },

  methods: {
    handleHeader(header) {
      this.header = header
    },
    handleRequest(request) {
      this.request = request
    },

    handleVariables(variables) {
      this.variables = variables
    },
    handleHooks(hooks) {
      this.hooks = hooks
    },
    handleParameters(parameters) {
      this.parameters = parameters
      if (this.id === '') {
        this.addConfig()
      } else {
        this.updateConfig()
      }
    },

    addConfig() {
      if (this.validateData()) {
        this.$api.addConfig({
          parameters: this.parameters,
          header: this.header,
          request: this.request,
          variables: this.variables,
          hooks: this.hooks,
          base_url: this.baseUrl,
          name: this.name,
          project: this.project

        }).then(resp => {
          if (resp.success) {
            this.$message.success({
              message: '配置添加成功',
              duration: this.$store.state.duration
            })
            this.$emit('addSuccess')
          } else {
            this.$message.error({
              message: resp.msg,
              duration: this.$store.state.duration
            })
          }
        })
      }
    },

    updateConfig() {
      if (this.validateData()) {
        this.$api.updateConfig(this.id, {
          parameters: this.parameters,
          header: this.header,
          request: this.request,
          variables: this.variables,
          hooks: this.hooks,
          base_url: this.baseUrl,
          name: this.name
        }).then(resp => {
          if (resp.success) {
            this.$message.success({
              message: '配置更新成功',
              duration: this.$store.state.duration
            })
            this.$emit('addSuccess')
          } else {
            this.$message.error({
              message: resp.msg,
              duration: this.$store.state.duration
            })
          }
        })
      }
    },

    validateData() {
      if (this.name === '') {
        this.$notify.error({
          title: '参数错误',
          message: '配置名称不能为空',
          duration: 1500
        })
        return false
      }
      return true
    }

  },

  data() {
    return {
      name: '',
      baseUrl: '',
      id: '',
      header: [],
      request: [],
      variables: [],
      hooks: [],
      parameters: [],
      save: false,
      activeTag: 'first'
    }
  },
  name: 'ConfigBody'
}
</script>

<style scoped>
.el-select {
    width: 130px;
}

.input-with-select {
    width: 600px;
    margin-top: 10px;
}

.request {
    margin-top: 15px;
    border: 1px solid #ddd;
}

</style>
