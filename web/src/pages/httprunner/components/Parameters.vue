<template>
    <el-table
        highlight-current-row
        :height="height"
        :data="tableData"
        style="width: 100%;"
        :border="false"
        @cell-mouse-enter="cellMouseEnter"
        @cell-mouse-leave="cellMouseLeave"
        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
    >
        <el-table-column
            label="数据Key">
            <template slot-scope="scope">
                <el-input
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 10}"
                    clearable
                    v-model="scope.row.key"
                    placeholder="key 、 key-key1"
                ></el-input>
            </template>
        </el-table-column>

        <el-table-column
            label="数据内容">
            <template slot-scope="scope">
                <el-input
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 8}"
                    clearable
                    v-model="scope.row.value"
                    placeholder="${ fun() } 、 [ value ] 、 [ [ value1, value2 ] ]"
                ></el-input>
            </template>
        </el-table-column>

        <el-table-column
            label="参数描述"
            width="200">
            <template slot-scope="scope">
                <el-input clearable v-model="scope.row.desc" placeholder="参数简要描述"></el-input>
            </template>
        </el-table-column>

        <el-table-column width="120">
            <template slot-scope="scope">
                <el-row v-show="scope.row === currentRow">
                    <el-button
                        icon="el-icon-circle-plus-outline"
                        size="mini"
                        type="info"
                        @click="handleEdit(scope.$index, scope.row)">
                    </el-button>

                    <el-button
                        icon="el-icon-delete"
                        size="mini"
                        style="margin-left: 0;"
                        type="danger"
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
    props: {
        save: Boolean,
        parameters: {
            require: false
        }
    },
    computed: {
        height() {
            return window.screen.height - 440
        }
    },
    methods: {
        parseParameters() {
            let parameters = {
                parameters: [],
                desc: {}
            };
            for (let content of this.tableData) {
                let value = content['value'];
                const key = content['key'];
                let obj = {};
                if (key !== '' && value !== '') {
                    try {
                        value = JSON.parse(value);
                    } catch (err) {
                    }
                    obj[key] = value;
                    parameters.parameters.push(obj);
                    parameters.desc[key] = content.desc;
                }
            }
            return parameters;
        },

        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        },

        handleEdit(index, row) {
            this.tableData.push({
                key: '',
                value: '',
                desc: ''
            });
        },

        handleDelete(index, row) {
            this.tableData.splice(index, 1);
        },

    },
    watch: {
        save: function () {
            this.$emit('parameters', this.parseParameters(), this.tableData);
        },

        parameters: function () {
            if (this.parameters.length !== 0) {
                this.tableData = this.parameters;
            }
        }
    },
    data() {
        return {
            currentRow: '',
            tableData: [{key: '', value: '', desc: ''}]
        }
    },
    name: "Parameters"
}
</script>

<style scoped>
</style>
