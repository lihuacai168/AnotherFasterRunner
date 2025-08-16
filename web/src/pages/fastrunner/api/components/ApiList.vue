<template>
    <el-container>
        <el-header style="padding: 0; height: 50px;">
            <div class="recordapi__header">
                <div class="recordapi__header--item" :style="{paddingLeft: '2px'}">
                    <el-checkbox
                        v-if="apiData.count > 0"
                        v-model="checked"
                        style="padding-top: 14px; padding-left: 2px"
                    >
                    </el-checkbox>
                </div>
                <div class="recordapi__header--item">
                    <el-input placeholder="请输入接口名称" clearable v-model="search" @keyup.enter.native="getAPIList"
                              style="width: 400px">
                        <el-button slot="append" icon="el-icon-search" @click="getAPIList"></el-button>
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
                            <!--                            <el-dropdown-item command="3">自动成功</el-dropdown-item>-->
                            <el-dropdown-item command="">所有</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <!--                            api环境字段暂时不使用-->

                <!--                <div class="recordapi__header&#45;&#45;item is-strench">-->
                <!--                    <el-dropdown @command="rigEnvChangeHandle">-->
                <!--                        <el-button type="primary">-->
                <!--                            环境-->
                <!--                            <i class="el-icon-arrow-down el-icon&#45;&#45;right"></i>-->
                <!--                        </el-button>-->
                <!--                        <el-dropdown-menu slot="dropdown">-->
                <!--                            <el-dropdown-item command="0">测试</el-dropdown-item>-->
                <!--                            <el-dropdown-item command="1">生产</el-dropdown-item>-->
                <!--                            <el-dropdown-item command="">所有</el-dropdown-item>-->
                <!--                        </el-dropdown-menu>-->
                <!--                    </el-dropdown>-->
                <!--                </div>-->

                <div class="recordapi__header--item">
                    <el-pagination
                        style="margin-top: 5px"
                        :page-size="11"
                        v-show="apiData.count !== 0 "
                        background
                        @current-change="handleCurrentChange"
                        :current-page.sync="currentPage"
                        layout="total, prev, pager, next, jumper"
                        :total="apiData.count"
                    >
                    </el-pagination>
                </div>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px;">
                <el-dialog
                    v-if="dialogTableVisible"
                    :visible.sync="dialogTableVisible"
                    width="70%"
                >
                    <report :summary="summary"></report>
                </el-dialog>

                <el-dialog
                    title="Run API"
                    :visible.sync="dialogTreeVisible"
                    width="45%"
                >
                    <div>
                        <div>
                            <el-row :gutter="2">
                                <el-col :span="8">
                                    <el-switch
                                        style="margin-top: 10px"
                                        v-model="asyncs"
                                        active-color="#13ce66"
                                        inactive-color="#ff4949"
                                        active-text="异步执行"
                                        inactive-text="同步执行">
                                    </el-switch>
                                </el-col>
                                <el-col :span="10">
                                    <el-input
                                        v-show="asyncs"
                                        clearable
                                        placeholder="请输入报告名称"
                                        v-model="reportName"
                                        :disabled="false">
                                    </el-input>

                                </el-col>
                            </el-row>
                        </div>
                        <div style="margin-top: 20px">
                            <el-input
                                placeholder="输入节点名称进行过滤"
                                v-model="filterText"
                                size="medium"
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
                            <span class="custom-tree-node"
                                  slot-scope="{ node, _ }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
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
                    title="Move API"
                    :visible.sync="dialogTreeMoveAPIVisible"
                    width="45%"
                >
                    <div>
                        <div style="margin-top: 20px">
                            <el-input
                                placeholder="输入节点名称进行过滤"
                                v-model="filterText"
                                size="medium"
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
                            <span class="custom-tree-node"
                                  slot-scope="{ node, _ }"
                            >
                                <span><i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}</span>
                            </span>
                            </el-tree>
                        </div>

                    </div>
                    <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogTreeMoveAPIVisible = false">取 消</el-button>
                    <el-button type="primary" @click="moveAPI">确 定</el-button>
                  </span>
                </el-dialog>

                <el-dialog
                    title="关联用例"
                    :visible.sync="dialogRelatedCasesVisible"
                    width="50%"
                >
                    <div v-if="relatedCases.length > 0">
                        <el-table :data="relatedCases" style="width: 100%">
                            <el-table-column label="序号" width="80" type="index" :index="1">
                            </el-table-column>
                            <el-table-column prop="name" label="用例名称">
                            </el-table-column>
                        </el-table>
                    </div>
                    <div v-else>
                        <el-empty description="暂无关联用例"></el-empty>
                    </div>
                    <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogRelatedCasesVisible = false">关 闭</el-button>
                    </span>
                </el-dialog>


                <div style="position: fixed; bottom: 0; right:0; left: 460px; top: 160px">
                    <el-table
                        highlight-current-row
                        height="calc(100%)"
                        ref="multipleTable"
                        :data="apiData.results"
                        :show-header="false"
                        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        style="width: 100%;"
                        @selection-change="handleSelectionChange"
                        v-loading="loading"
                    >
                        <el-table-column
                            type="selection"
                            width="42"
                        >
                        </el-table-column>
                        <el-table-column
                            width="25"
                        >
                            <template slot-scope="_">
                                <el-dropdown @command="dropdownMenuChangeHandle">
                                    <span><i class="el-icon-more"></i></span>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item disabled style="background-color: #e2e2e2">选中({{ selectAPI.length }} 条)</el-dropdown-item>
                                        <el-dropdown-item :disabled="selectAPI.length === 0" command="success">更新为成功</el-dropdown-item>
                                        <el-dropdown-item :disabled="selectAPI.length === 0" command="fail">更新为失败</el-dropdown-item>
                                        <el-dropdown-item :disabled="selectAPI.length === 0" command="deprecated">更新为废弃</el-dropdown-item>
                                        <el-dropdown-item :disabled="selectAPI.length === 0" command="move">移动API</el-dropdown-item>
                                    </el-dropdown-menu>
                                </el-dropdown>
                            </template>

                        </el-table-column>

                        <el-table-column
                            min-width="325"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <div class="block" :class="`block_${scope.row.method.toLowerCase()}`">
                                    <span class="block-method block_method_color"
                                          :class="`block_method_${scope.row.method.toLowerCase()}`">
                                        {{ scope.row.method.toUpperCase() }}
                                    </span>
                                    <span class="block-method block_method_color block_method_group"
                                          :title="'API分组：' + scope.row.relation_name">
                                        {{ scope.row.relation_name }}
                                    </span>
                                    <div class="block">
                                       <span class="block-method block_method_color block_method_options"
                                             v-if="scope.row.creator==='yapi'"
                                             :title="'从YAPI导入的接口'">
                                            YAPI
                                       </span>
                                    </div>
                                    <el-tooltip :content="scope.row.url" placement="top" effect="light">
                                        <span class="block-method block_url text-ellipsis">{{ scope.row.url }}</span>
                                    </el-tooltip>
                                    <el-tooltip :content="scope.row.name" placement="top" effect="light">
                                        <span class="block-summary-description text-ellipsis">{{ scope.row.name }}</span>
                                    </el-tooltip>
                                    <span v-if="scope.row.cases.length > 0"
                                          class="block-method block_method_color block_method_cases clickable"
                                          :title="`API已被用例引用,共计: ${scope.row.cases.length} 次`"
                                          @click="showRelatedCases(scope.row.cases)">
                                        关联用例: {{ scope.row.cases.length }} 次
                                    </span>
                                </div>
                            </template>
                        </el-table-column>

                        <el-table-column
                            prop="tag"
                            label="标签"
                            width="90"
                            filter-placement="bottom-end">
                            <template slot-scope="scope">
                                <el-tag
                                    :type="scope.row.tag === 0 ? 'info' : scope.row.tag === 2 ? 'danger' : 'success' "
                                    effect="light"
                                >
                                    {{ scope.row.tag_name }}
                                </el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column>
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        icon="el-icon-edit"
                                        circle size="mini"
                                        @click="handleRowClick(scope.row)"
                                    ></el-button>

                                    <el-button
                                        type="success"
                                        icon="el-icon-document"
                                        title="复制API"
                                        circle size="mini"
                                        @click="handleCopyAPI(scope.row.id, scope.row.name)"
                                    >
                                    </el-button>

                                    <el-button
                                        type="primary"
                                        icon="el-icon-caret-right"
                                        title="运行API"
                                        circle size="mini"
                                        @click="handleRunAPI(scope.row.id)"
                                    ></el-button>

                                    <el-popover
                                        style="margin-left: 10px"
                                        trigger="hover"
                                    >
                                        <div style="text-align: center">
                                            <el-button
                                                type="danger"
                                                icon="el-icon-delete"
                                                :title="userName === scope.row.creator || isSuperuser ? '删除' : '只有API创建者才能删除'"
                                                :disabled="userName != scope.row.creator && !isSuperuser"
                                                circle size="mini"
                                                @click="handleDelApi(scope.row.id)"
                                            >
                                            </el-button>
                                            <el-button
                                                v-show="(userName === scope.row.creator || isSuperuser ) && scope.row.cases.length>0"
                                                :disabled="userName != scope.row.creator && !isSuperuser"
                                                type="warning"
                                                icon="el-icon-refresh"
                                                :title="userName === scope.row.creator || isSuperuser ? '同步用例步骤' : '同步用例权限不足'"
                                                circle size="mini"
                                                @click="handleSyncCaseStep(scope.row.id)"
                                            >
                                            </el-button>
                                        </div>
                                        <el-button icon="el-icon-more" title="更多" circle size="mini"
                                                   slot="reference"></el-button>
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
import Report from '../../../reports/DebugReport'
import apiListMixin from '@/mixins/apiListMixin';


export default {
    mixins: [apiListMixin],
    components: {
        Report
    },
    name: "ApiList",
    props: {
        host: {
            require: true
        },
        config: {
            require: true
        },
        run: Boolean,
        move: Boolean,
        back: Boolean,
        pNode: {
            require: true
        },
        project: {
            require: true
        },
        del: Boolean,
        listCurrentPage: Number,
        visibleTag: [Number, String],
        rigEnv: [Number, String],
        onlyMe: Boolean,
        showYAPI: Boolean,
        isSelectAPI: Boolean
    },
    data() {
        return {
            isSuperuser: this.$store.state.is_superuser,
            userName: this.$store.state.user,
            checked: false,
            search: '',
            reportName: '',
            asyncs: false,
            filterText: '',
            loading: false,
            expand: '&#xe65f;',
            dataTree: {},
            dialogTreeVisible: false,
            dialogTreeMoveAPIVisible: false,
            dialogTableVisible: false,
            dialogRelatedCasesVisible: false,
            summary: {},
            relatedCases: [],
            selectAPI: [],
            currentRow: '',
            currentPage: this.listCurrentPage,
            node: '',
            apiData: {
                count: 0,
                results: []
            },
            // tag: this.visibleTag,
            // rigEnv: this.rigEnv,
        }
    },
    watch: {
        filterText(val) {
            this.$refs.tree.filter(val);
        },

        run() {
            this.asyncs = false;
            this.reportName = "";
            this.getTree('run');
        },

        move() {
            this.asyncs = false;
            this.reportName = "";
            this.getTree('move');
        },

        back() {
            this.getAPIList();
        },
        pNode() {
            this.node = this.pNode
            this.search = '';
            this.getAPIList();
        },
        checked() {
            if (this.checked) {
                this.toggleAll();
            } else {
                this.toggleClear();
            }
        },

        del() {
            if (this.selectAPI.length !== 0) {
                this.$confirm('此操作将永久删除API，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    this.$api.delAllAPI({data: this.selectAPI}).then(resp => {
                        this.getAPIList();
                    })
                }).catch(e => e)
            } else {
                this.$notify.warning({
                    title: '提示',
                    message: '请至少选择一个接口',
                    duration: this.$store.state.duration
                })
            }
        },
        // 监听listCurrentPage的变化,修改原本currentPage的值
        // 因为原本有些函数用到的值是currentPage,所以不能直接修改currentPage的值.
        listCurrentPage(newValue) {
            this.currentPage = newValue
        },

        // 监只看自己按钮的状态
        onlyMe() {
            this.getAPIList()
        },
        showYAPI() {
            this.getAPIList()
        },
        search() {
            this.getAPIList()
        }
    },

    methods: {
        tagChangeHandle(command) {
            // this.tag = command;
            this.$emit('update:visibleTag', command);
            this.getAPIList();
        },
        dropdownMenuChangeHandle(command) {
            let tag = -1
            switch (command) {
                case 'success':
                    tag = 1
                    break;
                case 'fail':
                    tag = 2
                    break;
                case 'deprecated':
                    tag = 4
                    break;
                case 'move':
                    this.$emit("update:move", !this.move)
                    break;
            }
            if (command !== 'move') {
                console.log("!=move...")
                let api_ids = []
                for (let selectAPIElement of this.selectAPI) {
                    api_ids.push(selectAPIElement.id)
                }
                this.$api.tagAPI({
                    tag: tag,
                    api_ids: api_ids,
                }).then(resp => {
                    this.selectAPI = []
                    this.checked = false
                    if (resp.success) {
                        this.getAPIList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            }
        },
        rigEnvChangeHandle(command) {
            // this.rigEnv = command;
            this.$emit('update:rigEnv', command);
            this.getAPIList();
        },
        resetSearch() {
            this.search = "";
            this.node = "";
            this.$emit('update:listCurrentPage', 1)
            // this.tag = "";
            // this.$emit('update:tag', '');
            this.$emit('update:visibleTag', '');
            this.$emit('update:rigEnv', '');
            this.$emit('update:onlyMe', true);
            this.$emit('update:showYAPI', true);
            this.getAPIList();
        },
        handleOnlyMeChange() {
            this.$emit('update:onlyMe', this.onlyMe);
            this.getAPIList()
        },
        handleCopyAPI(id, name) {
            this.$prompt('请输入接口名称', '提示', {
                confirmButtonText: '确定',
                inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                inputErrorMessage: '接口名称不能为空',
                inputValue: name,
            }).then(({value}) => {
                this.$api.copyAPI(id, {
                    'name': value
                }).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
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
                    title: '提示',
                    message: '请至少选择一个节点',
                    duration: 1500
                });
            } else {
                this.$api.runAPITree({
                    "host": this.host,
                    "project": this.project,
                    "relation": relation,
                    "async": this.asyncs,
                    "name": this.reportName,
                    "config": this.config
                }).then(resp => {
                    if (resp.hasOwnProperty("status")) {
                        this.$message.info({
                            message: resp.msg,
                            duration: 1500
                        });
                    } else {
                        this.summary = resp;
                        this.dialogTableVisible = true;
                    }

                })
            }
        },
        moveAPI() {
            this.dialogTreeVisible = false;
            const relation = this.$refs.tree.getCheckedKeys();
            let length = relation.length;
            if (length === 0) {
                this.$notify.error({
                    title: '提示',
                    message: '请至少选择一个节点',
                    duration: 1500
                });
            } else if (length !== 1) {
                this.$notify.error({
                    title: '提示',
                    message: 'API只能移动到一个节点, 现在选了' + length + '个节点',
                    duration: 1500
                });
            } else {
                this.$api.moveAPI({
                    "project": this.project,
                    "relation": relation[0],
                    "api": this.selectAPI
                }).then(resp => {
                    this.selectAPI = []
                    this.checked = false
                    if (resp.success) {
                        this.$message.success({
                            message: '移动API成功',
                            duration: 1500
                        });
                        this.dialogTreeMoveAPIVisible = false
                        this.resetSearch()
                    } else {
                        this.$message.error({
                            message: resp.msg,
                            duration: 1500
                        })
                    }
                })
            }
        },
        getTree(showType) {
            this.$api.getTree(this.$route.params.id, {params: {type: 1}}).then(resp => {
                this.dataTree = resp.tree;
                // run是批量运行api弹窗，其他是批量更新api relation弹窗
                if (showType === 'run') {
                    this.dialogTreeVisible = true;
                } else {
                    this.dialogTreeMoveAPIVisible = this;
                }
            })
        },

        handleSelectionChange(val) {
            this.selectAPI = val;
            // 更新是否已经选择API, 父组件依赖这个属性来判断是否显示Move API按钮
            if (this.selectAPI.length > 0) {
                this.$emit('update:isSelectAPI', true);
            } else {
                this.$emit('update:isSelectAPI', false);
            }

        },

        toggleAll() {
            this.$refs.multipleTable.toggleAllSelection();
        },

        toggleClear() {
            this.$refs.multipleTable.clearSelection();
        },

        handleCurrentChange(val) {
            this.$api.getPaginationBypage({
                params: {
                    page: this.currentPage,
                    node: this.node,
                    project: this.project,
                    search: this.search,
                    tag: this.visibleTag,
                    rigEnv: this.rigEnv,
                    onlyMe: this.onlyMe,
                    showYAPI: this.showYAPI
                }
            }).then(res => {
                this.apiData = res;
                this.$emit("click-pager", val)
            })
        },

        //删除api
        handleDelApi(index) {
            this.$confirm('此操作将永久删除该API，是否继续???', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.delAPI(index).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
        },
        handleTagApi(index, tag) {
            if (tag == "success" || tag == "bug") {
                this.$api.tagAPI(index, {
                    tag: tag === "success" ? 1 : 2
                }).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            }
        },
        // api同步用例步骤
        handleSyncCaseStep(id) {
            this.$confirm('是否确定把当前api同步到用例步骤', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.syncCaseStep(id).then(resp => {
                    if (resp.success) {
                        this.getAPIList();
                        this.$notify.success({
                            title: '提示',
                            message: '用例步骤同步成功',
                            duration: 1500
                        })
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            }).catch(e => e)
        },
        // 编辑API
        handleRowClick(row) {
            this.$api.getAPISingle(row.id).then(resp => {
                if (resp.success) {
                    this.$emit('api', resp);
                } else {
                    this.$message.error(resp.msg)
                }
            })
        },
        // 运行API
        handleRunAPI(id) {
            // 如果没有选择配置的时候，并且api的不是http开头的, 并且不是变量的时候，提示用户选择配置
            if (this.config === '请选择' && this.host === '请选择' && !this.currentRow.url.startsWith("http") && !this.currentRow.url.startsWith("$")){
                this.$message.warning("请先在左上角选择配置再运行哦~")
                return
            }
            this.loading = true;
            this.$api.runAPIByPk(id, {
                params: {
                    host: this.host,
                    config: this.config
                }
            }).then(resp => {
                this.summary = resp;
                this.dialogTableVisible = true;
                this.loading = false;
            }).catch(resp => {
                this.loading = false;
            })
        },

        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        },

        showRelatedCases(cases) {
            this.relatedCases = cases;
            this.dialogRelatedCasesVisible = true;
        },
    }
    ,
    mounted() {
        this.getAPIList();
    }
}
</script>

<style scoped>
.recordapi__header {
    display: flex;
    align-items: center;
}

.recordapi__header--item.is-strench {
    flex: 1;
}

.recordapi__header--item {
    margin: 0 8px;
}

.block-method {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 24px; /* 设置一个固定高度 */
    padding: 0 8px;
    font-size: 12px;
    border-radius: 4px;
    margin-right: 5px;
}

.block_method_color {
    color: white;
}

.block_method_group {
    background-color: #67c23a;
}

.block_method_cases {
    background-color: #409eff;
}


/* 如果需要调整间距 */
.block > * {
    margin-right: 5px;
}

/* 确保 YAPI 标签也保持一致的高度 */
.block_method_options {
    height: 24px;
    line-height: 24px;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px; /* 根据需要调整 */
  display: inline-block;
}

.block_url {
  max-width: 250px; /* 根据需要调整 */
}

.clickable {
  cursor: pointer;
  transition: opacity 0.3s;
}

.clickable:hover {
  opacity: 0.8;
}
</style>

