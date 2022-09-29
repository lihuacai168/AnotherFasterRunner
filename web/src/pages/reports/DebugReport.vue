<template>
    <div>
        <el-table
            :data="[summary]"
            size="medium"
            style="width: 100%"
            border
            stripe
            :header-cell-style="{textAlign:'center', background: '#F8F8FA'}"
            :cell-style="{textAlign:'center'}"
        >
            <el-table-column label="测试时间" width="160">
                <template v-slot="scope">
                    <span>{{ scope.row.time.start_at|timestampToTime }}</span>
                </template>
            </el-table-column>

            <el-table-column label="持续时间" width="100">
                <template v-slot="scope">
                    <span v-text="scope.row.time.duration.toFixed(3)+' 秒'"></span>
                </template>
            </el-table-column>

            <el-table-column label="Total" width="100">
                <template v-slot="scope">
                    <el-tag>{{ scope.row.stat.testsRun }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Success" width="100">
                <template v-slot="scope">
                    <el-tag type="success">{{ scope.row.stat.successes }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Failed" width="100">
                <template v-slot="scope">
                    <el-tag type="danger">{{ scope.row.stat.failures }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Error" width="100">
                <template v-slot="scope">
                    <el-tag type="warning">{{ scope.row.stat.errors }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Skipped" width="100">
                <template v-slot="scope">
                    <el-tag type="info">{{ scope.row.stat.skipped }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Platform">
                <template v-slot="scope">
                    <el-popover trigger="hover" placement="top">
                        <p>HttpRunner: {{ scope.row.platform.httprunner_version }}</p>
                        <p>Python: {{ scope.row.platform.python_version }}</p>
                        <div slot="reference" class="name-wrapper">
                            <el-tag size="medium">{{ scope.row.platform.platform }}</el-tag>
                        </div>
                    </el-popover>
                </template>
            </el-table-column>
        </el-table>

        <br/>
        <br/>

        <slot v-for="item in summary.details">
            <div>
                <span style="font-weight: bold; font-size: medium">{{ item.name }}</span>
                <el-popover placement="top-start" width="400" trigger="hover">
                    <pre class="code-block">{{ item.in_out }}</pre>
                    <el-button slot="reference" round type="text">parameters & output</el-button>
                </el-popover>
            </div>
            <el-table
                :data="item.records"
                @expand-change="expandChange"
                :row-class-name="tableRowClassName"
                style="width: 100%"
                border
                :header-cell-style="{textAlign:'center', background: '#F8F8FA'}"
                :cell-style="{textAlign:'center'}"
            >
                <el-table-column type="expand" fixed>
                    <template slot-scope="props">
                        <el-tabs @tab-click="handleClick">
                            <el-tab-pane label="Request">
                                <pre class="code-block" v-html="handleRequest(props.row.meta_data.request)"></pre>
                            </el-tab-pane>

                            <el-tab-pane label="Content" v-if="props.row.meta_data.response.jsonCopy !== null">
                                <v-jsoneditor ref="jsonEditor" v-model="props.row.meta_data.response.jsonCopy"
                                              :options="options" :plus="true"
                                              :height="height"
                                              @error="onError">
                                </v-jsoneditor>
                            </el-tab-pane>

                            <el-tab-pane label="Response">
                                <pre class="code-block" v-text="handleResponse(props.row.meta_data.response)"></pre>
                            </el-tab-pane>
                            <el-tab-pane label="Validators" v-if="props.row.meta_data.validators.length !== 0">
                                <!--                                <pre class="code-block" v-html="props.row.meta_data.validators"></pre>-->
                                <el-table
                                    :data="props.row.meta_data.validators"
                                    stripe
                                    border
                                    style="width: 100%">
                                    <el-table-column
                                        prop="check_result"
                                        label="是否通过"
                                        width="80">
                                    </el-table-column>
                                    <el-table-column

                                        prop="check"
                                        label="取值表达式"
                                        width="350">
                                    </el-table-column>
                                    <el-table-column
                                        prop="check_value"
                                        label="实际值"
                                        :formatter="checkValueFormatter"
                                    >
                                    </el-table-column>
                                    <el-table-column
                                        prop="comparator"
                                        label="比较器">
                                    </el-table-column>
                                    <el-table-column
                                        prop="expect"
                                        label="期望值"
                                        :formatter="expectValueFormatter"
                                    >
                                    </el-table-column>
                                    <el-table-column
                                        prop="desc"
                                        label="描述"
                                        :formatter="descValueFormatter"
                                    >
                                    </el-table-column>
                                </el-table>
                            </el-tab-pane>
                            <el-tab-pane label="Exception" v-if="props.row.attachment !== ''">
                                <pre class="code-block" v-html="props.row.attachment"></pre>
                            </el-tab-pane>

                        </el-tabs>
                    </template>
                </el-table-column>

                <el-table-column label="名 称">
                    <template v-slot="scope">
                        <span>{{ scope.row.name }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="请求地址">
                    <template v-slot="scope">
                        <span>{{ scope.row.meta_data.request.url }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="请求方法" width="100px">
                    <template v-slot="scope">
            <span
                :class="scope.row.meta_data.request.method"
            >{{ scope.row.meta_data.request.method }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="响应时间 (ms)" width="130px">
                    <template v-slot="scope">
                        <span>{{ scope.row.meta_data.response.elapsed_ms }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="测试结果" width="100px">
                    <template v-slot="scope">
                        <div :class="scope.row.status">{{ scope.row.status }}</div>
                    </template>
                </el-table-column>

                <el-table-column label="Convert" width="200px">

                    <template v-slot="scope">
                        <el-popover placement="right-start" width="400" trigger="hover">
                            <pre class="code-block">{{ scope.row.meta_data.boomer }}</pre>
                            <el-button slot="reference" round type="text"
                                       @click="copyDataText(scope.row.meta_data.boomer, 'boomer')">boomer
                            </el-button>
                        </el-popover>
                        <el-popover placement="right-start" width="400" trigger="hover">
                            <pre class="code-block">{{ scope.row.meta_data.curl }}</pre>
                            <el-button slot="reference" round type="text"
                                       @click="copyDataText(scope.row.meta_data.curl, 'curl')">curl
                            </el-button>
                        </el-popover>

                    </template>
                </el-table-column>

            </el-table>
        </slot>
    </div>
</template>

<script>

export default {
    name: "DebugReport",
    props: {
        summary: {
            require: true,
        },
    },
    data() {
        let self = this
        return {
            jsonPathOrValue: "",
            expandedRows: [],
            options: {
                onModeChange(newMode, oldMode) {
                    if (newMode === 'view') {
                        self.$refs.jsonEditor[0].editor.expandAll()
                    }
                },
                onEvent: function (node, event) {
                    if (event.type === 'click') {
                        let value = node.value
                        // 当前点击的位置有value，复制value
                        if (value) {
                            self.jsonPathOrValue = value
                            self.copyData('复制json value成功')
                        } else {
                            // 当前点击的位置是key，复制key的jsonpath
                            let arr = node.path
                            arr.unshift("content")
                            self.jsonPathOrValue = arr.join(".")
                            self.copyData('复制jsonpath成功')
                        }
                    }
                },
                mode: 'view',
                modes: ['view', 'code'], // allowed modes
            },
        }
    },
    computed: {
        height() {
            return (window.screen.height - 464).toString() + "px"
        }
    },
    methods: {
        checkValueFormatter(row, column) {
            return this.valueFormatter(row.check_value)
        },
        expectValueFormatter(row, column) {
            return this.valueFormatter(row.expect)
        },
        descValueFormatter(row, column) {
            return this.valueFormatter(row.desc)
        },
        valueFormatter(value) {
            let parsedValue = ""
            switch (typeof value) {
                case "object":
                    parsedValue = JSON.stringify(value)
                    break
                case "boolean":
                    if (value === true) {
                        parsedValue = "True"
                    } else {
                        parsedValue = "False"
                    }
                    break
                default:
                    parsedValue = value
            }
            return parsedValue
        },
        expandChange(row, expandedRow) {
            this.expandedRows = expandedRow.length
        },
        tableRowClassName({row, rowIndex}) {
            row.row_index = rowIndex
        },
        handleClick(tab, event) {
            // TODO 修复产生2个editor
            if (tab.label === "Content") {
                for (let i = 0; i < this.expandedRows; i++) {
                    debugger
                    console.log(i)
                    this.$refs.jsonEditor[i * 2].editor.expandAll()
                }
            }
        },
        copyDataText(text, title) {
            this.$copyText(text).then(e => {
                this.$notify.success({
                    title: 'copy ' + title,
                    message: text,
                    duration: 2000
                });
            }, function (e) {
                this.$notify.error({
                    title: '复制' + title + '失败',
                    message: e,
                    duration: 2000
                });
            })
        },
        copyData(title) {
            this.$copyText(this.jsonPathOrValue).then(e => {
                this.$notify.success({
                    title: title,
                    message: this.jsonPathOrValue,
                    duration: 2000
                });
            }, function (e) {
                this.$notify.error({
                    title: '复制提取路径错误',
                    message: e,
                    duration: 2000
                });
            })
        },


        onError() {
            console.log('error')
        },
        handleRequest(request) {
            const keys = ["start_timestamp"];

            keys.forEach(function (item) {
                delete request[item];
            });
            try {
                request["body"] = JSON.parse(request["body"]);
            } catch (e) {
            }

            return request;
        },

        handleContent(content) {
            try {
                content = JSON.parse(content);
            } catch (e) {
            }
            return content;
        },

        handleResponse(response) {
            const keys = [
                "response_time_ms",
                "encoding",
                "ok",
                "reason",
                "url",
                "text",
                "json",
                "content_size",
                "content_type",
            ];

            keys.forEach(function (item) {
                delete response[item];
            });
            return response;
        },
    },
};
</script>

<style scoped>
pre {
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>
