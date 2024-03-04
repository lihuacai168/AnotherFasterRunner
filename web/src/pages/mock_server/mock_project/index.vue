<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button @click="showCreateProjectModal=true" type="success" size="small">新增Mock项目</el-button>
                    <!-- 新增项目模态框 -->
                    <el-dialog :visible.sync="showCreateProjectModal" title="新增项目">
                        <el-form :model="newProject">
                            <el-form-item label="项目名称" :label-width="formLabelWidth">
                                <el-input v-model.trim="newProject.project_name"
                                          placeholder="请输入项目名称"></el-input>
                            </el-form-item>
                            <el-form-item label="项目描述" :label-width="formLabelWidth">
                                <el-input
                                    type="textarea"
                                    v-model.trim="newProject.project_desc"
                                    placeholder="请输入项目描述"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="是否激活" :label-width="formLabelWidth">
                                <el-switch v-model="newProject.is_active"></el-switch>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="createProject()">创建</el-button>
                            </el-form-item>
                        </el-form>
                    </el-dialog>
                </div>
            </div>
        </el-header>
        <el-container>
            <el-header>
                <div style="padding-top: 2px; display: flex">
                    <div>
                        <!-- 查询表单 -->
                        <el-form :inline="true" @submit.native.prevent="fetchProjectList">
                            <el-form-item>
                                <el-input v-model="search.project_name" placeholder="项目名称"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="search.project_desc" placeholder="项目描述"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="search.creator" placeholder="创建者"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="fetchProjectList">查询</el-button>
                                <el-button type="info" @click="resetSearch">重置查询</el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                    <div style="display: flex; justify-content: center; padding-top: 5px">
                        <el-pagination
                            :page-size="pageSize"
                            v-show="projects_count !== 0 "
                            background
                            @current-change="handleCurrentChange"
                            :current-page.sync="currentPage"
                            layout="total, prev, pager, next, jumper"
                            :total="projects_count"
                        >
                        </el-pagination>
                    </div>
                </div>
            </el-header>
            <el-main style="padding: 0; margin-left: 1px; margin-top: 10px;">
                <div style="position: fixed; bottom: 0; right:0; left: 230px; top: 150px">

                    <!-- 项目列表 -->
                    <el-row :gutter="20">
                        <el-table :data="projects" style="width: 100%">

                            <el-table-column label="项目名称" width="180">
                                <template slot-scope="scope">
                                    <el-tag color="#2C3E50" style="color: white">{{ scope.row.project_name }}</el-tag>
                                </template>
                            </el-table-column>

                            <el-table-column label="项目描述">
                                <template slot-scope="scope">
                                    <div>{{ scope.row.project_desc }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column label="最后更新人" width="120">
                                <template slot-scope="scope">
                                    <div>{{ scope.row.updater }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column label="更新时间" width="180">
                                <template slot-scope="scope">
                                    <div>{{ datetimeObj2str(scope.row.update_time) }}</div>
                                </template>
                            </el-table-column>

                            <el-table-column label="操作" width="180">
                                <template slot-scope="scope">
                                    <el-button
                                        type="primary"
                                        size="mini"
                                        @click="showEditProjectModalHandle(scope.row)"
                                    >编辑
                                    </el-button>
                                    <el-button
                                        type="danger"
                                        size="mini"
                                        @click="deleteProject(scope.row.id)"
                                    >删除
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-row>

                    <!-- 编辑项目模态框 -->
                    <el-dialog :visible.sync="showEditProjectModal.visible" title="编辑项目">
                        <el-form :model="editProjectDetails">
                            <el-form-item label="项目名称" :label-width="formLabelWidth">
                                <el-input v-model.trim="editProjectDetails.project_name"
                                          placeholder="请输入项目名称"></el-input>
                            </el-form-item>
                            <el-form-item label="项目描述" :label-width="formLabelWidth">
                                <el-input
                                    type="textarea"
                                    v-model.trim="editProjectDetails.project_desc"
                                    placeholder="请输入项目描述"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="是否激活" :label-width="formLabelWidth">
                                <el-switch v-model="editProjectDetails.is_active"></el-switch>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="editProject()">保存修改</el-button>
                            </el-form-item>
                        </el-form>
                    </el-dialog>
                </div>
            </el-main>

        </el-container>
    </el-container>
</template>

<script>
import {datetimeObj2str} from "@/util/format";

export default {
    data() {
        return {
            showCreateProjectModal: false, // 控制创建项目模态框的显示
            newProject: { // 新项目的数据模型
                project_name: '',
                project_desc: '',
                is_active: true,
            },
            formLabelWidth: '120px', // 表单标签宽度

            projects: [], // 项目列表数据
            projects_count: 0,
            currentPage: 1,
            pageSize: 11,
            search: { // 搜索条件
                project_name: '',
                project_desc: '',
                creator: '',
                page: this.currentPage
            },
            showEditProjectModal: {visible: false, data: null}, // 控制编辑项目模态框的显示和数据
            editProjectDetails: { // 编辑项目的数据模型
                id: '',
                project_name: '',
                project_desc: '',
                is_active: true,
            },
        };
    },
    // 页面加载时拉取项目列表
    created() {
        this.fetchProjectList();
    },
    methods: {
        datetimeObj2str,
        handleCurrentChange() {
            this.fetchProjectList()
        },
        fetchProjectList() {
            const params = {
                project_name: this.search.project_name,
                project_desc: this.search.project_desc,
                creator: this.search.creator,
                page: this.currentPage,
                size: this.pageSize,
            };
            this.$api.getMockProject({params: params})
                .then(response => {
                    this.projects = response.results;
                    this.projects_count = response.count;
                })
                .catch(error => {
                    this.$message.error('项目列表获取失败');
                });
        },
        createProject() {
            // 这里你需要根据你的API端点去提交数据
            // 这个例子假设你的API端点是 '/api/projects/'
            this.$api.createMockProject(this.newProject)
                .then(response => {
                    // 处理成功响应
                    this.$message.success('项目创建成功');
                    this.showCreateProjectModal = false;
                    this.fetchProjectList()
                    // 更新项目列表 (可以直接添加到列表或者重新获取列表)
                })
                .catch(error => {
                    // 处理出错情况
                    this.$message.error('项目创建失败');
                });
        },

        resetSearch() {
            // 重置搜索条件
            this.search = {
                project_name: '',
                project_desc: '',
                creator: '',
            };
            this.currentPage = 1;
            // 重新获取项目列表
            this.fetchProjectList();
        },
        showEditProjectModalHandle(project) {
            this.editProjectDetails = {...project}; // Deep copy project object to form
            console.log(this.editProjectDetails)
            this.showEditProjectModal.visible = true; // Open modal
        },
        editProject() {
            const editedProject = {...this.editProjectDetails};
            // Call your API to update the project
            console.log(editedProject.project_id)
            this.$api.updateMockProject(editedProject.id, editedProject)
                .then(() => {
                    this.$message.success('项目更新成功');
                    this.showEditProjectModal.visible = false;
                    this.fetchProjectList();
                })
                .catch(() => {
                    this.$message.error('项目更新失败');
                });
        },
        deleteProject(projectId) {
            // Call your API to delete the project
            this.$confirm('确定删除这个项目吗?', '警告', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$api.deleteMockProject(projectId)
                    .then(() => {
                        this.$message.success('项目删除成功');
                        this.fetchProjectList();
                    })
                    .catch(() => {
                        this.$message.error('项目删除失败');
                    });
            }).catch(() => {
                this.$message.info('已取消删除');
            });
        },
    }
};
</script>
