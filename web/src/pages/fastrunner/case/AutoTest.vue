<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 10px">
                    <el-button
                        v-if="false"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus"
                        @click="dialogVisible = true"
                        :disabled="!addTestActivate"
                    >
                        新建节点
                    </el-button>

                    <el-dialog
                        title="新建节点"
                        :visible.sync="dialogVisible"
                        width="30%"
                        align="center"
                    >
                        <el-form
                            :model="nodeForm"
                            :rules="rules"
                            ref="nodeForm"
                            label-width="100px"
                            class="project">
                            <el-form-item label="节点名称" prop="name">
                                <el-input v-model="nodeForm.name"></el-input>
                            </el-form-item>
                        </el-form>

                        <el-radio-group v-model="radio" size="small">
                            <el-radio-button label="同级节点"></el-radio-button>
                            <el-radio-button label="子节点"></el-radio-button>
                        </el-radio-group>

                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('nodeForm')">确 定</el-button>
                      </span>
                    </el-dialog>

                    <el-button
                        v-if="false"
                        type="danger"
                        size="small"
                        icon="el-icon-delete"
                        @click="deleteNode"
                        :disabled="buttonActivate"
                    >删除节点
                    </el-button>

                    <el-button
                        v-if="false"
                        :disabled="currentNode === '' "
                        type="info"
                        size="small"
                        icon="el-icon-edit-outline"
                        @click="renameNode(currentNode)"
                    >重命名
                    </el-button>

                    <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="buttonActivate=false"
                        :disabled="buttonActivate"
                    >添加用例
                    </el-button>
                    <span v-show="this.$store.state.show_hosts">
                    &nbspHosts:
                    <el-select
                        placeholder="请选择"
                        size="small"
                        tyle="margin-left: -6px"
                        v-model="currentHost"
                    >
                        <el-option
                            v-for="item in hostOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name">
                        </el-option>
                    </el-select>
                    </span>
                    <span style="margin-left: 10px">配置:</span>
                    <el-select
                        placeholder="请选择"
                        size="small"
                        tyle="margin-left: -6px"
                        v-model="currentConfig"
                        :disabled="addTestActivate"
                    >
                        <el-option
                            v-for="item in configOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name"
                        >
                        </el-option>
                    </el-select>


                    <el-button
                        v-if="addTestActivate"
                        style="margin-left: 20px"
                        type="primary"
                        size="small"
                        title="批量运行用例"
                        @click="run = !run"
                    >运行用例
                    </el-button>

                    <el-button
                        v-if="addTestActivate"
                        :disabled="!isSelectCase"
                        style="margin-left: 0px"
                        type="success"
                        size="small"
                        title="移动用例到指定节点"
                        @click="move = !move"
                    >移动用例
                    </el-button>

                    <el-button
                        v-if="addTestActivate"
                        :disabled="!(onlyMe && isSelectCase)"
                        style="margin-left: 0px"
                        type="danger"
                        icon="el-icon-delete"
                        size="small"
                        title="批量删除当前用户的用例"
                        @click="del = !del"
                    >删除用例
                    </el-button>

                    <el-switch
                        style="margin-left: 20px"
                        v-model="onlyMe"
                        v-if="addTestActivate"
                        active-color="#13ce66"
                        inactive-color="#ff4949"
                        active-text="只看自己">
                    </el-switch>

                    <el-button
                        :disabled="addTestActivate"
                        type="primary"
                        size="small"
                        icon="el-icon-back"
                        style="position: absolute; right: 10px;"
                        @click="handleBackList"
                    >返回列表
                    </el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-aside
                style="margin-top: 10px;"
                v-show="addTestActivate"
            >
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
                            draggable
                            highlight-current
                            :filter-node-method="filterNode"
                            ref="tree2"
                            @node-drag-end="handleDragEnd"
                        >
                            <span class="custom-tree-node"
                                  slot-scope="{ node, data }"
                                  @mouseenter="mouseenter(node)" @mouseleave="mouseleave"
                                  style="display: flex; width: 180px"
                            >
                                <span style="overflow: hidden; text-overflow:ellipsis; flex: 1">
                                    <i class="iconfont" v-html="expand"></i>&nbsp;&nbsp;{{ node.label }}
                                </span>
                                <span class="icon-group" v-show="node.id === mouseNodeId" >
                                        <i class="el-icon-folder-add" @click="dialogVisible=true"  :disabled="!addTestActivate"></i>
                                        <i class="el-icon-edit" @click="renameNode(node)"></i>
                                        <i class="el-icon-delete" @click="deleteNode(node)"></i>
                                </span>
                            </span>
                        </el-tree>

                    </div>
                </div>


            </el-aside>

            <el-main style="padding: 0;">
                <test-list
                    v-show="addTestActivate"
                    :project="$route.params.id"
                    :node="currentNode !== '' ? currentNode.id : '' "
                    :del="del"
                    v-on:testStep="handleTestStep"
                    :back="back"
                    :run="run"
                    :move="move"
                    :host="currentHost"
                    :only-me.sync="onlyMe"
                    :isSelectCase.sync="isSelectCase"
                >
                </test-list>

                <edit-test
                    :back="back"
                    v-show="!addTestActivate"
                    :project="$route.params.id"
                    :node="currentNode.id"
                    :testStepResp="testStepResp"
                    :config="currentConfig"
                    :host="currentHost"
                    :rigEnv.sync="rigEnv"
                    :tag.sync="tag"
                    :search.sync="search"
                    :addTestActivate="addTestActivate"
                    v-on:addSuccess="handleBackList"
                >
                </edit-test>

            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import EditTest from './components/EditTest'
import TestList from './components/TestList'

export default {
    computed: {
        buttonActivate: {
            get: function () {
                return !this.addTestActivate || this.currentNode === '';
            },
            set: function (value) {
                this.addTestActivate = value;
                this.testStepResp = [];
            }
        }
    },
    watch: {
        filterText(val) {
            this.$refs.tree2.filter(val);
        }
    },
    components: {
        EditTest,
        TestList,
    },
    data() {
        return {
            mouseNodeId: -1,
            testStepResp: [],
            nodeForm: {
                name: '',
            },
            rules: {
                name: [
                    {required: true, message: '请输入节点名称', trigger: 'blur'},
                    {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                ]
            },
            hostOptions: [],
            back: false,
            del: false,
            run: false,
            move: false,
            radio: '同级节点',
            addTestActivate: true,
            currentConfig: '请选择',
            currentHost: '请选择',
            treeId: '',
            maxId: '',
            dialogVisible: false,
            currentNode: '',
            data: '',
            filterText: '',
            expand: '&#xe65f;',
            dataTree: [],
            configOptions: [],
            rigEnv: "",
            tag: "",
            search: "",
            onlyMe: true,
            isSelectCase: false,
        }
    },
    methods: {
        handleDragEnd() {
            this.updateTree(false);
        },
        getConfig() {
            this.$api.getAllConfig(this.$route.params.id).then(resp => {
                this.configOptions = resp;
                this.configOptions.push({
                    name: '请选择'
                })
            })
        },

        handleBackList() {
            this.addTestActivate = true;
            this.testStepResp = []
            this.back = !this.back;
        },

        handleTestStep(resp) {
            this.testStepResp = resp;
            this.addTestActivate = false;
        },
        getTree() {
            this.$api.getTree(this.$route.params.id, {params: {type: 2}}).then(resp => {
                this.dataTree = resp['tree'];
                this.treeId = resp['id'];
                this.maxId = resp['max'];
            })
        },

        updateTree(mode) {
            this.$api.updateTree(this.treeId, {
                mode: mode,
                body: this.dataTree,
                node: this.currentNode.id,
                type: 2
            }).then(resp => {
                if (resp['success']) {
                    this.dataTree = resp['tree'];
                    this.maxId = resp['max'];
                } else {
                    this.$message.error(resp['msg']);
                }
            })
        },
        renameNode(nodeObj) {
            this.$prompt('请输入节点名', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputPattern: /\S/,
                inputErrorMessage: '节点名称不能为空',
                inputValue: nodeObj.label
            }).then(({value}) => {
                const parent = this.data.parent;
                const children = parent.data.children || parent.data;
                const index = children.findIndex(d => d.id === this.currentNode.id);
                children[index]["label"] = value
                this.updateTree(false);
            });
        },

        deleteNode(node) {
            this.$confirm(`删除 ${node.label} 节点的所有用例, 是否继续?`, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                if (this.currentNode === '') {
                    this.$message.info('请选择一个节点');
                } else {
                    if (this.currentNode.children.length !== 0) {
                        this.$message.warning('此节点有子节点，不可删除！');
                    } else {
                        this.remove(this.currentNode, this.data);
                        this.updateTree(true);
                    }
                }

            })
        },

        handleConfirm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.append(this.currentNode);
                    this.updateTree(false);
                    this.dialogVisible = false;
                    this.nodeForm.name = ''
                }
            });
        },

        handleNodeClick(node, data) {
            this.currentNode = node;
            this.data = data;
        },

        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },

        remove(data, node) {
            const parent = node.parent;
            const children = parent.data.children || parent.data;
            const index = children.findIndex(d => d.id === data.id);
            children.splice(index, 1);
        },

        append(data) {
            const newChild = {id: ++this.maxId, label: this.nodeForm.name, children: []};
            if (data === '' || this.dataTree.length === 0 || this.radio === '同级节点') {
                this.dataTree.push(newChild);
                return
            }
            if (!data.children) {
                this.$set(data, 'children', []);
            }
            data.children.push(newChild);
        },
        getHost() {
            this.$api.getAllHost(this.$route.params.id).then(resp => {
                this.hostOptions = resp;
                this.hostOptions.push({
                    name: '请选择'
                })
            })
        },
        mouseenter(node) {
            this.mouseNodeId = node.id;
        },
        mouseleave(){
            this.mouseNodeId = -1;
        }
    },
    name: "AutoTest",
    mounted() {
        this.getTree();
        this.getConfig();
        this.getHost();
    }
}
</script>

<style scoped>
.icon-group {
    margin-right: 6px;
}

.icon-group i {
    margin-left: 4px;
    padding: 2px;
}

</style>
