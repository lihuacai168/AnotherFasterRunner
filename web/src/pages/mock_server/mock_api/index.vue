<template>
    <el-data-table v-bind="tableConfig" style="margin: 10px">
        <template v-slot:operation="{row}">
            <el-button @click="handelCopyCurl(row)" type="primary" size="mini">Curl</el-button>
        </template>
        <template v-slot:form="{row}">
            <!-- 修改按钮 -->
            <el-row v-if="row">
                <el-form ref="form" :model="row" :rules="rules" class="custom-form" label-position="left">
                    <!-- project一行 -->
                    <el-row>
                        <el-col :span="5">
                            <el-form-item label="所属项目" prop="project">
                                <el-input v-model="row.project_name" placeholder="API 名称" :disabled="true"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="19">
                            <el-form-item label="API 名称" prop="api_name">
                                <el-input v-model="row.api_name" placeholder="API 名称"></el-input>
                            </el-form-item>
                        </el-col>

                    </el-row>

                    <!-- api_name和request_path在同一行 -->
                    <el-row :gutter="5" v-if="false">
                        <el-col :span="5">
                            <el-form-item label="API 描述" prop="api_desc">
                                <el-input v-model="row.api_desc" placeholder="描述"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="3">
                            <el-form-item label="请求方法" prop="request_method">
                                <el-select v-model="row.request_method" placeholder="请选择">
                                    <el-option
                                        v-for="item in request_methods"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="21">
                            <el-form-item label="请求路径" prop="request_path">
                                <el-input v-model="row.request_path" placeholder="请输入请求路径">
                                    {{fullDomain}}}
                                    <template slot="prepend">{{fullDomain}}/mock/{{ row.project }}</template>
<!--                                    <el-button slot="append" type="success">Debug</el-button>-->
                                </el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <!-- custom-ace-editor单独一行 -->
                    <el-row>
                        <el-tabs v-model="activeName">
                            <el-tab-pane label="响应设置" name="resp">
                                <el-col :span="24">
                                    <el-form-item>
                                        <custom-ace-editor
                                            ref="defaultEditor"
                                            v-model="row.response_text"
                                            @init="editorInit"
                                        ></custom-ace-editor>
                                    </el-form-item>
                                </el-col>
                            </el-tab-pane>
                            <el-tab-pane label="请求body" name="req">
                                <v-jsoneditor v-model="row.request_body"
                                              :height="jsonEditorHeight"
                                              :options="jsonEditorOptions"
                                              :plus="true"
                                              ref="requestEditor"
                                >
                                </v-jsoneditor>
                            </el-tab-pane>
                        </el-tabs>
                    </el-row>

                </el-form>
            </el-row>
            <div v-else>
                <!-- 新增， row 为空时，使用 response_text 作为 model -->
                <el-form ref="form" :model="form" :rules="rules" class="custom-form" label-position="left">
                    <!-- project一行 -->
                    <el-row>
                        <el-col :span="5">
                            <el-form-item label="所属项目" prop="project">
                                <el-select v-model="form.project" placeholder="请选择">
                                    <el-option
                                        v-for="item in projectList"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="19">
                            <el-form-item label="API 名称" prop="api_name">
                                <el-input v-model="form.api_name" placeholder="API 名称"></el-input>
                            </el-form-item>
                        </el-col>

                    </el-row>

                    <!-- api_name和request_path在同一行 -->
                    <el-row :gutter="5" v-if="false">
                        <el-col :span="5">
                            <el-form-item label="API 描述" prop="api_desc">
                                <el-input v-model="form.api_desc" placeholder="描述"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="5">
                            <el-form-item label="请求方法" prop="request_method">
                                <el-select v-model="form.request_method" placeholder="请选择">
                                    <el-option
                                        v-for="item in request_methods"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="19">
                            <el-form-item label="请求路径" prop="request_path">
                                <el-input v-model="form.request_path" placeholder="请输入请求路径"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <!-- custom-ace-editor单独一行 -->
                    <el-row>
                        <el-tabs v-model="activeName">
                            <el-tab-pane label="响应设置" name="resp">
                                <el-col :span="24">
                                    <el-form-item>
                                        <custom-ace-editor
                                            ref="defaultEditor"
                                            v-model="form.response_text"
                                            @init="editorInit"
                                        ></custom-ace-editor>
                                    </el-form-item>
                                </el-col>
                            </el-tab-pane>
                            <el-tab-pane label="入参样例" name="req">
                                <v-jsoneditor v-model="form.request_body"
                                              :height="jsonEditorHeight"
                                              :options="jsonEditorOptions"
                                              :plus="true"
                                              ref="requestEditor"
                                >
                                </v-jsoneditor>
                            </el-tab-pane>
                        </el-tabs>
                    </el-row>
                </el-form>
            </div>
        </template>
    </el-data-table>
</template>
<script>

import Editor from 'vue2-ace-editor'
import CustomAceEditor from './CustomAceEditor.vue';
import VJsoneditor from 'v-jsoneditor'

import {datetimeObj2str} from "@/util/format";

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
            form: {
                project: '',          // 项目
                api_name: '',         // API名称
                api_desc: '',         // API描述
                request_path: '',      // 请求
                request_method: 'POST',     //请求路径
                request_body: {},
                response_text: `
# req是请求对象,所有下面的属性
# body：请求体 字典类型，
# query_params：查询参数比如 a=1&b=2
# path: 请求路径，比如/a/b/c
# headers, 请求体，字典类型

# resp是响应对象
# 设置响应body，resp.data = {'a': 123}
# 设置响应headers, resp.headers.setdefault('x-mock-id', '123')
# 不需要return
def execute(req, resp):
    resp.data = {'a': 123}`,
            },
            rules: {
                project: [
                    {required: true, message: '请选择项目', trigger: 'blur'}
                ],
                api_name: [
                    {required: true, message: '请输入API名称', trigger: 'blur'}
                ],
                request_path: [
                    {required: true, message: '请输入请求路径', trigger: 'blur'}
                ],
                request_method: [
                    {required: true, message: '请选择请求方法', trigger: 'blur'}
                ]
            },
            projectList: [],
            tableConfig: {
                dataPath: "results",
                totalPath: "count",
                url: '/api/mock/mock_api',
                columns: [
                    {
                        prop: 'project_name',
                        label: '所属项目'
                    },
                    {
                        prop: 'api_name',
                        label: 'API 名称'
                    },
                    {
                        prop: 'request_method',
                        label: '请求方法'
                    },
                    {
                        prop: 'request_path',
                        label: '请求路径'
                    },
                    {
                        prop: 'creator',
                        label: '创建者'
                    },
                    {
                        prop: 'update_time',
                        label: '最后更新',
                        formatter: row => (datetimeObj2str(row.update_time))
                    },

                ],
                paginationSize: 10,
                searchForm: [
                    {
                        type: 'input',
                        id: 'request_path',
                        label: '请求路径',
                        el: {
                            placeholder: '请输入请求路径'
                        }
                    },
                    {
                        type: 'input',
                        id: 'project_name',
                        label: '所属项目',
                        el: {
                            placeholder: '请输入所属项目名称',
                        },

                    },
                    {
                        type: 'input',
                        id: 'api_name',
                        label: 'API 名称',
                        el: {
                            placeholder: '请输入 API 名称'
                        }
                    },
                    {
                        type: 'input',
                        id: 'creator',
                        label: '创建者',
                        el: {
                            placeholder: '请输入创建者'
                        }
                    }
                    // Add more search fields as needed
                ],
                onSuccess: (type, data) => {
                    const oper = {
                        new: '新增',
                        edit: '编辑',
                        delete: '删除',
                    }[type]
                    this.$message.success(`${oper}成功`)
                },
                onEdit: (data, row) => {
                    return this.$axios.put(
                        `${this.tableConfig.url}/${data.id}`,
                        row
                    ).catch(error => {
                        if (error.response) {
                            this.$message.error(`接口返回错误：${JSON.stringify(error.response.data)}`);
                        }
                        throw error;
                    });
                },
                onNew: (data, row) => {
                    return this.$axios.post(
                        `${this.tableConfig.url}/`,
                        this.form
                    ).catch(error => {
                        if (error.response) {
                            this.$message.error(`接口返回错误：${JSON.stringify(error.response.data)}`);
                        }
                        throw error;
                    });
                },
            }
        }
    },
    mounted() {
        this.fetchProjectList()
        this.setExtraBody();
        this.setFullDomain()

    },
    computed: {
        jsonEditorHeight() {
            return (window.screen.height - 464).toString() + "px"
        }
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.$message('submit!');
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
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
            let base_url = `${this.fullDomain}/mock/${row.project}`
            let method = row.request_method.toUpperCase(); // 转换为大写
            let url = `${base_url}${row.request_path}`; // 拼接URL
            console.log(row)
            // 添加HTTP方法
            curlCmd += ` -X ${method}`;

            // 添加请求体。如果请求方法不是GET或HEAD并且存在请求样本，则添加它
            if (['GET', 'HEAD'].indexOf(method) === -1 && row.request_body) {
                // 确保请求样本是字符串形式的JSON
                let requestBody = typeof row.request_body === 'object'
                    ? JSON.stringify(row.request_body)
                    : row.request_body;

                curlCmd += ` -H "Content-Type: application/json" -d '${requestBody}'`;
            }

            // 拼接完整的URL
            curlCmd += ` "${url}"`;
            this.copyData("copyCurl", curlCmd)
        },
        setExtraBody() {
            if (this.$refs.aceEditor && this.$refs.aceEditor.editor) {
                this.tableConfig.extraBody = {row122: this.$refs.aceEditor.editor.getValue()};
            }
        },
        fetchProjectList() {
            this.$api.getMockProject().then(response => {
                // 使用返回的数据来设置`projectList`和`form`中的`options`
                this.projectList = response.results.map(p => ({label: p.project_name, value: p.project_id}));
                // this.tableConfig.form.find(f => f.id === 'project').options = this.projectList.map(p => ({
                //     label: p.project_name,
                //     value: p.project_id
                // }));
            }).catch(error => {
                this.$message.error("获取mock项目列表失败");
            });
        },
        editorInit: function () {
            require('brace/ext/language_tools') // language extension prerequsite...
            require('brace/mode/python')
            require('brace/theme/dracula')
        },
        updateResponseText(row, newValue) {
            if (row) {
                row.response_text = newValue;
            }
        },
    },
}
</script>
<style scoped>
.custom-form .el-form-item {
    margin-bottom: 5px; /* 设置您希望的间距大小 */
}
</style>
