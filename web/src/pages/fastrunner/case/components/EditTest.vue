<template>
    <el-container>
        <el-aside style="width: 260px; margin-top: 10px;">
            <div class="nav-api-side">
                <div class="api-tree">
                    <el-input
                        placeholder="输入关键字进行过滤"
                        v-model="filterText"
                        size="medium"
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
            <span class="custom-tree-node" slot-scope="{ node, data }">
              <span>
                <i class="iconfont" v-html="expand"></i>
                &nbsp;&nbsp;{{ node.label }}
              </span>
            </span>
                    </el-tree>
                </div>
            </div>
        </el-aside>

        <el-main>
            <div v-show="!editTestStepActivate" class="recordapi__header">
                <div class="recordapi__header" :style="{flex:1}">
                    <div class="recordapi__header--item">
                        <el-input placeholder="请输入接口名称" style="width: 350px; text-align: center" clearable
                                  @input="inputVal" :value="search" @keyup.enter.native="getAPIList">
                        </el-input>
                    </div>
                    <div class="recordapi__header--item">
                        <el-button
                            type="primary"
                            @click="resetSearch"
                        >重置
                        </el-button>
                    </div>

                    <div class="recordapi__header--item">
                        <el-dropdown @command="tagChangeHandle">
                            <el-button type="primary">
                                状态
                                <i class="el-icon-arrow-down el-icon--right"></i>
                            </el-button>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="1">成功</el-dropdown-item>
                                <el-dropdown-item command="0">未知</el-dropdown-item>
                                <el-dropdown-item command="2">失败</el-dropdown-item>
                                <el-dropdown-item command="">所有</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                    </div>
                    <div class="recordapi__header--item">
                        <el-select v-model="selectUser" placeholder="创建人" filterable
                                   :style="{width: '120px'}">
                            <el-option v-for="(item, index) in users" :key="index"
                                       :label="item.label"
                                       :value="item.value" :disabled="item.disabled"></el-option>
                        </el-select>
                    </div>

                </div>
                <div class="recordapi__header" :style="{flex:1}">
                    <div class="recordapi__header--item">
                        <el-input
                            style="width: 500px; text-align: center"
                            placeholder="请输入测试用例名称"
                            v-model="testName"
                            clearable
                            v-if="testData.length > 0"
                        >
                            <el-select v-model="testTag" slot="prepend" placeholder="请选择" style="width: 105px">

                                <el-option
                                    v-for="value in tagOptions" :key="value"
                                    :label="value"
                                    :value="value"
                                ></el-option>

                            </el-select>
                        </el-input>
                    </div>

                    <el-button
                        slot="append"
                        type="success"
                        @click="handleClickSave"
                        :title="disabledSave ? '不能修改其他人的用例': '保存用例'"
                        :disabled="disabledSave"
                    >Save
                    </el-button>

                    <div class="recordapi__header--item">
                        <el-button
                            type="primary"
                            v-loading="suite_loading"
                            @click="handleClickRun"
                        >Send
                        </el-button>
                    </div>
                </div>
            </div>

            <div v-show="!editTestStepActivate" style="margin-top: 10px; ">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <div
                            v-for="(item,index) in apiData.results"
                            draggable='true'
                            @dragstart="currentAPI = JSON.parse(JSON.stringify(item))"
                            style="cursor: pointer; margin-top: 10px; overflow: auto;"
                            :key="index"

                        >
                            <!--编辑用例时的API列表-->
                            <div class="block edit__block" :class="`block_${item.method.toLowerCase()}`">
                                    <span class="block-method block_method_color"
                                          :class="`block_method_${item.method.toLowerCase()}`">
                                        {{ item.method.toUpperCase() }}
                                    </span>
                                <span class="block-method block_method_color block_method_options"
                                      v-if="item.creator==='yapi'"
                                      :title="'从YAPI导入的接口'">
                                            YAPI
                                    </span>

                                <div class="edit__block--inner">
                                    <span class="block-method block_url">{{ item.url }}</span>
                                    <span class="block-summary-description">{{ item.name }}</span>
                                </div>
                                <div>
                                       <span class="el-icon-s-flag"
                                             v-if="item.cases.length > 0 "
                                             :title="'API已经被用例引用,共计: ' + item.cases.length + '次'">
                                       </span>
                                </div>
                            </div>


                        </div>

                    </el-col>
                    <el-col :span="12" class="el-col">
                        <el-dialog
                            v-if="dialogTableVisible"
                            :visible.sync="dialogTableVisible"
                            width="70%"
                        >
                            <report :summary="summary"></report>
                        </el-dialog>

                        <div style="max-height: 1000px; overflow: auto"
                             @drop='drop($event)'
                             @dragover='allowDrop($event)'
                        >
                            <div class='test-list'>
                                <span
                                    v-if="testData.length ===0"
                                    style="color: red">温馨提示：<br/>选择左侧相应API节点显示可拖拽的API<br/>从左边拖拽API至此区域组成业务用例<br/>
                                    上下拖动此区域接口调整接口调用顺序
                                </span>
                                <div
                                    v-if="isConfigExist"
                                    class="block block_test"
                                    @mousemove="currentTest = -1"
                                >
                                    <span
                                        class="block-method block_method_config block_method_color">{{
                                            testData[0].body.method
                                        }}</span>
                                    <input class="block-test-name" v-model="testData[0].body.name" disabled/>

                                    <el-button
                                        style="position: absolute; right: 12px; top: 8px"
                                        v-show="currentTest === -1"
                                        type="danger"
                                        icon="el-icon-delete"
                                        title="删除"
                                        circle size="mini"
                                        @click="testData.splice(index, 1)"
                                    >
                                    </el-button>
                                </div>
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
                                        v-if="test.body.method !== 'config'"
                                    >
                                        <span
                                            class="block-method block_method_test block_method_color">Step_{{index}}</span>
                                        <input class="block-test-name"
                                               v-model="test.body.name"
                                        />


                                        <el-button
                                            style="position: absolute; right: 156px; top: 8px"
                                            v-show="currentTest === index"
                                            type="info"
                                            icon="el-icon-edit"
                                            title="编辑"
                                            circle size="mini"
                                            @click="editTestStepActivate = true"
                                        >
                                        </el-button>

                                        <el-button
                                            style="position: absolute; right: 84px; top: 8px"
                                            v-show="currentTest === index"
                                            type="success"
                                            icon="el-icon-caret-right"
                                            circle size="mini"
                                            title="单个运行"
                                            @click="handleSingleRun()"
                                        >
                                        </el-button>

                                        <el-button
                                            style="position: absolute; right: 48px; top: 8px"
                                            v-show="currentTest === index"
                                            type="primary"
                                            icon="el-icon-caret-right"
                                            circle size="mini"
                                            title="运行开始到当前位置的所有api"
                                            @click="handlePartialRun(index)"
                                        >
                                        </el-button>


                                        <el-button
                                            style="position: absolute; right: 120px; top: 8px"
                                            v-show="currentTest === index"
                                            type="danger"
                                            icon="el-icon-document-copy"
                                            title="复制当前步骤"
                                            circle size="mini"
                                            @click="handleCopyStep(index)"
                                        >
                                        </el-button>

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
                <div class="recordapi__header--item">
                    <el-pagination
                        :page-size="11"
                        v-show="apiData.count !== 0"
                        background
                        @current-change="handlePageChange"
                        :current-page.sync="currentPage"
                        layout="total, prev, pager, next, jumper"
                        :total="apiData.count"
                        style="margin-top: 5px"
                    >
                    </el-pagination>
                </div>
            </div>

            <http-runner
                :host="host"
                v-if="editTestStepActivate"
                :response="testData[currentTest]"
                :config="config"
                v-on:escEdit="editTestStepActivate = false"
                v-on:getNewBody="handleNewBody"
                :disabledSave="disabledSave"
            >
            </http-runner>
        </el-main>

    </el-container>


</template>

<script>
import draggable from 'vuedraggable'
import HttpRunner from './TestBody'
import Report from '../../../reports/DebugReport'

export default {
    components: {
        draggable,
        HttpRunner,
        Report
    },
    computed: {
        isConfigExist: {
            get() {
                if (this.testData.length > 0 && this.testData[0].body.method === "config" && this.testData[0].body.name !== '请选择') {
                    return true;
                }
                return false;
            }
        }
    },
    props: {
        host: {
            require: true
        },
        config: {
            require: true
        },
        project: {
            require: true
        },
        node: {
            require: true
        },
        testStepResp: {
            require: false
        },
        back: Boolean,
        rigEnv: [String, Number],
        tag: [String, Number],
        search: [String, Number],
        addTestActivate: {
            require: true,
            type: Boolean
        }
    },

    name: "EditTest",
    watch: {
        config() {

            const temp = {body: {name: this.config, method: 'config'}};
            if ((this.testData.length === 0 || this.testData[0].body.method !== 'config') && this.config !== '请选择') {
                this.testData.splice(0, 0, temp)
            } else {
                if (this.config !== '请选择') {
                    this.testData.splice(0, 1, temp)
                }

            }

        },
        back() {
            if (this.back) {
                this.testId = ""
                this.testName = ""
                this.testData = []
            }
            this.editTestStepActivate = false;
        },

        filterText(val) {
            this.$refs.tree2.filter(val);
        },

        testStepResp() {
            this.handleSavePermission()
            try {
                this.testName = this.testStepResp.case.name;
                this.testId = this.testStepResp.case.id;
                this.testTag = this.testStepResp.case.tag;
                this.relation = this.testStepResp.case.relation;
                this.testData = JSON.parse(JSON.stringify(this.testStepResp.step))
            } catch (e) {
                this.testName = '';
                this.testId = '';
                this.testTag = '集成用例';
                this.testData = JSON.parse(JSON.stringify(this.testStepResp))
            }
        },

        search() {
            this.getAPIList()
        },
        selectUser() {
            this.getAPIList()
        },
    },

    data() {
        return {
            tagOptions: {
                1: '冒烟用例',
                2: '集成用例',
                3: '监控脚本',
                4: '核心用例',
            },
            isSuperuser: this.$store.state.is_superuser,
            userName: this.$store.state.user,
            disabledSave: true,
            suite_loading: false,
            loading: false,
            dialogTableVisible: false,
            editTestStepActivate: false,
            currentPage: 1,
            length: 0,
            testId: '',
            testName: '',
            relation: '',
            testTag: '集成用例',
            currentTest: '',
            currentNode: '',
            currentAPI: '',
            data: '',
            filterText: '',
            expand: '&#xe65f;',
            dataTree: [],
            summary: {},
            apiData: {
                count: 0,
                results: []
            },

            testData: [],
            selectUser: this.$store.state.user,
            users: [],
            // rigEnv: ''
        }
    },
    methods: {
        handleSavePermission() {
            // 新增用例，所有人都能保存
            if (this.addTestActivate === false) {
                this.disabledSave = false
            }
            // 用例创建人和超级管理员可以编辑并保存用例
            // 其他人只能打开用例，无法保存
            if (this.isSuperuser || this.testStepResp.case.creator === this.userName) {
                this.disabledSave = false
            } else {
                this.disabledSave = true
            }
        },
        inputVal(val) {
            this.$emit('update:search', val)
        },

        handleNewBody(body, newBody) {
            this.editTestStepActivate = false;
            const step = this.testData[this.currentTest].case;
            const id = this.testData[this.currentTest].id;
            this.testData[this.currentTest] = {
                body: body,
                newBody: newBody,
                case: step,
                id: id
            };
            // 编辑用例步骤时，也调用接口保存
            this.handleClickSave(false)
        },
        rigEnvChangeHandle(command) {
            this.$emit('update:rigEnv', command);
            this.getAPIList();
        },
        validateData() {
            if (this.testName === '' || this.testName.length > 100) {
                this.$notify.warning({
                    title: '提示',
                    duration: this.$store.state.duration,
                    message: '用例集名称必填，不能超过100个字符'
                });
                return false
            }

            if (this.testData.length === 0) {
                this.$notify.warning({
                    title: '提示',
                    duration: this.$store.state.duration,
                    message: '测试用例集至少包含一个接口'
                });
                return false
            }

            if (this.testData[0].body.method === "config" && this.testData.length === 1) {
                this.$notify.warning({
                    title: '提示',
                    duration: this.$store.state.duration,
                    message: '测试用例集至少包含一个接口'
                });
                return false
            }

            if (this.testData[0].body.name === "请选择" || this.testData[0].body.method !== "config") {
                this.$notify.warning({
                    title: '提示',
                    duration: this.$store.state.duration,
                    message: '测试用例必须包含配置'
                });
                return false
            }

            return true;
        },

        addTestSuite(addTestFinish) {
            var length = this.testData.length;

            if (this.testData[0].body.method === "config") {
                length -= 1;
            }

            this.$api.addTestCase({
                length: length,
                project: this.project,
                relation: this.node,
                name: this.testName,
                body: this.testData,
                tag: this.testTag
            }).then(resp => {
                if (resp.success) {
                    this.testId = resp.test_id
                    if (addTestFinish) {
                        this.$emit("addSuccess");
                    }
                    this.$notify({
                        message: resp.msg,
                        type: 'success',
                        duration: this.$store.state.duration
                    })
                } else {
                    this.$notify({
                        message: resp.msg,
                        type: 'error',
                        duration: this.$store.state.duration
                    });
                }
            })
        },

        updateTestSuite(addTestFinish, refresh=false) {
            var length = this.testData.length;
            if (this.testData[0].body.method === "config") {
                length -= 1;
            }
            this.$api.updateTestCase(this.testId, {
                length: length,
                name: this.testName,
                tag: this.testTag,
                body: this.testData,
                project: this.project,
                relation: this.relation
            }).then(resp => {
                // 刷新用例步骤
                // 注意需要等到用例已经更新完成后
                if(refresh){
                    this.refreshStep()
                }
                if (resp.success) {
                    if (addTestFinish) {
                        this.$emit("addSuccess")
                    }
                    this.$notify({
                        message: resp.msg,
                        type: 'success',
                        duration: this.$store.state.duration
                    })
                } else {
                    this.$notify({
                        message: resp.msg,
                        type: 'error',
                        duration: this.$store.state.duration
                    });
                }
            })
        },

        handleClickSave(addTestFinish = true) {
            if (this.validateData()) {
                if (this.testId === '') {
                    this.addTestSuite(addTestFinish);
                } else {
                    this.updateTestSuite(addTestFinish);
                }
            }
        },
        // 全部运行
        handleClickRun() {
            if (this.validateData()) {
                this.suite_loading = true;
                this.$api.runSingleTestSuite({
                    host: this.host,
                    name: this.testName,
                    body: this.testData,
                    project: this.project
                }).then(resp => {
                    this.suite_loading = false;
                    this.summary = resp;
                    this.dialogTableVisible = true;
                }).catch(resp => {
                    this.suite_loading = false;
                })
            }
        },
        handlePartialRun(index) {
            if (this.validateData()) {
                this.suite_loading = true;
                this.$api.runSingleTestSuite({
                    host: this.host,
                    name: this.testName,
                    body: this.testData.slice(0, index + 1),
                    project: this.project
                }).then(resp => {
                    this.suite_loading = false;
                    this.summary = resp;
                    this.dialogTableVisible = true;
                }).catch(resp => {
                    this.suite_loading = false;
                })
            }

        },
        // 单个运行
        handleSingleRun() {
            this.loading = true;
            var config = null;
            if (this.testData.length > 0 && this.testData[0].body.method === "config") {
                config = this.testData[0].body;
            }
            this.$api.runSingleTest({
                host: this.host,
                config: config,
                body: this.testData[this.currentTest],
                project: this.project
            }).then(resp => {
                this.loading = false;
                this.summary = resp;
                this.dialogTableVisible = true;
            }).catch(resp => {
                this.loading = false;
            })
        },

        handlePageChange(val) {
            this.$api.getPaginationBypage({
                params: {
                    page: this.currentPage,
                    node: this.currentNode,
                    project: this.project,
                    tag: this.tag,
                    rigEnv: this.rigEnv,
                    search: this.search
                }
            }).then(res => {
                this.apiData = res;
            })
        },

        //  接口状态搜索
        tagChangeHandle(command) {
            // this.tag = command
            this.$emit('update:tag', command);
            this.$nextTick(() => {
                this.$api.apiList({
                    params: {
                        node: this.currentNode,
                        project: this.project,
                        tag: this.tag,
                        rigEnv: this.rigEnv,
                        search: this.search
                    }
                }).then(res => {
                    this.apiData = res;
                })
            })
        },
        resetSearch() {
            this.selectUser = this.$store.state.user,
            this.currentNode = '',
            this.$emit('update:search', '');
            this.$emit('update:tag', '');
            this.$emit('update:rigEnv', '');
            this.getAPIList();
        },
        getAPIList() {
            this.$nextTick(() => {
                this.$api.apiList({
                    params: {
                        node: this.currentNode,
                        project: this.project,
                        search: this.search,
                        rigEnv: this.rigEnv,
                        tag: this.tag,
                        creator: this.selectUser
                    }
                }).then(res => {
                    this.apiData = res;
                })
            })
        },

        getTree() {
            this.$api.getTree(this.$route.params.id, {
                params: {
                    type: 1
                }
            }).then(resp => {
                this.dataTree = resp['tree'];
            })
        },

        handleNodeClick(node, data) {
            this.currentNode = node.id;
            this.data = data;
            this.getAPIList();

        },

        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },

        dragEnd(event) {
            if (this.testData.length > this.length) {
                this.testData.splice(this.length, 1)
            }
        },

        drop(event) {
            event.preventDefault();
            // 创建用例时,默认加上config
            if (this.testData.length === 0) {
                this.testData.push({body: {name: this.config, method: 'config'}})
            }
            if (this.currentAPI) {
                this.testData.push(this.currentAPI)
                this.currentAPI = ''
            }
        },
        allowDrop(event) {
            event.preventDefault();
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

        refreshStep(){
            this.$api.editTest(this.testId).then(resp => {
                this.testData = JSON.parse(JSON.stringify(resp.step))
            })
        },
        handleCopyStep(index) {
            let copyStepObj = JSON.parse(JSON.stringify(this.testData[index]))
            copyStepObj.is_copy = true
            this.testData.splice(index+1,0, copyStepObj)
            this.updateTestSuite(false, true)
        }
    },
    mounted() {
        this.getTree();
        this.getAPIList();
        this.getUserList()
    }
}
</script>

<style scoped>

.el-col {
    min-height: 1px;
}
.test-list {
    height: 750px;
}

.block_test {
    margin-top: 10px;
    border: 1px solid #49cc90;
    background-color: rgba(236, 248, 238, .4)
}

.block_method_test {
    background-color: darkcyan;
}

.block_method_config {
    background-color: red;
}

.block-test-name {
    /*修改用例中API名字显示不全*/
    width: 450px;
    /*超过宽度自动变成...*/
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;

    padding-left: 10px;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    font-family: Open Sans, sans-serif;
    color: #3b4151;
    border: none;
    outline: none;
    background: rgba(236, 248, 238, .4)

}

.recordapi__header {
    display: flex;
    align-items: center;
}

.recordapi__header--item.is-strench {
    flex: 1;
}

.recordapi__header--item {
    margin: 0 2px;
}

.edit__block {
    height: auto;
    padding: 0 5px;
    line-height: 1;
}

.edit__block--inner {
    padding: 10px 0 10px 15px;
}

.edit__block--inner .block-method {
    padding: 0;
    text-align: left;
    margin-bottom: 4px;
}
</style>
