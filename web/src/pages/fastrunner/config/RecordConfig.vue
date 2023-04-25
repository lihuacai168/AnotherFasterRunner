<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="addConfig"
                    >新增配置
                    </el-button>

                    <!--  <el-button
                          type="primary"
                          plain
                          size="small"
                          icon="el-icon-upload"
                      >导入配置
                      </el-button>

                      <el-button
                          type="info"
                          plain
                          size="small"
                          icon="el-icon-download"
                      >导出配置
                      </el-button>-->

                    <el-button
                        style="margin-left: 20px"
                        type="danger"
                        icon="el-icon-delete"
                        circle
                        size="mini"
                        @click="del= !del"
                    ></el-button>

                    <el-button
                        :disabled="!addConfigActivate"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="addConfigActivate=false"
                    >返回列表
                    </el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px">
                <config-body
                    v-show="addConfigActivate"
                    :project="$route.params.id"
                    :response="respConfig"
                    :type="type"
                    v-on:addSuccess="handleAddSuccess"
                >
                </config-body>

                <config-list
                    v-if="!addConfigActivate"
                    :project="$route.params.id"
                    v-on:respConfig="handleRespConfig"
                    :del="del"
                    :back="back"
                >
                </config-list>
            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import ConfigBody from './components/ConfigBody'
import ConfigList from './components/ConfigList'

export default {
  components: {
    ConfigBody,
    ConfigList
  },

  computed: {
    initResponse: {
      get() {
        return this.addConfigActivate
      },
      set(value) {
        this.addConfigActivate = value
        this.respConfig = {
          is_default: false,
          id: '',
          body: {
            name: '',
            base_url: '',
            header: [{
              key: '',
              value: '',
              desc: ''
            }],
            request: {
              data: [{
                key: '',
                value: '',
                desc: '',
                type: 1
              }],
              params: [{
                key: '',
                value: '',
                desc: '',
                type: 1
              }],
              json_data: ''
            },
            variables: [{
              key: '',
              value: '',
              desc: '',
              type: 1
            }],
            hooks: [{
              setup: '',
              teardown: ''
            }],
            parameters: [{
              key: '',
              value: '',
              desc: ''
            }]

          }
        }
      }
    }
  },
  data() {
    return {
      back: false,
      del: false,
      addConfigActivate: false,
      respConfig: '',
      type: ''
    }
  },
  methods: {
    handleAddSuccess() {
      this.back = !this.back
      this.addConfigActivate = false
    },
    addConfig() {
      this.initResponse = true
      this.type = 'add'
    },
    handleRespConfig(row) {
      this.respConfig = row
      this.type = 'edit'
      this.addConfigActivate = true
    }
  },
  name: 'RecordConfig',
  mounted() {

  }
}
</script>

<style>

</style>
