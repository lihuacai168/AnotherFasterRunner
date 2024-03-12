<script>
import {datetimeObj2str} from "@/util/format";

export default {
    data() {
        return {

            tableConfig: {
                url: '/api/mock/mock_project',
                dataPath: "results",
                totalPath: "count",
                paginationSize: 10,
                operationButtonType: 'button',
                canDelete: () => false,
                form: [
                    {
                        type: 'input',
                        id: 'project_name',
                        label: '项目名称',
                        rules: [
                            {
                                required: true,
                                message: '请输入项目名称',
                                trigger: 'blur',
                                transform: v => v && v.trim()
                            }
                        ],
                        el: {placeholder: '请输入项目名称'}
                    },
                    {
                        type: 'input',
                        id: 'project_desc',
                        label: '项目描述',
                        rules: [
                            {
                                required: true,
                                message: '请输入项目描述',
                                trigger: 'blur',
                                transform: v => v && v.trim()
                            }
                        ],
                        el: {placeholder: '请输入项目描述'}
                    },
                ],
                searchForm: [
                    {
                        type: 'input',
                        id: 'project_name',
                        label: '项目名称',
                        el: {
                            placeholder: '请输入所属项目名称',
                        },

                    },
                ],
                columns: [
                    {
                        prop: 'project_name',
                        label: '项目名称'
                    },
                    {
                        prop: 'project_desc',
                        label: '项目名称'
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
                onEdit: (data, row) => {
                    return this.$axios.put(
                        `${this.tableConfig.url}/${data.id}`,
                        data
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
                        data
                    ).catch(error => {
                        if (error.response) {
                            this.$message.error(`接口返回错误：${JSON.stringify(error.response.data)}`);
                        }
                        throw error;
                    });
                },
            }
        }
    }
}
</script>

<template>
    <el-data-table v-bind="tableConfig" style="margin: 10px">
    </el-data-table>
</template>

<style scoped>

</style>
