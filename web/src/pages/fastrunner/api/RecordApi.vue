<template>

    <el-container>
        <el-header style="background: #fff; padding: 0; ">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 10px">
                    <el-button
                        v-show="false"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus"
                        @click="dialogVisible = true"
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
                            <el-radio-button label="根节点"></el-radio-button>
                            <el-radio-button label="子节点"></el-radio-button>
                        </el-radio-group>

                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('nodeForm')">确 定</el-button>
                      </span>
                    </el-dialog>


                    <el-button
                        v-show="false"
                        :disabled="currentNode === '' || !isSuperuser"
                        :title="isSuperuser ? '删除所选节点' : '删除节点权限不足' "
                        type="danger"
                        size="small"
                        icon="el-icon-delete"
                        @click="deleteNode"
                    >删除节点
                    </el-button>


                    <el-button
                        v-show="false"
                        :disabled="currentNode === '' "
                        type="info"
                        size="small"
                        icon="el-icon-edit-outline"
                        @click="renameNode(currentNode)"
                    >重命名
                    </el-button>


                    <el-button
                        :disabled="currentNode === '' "
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="initResponse = true"
                    >添加接口
                    </el-button>

                    <el-button
                        v-show="userName === projectInfo.responsible || isSuperuser"
                        type="primary"
                        size="small"
                        icon="el-icon-circle-plus-outline"
                        @click="importYAPIdialogVisible = true"
                    >导入接口
                    </el-button>

                    <el-dialog width="30%" title="导入YAPI接口" align="center"
                               :visible.sync="importYAPIdialogVisible">
                        <el-form ref="elForm" :model="YAPIformData" :rules="rules" size="medium" label-width="100px">
                            <el-form-item label="YAPI的地址" prop="yapi_base_url">
                                <el-input v-model="YAPIformData.yapi_base_url" readonly
                                          placeholder="http://yapi.xxx.com" clearable
                                          :style="{width: '100%'}"></el-input>
                            </el-form-item>
                            <el-form-item label="token" prop="yapi_openapi_token">
                                <el-input v-model="YAPIformData.yapi_openapi_token" readonly
                                          placeholder="yapi项目的openapi token" clearable
                                          :style="{width: '100%'}"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer">
                            <el-button @click="importYAPIdialogVisible = false">取消</el-button>
                            <el-button type="primary" @click="handleConfirmYAPI"
                                       :title="YAPIformData.yapi_openapi_token === YAPIformDataDefaultValue || YAPIformData.yapi_base_url === YAPIformDataDefaultValue ? '请到项目详情中配置yapi信息' : '导入YAPI节点和接口'"
                                       :disabled="YAPIformData.yapi_openapi_token === YAPIformDataDefaultValue || YAPIformData.yapi_base_url === YAPIformDataDefaultValue">
                                导入
                            </el-button>
                        </div>
                    </el-dialog>
                    <span v-show="this.$store.state.show_hosts">
                    &nbspHosts:
                    <el-select
                        placeholder="请选择"
                        size="small"
                        style=“width:100%”
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
                    &nbsp配置:
                    <el-select
                        placeholder="请选择"
                        size="small"
                        tyle="margin-left: -6px"
                        v-model="currentConfig"
                        value-key="id"
                    >
                        <el-option
                            v-for="item in configOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item">
                        </el-option>
                    </el-select>


                    <el-button
                        v-if="!addAPIFlag"
                        style="margin-left: 20px"
                        type="primary"
                        size="mini"
                        @click="run = !run"
                    >批量运行
                    </el-button>

                    <el-button
                        v-if="!addAPIFlag"
                        :disabled="!(!addAPIFlag && onlyMe && isSelectAPI)"
                        style="margin-left: 20px"
                        type="success"
                        size="mini"
                        @click="move = !move"
                        :title="'移动API到指定节点'"
                    >移动API
                    </el-button>


                    <el-button
                        v-if="isSuperuser"
                        type="danger"
                        icon="el-icon-delete"
                        circle
                        size="mini"
                        :title="isSuperuser === true ? '批量删除所选API' : '批量删除API权限不足'"
                        :disabled="!isSuperuser"
                        @click="del = !del"
                    ></el-button>


                    <el-switch
                        style="margin-left: 10px"
                        v-model="onlyMe"
                        v-if="!addAPIFlag"
                        active-color="#13ce66"
                        inactive-color="#ff4949"
                        active-text="只看自己">
                    </el-switch>

                    <el-switch
                        style="margin-left: 10px"
                        v-model="showYAPI"
                        v-if="!addAPIFlag"
                        active-color="#13ce66"
                        inactive-color="#ff4949"
                        active-text="显示YAPI">
                    </el-switch>

                    <el-button
                        :disabled="!addAPIFlag"
                        type="text"
                        style="position: absolute; right: 30px;"
                        @click="handleBackList"
                    >返回列表
                    </el-button>

                </div>
            </div>
        </el-header>

        <el-container>
            <el-aside style="width:260px;margin-top: 10px;">
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
                                        <i class="el-icon-folder-add" @click="dialogVisible=true"></i>
                                        <i class="el-icon-edit" @click="renameNode(node)"></i>
                                        <i class="el-icon-delete" @click="deleteNode(node)"></i>
                                </span>

                            </span>
                        </el-tree>
                    </div>

                </div>

            </el-aside>

            <el-main style="padding: 0;">
                <api-body
                    v-show="addAPIFlag"
                    :isSaveAs="isSaveAs"
                    :nodeId="currentNode.id"
                    :project="$route.params.id"
                    :response="response"
                    v-on:addSuccess="handleAddSuccess"
                    :config="currentConfig"
                    :host="currentHost"
                >
                </api-body>
                <api-list
                    v-show="!addAPIFlag"
                    v-on:api="handleAPI"
                    :pNode="currentNode !== '' ? currentNode.id : '' "
                    :project="$route.params.id"
                    :config="currentConfig.name"
                    :host="currentHost"
                    :del="del"
                    :back="back"
                    :run="run"
                    :move.sync="move"
                    :listCurrentPage.sync="listCurrentPage"
                    :visibleTag.sync="visibleTag"
                    :rigEnv.sync="rigEnv"
                    :only-me.sync="onlyMe"
                    :showYAPI.sync="showYAPI"
                    :isSelectAPI.sync="isSelectAPI"
                    @click-pager="handleChangePage"
                >
                </api-list>

            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import ApiBody from './components/ApiBody'
import ApiList from './components/ApiList'

export default {
    watch: {
        filterText(val) {
            this.$refs.tree2.filter(val);
        }
    },
    components: {
        // 子组件
        ApiBody,
        ApiList
    },

    computed: {
        initResponse: {
            get() {
                return this.addAPIFlag;
            },
            set(value) {
                this.addAPIFlag = value;
                this.response = {
                    id: '',
                    body: {
                        name: '',
                        times: 1,
                        url: '',
                        method: 'POST',
                        header: [{
                            key: "",
                            value: "",
                            desc: ""
                        }],
                        request: {
                            data: [{
                                key: "",
                                value: "",
                                desc: "",
                                type: 1
                            }],
                            params: [{
                                key: "",
                                value: "",
                                desc: "",
                                type: 1
                            }],
                            json_data: ''
                        },
                        validate: [{
                            expect: "",
                            actual: "",
                            comparator: "equals",
                            type: 1
                        }],
                        variables: [{
                            key: "",
                            value: "",
                            desc: "",
                            type: 1
                        }],
                        extract: [{
                            key: "",
                            value: "",
                            desc: ""
                        }],
                        hooks: [{
                            setup: "",
                            teardown: ""
                        }]
                    }
                };
            }
        },
    },
    data() {
        const YAPIformDataDefaultValue = '请到项目详情编辑'
        return {
            mouseNodeId: -1,
            isSuperuser: this.$store.state.is_superuser,
            userName: this.$store.state.user,
            projectInfo: {},
            configOptions: [],
            hostOptions: [],
            // currentConfig: '请选择',
            currentConfig: '',
            currentHost: '请选择',
            back: false,
            del: false,
            run: false,
            move: false,
            response: '',
            nodeForm: {
                name: '',
            },
            rules: {
                yapi_base_url: [{
                    required: true,
                    message: 'yapi的openapi url',
                    trigger: 'blur'
                }],
                yapi_openapi_token: [{
                    required: true,
                    message: 'yapi的openapi token',
                    trigger: 'blur'
                }],
                name: [
                    {required: true, message: '请输入节点名称', trigger: 'blur'},
                    {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                ],

            },
            radio: '根节点',
            addAPIFlag: false,
            treeId: '',
            maxId: '',
            dialogVisible: false,
            importYAPIdialogVisible: false,
            currentNode: '',
            data: '',
            filterText: '',
            expand: '&#xe65f;',
            dataTree: [],
            listCurrentPage: 1,
            visibleTag: '',
            rigEnv: '',
            onlyMe: true,
            showYAPI: true,
            isSelectAPI: false,
            isSaveAs: false,
            YAPIformDataDefaultValue: YAPIformDataDefaultValue,
            YAPIformData: {
                yapi_base_url: YAPIformDataDefaultValue,
                yapi_openapi_token: YAPIformDataDefaultValue,
            },
        }
    },
    methods: {
        handleDragEnd() {
            this.updateTree(false);
        },
        handleAddSuccess() {
            this.rigEnv = '';
            this.visibleTag = '';
            this.back = !this.back;
            this.addAPIFlag = false;
            this.isSaveAs = false;
        },

        handleAPI(response) {
            this.addAPIFlag = true;
            this.response = response;
            this.isSaveAs = true;
        },

        handleChangePage(val) {
            this.listCurrentPage = val;
        },

        getTree() {
            this.$api.getTree(this.$route.params.id, {params: {type: 1}}).then(resp => {
                this.dataTree = resp['tree'];
                this.treeId = resp['id'];
                this.maxId = resp['max'];
            })
        },
        getConfig() {
            this.$api.getAllConfig(this.$route.params.id).then(resp => {
                this.configOptions = resp;
                this.configOptions.unshift({
                    name: '请选择'
                });
                const _config = this.configOptions.filter(item => item.is_default === true);
                if (_config.length) {
                    this.currentConfig = _config[0]
                } else {
                    this.currentConfig = '请选择'
                }
            });

        },

        getHost() {
            this.$api.getAllHost(this.$route.params.id).then(resp => {
                this.hostOptions = resp;
                this.hostOptions.push({
                    name: '请选择'
                })
            })
        },

        updateTree(mode) {
            this.$api.updateTree(this.treeId, {
                body: this.dataTree,
                node: this.currentNode.id,
                mode: mode,
                type: 1
            }).then(resp => {
                if (resp['success']) {
                    this.dataTree = resp['data']['tree'];
                    this.maxId = resp['data']['max'];
                } else {
                    this.$message.error(resp['msg']);
                }
            })
        },

        deleteNode(node) {
            this.$confirm(`删除 ${node.label} 节点下所有接口, 是否继续?`, '提示', {
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


        handleConfirm(formName) {
            console.log(formName);
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
            // 点击分节点之前,先把页码设置为1.2019年7月2日,并且传给子组件.
            this.listCurrentPage = 1;
            this.visibleTag = '';
            this.addAPIFlag = false;
            this.isSaveAs = false;
            this.currentNode = node;
            this.data = data;
            this.rigEnv = '';
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
            if (data === '' || this.dataTree.length === 0 || this.radio === '根节点') {
                this.dataTree.push(newChild);
                return
            }
            if (!data.children) {
                this.$set(data, 'children', []);
            }
            data.children.push(newChild);
        },

        handleBackList() {
            this.addAPIFlag = false
            this.isSaveAs = false
        },

        getYapiInfo() {
            const pk = this.$route.params.id;
            this.$api.getProjectYapiInfo(pk).then(res => {
                this.projectInfo = res
                if (res.yapi_base_url !== '') {
                    this.YAPIformData.yapi_base_url = res.yapi_base_url
                }
                if (res.yapi_openapi_token !== '') {
                    this.YAPIformData.yapi_openapi_token = res.yapi_openapi_token
                }
            })
        },
        mouseenter(node) {
            this.mouseNodeId = node.id;
        },
        mouseleave(){
            this.mouseNodeId = -1;
        },
        handleConfirmYAPI() {
            this.$refs['elForm'].validate(valid => {
                if (!valid) return
                const project_id = this.$route.params.id;
                this.$message.info({
                    title: '提示',
                    message: '如果是首次导入，可能时间稍长，请耐心等待~',
                    duration: this.$store.state.duration
                })
                this.importYAPIdialogVisible = false
                this.$api.addYAPI(project_id).then(resp => {
                    if (resp.success) {
                        let created =  "新增：" + resp.createdCount + " 条API"
                        let updated = "更新：" + resp.updatedCount  + " 条API"
                        if (resp.createdCount > 0 || resp.updatedCount > 0){
                            this.$notify.success({
                            title: '导入API提示',
                            message: created + " ；" + updated,
                            duration: this.$store.state.duration
                            })
                        }
                        const NOT_CREATED_AND_UPDATED_CODE = '0002'
                        if (resp.code === NOT_CREATED_AND_UPDATED_CODE){
                            this.$notify.success({
                            title: '导入API提示',
                            message: resp.msg,
                            duration: this.$store.state.duration
                            })
                        }
                        const CREATED_OR_UPDATED_CODE = '0001'
                        if (resp.code === CREATED_OR_UPDATED_CODE){
                            this.getTree()
                            // 重置tree节点，触发子组件更新apiList
                            // TODO 改成直接调用子组件的getAPIList方法
                            this.currentNode = ''
                            this.onlyMe = false
                            this.showYAPI = true
                        }
                    } else {
                        this.$message.error({
                            message: resp.msg,
                            duration: this.$store.state.duration
                        })
                    }
                })
            })
        },

    },
    name: "RecordApi",
    mounted() {
        this.getTree();
        this.getConfig();
        this.getHost();
        this.getYapiInfo();
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
