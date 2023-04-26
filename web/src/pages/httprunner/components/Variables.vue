<template>

    <el-table
        highlight-current-row
        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
        strpe
        :height="height"
        :data="tableData"
        style="width: 100%;"
        @cell-mouse-enter="cellMouseEnter"
        @cell-mouse-leave="cellMouseLeave"
    >
        <el-table-column
            label="变量名"
            width="250">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.key" placeholder="Key"></el-input>
            </template>
        </el-table-column>

        <el-table-column
            label="类型"
            width="120">
            <template slot-scope="scope">

                <el-select v-model="scope.row.type">
                    <el-option
                        v-for="item in dataTypeOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>

            </template>
        </el-table-column>

        <el-table-column
            label="变量值"
            width="375">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.value" placeholder="Value"></el-input>
            </template>
        </el-table-column>

        <el-table-column
            label="内容"
            width="375">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.desc" placeholder="变量简要描述"></el-input>
            </template>
        </el-table-column>

        <el-table-column>
            <template slot-scope="scope">
                <el-row v-show="scope.row === currentRow">
                    <el-button
                        icon="el-icon-circle-plus-outline"
                        size="mini"
                        type="info"
                        title="增加变量"
                        @click="handleEdit(scope.$index, scope.row)">
                    </el-button>
                    <el-button
                        icon="el-icon-document-copy"
                        size="mini"
                        type="info"
                        title="复制变量"
                        @click="handleCopy(scope.$index, scope.row)">
                    </el-button>
                    <el-button
                        icon="el-icon-delete"
                        size="mini"
                        type="danger"
                        title="删除变量"
                        v-show="scope.$index !== 0"
                        @click="handleDelete(scope.$index, scope.row)">
                    </el-button>
                </el-row>

            </template>
        </el-table-column>
    </el-table>

</template>

<script>
export default {
    name: "Variables",

    props: {
        save: Boolean,
        variables: {
            require: false
        }
    },
    computed: {
        height() {
            return window.screen.height - 440
        }
    },

    watch: {
        save: function () {
            this.$emit('variables', this.parseVariables(), this.tableData);
        },

        variables: function () {
            if (this.variables.length !== 0) {
                this.tableData = this.variables;
            }
        }
    },

    methods: {
        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        },

        handleEdit(index, row) {
            this.tableData.splice(index + 1, 0, {
                key: '',
                value: '',
                type: 1,
                desc: ''
            })
            //
            // this.tableData.push({
            //     key: '',
            //     value: '',
            //     type: 1,
            //     desc: ''
            // });
        },
        handleCopy(index, row) {
            this.tableData.splice(index + 1, 0, {
                key: row.key,
                value: row.value,
                type: row.type,
                desc: row.desc
            });
        },
        handleDelete(index, row) {
            this.tableData.splice(index, 1);
        },

        // 类型转换
        parseType(type, value) {
            let tempValue;
            const msg = value + ' => ' + this.dataTypeOptions[type - 1].label + ' 转换异常, 该数据自动剔除';
            switch (type) {
                case 1:
                    tempValue = value;
                    break;
                case 2:
                    // 包含$是引用类型,可以任意类型
                    if (value.indexOf("$") != -1) {
                        tempValue = value
                    } else {
                        tempValue = parseInt(value);
                    }
                    break;
                case 3:
                    tempValue = parseFloat(value);
                    break;
                case 4:
                    if (value === 'False' || value === 'True') {
                        let bool = {
                            'True': true,
                            'False': false
                        };
                        tempValue = bool[value];
                    } else {
                        this.$notify.error({
                            title: '类型转换错误',
                            message: msg,
                            duration: 2000
                        });
                        return 'exception'
                    }
                    break;
                case 5:
                case 6:
                    try {
                        tempValue = JSON.parse(value);
                    } catch (err) {
                        // 包含$是引用类型,可以任意类型
                        if (value.indexOf("$") != -1) {
                            tempValue = value
                        } else {
                            tempValue = false
                        }
                    }
                    break;
            }
            if (tempValue !== 0 && !tempValue && type !== 4 && type !== 1) {
                this.$notify.error({
                    title: '类型转换错误',
                    message: msg,
                    duration: 2000
                });
                return 'exception'
            }
            return tempValue;
        },

        //变量格式化variables
        parseVariables() {
            let variables = {
                variables: [],
                desc: {}
            };
            for (let content of this.tableData) {
                if (content['key'] !== '') {
                    let obj = {};
                    const value = this.parseType(content['type'], content['value']);
                    if (value === 'exception') {
                        continue;
                    }
                    obj[content['key']] = value;
                    variables.variables.push(obj);
                    variables.desc[content['key']] = content['desc'];
                }
            }
            return variables;
        },
    },
    data() {
        return {
            currentRow: '',
            tableData: [{
                key: '',
                value: '',
                type: 1,
                desc: ''
            }],

            dataTypeOptions: [{
                label: 'String',
                value: 1
            }, {
                label: 'Integer',
                value: 2
            }, {
                label: 'Float',
                value: 3
            }, {
                label: 'Boolean',
                value: 4
            }, {
                label: 'List',
                value: 5
            }, {
                label: 'Dict',
                value: 6
            }],

            dataType: 'data'
        }
    }
}
</script>

<style scoped>

</style>
