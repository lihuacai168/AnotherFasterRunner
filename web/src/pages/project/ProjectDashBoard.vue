<template>
    <el-container>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap">
            <div class="api-case">
                <el-card>
                    <div slot="header"><span>每日指标趋势</span></div>
                    <ApexCharts :options="optionsLine" :series="apiCaseLineSeries"></ApexCharts>
                </el-card>
            </div>

            <div class="api-case">
                <el-card>
                    <div slot="header"><span>每周指标</span></div>
                    <ApexCharts :options="optionsWeekBar" :series="weekBarSeries"></ApexCharts>
                </el-card>
            </div>
            <div class="api-case">
                <el-card>
                    <div slot="header"><span>每月指标</span></div>
                    <ApexCharts :options="optionsMonthBar" :series="monthBarSeries"></ApexCharts>
                </el-card>
            </div>

            <div class="api-case">
                <el-card>
                    <div slot="header"><span>报告日-周-月趋势</span></div>
                    <ApexCharts :options="reportOptionsLine" :series="reportLineSeries"></ApexCharts>
                </el-card>
            </div>
            <div class="api-case">
                <el-card>
                    <div slot="header"><span>报告比例</span></div>
                    <div style="display: flex; flex-wrap: wrap">
                        <div style="width: 66%">
                            <ApexCharts :options="reportPieOptions" :series="reportPieSeries"></ApexCharts>
                        </div>
                        <div style="width: 30%; align-self: flex-end">
                            <ApexCharts :options="reportRadiaOptions" :series="reportRadiaSeries"></ApexCharts>
                        </div>
                    </div>
                </el-card>
            </div>
        </div>
    </el-container>
</template>

<script>
export default {
    name: "ProjectDashBoard",
    data() {
        return {
            weekBarSeries: [],
            monthBarSeries: [],
            optionsWeekBar: {
                chart: {
                    // height: "50%",
                    type: "bar", stacked: true
                },
                plotOptions: {bar: {columnWidth: "30%", horizontal: false}},
                xaxis: {categories: ["前5周", "前4周", "前3周", "前2周", "前1周", "当前周"]},
                fill: {opacity: 1}
            },
            optionsMonthBar: {
                chart: {
                    // height: "50%",
                    type: "bar", stacked: true
                },
                plotOptions: {bar: {columnWidth: "30%", horizontal: false}},
                xaxis: {categories: ["前5月", "前4月", "前3月", "前2月", "前1月", "当前月"]},
                fill: {opacity: 1}
            },
            apiCaseLineSeries: [],
            reportLineSeries: [],
            optionsLine: {
                chart: {
                    // height: 328,
                    type: "area", zoom: {enabled: false},
                    dropShadow: {
                        // enabled: true,
                        top: 3, left: 2, blur: 4, opacity: 1
                    }
                },
                stroke: {curve: "smooth", width: 2},
                markers: {size: 6, strokeWidth: 0,
                    hover: {size: 9}
                },
                grid: {show: true, padding: {bottom: 0}},
                labels: [],
                xaxis: {tooltip: {enabled: true}},
                // 底部说明
                legend: {position: "bottom", horizontalAlign: "center"}
            },
            reportOptionsLine: {
                chart: {
                    // height: 328,
                    type: "area", zoom: {enabled: false},
                    dropShadow: {
                        // enabled: true,
                        top: 3, left: 2, blur: 4, opacity: 1
                    }
                },
                stroke: {curve: "smooth", width: 2},
                //colors: ["#3F51B5", '#2196F3'],
                markers: {size: 6, strokeWidth: 0, hover: {size: 9}},
                grid: {show: true, padding: {bottom: 0}},
                labels: ["前5", "前4", "前3", "前2", "前1", "当前"],
                xaxis: {tooltip: {enabled: true}},
                legend: {position: "bottom", horizontalAlign: "center"}
            },
            reportPieOptions: {
                plotOptions: {
                    pie: {
                        donut: {
                            size: "50%",
                            labels: {show: true, total: {show: true, showAlways: true, label: "Total"}}
                        }
                    }
                },
                show: true,
                chart: {
                    animations: {enabled: true, easing: "easeinout", speed: 800},
                    type: "donut"
                },
                // 饼图右上角的分类，会被接口返回值的覆盖
                labels: ["调试", "异步", "定时", "部署"]
            },
            reportPieSeries: [],
            reportRadiaOptions: {
                chart: {type: "pie"},
                colors: ["#08f540", "#e50810"],
                labels: ["成功", "失败"],
                theme: {monochrome: {enabled: false}},
                plotOptions: {
                    radialBar: {
                        size: "20%"
                        // offsetY: -30
                    }
                },
                legend: {show: true, position: "left", containerMargin: {right: 0}}
            },
            reportRadiaSeries: []
        };
    },
    methods: {
        getData() {
            this.$api.getDashBoard().then(resp => {
                this.reportPieSeries = resp.report.type;
                this.reportRadiaSeries = resp.report.status;

                // 报告趋势
                this.reportLineSeries.push({name: "日", data: resp.report.day});
                this.reportLineSeries.push({name: "周", data: resp.report.week});
                this.reportLineSeries.push({name: "月", data: resp.report.month});

                // 每日
                this.apiCaseLineSeries.push({name: "Case", data: resp.case.day});
                this.apiCaseLineSeries.push({name: "API", data: resp.api.day});
                this.apiCaseLineSeries.push({name: "Yapi", data: resp.yapi.day});
                this.optionsLine = {
                    ...this.optionsLine,
                    ...{ labels: resp.recent_days }
                };

                // 每周
                this.weekBarSeries.push({ name: "Case", data: resp.case.week });
                this.weekBarSeries.push({ name: "API", data: resp.api.week });
                this.weekBarSeries.push({ name: "Yapi", data: resp.yapi.week });
                this.optionsWeekBar = {
                    ...this.optionsWeekBar,
                    ...{ xaxis: { categories: resp.recent_weeks } }
                };

                // 每月
                this.monthBarSeries.push({name: "Case", data: resp.case.month});
                this.monthBarSeries.push({name: "API", data: resp.api.month});
                this.monthBarSeries.push({name: "Yapi", data: resp.yapi.month
                });
                this.optionsMonthBar = {
                    ...this.optionsMonthBar,
                    ...{ xaxis: { categories: resp.recent_months } }
                };
            });
        }
    },
    mounted() {
        this.getData();
    }
};
</script>

<style scoped>
.api-case {
    margin-top: 10px;
    margin-left: 10px;
    /*width: 30%;*/
}
</style>
