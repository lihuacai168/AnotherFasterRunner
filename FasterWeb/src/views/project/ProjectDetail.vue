<template>
  <el-main>
    <div v-loading="loading" element-loading-text="正在玩命加载">
      <ul class="title-project">
        <li class="title-li" title="Test API Project">
          <b>{{ projectInfo.name }}</b>
          <b class="desc-li">{{ projectInfo.desc }}</b>
        </li>
      </ul>

      <ul class="project_detail" style="display: none">
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe74a;</i> &nbsp;{{ projectInfo.api_count }}
            个接口
          </p>
          <p class="desc-p">接口总数</p>
        </li>
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe61f;</i> &nbsp;{{
              projectInfo.case_step_count
            }}
            个监控接口
          </p>
          <p class="desc-p">监控接口个数</p>
        </li>
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe61e;</i> &nbsp;{{ projectInfo.task_count }}
            项任务
          </p>
          <p class="desc-p">定时任务个数</p>
        </li>

        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe6da;</i> &nbsp;{{ projectInfo.case_count }}
            个用例
          </p>
          <p class="desc-p">用例集总数</p>
        </li>
      </ul>
      <ul class="project_detail" style="display: none">
        <!--            <li class="pull-left">-->
        <!--                <p class="title-p"><i class="iconfont">&#xe609;</i> &nbsp;{{ projectInfo.host_count }} 套环境</p>-->
        <!--                <p class="desc-p">环境总数</p>-->
        <!--            </li>            -->
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe609;</i> &nbsp;{{
              projectInfo.api_cover_rate
            }}% 接口覆盖率
          </p>
          <p class="desc-p">用例步骤和接口总数的比例</p>
        </li>
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe66e;</i> 共
            {{ projectInfo.report_count }} 个报告
            {{ projectInfo.report_success }} 成功,{{ projectInfo.report_fail }}
            失败
          </p>
          <p class="desc-p">测试报告总数</p>
        </li>
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xee32;</i> &nbsp;{{
              projectInfo.config_count
            }}
            套配置
          </p>
          <p class="desc-p">配置总数</p>
        </li>
        <li class="pull-left">
          <p class="title-p">
            <i class="iconfont">&#xe692;</i> &nbsp;{{
              projectInfo.variables_count
            }}
            对变量
          </p>
          <p class="desc-p">全局变量对数</p>
        </li>
      </ul>

      <div style="display: flex; margin: 10px">
        <el-card style="width: 500px; height: 400px; margin-right: 5px">
          <div slot="header">
            <span>API</span>
            <i class="iconfont">&#xe74a;</i>
          </div>
          <el-row type="flex">
            <el-col :span="16">
              <ApexCharts
                :options="apiPieOptions"
                :series="apiPieSeries"
              ></ApexCharts>
            </el-col>
          </el-row>
          <el-row type="flex" justify="end">
            <el-col :span="12">
              <ApexCharts
                :options="apiCoverRateOptions"
                :series="apiCoverRateSeries"
              ></ApexCharts>
            </el-col>
          </el-row>
        </el-card>

        <el-card style="width: 500px; height: 400px">
          <div slot="header">
            <span>Case</span>
            <i class="iconfont">&#xe6da;</i>
          </div>
          <el-row type="flex">
            <el-col :span="16">
              <ApexCharts
                :options="casePieOptions"
                :series="casePieSeries"
              ></ApexCharts>
            </el-col>
          </el-row>

          <el-row type="flex" justify="end">
            <el-col :span="12">
              <ApexCharts
                :options="coreCaseCoverRateOptions"
                :series="coreCaseCoverRateSeries"
              ></ApexCharts>
            </el-col>
          </el-row>
        </el-card>
      </div>

      <div
        style="display: flex; justify-content: space-around; margin-top: 10px"
        v-if="false"
      >
        <el-card style="width: 33%">
          <div slot="header">
            <span>API每日创建</span>
            <i class="iconfont">&#xe74a;</i>
          </div>

          <ApexCharts
            type="area"
            :options="apiAreaOptions"
            :series="apiAreaSeries"
          ></ApexCharts>
        </el-card>
        <el-card style="width: 33%">
          <div slot="header">
            <span>Case每日创建</span>
            <i class="iconfont">&#xe6da;</i>
          </div>
          <ApexCharts
            type="area"
            :options="caseAreaOptions"
            :series="caseAreaSeries"
          ></ApexCharts>
        </el-card>
        <el-card style="width: 33%">
          <div slot="header">
            <span>Report每日创建</span>
            <i class="iconfont">&#xe66e;</i>
            <!--                    TODO 日期选择-->
            <!--                    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>-->
          </div>
          <ApexCharts
            type="area"
            :options="reportAreaOptions"
            :series="reportAreaSeries"
          ></ApexCharts>
        </el-card>
      </div>
      <div style="display: flex; margin: 10px">
        <el-card style="width: 500px; height: 430px; margin-right: 5px">
          <div slot="header">
            <span>Report</span>
            <i class="iconfont">&#xe66e;</i>
          </div>
          <ApexCharts
            :options="reportPieOptions"
            :series="reportPieSeries"
          ></ApexCharts>
        </el-card>
        <el-card style="width: 500px; height: 430px">
          <div slot="header"><span>每日数据</span></div>
          <ApexCharts
            type="area"
            :options="apiAreaOptions"
            :series="[...apiAreaSeries, ...caseAreaSeries, ...reportAreaSeries]"
          ></ApexCharts>
        </el-card>
      </div>
    </div>
  </el-main>
</template>

<script>
export default {
  name: "ProjectDetail",
  data() {
    return {
      loading: false,
      visitInfo: {},
      projectInfo: {},
      apiPieOptions: {
        plotOptions: {
          pie: {
            donut: {
              size: "50%",
              labels: {
                show: true,
                total: { show: true, showAlways: true, label: "Total" },
              },
            },
          },
        },
        show: true,
        chart: { id: "apiPie", type: "donut" },
        // 饼图右上角的分类，会被接口返回值的覆盖
        labels: ["手动创建的API", "从YAPI导入API"],
      },
      apiCoverRateSeries: [],
      coreCaseCoverRateSeries: [],
      apiCoverRateOptions: {
        chart: { height: 20, type: "radialBar" },
        plotOptions: {
          radialBar: {
            hollow: { margin: 15, size: "50%" },
            dataLabels: {
              showOn: "always",
              name: { offsetY: 0, show: true, color: "#888", fontSize: "13px" },
              value: { color: "#111", fontSize: "16px", show: true },
            },
          },
        },
        stroke: {
          lineCap: "round",
        },
        labels: ["接口覆盖率"],
      },
      coreCaseCoverRateOptions: {
        chart: { height: 20, type: "radialBar" },
        plotOptions: {
          radialBar: {
            hollow: { margin: 15, size: "50%" },
            dataLabels: {
              showOn: "always",
              name: { offsetY: 0, show: true, color: "#888", fontSize: "13px" },
              value: { color: "#111", fontSize: "16px", show: true },
            },
          },
        },
        stroke: {
          lineCap: "round",
        },
        labels: ["核心用例覆盖率"],
      },
      casePieOptions: {
        plotOptions: {
          pie: {
            donut: {
              size: "50%",
              labels: {
                show: true,
                total: { show: true, showAlways: true, label: "Total" },
              },
            },
          },
        },
        show: true,
        chart: { id: "casePie", type: "donut" },
        // 饼图右上角的分类，会被接口返回值的覆盖
        labels: ["冒烟用例", "集成用例", "监控脚本", "核心用例"],
      },
      reportPieOptions: {
        plotOptions: {
          pie: {
            donut: {
              size: "50%",
              labels: {
                show: true,
                total: { show: true, showAlways: true, label: "Total" },
              },
            },
          },
        },
        show: true,
        chart: {
          type: "donut",
        },
        // 饼图右上角的分类，会被接口返回值的覆盖
        labels: ["调试", "异步", "定时", "部署"],
      },
      apiPieSeries: [],
      casePieSeries: [],
      reportPieSeries: [],
      visitChartOptions: {
        chart: { id: "vuechart-example" },
        xaxis: { categories: [] },
      },
      apiAreaOptions: {
        chart: { foreColor: "#aaa", id: "apiArea" },
        xaxis: { categories: [] },
      },
      caseAreaOptions: {
        chart: { id: "caseArea" },
        xaxis: { categories: [] },
      },
      reportAreaOptions: {
        chart: { id: "reportArea" },
        xaxis: { categories: [] },
      },
      visitSeries: [{ name: "访问量", data: [] }],
      apiAreaSeries: [{ name: "API创建数量", data: [] }],
      caseAreaSeries: [{ name: "Case创建数量", data: [] }],
      reportAreaSeries: [{ name: "Report创建数量", data: [] }],
    };
  },
  methods: {
    getVisitData() {
      const project = this.$route.params.id;
      this.$api
        .getVisit({
          params: {
            project: project,
          },
        })
        .then((res) => {
          this.visitChartOptions = {
            ...this.visitChartOptions,
            ...{ xaxis: { categories: res.recent7days } },
          };
        });
    },
    success(resp) {
      this.$notify({
        message: resp["msg"],
        type: "success",
        duration: this.$store.state.duration,
      });
    },
    failure(resp) {
      this.$notify.error({
        message: resp.msg,
        duration: this.$store.state.duration,
      });
    },

    handleArea() {
      const res = this.projectInfo.daily_create_count;
      const apiDays = res.api.days;
      const caseDays = res.case.days;
      const reportDays = res.report.days;
      const apiCount = res.api.count;
      const caseCount = res.case.count;
      const reportCount = res.report.count;
      this.apiAreaOptions = {
        ...this.apiAreaOptions,
        ...{ xaxis: { categories: apiDays } },
      };
      this.caseAreaOptions = {
        ...this.caseAreaOptions,
        ...{ xaxis: { categories: caseDays } },
      };
      this.reportAreaOptions = {
        ...this.reportAreaOptions,
        ...{ xaxis: { categories: reportDays } },
      };
      this.apiAreaSeries[0].data = apiCount;
      this.caseAreaSeries[0].data = caseCount;
      this.reportAreaSeries[0].data = reportCount;

      this.apiCoverRateSeries.push(this.projectInfo.api_cover_rate);
      this.coreCaseCoverRateSeries.push(this.projectInfo.core_case_cover_rate);
    },
    handlePie() {
      const pi = this.projectInfo;
      this.apiPieSeries = pi.api_count_by_create_type.count;
      this.apiPieOptions = {
        ...this.apiPieOptions,
        ...{ labels: pi.api_count_by_create_type.type },
      };

      this.casePieSeries = pi.case_count_by_tag.count;
      this.casePieOptions = {
        ...this.casePieOptions,
        ...{ labels: pi.case_count_by_tag.tag },
      };

      this.reportPieSeries = pi.report_count_by_type.count;
      this.reportPieOptions = {
        ...this.reportPieOptions,
        ...{ labels: pi.report_count_by_type.type },
      };
    },
    getProjectDetail() {
      this.loading = true;
      const pk = this.$route.params.id;
      this.$api.getProjectDetail(pk).then((res) => {
        this.projectInfo = res;
        this.handleArea();
        this.handlePie();
        this.loading = false;
      });
    },
    sum(arr) {
      return arr.reduce(function (total, value) {
        return total + value;
      }, 0);
    },
  },
  mounted() {
    this.getVisitData();
    this.getProjectDetail();
  },

  beforeMount() {},
};
</script>

<style scoped>
.desc-p {
  padding-top: 10px;
  font-size: 12px;
  color: #b6b6b6;
}

.title-p {
  font-size: 18px;
  margin-top: 10px;
}

.title-project li a {
  font-size: 12px;
  text-decoration: none;
  color: #a3a3a3;
  margin-left: 20px;
}

.pull-left {
  float: left;
  margin-left: 10px;
}

.project_detail li {
  margin-top: 10px;
  text-indent: 20px;
  display: inline-block;
  height: 90px;
  width: calc(20% - 1.5px);
  border: 1px solid #ddd;
}

.project_detail {
  height: 100px;
  margin-top: 20px;
}

.title-project {
  margin-top: 10px;
  margin-left: 10px;
}

ul li {
  list-style: none;
}

.title-li {
  font-size: 24px;
  color: #607d8b;
}

.desc-li {
  margin-top: 10px;
  color: #b6b6b6;
  font-size: 14px;
}
</style>
