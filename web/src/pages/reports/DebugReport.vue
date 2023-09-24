<template>
    <div>
        <el-table
            :data="[summary]"
            size="medium"
            style="width: 100%"
            border
            stripe
            :header-cell-style="{ textAlign: 'center', background: '#F8F8FA' }"
            :cell-style="{ textAlign: 'center' }"
        >
            <el-table-column label="测试时间" width="160">
                <template slot-scope="scope">
                    <span>{{ scope.row.time.start_at | timestampToTime }}</span>
                </template>
            </el-table-column>

            <el-table-column label="持续时间" width="100">
                <template slot-scope="scope">
                    <span v-text="scope.row.time.duration.toFixed(3) + ' 秒'"></span>
                </template>
            </el-table-column>

            <el-table-column label="Total" width="100">
                <template slot-scope="scope">
                    <el-tag>{{ scope.row.stat.testsRun }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Success" width="100">
                <template slot-scope="scope">
                    <el-tag type="success">{{ scope.row.stat.successes }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Failed" width="100">
                <template slot-scope="scope">
                    <el-tag type="danger">{{ scope.row.stat.failures }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Error" width="100">
                <template slot-scope="scope">
                    <el-tag type="warning">{{ scope.row.stat.errors }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Skipped" width="100">
                <template slot-scope="scope">
                    <el-tag type="info">{{ scope.row.stat.skipped }}</el-tag>
                </template>
            </el-table-column>

            <el-table-column label="Platform">
                <template slot-scope="scope">
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

        <br />
        <br />

        <slot v-for="item in summary.details">
            <div>
                <!-- 鼠标悬停时显示的popover -->
                <el-popover placement="top" width="1600" trigger="hover" popper-class="custom-popper">
                    <div class="popover-content">
                        <!-- 左侧：JSON编辑器 -->
                        <div class="json-editor">
                            <!-- 左侧标题 -->
                            <div class="section-title">
                                <h3>初始变量，包含：配置变量，全局变量，驱动代码变量</h3>
                            </div>
                            <v-jsoneditor
                                ref="jsonEditor"
                                v-model="item.vars_trace[0].before"
                                :options="options"
                                :plus="true"
                                :height="height"
                                @error="onError"
                            >
                            </v-jsoneditor>
                        </div>
                        <!-- 右侧：Timeline -->
                        <div class="timeline-container">
                            <!-- 右侧标题 -->
                            <div class="section-title">
                                <h3>变量trace</h3>
                            </div>
                            <el-timeline>
                                <el-timeline-item
                                    v-for="(trace, index) in item.vars_trace"
                                    :key="index"
                                    :timestamp="`Step_${trace.step_index + 1} ${trace.step_name}， 更新的变量：`"
                                    size="normal"
                                    icon="🚀"
                                    :type="trace.update.length > 0 ? 'success' : 'info'"
                                    placement="top"
                                >
                                    <el-table :data="trace.update" stripe border style="width: 100%" v-if="trace.update.length > 0">
                                        <el-table-column type="index" width="50" label="序号"></el-table-column>
                                        <el-table-column
                                            prop="output_variable_name"
                                            label="变量名"
                                            width="130"
                                        ></el-table-column>
                                        <el-table-column
                                            prop="extract_expr"
                                            label="取值表达式"
                                            width="300"
                                        ></el-table-column>
                                        <el-table-column prop="actual_value" label="实际值">
                                            <template slot-scope="scope">
                                                {{ scope.row.actual_value }}
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                    <p v-if="trace.update.length ===0 ">😊😊😊木有变量变更~</p>
                                </el-timeline-item>
                            </el-timeline>
                        </div>
                    </div>
                    <el-button slot="reference">查看变量trace</el-button>
                </el-popover>
            </div>
            <el-table
                :data="item.records"
                @expand-change="expandChange"
                :row-class-name="tableRowClassName"
                style="width: 100%"
                border
                :header-cell-style="{ textAlign: 'center', background: '#F8F8FA' }"
                :cell-style="{ textAlign: 'center' }"
            >
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-tabs @tab-click="handleClick">
                            <el-tab-pane label="Request">
                                <pre class="code-block" v-html="handleRequest(props.row.meta_data.request)"></pre>
                            </el-tab-pane>

                            <el-tab-pane label="Content" v-if="props.row.meta_data.response.jsonCopy !== null">
                                <v-jsoneditor
                                    ref="jsonEditor"
                                    v-model="props.row.meta_data.response.jsonCopy"
                                    :options="options"
                                    :plus="true"
                                    :height="height"
                                    @error="onError"
                                >
                                </v-jsoneditor>
                            </el-tab-pane>

                            <el-tab-pane label="Response">
                                <pre class="code-block" v-text="handleResponse(props.row.meta_data.response)"></pre>
                            </el-tab-pane>
                            <el-tab-pane label="Extractors">
                                <template v-if="props.row.meta_data.extractors.length !== 0">
                                    <el-table :data="props.row.meta_data.extractors" stripe border style="width: 100%">
                                        <el-table-column
                                            prop="output_variable_name"
                                            label="输出的变量名"
                                            width="130"
                                        ></el-table-column>
                                        <el-table-column
                                            prop="extract_expr"
                                            label="取值表达式"
                                            width="300"
                                        ></el-table-column>
                                        <el-table-column prop="actual_value" label="实际值">
                                            <template slot-scope="scope">
                                                {{ scope.row.actual_value }}
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </template>
                                <template v-else>
                                    <i class="el-icon-warning centered-content"
                                        >暂无提取器, 提取出来的变量可以用来验证和传递给下面的步骤哦，去加一个试试吧~</i
                                    >
                                </template>
                            </el-tab-pane>

                            <el-tab-pane label="Validators">
                                <template v-if="props.row.meta_data.validators.length !== 0">
                                    <el-table :data="props.row.meta_data.validators" stripe border style="width: 100%">
                                        <el-table-column prop="check_result" label="是否通过" width="80">
                                            <template slot-scope="scope">
                                                <span v-if="scope.row.check_result === 'pass'">✅</span>
                                                <span v-else>❌</span>
                                            </template>
                                        </el-table-column>
                                        <el-table-column prop="check" label="取值表达式" width="150"></el-table-column>
                                        <el-table-column
                                            prop="check_value"
                                            label="实际值"
                                            :formatter="checkValueFormatter"
                                        ></el-table-column>
                                        <el-table-column prop="comparator" label="比较器"></el-table-column>
                                        <el-table-column
                                            prop="expect"
                                            label="期望值"
                                            :formatter="expectValueFormatter"
                                        ></el-table-column>
                                        <el-table-column prop="validate_msg" label="验证信息"></el-table-column>
                                        <el-table-column
                                            prop="desc"
                                            label="描述"
                                            :formatter="descValueFormatter"
                                        ></el-table-column>
                                    </el-table>
                                </template>
                                <template v-else>
                                    <div class="centered-content">
                                        <i class="el-icon-warning"
                                            >暂无验证器或者解析验证器异常了， 验证器可以使用例更加健壮哦，
                                            去加一个试试吧~</i
                                        >
                                    </div>
                                </template>
                            </el-tab-pane>

                            <el-tab-pane label="Logs">
                                <el-timeline>
                                    <el-timeline-item
                                        v-for="(log, index) in props.row.meta_data.logs"
                                        :key="index"
                                        :color="getLogColor(log)"
                                    >
                                        {{ log }}
                                    </el-timeline-item>
                                </el-timeline>
                            </el-tab-pane>

                            <el-tab-pane label="Exception">
                                <template v-if="props.row.attachment && props.row.attachment !== ''">
                                    <pre class="code-block" v-html="props.row.attachment"></pre>
                                </template>
                                <template v-else>
                                    <div class="centered-content">
                                        <i class="el-icon-warning">莫慌，没有异常呢~~~</i>
                                    </div>
                                </template>
                            </el-tab-pane>
                        </el-tabs>
                    </template>
                </el-table-column>

                <el-table-column label="名 称">
                    <template slot-scope="scope">
                        <span>{{ scope.row.name }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="请求地址">
                    <template slot-scope="scope">
                        <span>{{ scope.row.meta_data.request.url }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="请求方法" width="100px">
                    <template slot-scope="scope">
                        <span :class="scope.row.meta_data.request.method">{{
                            scope.row.meta_data.request.method
                        }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="响应时间 (ms)" width="130px">
                    <template slot-scope="scope">
                        <span>{{ scope.row.meta_data.response.elapsed_ms }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="测试结果" width="100px">
                    <template slot-scope="scope">
                        <div :class="scope.row.status">{{ scope.row.status }}</div>
                    </template>
                </el-table-column>

                <el-table-column label="Convert" width="200px">
                    <template slot-scope="scope">
                        <!--                        <el-popover placement="right-start" width="400" trigger="hover">-->
                        <!--                            <pre class="code-block">{{ scope.row.meta_data.boomer }}</pre>-->
                        <!--                            <el-button slot="reference" round type="text"-->
                        <!--                                       @click="copyDataText(scope.row.meta_data.boomer, 'boomer')">boomer-->
                        <!--                            </el-button>-->
                        <!--                        </el-popover>-->
                        <el-popover placement="right-start" width="400" trigger="hover">
                            <pre class="code-block">{{ scope.row.meta_data.curl }}</pre>
                            <el-button
                                slot="reference"
                                round
                                type="text"
                                @click="copyDataText(scope.row.meta_data.curl, 'curl')"
                                >curl
                            </el-button>
                        </el-popover>
                    </template>
                </el-table-column>
            </el-table>
        </slot>
    </div>
</template>

<script>
import VJsoneditor from 'v-jsoneditor'

export default {
    name: 'DebugReport',
    components: {
        VJsoneditor
    },
    props: {
        summary: {
            require: true
        }
    },
    data() {
        let self = this
        return {
            jsonPathOrValue: '',
            expandedRows: [],
            options: {
                onModeChange(newMode, oldMode) {
                    if (newMode === 'view') {
                        self.$refs.jsonEditor[0].editor.expandAll()
                    }
                },
                onEvent: function(node, event) {
                    if (event.type === 'click') {
                        let value = node.value
                        // 当前点击的位置有value，复制value
                        if (value) {
                            self.jsonPathOrValue = value
                            self.copyData('复制json value成功')
                        } else {
                            // 当前点击的位置是key，复制key的jsonpath
                            let arr = node.path
                            arr.unshift('content')
                            self.jsonPathOrValue = arr.join('.')
                            self.copyData('复制jsonpath成功')
                        }
                    }
                },
                mode: 'view',
                modes: ['view', 'code'] // allowed modes
            }
        }
    },
    computed: {
        height() {
            return (window.screen.height - 464).toString() + 'px'
        }
    },
    methods: {
        getLogColor(log) {
            if (log.includes('ERROR')) {
                return 'red'
            } else if (log.includes('WARN')) {
                return 'yellow'
            } else if (log.includes('INFO')) {
                return 'green'
            } else {
                return 'blue' // 默认颜色，可以根据需要修改
            }
        },
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
            let parsedValue = ''
            switch (typeof value) {
                case 'object':
                    parsedValue = JSON.stringify(value)
                    break
                case 'boolean':
                    if (value === true) {
                        parsedValue = 'True'
                    } else {
                        parsedValue = 'False'
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
        tableRowClassName({ row, rowIndex }) {
            row.row_index = rowIndex
        },
        handleClick(tab, event) {
            // TODO 修复产生2个editor
            if (tab.label === 'Content') {
                for (let i = 0; i < this.expandedRows; i++) {
                    this.$refs.jsonEditor[i * 2].editor.expandAll()
                }
            }
        },
        copyDataText(text, title) {
            this.$copyText(text).then(
                e => {
                    this.$notify.success({
                        title: 'copy ' + title,
                        message: text,
                        duration: 2000
                    })
                },
                function(e) {
                    this.$notify.error({
                        title: '复制' + title + '失败',
                        message: e,
                        duration: 2000
                    })
                }
            )
        },
        copyData(title) {
            this.$copyText(this.jsonPathOrValue).then(
                e => {
                    this.$notify.success({
                        title: title,
                        message: this.jsonPathOrValue,
                        duration: 2000
                    })
                },
                function(e) {
                    this.$notify.error({
                        title: '复制提取路径错误',
                        message: e,
                        duration: 2000
                    })
                }
            )
        },

        onError() {
            console.log('error')
        },
        handleRequest(request) {
            const keys = ['start_timestamp']

            keys.forEach(function(item) {
                delete request[item]
            })
            try {
                request['body'] = JSON.parse(request['body'])
            } catch (e) {}

            return request
        },

        handleContent(content) {
            try {
                content = JSON.parse(content)
            } catch (e) {}
            return content
        },

        handleResponse(response) {
            const keys = [
                'response_time_ms',
                'encoding',
                'ok',
                'reason',
                'url',
                'text',
                'json',
                'content_size',
                'content_type'
            ]

            keys.forEach(function(item) {
                delete response[item]
            })
            return response
        }
    }
}
</script>

<style scoped>
pre {
    white-space: pre-wrap;
    word-wrap: break-word;
}

.centered-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%; /* 根据你的需要调整高度 */
    width: 100%; /* 根据你的需要调整宽度 */
    text-align: center;
}

.popover-content {
    display: flex;
    justify-content: space-between;
}

.json-editor {
    width: 50%;
    padding-right: 10px;
}

.timeline-container {
    padding-left: 10px;
    width: 50%;
    overflow-y: auto;
}

.section-title {
    text-align: center;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
