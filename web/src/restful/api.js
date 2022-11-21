import axios from "axios";
import store from "../store/state";
import router from "../router";
import { Message, Notification } from "element-ui";

let base_Url;
if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
  base_Url = window.location.protocol + "//" + "127.0.0.1" + ":" + "8000";
} else {
  // var base_Url = window.location.protocol + "//" + window.location.host;
  base_Url = window.location.protocol + "//testapi.caibeike.net";
}
export const baseUrl = base_Url;
// export let baseUrl = "http://119.91.147.215:8000";
// export let baseUrl = "http://192.168.22.19:8000";

// if (process.env.NODE_ENV === "production") {
//     baseUrl = "http://119.91.147.215:8000";
// }

axios.defaults.withCredentials = true;
axios.defaults.baseURL = baseUrl;

axios.interceptors.request.use(
  function (config) {
    if (!config.url.startsWith("/api/user/") || config.url === "/api/user/list/") {
      // 在请求拦截中，每次请求，都会加上一个Authorization头
      config.headers.Authorization = store.token;

      // 取url地址的第四位作为projectId，如果不存在，默认设置为0
      // let projectId = window.location.pathname.split("/")[3];
      let projectId = store.projectId;
      projectId = projectId ? projectId : 0;
      config.headers["Project"] = projectId;
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    try {
      if (error.response.status === 401) {
        Notification.warning({ message: "请先登录" });
        router.replace({
          name: "Login"
        });
      } else if (error.response.status === 500 || error.response.status === 404) {
        Notification.error({
          message: "服务器内部异常, 请检查",
          duration: 2000
        });
      } else if (error.response.status === 504) {
        Notification.error({
          message: "请求超时,请联系系统管理员"
        });
      } else if (error.response.status === 405) {
        Notification.error({
          message: "Not Allowed"
        });
      } else if (error.response.status === 403) {
        Notification.error({
          message: error.response.data.msg,
          duration: this.$store.state.duration
        });
      } else {
        if (error.response.data.constructor === String) {
          Notification.error({
            title: "error",
            message: error.response.data
          });
        } else {
          for (let key in error.response.data) {
            if (error.response.data[key].constructor === Array) {
              Notification.error({
                title: key,
                message: error.response.data[key][0]
              });
            } else if (error.response.data[key].constructor === String) {
              Notification.error({
                title: key,
                message: error.response.data[key]
              });
            }
          }
        }
      }
      return Promise.reject(error.response.data);
    } catch (e) {
      Notification.error({
        message: "服务器连接超时，请重试",
        duration: 2000
      });
    }
  }
);

// user api
export const register = async (params) => {
  const res = await axios.post("/api/user/register/", params);
  return res.data;
};

export const login = async (params) => {
  const res = await axios.post("/api/user/login/", params);
  return res.data;
};

export const getUserList = () => {
  return axios.get("/api/user/list/").then((res) => res.data);
};

// fastrunner api
export const addProject = async (params) => {
  const res = await axios.post("/api/fastrunner/project/", params);
  return res.data;
};

export const deleteProject = async (config) => {
  const res = await axios.delete("/api/fastrunner/project/", config);
  return res.data;
};

export const getProjectList = (params) => {
  return axios.get("/api/fastrunner/project/").then((res) => res.data);
};

export const getProjectDetail = (pk) => {
  return axios.get("/api/fastrunner/project/" + pk + "/").then((res) => res.data);
};

export const getDashBoard = () => {
  return axios.get("/api/fastrunner/dashboard/").then((res) => res.data);
};

export const getProjectYapiInfo = (pk) => {
  return axios.get("/api/fastrunner/project/yapi/" + pk + "/").then((res) => res.data);
};

export const getVisit = (params) => {
  return axios.get("/api/fastrunner/visit/", params).then((res) => res.data);
};

export const getPagination = (url) => {
  return axios.get(url).then((res) => res.data);
};

export const updateProject = async (params) => {
  const res = await axios.patch("/api/fastrunner/project/", params);
  return res.data;
};

export const getDebugtalk = (url) => {
  return axios.get("/api/fastrunner/debugtalk/" + url + "/").then((res) => res.data);
};

export const updateDebugtalk = async (params) => {
  const res = await axios.patch("/api/fastrunner/debugtalk/", params);
  return res.data;
};

export const runDebugtalk = async (params) => {
  const res = await axios.post("/api/fastrunner/debugtalk/", params);
  return res.data;
};

export const getTree = (url, params) => {
  return axios.get("/api/fastrunner/tree/" + url + "/", params).then((res) => res.data.data);
};

export const updateTree = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/tree/" + url + "/", params);
  return res.data;
};

export const uploadFile = (url) => {
  return baseUrl + "/api/fastrunner/file/?token=" + store.token;
};

export const addAPI = async (params) => {
  const res = await axios.post("/api/fastrunner/api/", params);
  return res.data;
};

export const updateAPI = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/api/" + url + "/", params);
  return res.data;
};

export const addYAPI = async (project_id) => {
  const res = await axios.post("/api/fastrunner/yapi/" + project_id + "/");
  return res.data;
};

export const apiList = (params) => {
  return axios.get("/api/fastrunner/api/", params).then((res) => res.data);
};

export const delAPI = async (url) => {
  const res = await axios.delete("/api/fastrunner/api/" + url + "/");
  return res.data;
};

export const tagAPI = async (params) => {
  const res = await axios.patch("/api/fastrunner/api/tag/", params);
  return res.data;
};

export const syncCaseStep = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/api/sync/" + url + "/");
  return res.data;
};

export const delAllAPI = async (params) => {
  const res = await axios.delete("/api/fastrunner/api/", params);
  return res.data;
};

export const getAPISingle = (url) => {
  return axios.get("/api/fastrunner/api/" + url + "/").then((res) => res.data);
};

export const getPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/api/", params).then((res) => res.data);
};

export const addTestCase = async (params) => {
  const res = await axios.post("/api/fastrunner/test/", params);
  return res.data;
};

export const updateTestCase = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/test/" + url + "/", params);
  return res.data;
};

export const testList = (params) => {
  return axios.get("/api/fastrunner/test/", params).then((res) => res.data);
};

export const deleteTest = async (url) => {
  const res = await axios.delete("/api/fastrunner/test/" + url + "/");
  return res.data;
};

export const syncTest = async (url) => {
  const res = await axios.put("/api/fastrunner/test/" + url + "/");
  return res.data;
};
export const delAllTest = async (params) => {
  const res = await axios.delete("/api/fastrunner/test/", params);
  return res.data;
};

export const coptTest = async (url, params) => {
  const res = await axios.post("/api/fastrunner/test/" + url + "/", params);
  return res.data;
};

export const editTest = (url) => {
  return axios.get("/api/fastrunner/teststep/" + url + "/").then((res) => res.data);
};

export const getTestPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/test/", params).then((res) => res.data);
};

export const addConfig = async (params) => {
  const res = await axios.post("/api/fastrunner/config/", params);
  return res.data;
};

export const updateConfig = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/config/" + url + "/", params);
  return res.data;
};

export const configList = (params) => {
  return axios.get("/api/fastrunner/config/", params).then((res) => res.data);
};

export const copyConfig = async (url, params) => {
  const res = await axios.post("/api/fastrunner/config/" + url + "/", params);
  return res.data;
};

export const copyAPI = async (url, params) => {
  const res = await axios.post("/api/fastrunner/api/" + url + "/", params);
  return res.data;
};

export const deleteConfig = async (url) => {
  const res = await axios.delete("/api/fastrunner/config/" + url + "/");
  return res.data;
};
export const delAllConfig = async (params) => {
  const res = await axios.delete("/api/fastrunner/config/", params);
  return res.data;
};

export const getConfigPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/config/", params).then((res) => res.data);
};

export const getAllConfig = (url) => {
  return axios.get("/api/fastrunner/config/" + url + "/").then((res) => res.data);
};

export const runSingleAPI = async (params) => {
  const res = await axios.post("/api/fastrunner/run_api/", params);
  return res.data;
};

export const runAPIByPk = (url, params) => {
  return axios.get("/api/fastrunner/run_api_pk/" + url + "/", params).then((res) => res.data);
};

export const runAPITree = async (params) => {
  const res = await axios.post("/api/fastrunner/run_api_tree/", params);
  return res.data;
};

export const moveAPI = async (params) => {
  const res = await axios.patch("/api/fastrunner/api/move_api/", params);
  return res.data;
};

export const moveCase = async (params) => {
  const res = await axios.patch("/api/fastrunner/test/move_case/", params);
  return res.data;
};

export const tagCase = async (params) => {
  const res = await axios.patch("/api/fastrunner/test/tag/", params);
  return res.data;
};

export const runSingleTestSuite = async (params) => {
  const res = await axios.post("/api/fastrunner/run_testsuite/", params);
  return res.data;
};

export const runSingleTest = async (params) => {
  const res = await axios.post("/api/fastrunner/run_test/", params);
  return res.data;
};

export const runMultiTest = async (params) => {
  const res = await axios.post("/api/fastrunner/run_multi_tests/", params);
  return res.data;
};

export const runTestByPk = (url, params) => {
  return axios.get("/api/fastrunner/run_testsuite_pk/" + url + "/", params).then((res) => res.data);
};

export const runSuiteTree = async (params) => {
  const res = await axios.post("/api/fastrunner/run_suite_tree/", params);
  return res.data;
};

export const addVariables = async (params) => {
  const res = await axios.post("/api/fastrunner/variables/", params);
  return res.data;
};

export const variablesList = (params) => {
  return axios.get("/api/fastrunner/variables/", params).then((res) => res.data);
};

export const getVariablesPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/variables/", params).then((res) => res.data);
};

export const updateVariables = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/variables/" + url + "/", params);
  return res.data;
};

export const updateTask = async (url, params, data) => {
  const res = await axios({
    url: "/api/fastrunner/schedule/" + url + "/",
    method: "PUT",
    params: params,
    data: data
  });
  return res.data;
};

export const patchTask = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/schedule/" + url + "/", params);
  return res.data;
};

export const deleteVariables = async (url) => {
  const res = await axios.delete("/api/fastrunner/variables/" + url + "/");
  return res.data;
};

export const delAllVariabels = async (params) => {
  const res = await axios.delete("/api/fastrunner/variables/", params);
  return res.data;
};

export const reportList = (params) => {
  return axios.get("/api/fastrunner/reports/", params).then((res) => res.data);
};

export const deleteReports = async (url) => {
  const res = await axios.delete("/api/fastrunner/reports/" + url + "/");
  return res.data;
};

export const getReportsPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/reports/", params).then((res) => res.data);
};

export const delAllReports = async (params) => {
  const res = await axios.delete("/api/fastrunner/reports/", params);
  return res.data;
};

export const watchSingleReports = (url) => {
  return axios.get("/api/fastrunner/reports/" + url + "/").then((res) => res.data);
};

export const addTask = async (params) => {
  const res = await axios.post("/api/fastrunner/schedule/", params);
  return res.data;
};

export const copyTask = async (task_id, params) => {
  const res = await axios.post("/api/fastrunner/schedule/" + task_id + "/", params);
  return res.data;
};
export const taskList = (params) => {
  return axios.get("/api/fastrunner/schedule/", params).then((res) => res.data);
};
export const getTaskPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/schedule/", params).then((res) => res.data);
};
export const deleteTasks = async (url) => {
  const res = await axios.delete("/api/fastrunner/schedule/" + url + "/");
  return res.data;
};

export const runTask = (url) => {
  return axios.get("/api/fastrunner/schedule/" + url + "/").then((res) => res.data);
};

export const addHostIP = async (params) => {
  const res = await axios.post("/api/fastrunner/host_ip/", params);
  return res.data;
};

export const hostList = (params) => {
  return axios.get("/api/fastrunner/host_ip/", params).then((res) => res.data);
};

export const updateHost = async (url, params) => {
  const res = await axios.patch("/api/fastrunner/host_ip/" + url + "/", params);
  return res.data;
};

export const deleteHost = async (url) => {
  const res = await axios.delete("/api/fastrunner/host_ip/" + url + "/");
  return res.data;
};

export const getHostPaginationBypage = (params) => {
  return axios.get("/api/fastrunner/host_ip/", params).then((res) => res.data);
};

export const getAllHost = (url) => {
  return axios.get("/api/fastrunner/host_ip/" + url + "/").then((res) => res.data);
};
