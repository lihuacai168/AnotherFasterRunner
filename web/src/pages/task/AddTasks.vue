<template>
    <el-container>
        <template v-if="!next">
            <el-main style="padding-top: 0">
                <div style="margin-top: 10px;">
                    <el-col :span="12">
                        <el-form
                            :model="ruleForm"
                            :rules="rules"
                            ref="ruleForm"
                            label-width="100px"
                        >
                            <el-form-item label="任务名称" prop="name">
                                <el-input v-model="ruleForm.name" placeholder="请输入任务名称" clearable=""></el-input>
                            </el-form-item>

                            <el-form-item label="时间配置" prop="crontab">
                                <el-input clearable v-model="ruleForm.crontab"
                                          placeholder="请输入cortab表达式，例如 2 12 * * *"></el-input>
                            </el-form-item>

                            <el-form-item label="运行配置" prop="config">
                                <el-select
                                    placeholder="请选择"
                                    size="small"
                                    tyle="margin-left: -6px"
                                    v-model="ruleForm.config"
                                    value-key="id"
                                >
                                    <el-option
                                        v-for="item in configOptions"
                                        :key="item.id"
                                        :label="item.name"
                                        :value="item.name">
                                    </el-option>
                                </el-select>
                                <el-tooltip placement="top">
                                    <div slot="content">指定任务运行的配置<br/>请选择: 使用用例中的配置 <br/>选择其他配置: 当前选择配置覆盖用例中的配置</div>
                                    <span class="el-icon-question"></span>
                                </el-tooltip>

                            </el-form-item>

                            <el-form-item label="CI环境" prop="ci_env">
                                <el-select
                                    placeholder="请选择"
                                    size="small"
                                    tyle="margin-left: -6px"
                                    v-model="ruleForm.ci_env"
                                    value-key="id"
                                >
                                    <el-option
                                        v-for="item in CIEnvOptions"
                                        :key="item"
                                        :label="item"
                                        :value="item">
                                    </el-option>
                                </el-select>
                                <el-tooltip placement="top">
                                    <div slot="content">CI触发环境<br/>Gitlab项目id且CI环境相等时，才会运行任务</div>
                                    <span class="el-icon-question"></span>
                                </el-tooltip>

                            </el-form-item>

                            <el-form-item label="Gitlab项目id" prop="ci_project_ids">
                                <el-input clearable v-model="ruleForm.ci_project_ids"
                                          placeholder="请输入Gitlab项目id,多个用逗号分隔，例如: 1,2"></el-input>

                            </el-form-item>

                            <el-form-item label="任务状态" prop="switch">
                                <el-switch v-model="ruleForm.switch"></el-switch>
                            </el-form-item>

                            <el-form-item label="运行模式" prop="is_parallel">
                                <template>
                                    <el-radio v-model="ruleForm.is_parallel" :label=false>串行</el-radio>
                                    <el-radio v-model="ruleForm.is_parallel" :label=true>并行</el-radio>
                                    <el-tooltip placement="top">
                                        <div slot="content">用例运行模式<br/>任务中的用例默认是一个接着一个运行；并行时，同时执行用例, 不分先后</div>
                                        <span class="el-icon-question"></span>
                                    </el-tooltip>

                                </template>
                            </el-form-item>

                            <el-form-item label="通知策略" prop="strategy">
                                <el-radio-group v-model="ruleForm.strategy">
                                    <el-radio label="始终发送"></el-radio>
                                    <el-radio label="仅失败发送"></el-radio>
                                    <el-radio label="从不发送"></el-radio>
                                </el-radio-group>
                            </el-form-item>

                            <!--                            <el-form-item label="邮件接收人列表" prop="receiver">-->
                            <!--                                <el-input type="textarea" v-model="ruleForm.receiver"-->
                            <!--                                          placeholder="多个接收人以;分隔" clearable></el-input>-->
                            <!--                            </el-form-item>-->
                            <!---->
                            <!--                            <el-form-item label="邮件抄送人列表" prop="mail_cc">-->
                            <!--                                <el-input type="textarea" v-model="ruleForm.mail_cc"-->
                            <!--                                          placeholder="多个抄送人以;分隔" clearable></el-input>-->
                            <!--                            </el-form-item>-->

                            <el-form-item label="webhook" prop="webhook">
                                <el-input type="textarea" v-model="ruleForm.webhook"
                                          :autosize="{ minRows: 1, maxRows: 3}"
                                          placeholder="飞书机器人webhook地址，多个时换行即可" clearable></el-input>
                            </el-form-item>

                            <el-form-item>
                                <el-button type="primary" @click="submitForm('ruleForm')">下一步</el-button>
                                <el-button @click="resetForm('ruleForm')">重置</el-button>
                            </el-form-item>
                        </el-form>

                    </el-col>

                </div>
            </el-main>
        </template>

        <template v-if="next">
            <el-aside style="margin-top: 10px;">
                <div class="nav-api-side">
                    <div class="api-tree">
                        <el-input
                            placeholder="输入关键字进行过滤"
                            v-model="filterText"
                            size="small"
                            clearable
                            prefix-icon="el-icon-search"
                        >
                        </el-input>

                        <el-tree
                            @node-click="handleNodeClick"
                            :data="dataTree"
                            node-key="id"
                            :default-expand-all="false"
                            :expand-on-click-node="false"
                            highlight-current
                            :filter-node-method="filterNode"
                            ref="tree2"
                        >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                        </el-tree>
                    </div>

                </div>

            </el-aside>
            <el-main style="padding-top: 0px">
                <div>
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-pagination
                                :page-size="11"
                                v-show="suiteData.count !== 0"
                                background
                                @current-change="handlePageChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="suiteData.count"
                                style="text-align: center"
                            >
                            </el-pagination>
                        </el-col>
                        <el-col :span="12">
                            <el-button type="primary" v-if="testData.length > 0" @click="saveTask">保存</el-button>
                            <el-button v-if="testData.length > 0" @click="next=false">上一步</el-button>
                        </el-col>


                    </el-row>
                </div>

                <div>
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <div
                                v-for="(item,index) in suiteData.results"
                                draggable='true'
                                @dragstart="currentSuite = JSON.parse(JSON.stringify(item))"
                                style="cursor: pointer; margin-top: 10px; overflow: auto"
                                :key="index"

                            >
                                <div class="block block_options">
                                    <span class="block-method block_method_options block_method_color">Case</span>
                                    <span class="block_name">{{ item.name }}</span>
                                    <i class="el-icon-success " style="color: green" v-if="item.tasks.length > 0 "
                                       :title="'已加入定时任务: ' + item.tasks.map(task => task.name).join('，')">
                                    </i>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="12">

                            <div style="max-height: 1000px; overflow: auto"
                                 @drop='drop($event)'
                                 @dragover='allowDrop($event)'
                            >
                                <span
                                    v-if="testData.length ===0"
                                    style="color: red">温馨提示：<br/>选择左侧相应用例节点显示可拖拽的用例<br/>从左边拖拽用例至此区域组成任务列表<br/>
                                    上下拖动此区域任务调整监控调用顺序
                                </span>
                                <div class='test-list'>
                                    <draggable
                                        v-model="testData"
                                        @end="dragEnd"
                                        @start="length = testData.length"
                                        :options="{animation:200}"
                                    >
                                        <div
                                            v-for="(test, index) in testData"
                                            :key="index"
                                            class="block block_test"
                                            @mousemove="currentTest = index"
                                        >
                                            <!--编辑用例列表-->
                                            <span
                                                class="block-method block_method_test block_method_color">Task</span>
                                            <span class="block-test-name">{{ test.name }}</span>
                                            <!--<el-button-->
                                            <!--style="position: absolute; right: 48px; top: 8px"-->
                                            <!--v-show="currentTest === index"-->
                                            <!--type="info"-->
                                            <!--icon="el-icon-edit"-->
                                            <!--circle size="mini"-->
                                            <!--@click="handleEditTestCase"-->
                                            <!--title="编辑"-->
                                            <!--&gt;-->
                                            <!--</el-button>-->
                                            <el-button
                                                style="position: absolute; right: 12px; top: 8px"
                                                v-show="currentTest === index"
                                                type="danger"
                                                icon="el-icon-delete"
                                                title="删除"
                                                circle size="mini"
                                                @click="testData.splice(index, 1)"
                                            >
                                            </el-button>
                                        </div>
                                    </draggable>
                                </div>

                            </div>
                        </el-col>
                    </el-row>
                </div>
            </el-main>
        </template>
    </el-container>


</template>

<script>
import draggable from 'vuedraggable'
import {isNumArray} from '../../validator'

export default {

    name: "AddTasks",
    props: {
        ruleForm: {
            require: true
        },
        args: {
            require: true
        },
        scheduleId: {
            require: true
        },
        configOptions: {
            require: true,
            type: Array
        },
        CIEnvOptions: {
            require: true,
            type: Array
        }
    },
    watch: {
        filterText(val) {
            this.$refs.tree2.filter(val);
        },
    },
    components: {
        draggable
    },


    data() {
        return {
            currentTest: '',
            length: 0,
            testData: [],
            currentSuite: '',
            search: '',
            next: false,
            node: '',
            currentPage: 1,
            filterText: '',
            expand: '&#xe65f;',
            dataTree: [],
            suiteData: {
                count: 0,
                results: []
            },
            rules: {
                name: [
                    {required: true, message: '请输入任务名称', trigger: 'blur'},
                    {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                ],
                crontab: [
                    {required: true, message: '请输入正确的crontab表达式', trigger: 'blur'}
                ],
                ci_project_ids: [
                    {required: false, message: '请输入正确的ci_project_ids', trigger: 'blur'},
                    {validator: isNumArray, trigger: 'blur'}
                ]

            },
            editTestCaseActivate: false,
        }
    },
    methods: {
        handleNewTestCase(kwargsForm) {
            this.editTestCaseActivate = false;
            this.next = true;
            this.testData[this.currentTest]["kwargs"] = kwargsForm;
        },

        saveTask() {
            var task = [];
            for (let value of this.testData) {
                task.push(value.id);
            }
            var form = this.ruleForm;
            form["data"] = task;
            form["project"] = this.$route.params.id;
            if (this.scheduleId === '') {
                this.$api.addTask(form).then(resp => {
                    if (resp.success) {
                        this.$notify.success(resp.msg)
                        this.$emit("changeStatus", false);
                    } else {
                        this.$notify.error(resp.msg)
                    }
                })
            } else {
                this.$api.updateTask(this.scheduleId, {project: this.$route.params.id}, form).then(resp => {
                    if (resp.success) {
                        this.$emit("changeStatus", false);
                        this.$notify.success('更新定时任务成功');
                    } else {
                        this.$notify.error(resp.msg)
                    }
                })
            }
        },

        dragEnd(event) {
            if (this.testData.length > this.length) {
                this.testData.splice(this.length, 1)
            }
        },
        drop(event) {
            event.preventDefault();
            this.testData.push(this.currentSuite);
        },
        allowDrop(event) {
            event.preventDefault();
        },
        handlePageChange(val) {
            this.$api.getTestPaginationBypage({
                params: {
                    page: this.currentPage,
                    node: this.node,
                    project: this.$route.params.id,
                    search: ''
                }
            }).then(res => {
                this.suiteData = res;
            })
        },
        handleCurrentChange(val) {
            this.$api.getTestPaginationBypage({
                params: {
                    page: this.currentPage,
                    project: this.$route.params.id,
                    node: this.node,
                    search: this.search
                }
            }).then(resp => {
                this.suiteData = resp;
            })
        },
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.next = true;
                } else {
                    return false;
                }
            });
            this.testData = this.args
            // 用map遍历args的所有caseId,如果和用例集中的id相等,就返回该用例的全部信息
            // 用map,filter过滤,case的数据在第二页时,会导致name=undefined
            // this.testData = this.args.map(caseId=> this.suiteData.results.filter(testCase=> testCase.id === caseId)[0]);
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },
        getTree() {
            this.$api.getTree(this.$route.params.id, {params: {type: 2}}).then(resp => {
                this.dataTree = resp.tree;
            })
        },

        handleNodeClick(node) {
            this.node = node.id;
            this.getTestList();

        },
        getTestList() {
            this.$api.testList({
                params: {
                    project: this.$route.params.id,
                    node: this.node,
                    search: this.search,
                    caseNameOrUrl: ""
                }
            }).then(resp => {
                this.suiteData = resp;
            })
        },

    },
    mounted() {
        this.getTree();
        this.getTestList();
    }
}
</script>

<style scoped>

.test-list {
    height: 750px;
}

.block_test {
    margin-top: 10px;
    border: 1px solid #49cc90;
    background-color: rgba(236, 248, 238, .4)
}

.block_method_test {
    background-color: #304056;
}

.block-test-name {
    width: 700px;
    padding-left: 10px;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    font-family: Open Sans, sans-serif;
    color: #3b4151;
    border: none;
    outline: none;
    background: rgba(236, 248, 238, .4)

}


</style>
