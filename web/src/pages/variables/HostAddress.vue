<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="dialogVisible=true"
                    >新增Hosts
                    </el-button>

                    <el-dialog
                        title="添加Hosts"
                        v-model:visible="dialogVisible"
                        width="35%"
                        align="center"
                    >
                        <el-form
                            :model="variablesForm"
                            :rules="rules"
                            ref="variablesForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="Hosts名" prop="name">
                                <el-input resize v-model="variablesForm.name" clearable
                                          placeholder="请输入Hosts名"></el-input>
                            </el-form-item>
                            <el-form-item label="IP域名映射" prop="value">
                                <el-input
                                    v-model="variablesForm.value"
                                    type="textarea"
                                    :autosize="{ minRows: 10, maxRows: 16}"
                                    placeholder="127.0.0.1 localhost
192.168.0.1 gateway"
                                    clearable
                                ></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('variablesForm')">确 定</el-button>
                      </span>
                    </el-dialog>

                    <el-dialog
                        title="编辑Hosts"
                        v-model:visible="editdialogVisible"
                        width="35%"
                        align="center"
                    >
                        <el-form
                            :model="editVariablesForm"
                            :rules="rules"
                            ref="editVariablesForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="Hosts名" prop="name">
                                <el-input resize v-model="editVariablesForm.name" clearable
                                          placeholder="请输入Hosts名"></el-input>
                            </el-form-item>
                            <el-form-item label="IP域名映射" prop="value">
                                <el-input
                                    v-model="editVariablesForm.value"
                                    type="textarea"
                                    :autosize="{ minRows: 10, maxRows: 16}"
                                    placeholder="127.0.0.1 localhost
192.168.0.1 gateway"
                                    clearable
                                ></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="editdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleEditConfirm('editVariablesForm')">确 定</el-button>
                      </span>
                    </el-dialog>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-header style="padding: 0; height: 50px;">
                <div style="padding-top: 8px; padding-left: 30px; overflow: hidden">
                    <el-pagination
                        :page-size="11"
                        v-show="hostIPData.count !== 0 "
                        background
                        @current-change="handleCurrentChange"
                        v-model:current-page="currentPage"
                        layout="total, prev, pager, next, jumper"
                        :total="hostIPData.count"
                    >
                    </el-pagination>

                </div>
            </el-header>

            <el-container>
                <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                    <div style="position: fixed; bottom: 0; right:0; left: 220px; top: 150px">
                        <el-table
                            highlight-current-row
                            :data="hostIPData.results"
                            :show-header="hostIPData.results.length !== 0 "
                            stripe
                            height="calc(100%)"
                            @cell-mouse-enter="cellMouseEnter"
                            @cell-mouse-leave="cellMouseLeave"
                        >
                            <el-table-column
                                label="Hosts名"
                            >
                                <template v-slot="scope">
                                    <div>{{ scope.row.name }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column
                                label="IP域名映射表"
                            >
                                <template v-slot="scope">
                                    <el-input
                                        v-model="scope.row.value"
                                        type="textarea"
                                        :autosize="{ minRows: 1, maxRows: 5}"
                                        clearable
                                        disabled
                                    ></el-input>
                                </template>
                            </el-table-column>

                            <el-table-column
                                label="更新时间"
                            >
                                <template v-slot="scope">
                                    <div>{{ scope.row.update_time|datetimeFormat }}</div>

                                </template>
                            </el-table-column>

                            <el-table-column>
                                <template v-slot="scope">
                                    <el-row v-show="currentRow === scope.row">
                                        <el-button
                                            type="info"
                                            icon="el-icon-edit"
                                            title="编辑"
                                            circle size="mini"
                                            @click="handleEditHostIP(scope.row)"
                                        ></el-button>

                                        <el-button
                                            v-show="hostIPData.count !== 0"
                                            type="danger"
                                            icon="el-icon-delete"
                                            title="删除"
                                            circle size="mini"
                                            @click="handleDelHost(scope.row.id)"
                                        >
                                        </el-button>
                                    </el-row>
                                </template>

                            </el-table-column>

                        </el-table>
                    </div>
                </el-main>
            </el-container>
        </el-container>
    </el-container>

</template>

<script>

export default {

  data() {
    return {
      search: '',
      currentRow: '',
      currentPage: 1,
      hostIPData: {
        count: 0,
        results: []
      },
      editdialogVisible: false,
      dialogVisible: false,
      variablesForm: {
        name: '',
        value: '',
        project: this.$route.params.id
      },

      editVariablesForm: {
        name: '',
        value: '',
        id: ''
      },

      rules: {
        name: [
          {required: true, message: '请输入变量名', trigger: 'blur'},
          {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
        ],
        value: [
          {required: true, message: '请输入变量值', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    cellMouseEnter(row) {
      this.currentRow = row
    },

    cellMouseLeave(row) {
      this.currentRow = ''
    },

    handleEditHostIP(row) {
      this.editVariablesForm = {
        name: row.name,
        value: row.value,
        id: row.id
      }

      this.editdialogVisible = true
    },

    handleDelHost(index) {
      this.$confirm('此操作将永久删除该域名，是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$api.deleteHost(index).then(resp => {
          if (resp.success) {
            this.getHostIPList()
          } else {
            this.$message.error(resp.msg)
          }
        })
      })
    },

    handleCurrentChange(val) {
      this.$api.getHostPaginationBypage({
        params: {
          page: this.currentPage,
          project: this.variablesForm.project
        }
      }).then(resp => {
        this.hostIPData = resp
      })
    },

    handleConfirm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.dialogVisible = false
          this.$api.addHostIP(this.variablesForm).then(resp => {
            if (!resp.success) {
              this.$message.info({
                message: resp.msg,
                duration: this.$store.state.duration
              })
            } else {
              this.variablesForm.name = ''
              this.variablesForm.value = ''
              this.getHostIPList()
            }
          })
        }
      })
    },

    handleEditConfirm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.editdialogVisible = false
          this.$api.updateHost(this.editVariablesForm.id, this.editVariablesForm).then(resp => {
            if (!resp.success) {
              this.$message.info({
                message: resp.msg,
                duration: this.$store.state.duration
              })
            } else {
              this.getHostIPList()
            }
          })
        }
      })
    },

    getHostIPList() {
      this.$api.hostList({
        params: {
          project: this.variablesForm.project
        }
      }).then(resp => {
        this.hostIPData = resp
      })
    }
  },
  name: 'HostAddress',
  mounted() {
    this.getHostIPList()
  }
}
</script>

<style>

</style>
