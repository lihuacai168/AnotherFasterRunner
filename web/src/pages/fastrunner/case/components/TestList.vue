<template>
    <el-container>
        <el-header style="padding-top: 10px; height: 50px;">
            <div style="display: flex; align-items: center">
                    <div v-if="testData.count >= 0">
                        <el-input
                            placeholder="请输入用例名称"
                            size="medium"
                            clearable
                            v-model="search"
                            @keyup.enter.native="getTestList"
                            class="input-with-select"
                        >
                            <el-button
                                slot="append"
                                icon="el-icon-search"
                                @click="getTestList"
                            ></el-button>

                            <el-select
                                v-model="searchType"
                                slot="prepend"
                                placeholder="用例"
                                @change="searchTypeChangeHandle"
                            >
                                <el-option label="用例" value="1"></el-option>
                                <el-option label="API" value="2"></el-option>
                            </el-select>
                        </el-input>
                    </div>

                    <div style="margin: 0 5px;">
                        <el-dropdown @command="caseTypeChangeHandle">
                            <el-button size="small" type="primary">类型
                                <i class="el-icon-arrow-down el-icon--right"></i>
                            </el-button>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="1">冒烟用例</el-dropdown-item>
                                <el-dropdown-item command="2">集成用例</el-dropdown-item>
                                <el-dropdown-item command="3">监控脚本</el-dropdown-item>
                                <el-dropdown-item command="4">核心用例</el-dropdown-item>
                                <el-dropdown-item command="">所有</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                    </div>
                    <div>
                        <el-button
                            type="primary"
                            size="small"
                            @click="resetSearch"
                            >重置
                        </el-button>
                    </div>
                <div style="margin: 0 5px;">
                    <el-dropdown @command="dropdownMenuChangeHandle">
<!--                        <span><i class="el-icon-more"></i></span>-->
                        <el-button type="info" size="small">操作
                            <i class="el-icon-more el-icon--right"></i>
                        </el-button>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item disabled style="background-color: #e2e2e2">
                                {{ selectTest.length }} 条更新为
                            </el-dropdown-item>
                            <el-dropdown-item :disabled="selectTest.length === 0" command="core">核心用例
                            </el-dropdown-item>
                            <el-dropdown-item :disabled="selectTest.length === 0" command="integrated">集成用例
                            </el-dropdown-item>
                            <el-dropdown-item :disabled="selectTest.length === 0" command="smoke">冒烟用例
                            </el-dropdown-item>
                            <el-dropdown-item :disabled="selectTest.length === 0" command="monitor">监控脚本
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                    <div style="margin: 0 5px;">
                        <el-pagination
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            :page-size="11"
                            v-show="testData.count !== 0"
                            background
                            layout="total, prev, pager, next, jumper"
                            :total="testData.count"
                        >
                        </el-pagination>
                    </div>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px; margin-bottom: 10px">
                <div style="position: fixed; bottom: 0; right:0; left: 255px; top: 160px">
                    <el-dialog
                        v-if="dialogTableVisible"
                        title="Test Result"
                        :visible.sync="dialogTableVisible"
                        width="70%"
                        :modal-append-to-body="false"
                    >
                        <report :summary="summary"></report>
                    </el-dialog>

                    <el-dialog
                        title="Run Case"
                        :visible.sync="dialogTreeVisible"
                        width="45%"
                        :modal-append-to-body="false"
                        @close="onCloseRunCase"
                        @open="onOpenRunCase"
                    >
                        <div>
                            <div>
                                <el-row :gutter="20">
                                    <el-col :span="10"><span>配置: </span></el-col>
                                    <el-col :span="10">
                                        <el-select
                                            placeholder="请选择"
                                            size="small"
                                            v-model="currentConfigId"
                                            style="width: 200px;"
                                        >
                                            <el-option
                                                v-for="item in configOptions"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id"
                                            >
                                            </el-option>
                                        </el-select>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="20" style="margin-top: 10px">
                                    <el-col :span="10">
                                        <el-switch
                                            v-model="asyncs"
                                            active-color="#13ce66"
                                            inactive-color="#ff4949"
                                            active-text="异步执行"
                                            inactive-text="同步执行"
                                        >
                                        </el-switch>
                                    </el-col>
                                    <el-col :span="10">
                                        <el-input
                                            v-show="asyncs"
                                            size="small"
                                            clearable
                                            placeholder="请输入报告名称"
                                            v-model="reportName"
                                            :disabled="false"
                                        >
                                        </el-input>
                                    </el-col>
                                </el-row>
                            </div>
                            <div style="margin-top: 20px;">
                                <el-input
                                    placeholder="输入关键字进行过滤"
                                    v-model="filterText"
                                    size="small"
                                    clearable
                                    prefix-icon="el-icon-search"
                                >
                                </el-input>

                                <el-tree
                                    :filter-node-method="filterNode"
                                    :data="dataTree"
                                    show-checkbox
                                    node-key="id"
                                    :expand-on-click-node="false"
                                    check-on-click-node
                                    :check-strictly="true"
                                    :highlight-current="true"
                                    ref="tree"
                                >
                                    <span class="custom-tree-node" slot-scope="{ node, data }">
                                        <span><i class="iconfont" v-html="expand"></i>
                                            &nbsp;&nbsp;{{ node.label }}</span>
                                    </span>
                                </el-tree>
                            </div>
                        </div>
                        <span slot="footer" class="dialog-footer">
                            <el-button @click="dialogTreeVisible = false">取 消</el-button>
                            <el-button type="primary" @click="runTree">确 定</el-button>
                        </span>
                    </el-dialog>
                    <el-dialog
                        title="Move Case"
                        :visible.sync="dialogTreeMoveCaseVisible"
                        width="45%"
                        :modal-append-to-body="false"
                    >
                        <div>
                            <div style="margin-top: 20px">
                                <el-input
                                    placeholder="输入关键字进行过滤"
                                    v-model="filterText"
                                    size="small"
                                    clearable
                                    prefix-icon="el-icon-search"
                                >
                                </el-input>

                                <el-tree
                                    :filter-node-method="filterNode"
                                    :data="dataTree"
                                    show-checkbox
                                    node-key="id"
                                    :expand-on-click-node="false"
                                    check-on-click-node
                                    :check-strictly="true"
                                    :highlight-current="true"
                                    ref="tree"
                                >
                                    <span class="custom-tree-node" slot-scope="{ node, data }">
                                        <span><i class="iconfont" v-html="expand"></i>
                                            &nbsp;&nbsp;{{ node.label }}</span>
                                    </span>
                                </el-tree>
                            </div>
                        </div>
                        <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogTreeMoveCaseVisible = false">取 消</el-button>
                    <el-button type="primary" @click="moveCase">确 定</el-button>
                  </span>
                    </el-dialog>
                    <el-table
                        highlight-current-row
                        v-loading="loading"
                        ref="multipleTable"
                        :data="testData.results"
                        :show-header="testData.count !== 0"
                        stripe
                        height="calc(100%)"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        @selection-change="handleSelectionChange"
                    >
                        <el-table-column type="selection" width="45"></el-table-column>
<!--                        <el-table-column width="25">-->
<!--                            <template v-slot="scope">-->
<!--                                <el-dropdown-->
<!--                                    @command="dropdownMenuChangeHandle"-->
<!--                                >-->
<!--                                    <span><i class="el-icon-more"></i></span>-->
<!--                                    <el-dropdown-menu slot="dropdown">-->
<!--                                        <el-dropdown-item disabled style="background-color: #e2e2e2">-->
<!--                                            {{ selectTest.length }} 条更新为-->
<!--                                        </el-dropdown-item>-->

<!--                                        <el-dropdown-item :disabled="selectTest.length === 0" command="core">核心用例-->
<!--                                        </el-dropdown-item>-->
<!--                                        <el-dropdown-item :disabled="selectTest.length === 0" command="integrated">集成用例-->
<!--                                        </el-dropdown-item>-->
<!--                                        <el-dropdown-item :disabled="selectTest.length === 0" command="smoke">-->
<!--                                            冒烟用例-->
<!--                                        </el-dropdown-item>-->
<!--                                        <el-dropdown-item :disabled="selectTest.length === 0" command="monitor">-->
<!--                                            监控脚本-->
<!--                                        </el-dropdown-item>-->
<!--                                    </el-dropdown-menu>-->
<!--                                </el-dropdown>-->
<!--                            </template>-->
<!--                        </el-table-column>-->

                        <el-table-column label="用例名称" min-width="200">
                            <template v-slot="scope">
                                <div>{{ scope.row.name }}
                                    <i class="el-icon-success " style="color: green" v-if="scope.row.tasks.length > 0 "
                                       :title="'已加入定时任务: ' + scope.row.tasks.map(task => task.name).join('，')">
                                    </i>
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column label="步骤" width="50">
                            <template v-slot="scope">
                                <div style="text-align:center">
                                    {{ scope.row.length }}
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column label="用例类型" width="100">
                            <template v-slot="scope">
                                <el-tag v-if="scope.row.tag==='冒烟用例'">{{ scope.row.tag }}</el-tag>
                                <el-tag v-if="scope.row.tag==='集成用例'" type="info">{{ scope.row.tag }}</el-tag>
                                <el-tag v-if="scope.row.tag==='监控脚本'" type="danger">{{ scope.row.tag }}</el-tag>
                                <el-tag v-if="scope.row.tag==='核心用例'" type="success">{{ scope.row.tag }}</el-tag>
                            </template>
                        </el-table-column>

                        <el-table-column label="更新时间" width="105">
                            <template v-slot="scope">
                                <div>{{ scope.row.update_time|datetimeFormat('MM-DD hh:mm') }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column label="创建时间" width="105">
                            <template v-slot="scope">
                                <div>{{ scope.row.create_time|datetimeFormat('MM-DD hh:mm') }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column label="创建人" width="80">
                            <template v-slot="scope">
                                <div>{{ scope.row.creator }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column label="更新人" width="80">
                            <template v-slot="scope">
                                <div>{{ scope.row.updater }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column label="用例操作" width="180">
                            <template v-slot="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        icon="el-icon-edit"
                                        circle size="mini"
                                        style="margin-left: 0"
                                        title="编辑"
                                        @click="handleEditTest(scope.row.id)"
                                    ></el-button>

                                    <el-button
                                        type="primary"
                                        icon="el-icon-caret-right"
                                        circle size="mini"
                                        style="margin-left: 0"
                                        title="同步运行用例"
                                        @click="handleRunTest(scope.row.id, scope.row.name)"
                                    ></el-button>

                                    <el-button
                                        type="primary"
                                        icon="el-icon-video-play"
                                        circle size="mini"
                                        style="margin-left: 0"
                                        title="异步运行用例"
                                        @click="handleAsyncRunTest(scope.row.id, scope.row.name, scope.row.relation)"
                                    ></el-button>

                                    <el-popover style="margin-left: 0" trigger="hover">
                                        <div style="text-align: left">
                                            <el-button
                                                type="success"
                                                icon="el-icon-document-copy"
                                                circle size="mini"
                                                style="margin-left: 0"
                                                title="复制用例"
                                                @click="handleCopyTest(scope.row.id, scope.row.name)"
                                            >
                                            </el-button>

                                            <el-button
                                                type="danger"
                                                icon="el-icon-delete"
                                                :title="userName === scope.row.creator || isSuperuser ? '删除' : '只有用例创建者才能删除'"
                                                :disabled="userName !== scope.row.creator && !isSuperuser"
                                                circle size="mini"
                                                style="margin-left: 0"
                                                @click="handleDelTest(scope.row.id)"
                                            >
                                            </el-button>

                                            <el-button
                                                type="warning"
                                                icon="el-icon-refresh"
                                                :title="userName === scope.row.creator || isSuperuser ? '从API同步用例步骤' : '只有用例创建者才能同步'"
                                                :disabled="userName !== scope.row.creator && !isSuperuser"
                                                circle size="mini"
                                                style="margin-left: 0"
                                                @click="handleSyncCaseStep(scope.row.id)"
                                            >
                                            </el-button>
                                        </div>
                                        <el-button
                                            icon="el-icon-more"
                                            title="更多"
                                            circle
                                            size="mini"
                                            slot="reference"
                                        ></el-button>
                                    </el-popover>
                                </el-row>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import Report from "../../../reports/DebugReport";

export default {
    name: "TestList",
    components: {
        Report
    },

    props: {
        run: Boolean,
        //父组件修改move状态，子组件监听move,调用getTree('move')修改dialogTreeMoveCaseVisible状态，激活移动用例弹窗
        move: Boolean,
        back: Boolean,
        project: {
            require: true
        },
        host: {
            require: true
        },
        node: {
            require: false
        },
        del: Boolean,
        onlyMe: Boolean,
        isSelectCase: Boolean
    },

    watch: {
        filterText(val) {
            this.$refs.tree.filter(val);
        },

        run() {
            this.asyncs = false;
            this.reportName = "";
            this.getTree("run");
        },

        move() {
            this.getTree("move");
        },

        node() {
            this.search = "";
            this.searchType = "1";
            this.getTestList();
        },

        // 监听只看自己按钮的状态
        onlyMe() {
            this.getTestList();
        },

        back() {
            this.getTestList();
        },

        del() {
            if (this.selectTest.length !== 0) {
                this.$confirm("此操作将永久删除测试用例集，是否继续?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning"
                }).then(() => {
                    this.$api
                        .delAllTest({ data: this.selectTest })
                        .then(resp => {
                            this.getTestList();
                        });
                });
            } else {
                this.$notify.warning({
                    title: "提示",
                    message: "请至少选择一个用例集",
                    duration: this.$store.state.duration
                });
            }
        },

        search() {
            this.getTestList();
        }
    },
    data() {
        return {
            isSuperuser: this.$store.state.is_superuser,
            userName: this.$store.state.user,
            search: "",
            reportName: "",
            asyncs: false,
            filterText: "",
            expand: "&#xe65f;",
            dialogTreeVisible: false,
            dataTree: {},
            loading: false,
            dialogTableVisible: false,
            dialogTreeMoveCaseVisible: false,
            selectTest: [],
            summary: {},
            currentRow: "",
            testData: {
                count: 0,
                results: []
            },
            currentPage: 1,
            caseType: "",
            searchType: "1", // 1：用例名称搜索 2：api名称或者api url
            currentConfigId: "",
            configOptions: []
        };
    },

    methods: {
        getTree(showType) {
            this.$api
                .getTree(this.$route.params.id, { params: { type: 2 } })
                .then(resp => {
                    this.dataTree = resp.tree;
                    // run是批量运行case弹窗，其他是批量更新case relation弹窗
                    if (showType === "run") {
                        this.dialogTreeVisible = true;
                    } else {
                        this.dialogTreeMoveCaseVisible = true;
                    }
                });
        },

        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },

        runTree() {
            this.dialogTreeVisible = false;
            const relation = this.$refs.tree.getCheckedKeys();
            if (relation.length === 0) {
                this.$notify.error({
                    title: "提示",
                    message: "请至少选择一个节点",
                    duration: 1500
                });
            } else {
                this.$api
                    .runSuiteTree({
                        host: this.host,
                        project: this.project,
                        relation: relation,
                        async: this.asyncs,
                        name: this.reportName,
                        config_id: this.currentConfigId
                    })
                    .then(resp => {
                        if (resp.hasOwnProperty("status")) {
                            this.$message.info({
                                message: resp.msg,
                                duration: 1500
                            });
                        } else {
                            this.summary = resp;
                            this.dialogTableVisible = true;
                        }
                    });
            }
        },

        moveCase() {
            this.dialogTreeVisible = false;
            const relation = this.$refs.tree.getCheckedKeys();
            let length = relation.length;
            if (length === 0) {
                this.$notify.error({
                    title: "提示",
                    message: "请至少选择一个节点",
                    duration: 1500
                });
            } else if (length !== 1) {
                this.$notify.error({
                    title: "提示",
                    message:
                        "API只能移动到一个节点, 现在选了" + length + "个节点",
                    duration: 1500
                });
            } else {
                this.$api
                    .moveCase({
                        project: this.project,
                        relation: relation[0],
                        case: this.selectTest
                    })
                    .then(resp => {
                        if (resp.success) {
                            this.$message.success({
                                message: "移动Case成功",
                                duration: 1500
                            });
                            this.dialogTreeMoveCaseVisible = false;
                            this.resetSearch();
                        } else {
                            this.$message.error({
                                message: resp.msg,
                                duration: 1500
                            });
                        }
                    });
            }
        },

        // 同步运行单个用例
        handleRunTest(id, name) {
            this.loading = true;
            this.$api
                .runTestByPk(id, {
                    params: {
                        project: this.project,
                        name: name,
                        host: this.host
                    }
                })
                .then(resp => {
                    this.summary = resp;
                    this.dialogTableVisible = true;
                    this.loading = false;
                })
                .catch(resp => {
                    this.loading = false;
                });
        },

        /*
         * 异步运行单个用例
         * @param id, 用例id
         * @param name，用例名称，测试报告使用这个名称
         */
        handleAsyncRunTest(id, name) {
            this.$api
                .runTestByPk(id, {
                    params: {
                        project: this.project,
                        name: name,
                        host: this.host,
                        async: true
                    }
                })
                .then(resp => {
                    if (resp.success) {
                        this.$message.info({
                            title: "提示",
                            message: resp.msg,
                            duration: 2000,
                            center: true
                        });
                    } else {
                        this.$message.error({
                            message: resp.msg,
                            duration: 2000,
                            center: true
                        });
                    }
                });
        },

        handleCurrentChange(val) {
            this.$api
                .getTestPaginationBypage({
                    params: {
                        page: this.currentPage,
                        project: this.project,
                        node: this.node,
                        search: this.search,
                        searchType: this.searchType,
                        caseType: this.caseType,
                        onlyMe: this.onlyMe
                    }
                })
                .then(resp => {
                    this.testData = resp;
                });
        },

        handleEditTest(id) {
            this.$api.editTest(id).then(resp => {
                this.$emit("testStep", resp);
            });
        },

        handleCopyTest(id, name) {
            this.$prompt("请输入用例集名称", "提示", {
                confirmButtonText: "确定",
                inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                inputErrorMessage: "用例集不能为空",
                inputValue: name
            }).then(({ value }) => {
                this.$api
                    .coptTest(id, {
                        name: value,
                        relation: this.node,
                        project: this.project
                    })
                    .then(resp => {
                        if (resp.success) {
                            this.getTestList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    });
            });
        },

        handleSelectionChange(val) {
            this.selectTest = val;
            // 更新是否已经选择Case, 父组件依赖这个属性来判断是否显示移动用例按钮
            if (this.selectTest.length > 0) {
                this.$emit("update:isSelectCase", true);
            } else {
                this.$emit("update:isSelectCase", false);
            }
        },

        handleDelTest(id) {
            this.$confirm("此操作将永久删除该测试用例集，是否继续?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
            }).then(() => {
                this.$api.deleteTest(id).then(resp => {
                    if (resp.success) {
                        this.getTestList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                });
            });
        },
        handleSyncCaseStep(id) {
            this.$confirm("同步测试用例中的用例步骤，是否继续?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
            }).then(() => {
                this.$api.syncTest(id).then(resp => {
                    if (resp.success) {
                        this.$notify.success("同步用例步骤成功");
                        this.getTestList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                });
            });
        },
        resetSearch() {
            (this.searchType = "1"),
                (this.search = ""),
                (this.node = ""),
                (this.caseType = ""),
                (this.currentPage = 1),
                this.$emit("update:onlyMe", true),
                this.getTestList();
        },

        caseTypeChangeHandle(command) {
            this.caseType = command;
            debugger;
            this.getTestList();
        },

        searchTypeChangeHandle(value) {
            this.searchType = value;
            this.getTestList();
        },

        getTestList() {
            this.$api
                .testList({
                    params: {
                        project: this.project,
                        node: this.node,
                        search: this.search,
                        searchType: this.searchType,
                        caseType: this.caseType,
                        onlyMe: this.onlyMe,
                        page: this.currentPage
                    }
                })
                .then(resp => {
                    this.testData = resp;
                });
        },
        cellMouseEnter(row) {
            this.currentRow = row;
        },
        getConfig() {
            this.$api.getAllConfig(this.$route.params.id).then(resp => {
                this.configOptions = resp;
                this.configOptions.push({
                    name: "请选择",
                    id: 0
                });
            });
        },
        cellMouseLeave(row) {
            this.currentRow = "";
        },
        onOpenRunCase() {
            this.getConfig();
        },
        onCloseRunCase() {
            this.currentConfigId = 0;
        },
        /*
        用例批量各类操作
        */
        dropdownMenuChangeHandle(command) {
            const opMap = {
                smoke: 1,
                integrated: 2,
                monitor: 3,
                core: 4
            };
            const tag = opMap[command];
            const case_ids = this.selectTest.map(test => test.id);
            this.$api
                .tagCase({
                    tag: tag,
                    case_ids: case_ids,
                    project_id: this.$route.params.id
                })
                .then(resp => {
                    this.selectTest = [];
                    this.$emit("update:isSelectCase", false);
                    if (resp.success) {
                        this.getTestList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                });
        }
    },
    mounted() {
        this.getTestList();
    }
};
</script>

<style scoped>
.el-select {
    width: 80px;
}
</style>
