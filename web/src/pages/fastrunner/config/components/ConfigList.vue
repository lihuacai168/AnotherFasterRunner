<template>
    <el-container>
        <el-header style="padding-top: 10px; height: 50px; overflow-x: hidden">
            <div>
                <el-row :gutter="50">
                    <el-col :span="6" v-if="configData.count > 11">
                        <el-input placeholder="请输入配置名称" clearable v-model="search">
                            <el-button slot="append" icon="el-icon-search" @click="getConfigList"></el-button>
                        </el-input>
                    </el-col>
                    <el-col :span="7">
                        <el-pagination
                            :page-size="11"
                            v-show="configData.count !== 0 "
                            background
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="configData.count"
                        >
                        </el-pagination>
                    </el-col>
                </el-row>
            </div>
        </el-header>

        <el-container>
            <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                <div style="position: fixed; bottom: 0; right:0; left: 220px; top: 150px">
                    <el-table
                        highlight-current-row
                        :data="configData.results"
                        :show-header="configData.results.length !== 0 "
                        stripe
                        height="calc(100%)"
                        @cell-mouse-enter="cellMouseEnter"
                        @cell-mouse-leave="cellMouseLeave"
                        @selection-change="handleSelectionChange"
                    >
                        <el-table-column
                            type="selection"
                            width="55"
                        >
                        </el-table-column>

                        <el-table-column
                            label="配置名称"

                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.name }}</div>
                            </template>
                        </el-table-column>

                        <el-table-column

                            label="基本请求地址"
                        >
                            <template slot-scope="scope">
                                <div v-text="scope.row.base_url === '' ? '无' : scope.row.base_url"></div>

                            </template>
                        </el-table-column>

                        <el-table-column
                            width="90"
                            label="是否为默认"
                        >
                            <template slot-scope="scope">
                                <el-switch
                                    disabled
                                    v-model="scope.row.is_default"
                                    active-color="#13ce66"
                                >
                                </el-switch>
                            </template>
                        </el-table-column>

                        <el-table-column

                            label="更新时间"
                        >
                            <template slot-scope="scope">
                                <div>{{ scope.row.update_time|datetimeFormat }}</div>

                            </template>
                        </el-table-column>

                        <el-table-column

                        >
                            <template slot-scope="scope">
                                <el-row v-show="currentRow === scope.row">
                                    <el-button
                                        type="info"
                                        icon="el-icon-edit"
                                        title="编辑"
                                        circle size="mini"
                                        @click="handleEditConfig(scope.row)"
                                    ></el-button>

                                    <el-button
                                        type="success"
                                        icon="el-icon-document"
                                        circle size="mini"
                                        @click="handleCopyConfig(scope.row.id, scope.row.name)"
                                    >
                                    </el-button>

                                    <el-button
                                        type="danger"
                                        icon="el-icon-delete"
                                        title="删除"
                                        circle size="mini"
                                        @click="handleDelConfig(scope.row.id)"
                                    >
                                    </el-button>
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
export default {
    name: "ConfigList",
    props: {
        back: Boolean,
        project: {
            require: true
        },
        del: Boolean
    },
    data() {
        return {
            search: '',
            selectConfig: [],
            currentRow: '',
            currentPage: 1,
            configData: {
                count: 0,
                results: []
            }
        }
    },
    watch: {
        back() {
            this.getConfigList();
        },

        del() {
            if (this.selectConfig.length !== 0) {
                this.$confirm('此操作将永久删除配置，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    this.$api.delAllConfig({data: this.selectConfig}).then(resp => {
                        if (resp.success) {
                            this.getConfigList();
                        } else {
                            this.$message.error(resp.msg);
                        }
                    })
                })
            } else {
                this.$notify.warning({
                    title: '提示',
                    message: '请至少勾选一个配置',
                    duration: this.$store.state.duration
                })
            }
        }
    },

    methods: {
        handleSelectionChange(val) {
            this.selectConfig = val;
        },

        handleCurrentChange(val) {
            this.$api.getConfigPaginationBypage({
                params: {
                    page: this.currentPage,
                    project: this.project,
                    search: this.search
                }
            }).then(resp => {
                this.configData = resp;
            })
        },

        //删除api
        handleDelConfig(index) {
            this.$confirm('此操作将永久删除该配置，是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                this.$api.deleteConfig(index).then(resp => {
                    if (resp.success) {
                        this.getConfigList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
        },

        handleEditConfig(row) {
            this.$emit('respConfig', row);
        },

        handleCopyConfig(id, name) {
            this.$prompt('请输入配置名称', '提示', {
                confirmButtonText: '确定',
                inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/,
                inputErrorMessage: '配置名称不能为空',
                inputValue: name
            }).then(({value}) => {
                this.$api.copyConfig(id, {
                    'name': value
                }).then(resp => {
                    if (resp.success) {
                        this.getConfigList();
                    } else {
                        this.$message.error(resp.msg);
                    }
                })
            })
        },

        cellMouseEnter(row) {
            this.currentRow = row;
        },

        cellMouseLeave(row) {
            this.currentRow = '';
        },

        getConfigList() {
            this.$api.configList({
                params: {
                    project: this.project,
                    search: this.search
                }
            }).then(resp => {
                this.configData = resp;
            })
        },
    },
    mounted() {
        this.getConfigList();
    }
}
</script>

<style scoped>


</style>
