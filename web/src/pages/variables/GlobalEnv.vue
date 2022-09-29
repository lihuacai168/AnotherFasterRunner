<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 10px">
                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="openFormModal('variablesForm', 'dialogVisible')"
                    >新增变量
                    </el-button>

                    <el-button
                        v-show="variablesData.count !== 0 "
                        style="margin-left: 20px"
                        type="danger"
                        icon="el-icon-delete"
                        circle
                        size="mini"
                        @click="delSelectionVariables"
                    ></el-button>

                    <el-dialog title="添加变量" :visible.sync="dialogVisible" width="30%" align="center">
                        <el-form
                            :model="variablesForm"
                            :rules="rules"
                            ref="variablesForm"
                            label-width="100px"
                            class="project"
                        >
                            <el-form-item label="变量名" prop="key">
                                <el-input v-model="variablesForm.key" clearable placeholder="请输入变量名"></el-input>
                            </el-form-item>

                            <el-form-item label="变量值" prop="value">
                                <el-input v-model="variablesForm.value" clearable placeholder="请输入变量值"></el-input>
                            </el-form-item>

                            <el-form-item label="变量描述" prop="description">
                                <el-input v-model="variablesForm.description" clearable
                                          placeholder="请输入变量描述"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
              <el-button @click="resetForm('variablesForm', 'dialogVisible')">取 消</el-button>
              <el-button type="primary" @click="handleConfirm('variablesForm')">确 定</el-button>
                        </span>
                    </el-dialog>

                    <el-dialog title="编辑变量" :visible.sync="editdialogVisible" width="30%" align="center">
                        <el-form
                            :model="editVariablesForm"
                            :rules="rules"
                            ref="editVariablesForm"
                            label-width="100px"
                            class="project"
                        >
                            <el-form-item label="变量名" prop="key">
                                <el-input v-model="editVariablesForm.key" clearable placeholder="请输入变量名"></el-input>
                            </el-form-item>
                            <el-form-item label="变量值" prop="value">
                                <el-input v-model="editVariablesForm.value" clearable placeholder="请输入变量值"></el-input>
                            </el-form-item>
                            <el-form-item label="变量描述" prop="description">
                                <el-input v-model="editVariablesForm.description" clearable
                                          placeholder="请输入变量描述"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
              <el-button @click="resetForm('editVariablesForm', 'editdialogVisible')">取 消</el-button>
              <el-button type="primary" @click="handleEditConfirm('editVariablesForm')">确 定</el-button>
                        </span>
                    </el-dialog>
                </div>
            </div>
        </el-header>

        <el-container>
            <el-header style="padding: 0; height: 50px;">
                <div style="padding-top: 8px; padding-left: 10px; overflow: hidden">
                    <el-row :gutter="50">
                        <el-col :span="6" style="padding-right: 0">
                            <el-input
                                placeholder="请输入变量名称"
                                v-if="variablesData.count >= 0"
                                clearable
                                size="medium"
                                v-model="search"
                            >
                                <el-button slot="append" icon="el-icon-search" @click="getVariablesList"></el-button>
                            </el-input>
                        </el-col>
                        <el-col :span="2" style="padding-left: 5px">
                            <el-button type="primary" size="medium" @click="resetSearch">重置</el-button>
                        </el-col>
                        <el-col :span="7">
                            <el-pagination
                                :page-size="11"
                                v-show="variablesData.count !== 0 "
                                background
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="variablesData.count"
                            ></el-pagination>
                        </el-col>
                    </el-row>
                </div>
            </el-header>

            <el-container>
                <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                    <div style="position: fixed; bottom: 0; right:0; left: 0; top: 150px">
                        <el-table
                            highlight-current-row
                            :data="variablesData.results"
                            :show-header="variablesData.results.length !== 0 "
                            stripe
                            height="calc(100%)"
                            @cell-mouse-enter="cellMouseEnter"
                            @cell-mouse-leave="cellMouseLeave"
                            @selection-change="handleSelectionChange"
                        >
                            <el-table-column type="selection" width="45"></el-table-column>

                            <el-table-column label="变量名">
                                <template v-slot="scope">
                                    <div>{{ scope.row.key }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column label="变量值">
                                <template v-slot="scope">
                                    <div>{{ scope.row.value }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column label="变量描述">
                                <template v-slot="scope">
                                    <div>{{ scope.row.description }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column label="更新时间">
                                <template v-slot="scope">
                                    <div>{{ scope.row.update_time|datetimeFormat }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column width="120">
                                <template v-slot="scope">
                                    <el-row v-show="currentRow === scope.row">
                                        <el-button
                                            type="info"
                                            icon="el-icon-edit"
                                            title="编辑"
                                            circle
                                            size="mini"
                                            @click="handleEditVariables(scope.row)"
                                        ></el-button>

                                        <el-button
                                            type="success"
                                            icon="el-icon-document-copy"
                                            title="复制"
                                            circle
                                            size="mini"
                                            style="margin-left: 0"
                                            @click="handleCopyVariables(scope.row)"
                                        ></el-button>

                                        <el-button
                                            v-show="variablesData.count !== 0"
                                            type="danger"
                                            icon="el-icon-delete"
                                            title="删除"
                                            circle
                                            size="mini"
                                            style="margin-left: 0"
                                            @click="handleDelVariables(scope.row.id)"
                                        ></el-button>
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
    name: "GlobalEnv",
    data() {
        return {
            search: "",
            selectVariables: [],
            currentRow: "",
            currentPage: 1,
            variablesData: {
                count: 0,
                results: [],
            },
            editdialogVisible: false,
            dialogVisible: false,
            variablesForm: {
                key: "",
                value: "",
                project: this.$route.params.id,
            },

            editVariablesForm: {
                key: "",
                value: "",
                id: "",
                description: "",
            },

            rules: {
                key: [
                    {required: true, message: "请输入变量名", trigger: "blur"},
                    {min: 1, max: 100, message: "最多不超过100个字符", trigger: "blur"},
                ],
                value: [
                    {required: true, message: "请输入变量值", trigger: "blur"},
                    {
                        min: 1,
                        max: 1024,
                        message: "最多不超过1024个字符",
                        trigger: "blur",
                    },
                ],
                description: [
                    {required: false, message: "请输入变量描述", trigger: "blur"},
                    {min: 0, max: 100, message: "最多不超过100个字符", trigger: "blur"},
                ],
            },
        };
    },
    mounted() {
        this.getVariablesList();
    },

    watch: {
        search() {
            this.getVariablesList()
        }
    },

    methods: {
        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = "";
        },

        handleEditVariables(row) {
            this.editVariablesForm = {
                key: row.key,
                value: row.value,
                id: row.id,
                description: row.description,
            };

            this.editdialogVisible = true;
        },

        handleCopyVariables(row) {
            this.dialogVisible = true;
            this.variablesForm.key = row.key;
            this.variablesForm.value = row.value;
            this.variablesForm.description = row.description;
        },

        handleDelVariables(index) {
            this.$confirm("此操作将永久删除该全局变量，是否继续?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
            }).then(() => {
                this.$api.deleteVariables(index).then((resp) => {
                    if (resp.success) {
                        this.getVariablesList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                });
            });
        },
        handleSelectionChange(val) {
            this.selectVariables = val;
        },

        handleCurrentChange(val) {
            this.$api
                .getVariablesPaginationBypage({
                    params: {
                        page: this.currentPage,
                        project: this.variablesForm.project,
                        search: this.search,
                    },
                })
                .then((resp) => {
                    this.variablesData = resp;
                });
        },
        delSelectionVariables() {
            if (this.selectVariables.length !== 0) {
                this.$confirm("此操作将永久删除勾选的全局变量，是否继续?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                }).then(() => {
                    this.$api
                        .delAllVariabels({data: this.selectVariables})
                        .then((resp) => {
                            this.getVariablesList();
                        });
                });
            } else {
                this.$notify.warning({
                    title: "提示",
                    message: "请至少勾选一个全局变量",
                    duration: this.$store.state.duration,
                });
            }
        },

        handleConfirm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.dialogVisible = false;
                    this.$api.addVariables(this.variablesForm).then((resp) => {
                        if (!resp.success) {
                            this.$message.info({
                                message: resp.msg,
                                duration: this.$store.state.duration,
                            });
                        } else {
                            this.variablesForm.key = "";
                            this.variablesForm.value = "";
                            this.getVariablesList();
                        }
                    });
                }
            });
        },

        /**
         * 表单重置
         */
        resetForm(formName, showFlag) {
            this[showFlag] = false;

            this.$refs[formName].resetFields();
            Object.keys(this[formName]).forEach(key => {
                if (key !== "project") {
                    this[formName][key] = "";
                }
            });
        },

        /**
         * 唤起表单弹窗
         */
        openFormModal(formName, showFlag) {
            Object.keys(this[formName]).forEach(key => {
                if (key !== "project") {
                    this[formName][key] = "";
                }
            });

            this[showFlag] = true;
        },

        handleEditConfirm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.editdialogVisible = false;
                    this.$api
                        .updateVariables(this.$route.params.id, this.editVariablesForm)
                        .then((resp) => {
                            if (!resp.success) {
                                this.$message.info({
                                    message: resp.msg,
                                    duration: this.$store.state.duration,
                                });
                            } else {
                                this.getVariablesList();
                            }
                        });
                }
            });
        },

        getVariablesList() {
            this.$api
                .variablesList({
                    params: {
                        project: this.variablesForm.project,
                        search: this.search,
                    },
                })
                .then((resp) => {
                    this.variablesData = resp;
                });
        },
        resetSearch() {
            (this.search = ""), this.getVariablesList();
        },
    },
};
</script>

<style>
</style>
