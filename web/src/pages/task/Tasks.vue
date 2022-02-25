<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="handleAddTask"
                    >添加任务
                    </el-button>

                    <el-button
                        :disabled="!addTasks"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="addTasks=false"
                    >返回列表
                    </el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-header v-if="!addTasks" style="padding: 0; height: 500px; margin-top: 10px;">

                <div style="padding-top: 2px; padding-left: 30px; display: flex">
                    <div>
                        <el-input placeholder="请输入任务名称" clearable v-model="searchTaskName"
                                  @keyup.enter.native="getTaskList"
                                  style="width: 400px">
                            <el-button slot="append" icon="el-icon-search" @click="getTaskList"></el-button>
                        </el-input>
                        <span style="margin-left: 10px">创建人: </span>
                        <el-select v-model="selectUser" placeholder="请选择创建人" filterable
                                   :style="{width: '120px'}">
                            <el-option v-for="(item, index) in users" :key="index"
                                       :label="item.label"
                                       :value="item.value" :disabled="item.disabled"></el-option>
                        </el-select>
                        <el-button
                            type="primary"
                            @click="resetSearch"
                        >重置
                        </el-button>
                    </div>
                    <div>
                        <el-pagination
                            style="margin-top: 2px"
                            :page-size="11"
                            v-show="tasksData.count !== 0 "
                            background
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="tasksData.count"
                        >
                        </el-pagination>
                    </div>
                </div>
            </el-header>
            <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                <div style="position: fixed; bottom: 0; right:0; left: 230px; top: 160px">
                    <el-table
                        v-if="!addTasks"
                        :data="tasksData.results"
                        :show-header="tasksData.results.length !== 0 "
                        stripe
                        highlight-current-row
                        height="calc(100%)"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                    >

                        <el-table-column
                            label="任务ID"
                            width="80"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.id }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            label="任务名称"
                            width="240"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.name }}</div>
                            </template>
                        </el-table-column>


                        <el-table-column
                            width="120"
                            label="时间配置"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.crontab }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="170"
                            label="下次执行时间"
                        >
                            <template slot-scope="scope">
                                <div>
                                    {{
                                        scope.row.kwargs.next_execute_time ? scope.row.kwargs.next_execute_time : '' | timestampToTime
                                    }}
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="70"
                            label="CI项目"
                        >
                            <template slot-scope="scope">
                                <div>
                                    {{
                                        scope.row.kwargs.ci_project_ids
                                    }}
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="70"
                            label="CI环境"
                        >
                            <template slot-scope="scope">
                                <div>
                                    {{
                                        scope.row.kwargs.ci_env === '请选择' ? "" : scope.row.kwargs.ci_env
                                    }}
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="180"
                            label="运行配置"
                        >

                            <template slot-scope="scope">
                                <div>
                                    {{
                                        scope.row.kwargs.config === '请选择' ? "用例配置" : scope.row.kwargs.config
                                    }}
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="100"
                            label="通知策略"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.strategy }}</div>

                            </template>
                        </el-table-column>
                        <el-table-column
                            width="70"
                            label="已运行"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.total_run_count }} 次</div>

                            </template>
                        </el-table-column>


                        <el-table-column
                            width="80"
                            label="状态"
                        >
                            <template slot-scope="scope">
                                <el-switch
                                    v-model="scope.row.enabled"
                                    active-color="#13ce66"
                                    @change="handleSwitchChange(scope.row.id, scope.row.enabled)"
                                    inactive-color="#ff4949">
                                </el-switch>
                            </template>
                        </el-table-column>
                        <!--                        <el-table-column-->
                        <!--                            width="320"-->
                        <!--                            label="接收人"-->
                        <!--                        >-->
                        <!--                            <template slot-scope="scope">-->
                        <!--                                <div>{{ scope.row.kwargs.receiver }}</div>-->
                        <!--                            </template>-->
                        <!--                        </el-table-column>-->
                        <!--                        <el-table-column-->
                        <!--                            width="320"-->
                        <!--                            label="抄送人"-->
                        <!--                        >-->
                        <!--                            <template slot-scope="scope">-->
                        <!--                                <div>{{ scope.row.kwargs.mail_cc }}</div>-->
                        <!--                            </template>-->
                        <!--                        </el-table-column>-->
                        <el-table-column
                            width="80"
                            label="更新人"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.updater }}</div>
                            </template>
                        </el-table-column>
                        <el-table-column
                            width="80"
                            label="创建人"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.kwargs.creator }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            width="200"
                        >
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        icon="el-icon-edit"
                                        title="编辑"
                                        circle size="mini"
                                        @click="handleEditSchedule(scope.row.id, scope.row)"
                                    ></el-button>
                                    <el-button
                                        type="success"
                                        icon="el-icon-document-copy"
                                        title="复制"
                                        circle size="mini"
                                        @click="handleCopyTask(scope.row.id, scope.row.name)"
                                    ></el-button>
                                    <el-button
                                        type="primary"
                                        icon="el-icon-caret-right"
                                        title="手动触发任务"
                                        circle size="mini"
                                        @click="runTask(scope.row.id)"
                                    >
                                    </el-button>
                                    <el-button
                                        type="danger"
                                        icon="el-icon-delete"
                                        title="删除"
                                        circle size="mini"
                                        @click="delTasks(scope.row.id)"
                                    >
                                    </el-button>
                                </el-row>
                            </template>

                        </el-table-column>

                    </el-table>
                </div>
            </el-main>
            <add-tasks
                v-if="addTasks"
                v-on:changeStatus="changeStatus"
                :ruleForm="ruleForm"
                :configOptions="configOptions"
                :CIEnvOptions="CIEnvOptions"
                :args="args"
                :scheduleId="scheduleId"
            >
            </add-tasks>
        </el-container>
    </el-container>

</template>

<script>
import AddTasks from './AddTasks'

export default {
    components: {
        AddTasks
    },
    data() {
        return {
            addTasks: false,
            currentPage: 1,
            currentRow: '',
            tasksData: {
                count: 0,
                results: []
            },
            ruleForm: {
                switch: true,
                crontab: '',
                ci_project_ids: '',
                strategy: '始终发送',
                receiver: '',
                mail_cc: '',
                name: '',
                sensitive_keys: '',
                self_error: '',
                fail_count: 1,
                webhook: '',
                config: '请选择',
                ci_env: '请选择',
                is_parallel: false,
            },
            users: [],
            selectUser: '',
            searchTaskName: '',
            configOptions: [],
            CIEnvOptions: ['请选择', 'dev', 'qa', 'qa1', 'uat', 'prod'],
        }
    },
    methods: {
        handleAddTask() {
            this.addTasks = true;
            this.scheduleId = '';
            this.ruleForm = {
                switch: true,
                crontab: '',
                strategy: '始终发送',
                receiver: '',
                mail_cc: '',
                name: '',
                sensitive_keys: '',
                self_error: '',
                fail_count: 1,
                webhook: '',
                ci_project_ids: '',
                config: "请选择",
                ci_env: "请选择",
                is_parallel: false,
            };
            this.args = [];
            this.initConfig()
        },
        delTasks(id) {
            this.$confirm('此操作将永久删除该定时任务，是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.deleteTasks(id).then(resp => {
                    if (resp.success) {
                        this.getTaskList();
                    }
                })
            })
        },
        runTask(id) {
            this.$api.runTask(id).then(resp => {
                if (resp.success) {
                    this.$message.info({
                        title: '提示',
                        message: resp.msg,
                        duration: 2000,
                        center: true
                    })
                } else {
                    this.$message.error({
                        message: resp.msg,
                        duration: 2000,
                        center: true
                    })
                }
            })
        },
        handleCurrentChange(val) {
            this.$api.getTaskPaginationBypage({
                params: {
                    page: this.currentPage,
                    creator: this.selectUser,
                    project: this.$route.params.id
                }
            }).then(resp => {
                this.tasksData = resp;
            })
        },
        handleSwitchChange(id, val) {
            this.$api.patchTask(id, {'switch': val}).then(resp => {
                if (resp.success) {
                    this.$notify.success('更新定时任务成功');
                } else {
                    this.$notify.success('更新定时任务失败');
                }
                this.getTaskList()
            })
        },
        handleEditSchedule(id, index_data) {
            // debugger;
            // 激活addTasks组件
            this.addTasks = true;
            this.scheduleId = id;
            this.ruleForm["crontab"] = index_data.kwargs.crontab;
            this.ruleForm["strategy"] = index_data.kwargs.strategy;
            this.ruleForm["receiver"] = index_data.kwargs.receiver;
            this.ruleForm["mail_cc"] = index_data.kwargs.mail_cc;
            this.ruleForm["fail_count"] = index_data.kwargs.fail_count;
            this.ruleForm["self_error"] = index_data.kwargs.self_error;
            this.ruleForm["sensitive_keys"] = index_data.kwargs.sensitive_keys;
            this.ruleForm["webhook"] = index_data.kwargs.webhook;
            this.ruleForm["ci_project_ids"] = index_data.kwargs.ci_project_ids;
            this.ruleForm["name"] = index_data.name;
            this.ruleForm["switch"] = index_data.enabled;
            this.ruleForm["updater"] = this.$store.state.user;
            this.ruleForm["creator"] = index_data.kwargs.creator;
            this.args = index_data.args;
            this.ruleForm["config"] = index_data.kwargs.config
            this.ruleForm["ci_env"] = index_data.kwargs.ci_env
            this.ruleForm["is_parallel"] = index_data.kwargs.is_parallel
            this.initConfig()
        },
        /*
        复制定时任务
         */
        handleCopyTask(id, name) {
            this.$prompt('请输入任务名称', '提示', {
                confirmButtonText: '确定',
                inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                inputErrorMessage: '任务名称不能为空',
                inputValue: name
            }).then(({value}) => {
                this.$api.copyTask(id, {
                    'name': value
                }).then(resp => {
                    if (resp.success) {
                        this.getTaskList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
        },
        // changeStatus(value) {
        //     this.getTaskList();
        //     this.addTasks = value;
        // },
        changeStatus(value) {
            this.getTaskList();
            this.addTasks = value;
            this.args = [];
            this.ruleForm = {
                switch: true,
                crontab: '',
                strategy: '始终发送',
                receiver: '',
                mail_cc: '',
                name: '',
                self_error: '',
                fail_count: '',
                sensitive_keys: '',
                webhook: '',
                ci_project_ids: '',
                config: '请选择',
                ci_env: '请选择',
                is_parallel: false,
            }
        },
        getTaskList() {
            this.$api.taskList({
                params: {
                    project: this.$route.params.id,
                    creator: this.selectUser,
                    task_name: this.searchTaskName
                }
            }).then(resp => {
                this.tasksData = resp
            })
        },
        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        },
        getUserList() {
            this.$api.getUserList().then(resp => {
                    for (let i = 0; i < resp.length; i++) {
                        this.users.push({"label": resp[i].username, "value": resp[i].username})
                    }
                    this.users.unshift({"label": "所有人", "value": ""})
                }
            )
        },
        resetSearch() {
            this.searchTaskName = ""
            this.selectUser = ""
        },

        initConfig() {
            this.$api.getAllConfig(this.$route.params.id).then(resp => {
                this.configOptions = resp;
                this.configOptions.unshift({name: '请选择'})
            });
        },
    },
    name: "Tasks",
    watch: {
        selectUser() {
            this.getTaskList()
        },
        searchTaskName() {
            this.getTaskList()
        },
    },
    mounted() {
        // this.initConfig()
        this.getUserList()
        this.getTaskList();
    }
}
</script>

<style>


</style>
