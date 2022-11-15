<template>
  <el-container>
    <el-header style="background: #fff; padding: 10px 10px; height: 50px">
      <div class="report__header">
        <div class="report__header--item">
          <el-input
            placeholder="请输入报告名称"
            size="medium"
            clearable
            v-model="search"
            style="width: 260px"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getReportList"
            ></el-button>
          </el-input>
        </div>
        <div class="report__header--item">
          <el-dropdown @command="reportTypeChangeHandle">
            <el-button type="primary" size="medium">
              类型
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="1">调试</el-dropdown-item>
              <el-dropdown-item command="3">定时</el-dropdown-item>
              <el-dropdown-item command="4">部署</el-dropdown-item>
              <el-dropdown-item command="2">异步</el-dropdown-item>
              <el-dropdown-item command="">全部</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <div class="report__header--item">
          <el-dropdown @command="reportStatusChangeHandle">
            <el-button type="primary" size="medium">
              结果
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="0">失败</el-dropdown-item>
              <el-dropdown-item command="1">成功</el-dropdown-item>
              <el-dropdown-item command="">全部</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>

        <div class="report__header--item">
          <el-button type="primary" size="medium" @click="resetSearch"
            >重置</el-button
          >
        </div>

        <el-switch
          style="margin-left: 20px"
          v-model="onlyMe"
          active-color="#13ce66"
          inactive-color="#ff4949"
          active-text="只看我的"
        >
        </el-switch>

        <div class="report__header--item">
          <el-button
            v-if="true"
            :title="'删除'"
            v-show="reportData.count !== 0"
            style="margin-left: 20px"
            type="danger"
            icon="el-icon-delete"
            circle
            size="mini"
            @click="delSelectionReports"
          ></el-button>
        </div>

        <!--        <div class="report__header&#45;&#45;item">-->
        <!--          <el-pagination-->
        <!--            :page-size="11"-->
        <!--            v-show="reportData.count !== 0"-->
        <!--            background-->
        <!--            @current-change="handleCurrentChange"-->
        <!--            :current-page.sync="currentPage"-->
        <!--            layout="total, prev, pager, next, jumper"-->
        <!--            :total="reportData.count"-->
        <!--          >-->
        <!--          </el-pagination>-->
        <!--        </div>-->
      </div>
    </el-header>

    <el-container>
      <el-main style="padding: 0; margin-left: 10px">
        <el-dialog
          v-if="dialogTableVisible"
          :visible.sync="dialogTableVisible"
          width="70%"
        >
          <report :summary="summary"></report>
        </el-dialog>

        <el-table
          style="width: 100%; height: auto"
          highlight-current-row
          :data="reportData.results"
          :show-header="reportData.results.length !== 0"
          stripe
          max-height="800px"
          @cell-mouse-enter="cellMouseEnter"
          @cell-mouse-leave="cellMouseLeave"
          @selection-change="handleSelectionChange"
          v-loading="loading"
        >
          <el-table-column type="selection" width="45"> </el-table-column>

          <el-table-column label="报告类型" width="100">
            <template v-slot="scope">
              <el-tag color="#2C3E50" style="color: white">{{
                scope.row.type
              }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="报告名称">
            <template v-slot="scope">
              <div>{{ scope.row.name }}</div>
            </template>
          </el-table-column>

          <el-table-column label="结果" width="60">
            <template v-slot="scope">
              <div
                :class="{
                  pass: scope.row.success,
                  fail: !scope.row.success,
                }"
                v-text="scope.row.success === true ? '通过' : '失败'"
              ></div>
            </template>
          </el-table-column>
          <el-table-column label="创建人" width="80">
            <template v-slot="scope">
              <div>{{ scope.row.creator }}</div>
            </template>
          </el-table-column>

          <el-table-column label="测试时间" width="180">
            <template v-slot="scope">
              <div>
                {{ scope.row.time.start_at | timestampToTime }}
              </div>
            </template>
          </el-table-column>

          <el-table-column label="耗时" width="100">
            <template v-slot="scope">
              <div v-text="scope.row.time.duration.toFixed(3) + ' 秒'"></div>
            </template>
          </el-table-column>

          <el-table-column width="80" label="总计接口">
            <template v-slot="scope">
              <el-tag>{{ scope.row.stat.testsRun }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column width="60" label="通过">
            <template v-slot="scope">
              <el-tag type="success"> {{ scope.row.stat.successes }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column width="60" label="失败">
            <template v-slot="scope">
              <el-tag type="danger">{{ scope.row.stat.failures }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column width="60" label="异常">
            <template v-slot="scope">
              <el-tag type="warning">{{ scope.row.stat.errors }}</el-tag>
            </template>
          </el-table-column>

          <!--                        <el-table-column-->
          <!--                            width="80"-->
          <!--                            label="跳过"-->
          <!--                        >-->
          <!--                            <template slot-scope="scope">-->
          <!--                                <el-tag type="info">{{ scope.row.stat.skipped }}</el-tag>-->
          <!--                            </template>-->
          <!--                        </el-table-column>-->

          <!--                        <el-table-column-->
          <!--                            label="系统信息"-->
          <!--                        >-->
          <!--                            <template slot-scope="scope">-->
          <!--                                <el-popover trigger="hover" placement="top">-->
          <!--                                    <p>HttpRunner: {{ scope.row.platform.httprunner_version }}</p>-->
          <!--                                    <p>Platform: {{ scope.row.platform.platform }}</p>-->
          <!--                                    <div slot="reference" class="name-wrapper">-->
          <!--                                        <el-tag size="medium">{{ scope.row.platform.python_version }}</el-tag>-->
          <!--                                    </div>-->
          <!--                                </el-popover>-->
          <!--                            </template>-->
          <!--                        </el-table-column>-->

          <el-table-column label="报告操作" width="120">
            <template v-slot="scope">
              <el-row v-show="currentRow === scope.row">
                <el-button
                  type="info"
                  icon="el-icon-refresh-right"
                  circle
                  size="mini"
                  title="重新运行失败用例"
                  v-show="handleShowRerun(scope.row)"
                  @click="handleRunFailCase(scope.row)"
                >
                </el-button>
                <el-button
                  type="info"
                  icon="el-icon-view"
                  title="查看"
                  circle
                  size="mini"
                  style="margin-left: 5px"
                  @click="handleWatchReports(scope.row.id)"
                >
                </el-button>

                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  title="删除"
                  circle
                  size="mini"
                  style="margin-left: 5px"
                  @click="handleDelReports(scope.row.id)"
                >
                </el-button>
              </el-row>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-footer>
        <div style="margin: 5px 5px">
          <el-pagination
            :page-size="11"
            v-show="reportData.count !== 0"
            background
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            layout="total, prev, pager, next, jumper"
            :total="reportData.count"
          >
          </el-pagination>
        </div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script>
import Report from "./DebugReport.vue";

export default {
  components: {
    Report,
  },
  data() {
    return {
      search: "",
      selectReports: [],
      currentRow: "",
      currentPage: 1,
      onlyMe: !this.$store.state.is_superuser,
      isSuperuser: this.$store.state.is_superuser,
      // (1, "调试"),
      //     (2, "异步"),
      //     (3, "定时"),
      //     (4, "部署"),
      //     ("", "全部"),
      reportType: "",
      reportStatus: "",
      reportData: {
        count: 0,
        results: [],
      },
      dialogTableVisible: false,
      summary: {},
      loading: false,
    };
  },

  watch: {
    search() {
      this.getReportList();
    },

    onlyMe() {
      this.getReportList();
    },
  },

  methods: {
    cellMouseEnter(row) {
      this.currentRow = row;
    },

    cellMouseLeave(row) {
      this.currentRow = "";
    },

    handleWatchReports(index) {
      window.open(this.$api.baseUrl + "/api/fastrunner/reports/" + index + "/");
    },

    handleSelectionChange(val) {
      this.selectReports = val;
    },
    reportTypeChangeHandle(command) {
      this.reportType = command;
      // this.$emit('update:reportType', command);
      // this.search = "";
      this.getReportList();
    },
    reportStatusChangeHandle(command) {
      this.reportStatus = command;
      this.getReportList();
    },
    resetSearch() {
      this.search = "";
      this.reportType = "";
      this.reportStatus = "";
      this.currentPage = 1;
      this.onlyMe = true;
      this.getReportList();
    },
    handleCurrentChange(val) {
      this.$api
        .getReportsPaginationBypage({
          params: {
            project: this.$route.params.id,
            search: this.search,
            reportType: this.reportType,
            reportStatus: this.reportStatus,
            page: this.currentPage,
            onlyMe: this.onlyMe,
          },
        })
        .then((resp) => {
          this.reportData = resp;
        });
    },
    handleRunFailCase(row) {
      this.loading = true;
      this.$api
        .runMultiTest({
          name: row.name,
          project: this.$route.params.id,
          case_config_mapping_list: row.stat.failure_case_config_mapping_list,
        })
        .then((resp) => {
          this.getReportList();
          this.loading = false;
          this.dialogTableVisible = true;
          this.summary = resp;
        })
        .catch((resp) => {
          this.loading = false;
        });
    },

    handleDelReports(index) {
      this.$confirm("此操作将永久删除该测试报告，是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        this.$api.deleteReports(index).then((resp) => {
          if (resp.success) {
            this.getReportList();
          } else {
            this.$message.error(resp.msg);
          }
        });
      });
    },

    delSelectionReports() {
      if (this.selectReports.length !== 0) {
        this.$confirm("此操作将永久删除勾选的测试报告，是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(() => {
          this.$api.delAllReports({ data: this.selectReports }).then((resp) => {
            this.getReportList();
          });
        });
      } else {
        this.$notify.warning({
          title: "提示",
          message: "请至少勾选一个测试报告",
          duration: this.$store.state.duration,
        });
      }
    },
    getReportList() {
      this.$api
        .reportList({
          params: {
            project: this.$route.params.id,
            search: this.search,
            reportType: this.reportType,
            reportStatus: this.reportStatus,
            page: this.currentPage,
            onlyMe: this.onlyMe,
          },
        })
        .then((resp) => {
          this.reportData = resp;
        });
    },
    handleShowRerun(row) {
      try {
        if (
          row.stat.failure_case_config_mapping_list[0].config_name !== undefined
        ) {
          return true;
        }
      } catch (e) {
        return false;
      }
    },
  },
  name: "ReportList",
  mounted() {
    this.getReportList();
  },
};
</script>

<style scoped>
.pass {
  font-weight: bold;
  color: #13ce66;
}

.fail {
  font-weight: bold;
  color: red;
}

.report__header {
  display: flex;
  align-items: center;
}

.report__header--item.is-stench {
  flex: 1;
}

.report__header--item {
  margin: 0 0 0 5px;
}
</style>
