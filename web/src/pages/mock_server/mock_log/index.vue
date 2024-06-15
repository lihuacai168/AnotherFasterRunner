<script>

import Editor from 'vue2-ace-editor'
import VJsoneditor from 'v-jsoneditor'

import {datetimeObj2str} from "@/util/format";
import CustomAceEditor from "@/pages/mock_server/mock_api/CustomAceEditor.vue";

export default {
    components: {
        'ace-editor': Editor, 'custom-ace-editor': CustomAceEditor,
        VJsoneditor,
    },
    data() {
        return {
            codeEditor: null,
            activeName: 'resp',
            fullDomain: "",
            jsonEditorOptions: {
                mode: 'code',
                modes: ['code', 'tree'], // allowed modes
            },
            request_methods: [{label: 'GET', value: 'GET'},
                {label: 'POST', value: 'POST'},
                {label: 'PUT', value: 'PUT'}, {label: 'PATCH', value: 'PATCH'}, {label: 'DELETE', value: 'DELETE'},],
            projectList: [],
            tableConfig: {
                url: '/api/mock/mock_log',
                dataPath: "results",
                totalPath: "count",
                paginationSize: 15,
                paginationSizes: [10, 15, 20, 30],
                operationButtonType: 'button',
                hasView: false,
                hasEdit: false,
                hasNew: false,
                canDelete: () => false,
                form: [
                    {
                        type: 'input',
                        id: 'request_id',
                        label: 'Request ID',
                        rules: [
                            {
                                required: true,
                                message: '请输入Request ID',
                                trigger: 'blur',
                                transform: v => v && v.trim()
                            }
                        ],
                        el: {placeholder: '请输入Request ID'}
                    },
                    {
                        type: 'input',
                        id: 'request_path',
                        label: 'Request Path',
                        rules: [
                            {
                                required: true,
                                message: '请输入Request Path',
                                trigger: 'blur',
                                transform: v => v && v.trim()
                            }
                        ],
                        el: {placeholder: '请输入Request Path'}
                    },
                ],
                searchForm: [
                    {
                        type: 'input',
                        id: 'request_id',
                        label: 'Request ID',
                        el: {placeholder: '请输入所属Request ID', style: 'width: 300px'}
                    },
                    {
                        type: 'input',
                        id: 'request_path',
                        label: 'Request Path',
                        el: {
                            placeholder: 'Request Full Path的/mock/{project}之后的路径,模糊查询',
                            style: 'width: 400px'
                        },
                        width: "400px"
                    },
                ],
                columns: [
                    {
                        prop: 'request_id',
                        label: 'Request ID',
                        width: "280px"
                    },
                    {
                        prop: 'request_path',
                        label: 'Request Full Path',
                        formatter: row => row.request_obj.mock_server_full_path,
                        width: "400px"
                    },
                    {
                        prop: 'project.project_name',
                        label: '项目名称'
                    },
                    {
                        prop: 'api.api_name',
                        label: 'API名称'
                    },

                    {
                        prop: 'create_time',
                        label: '请求时间',
                        formatter: row => datetimeObj2str(row.create_time)
                    },


                ],
            },

            // 传递给弹窗的数据
            viewDialogVisible: false,
            viewRow: {
                request_obj: {},
                response_obj: {}
            }
        }
    },
    mounted() {
        this.fetchProjectList()
        this.setFullDomain()
    },
    computed: {
        jsonEditorHeight() {
            return (window.screen.height - 464).toString() + "px"
        }
    },
    methods: {
        setFullDomain() {
            let domain = window.location.hostname;
            if (domain === "localhost") {
                domain = domain + ":8000"
            }
            this.fullDomain = window.location.protocol + '//' + domain
        },
        copyData(title, content) {
            this.$copyText(content).then(
                e => {
                    this.$notify.success({
                        title: title,
                        message: content,
                        duration: 2000
                    })
                },
                function (e) {
                    this.$notify.error({
                        title: '复制提取路径错误',
                        message: e,
                        duration: 2000
                    })
                }
            )
        },
        handelCopyCurl(row) {
            let curlCmd = 'curl';
            let base_url = `${this.fullDomain}`
            let method = row.request_obj.method.toUpperCase(); // 转换为大写
            let url = `${base_url}${row.request_obj.mock_server_full_path}`; // 拼接URL
            console.log(row)
            // 添加HTTP方法
            curlCmd += ` -X ${method}`;

            // 添加请求体。如果请求方法不是GET或HEAD并且存在请求样本，则添加它
            if (['GET', 'HEAD'].indexOf(method) === -1 && row.request_obj.body) {
                // 确保请求样本是字符串形式的JSON
                let requestBody = typeof row.request_obj.body === 'object'
                    ? JSON.stringify(row.request_obj.body)
                    : row.request_obj.body;

                curlCmd += ` -H "Content-Type: application/json" -d '${requestBody}'`;
            }

            // 拼接完整的URL
            curlCmd += ` "${url}"`;
            this.copyData("copyCurl", curlCmd)
        },
        fetchProjectList() {
            this.$api.getMockProject().then(response => {
                // 使用返回的数据来设置`projectList`
                this.projectList = response.results.map(p => ({
                    label: p.project_name,
                    value: p.project_id
                }));
            }).catch(error => {
                this.$message.error("获取mock项目列表失败");
            });
        },
        handleView(row) {
            this.viewRow = Object.assign({}, row);
            this.viewDialogVisible = true;
        }
    },
}
</script>

<template>
    <div>
        <el-data-table v-bind="tableConfig" style="margin: 10px">
            <template v-slot:operation="{ row }">
                <el-button @click="handleView(row)" type="success" size="mini">查看详情</el-button>
                <el-button @click="handelCopyCurl(row)" type="primary" size="mini">复制Curl</el-button>
            </template>
            <!-- 其余内容保持不变 -->
        </el-data-table>

        <!-- 新增弹窗 -->
        <el-dialog title="查看详情" :visible.sync="viewDialogVisible" width="70%">
            <el-form ref="viewForm" :model="viewRow" class="custom-form" label-position="left">
                <el-row>
                    <el-col :span="12">
                        <el-form-item>
                            <label class="custom-label">请求对象</label>
                            <v-jsoneditor v-model="viewRow.request_obj" :height="jsonEditorHeight"
                                          :options="jsonEditorOptions" ref="requestObjEditor">
                            </v-jsoneditor>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item>
                            <label class="custom-label">响应对象</label>
                            <v-jsoneditor v-model="viewRow.response_obj" :height="jsonEditorHeight"
                                          :options="jsonEditorOptions" ref="responseObjEditor">
                            </v-jsoneditor>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="viewDialogVisible = false">关闭</el-button>
            </div>
        </el-dialog>
    </div>
</template>
<style scoped>
.custom-form .el-form-item {
    margin-bottom: 5px;
}

.custom-label {
    display: block;
    font-weight: bold;
    margin-bottom: 10px; /* 调整为适当的间距 */
    text-align: center; /* 居中对齐 */
    font-size: 28px; /* 调整字体大小 */
}
</style>
