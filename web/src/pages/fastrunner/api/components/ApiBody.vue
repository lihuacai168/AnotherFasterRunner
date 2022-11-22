<template>
  <div>
    <div>
      <div>
        <el-input
          style="width: 60%; min-width: 500px"
          placeholder="请输入接口名称"
          v-model="name"
          clearable
          size="medium"
        >
          <template slot="prepend">接口信息录入</template>
        </el-input>
        <el-button
          slot="append"
          type="success"
          size="medium"
          :title="userName === creator || isSuperuser || !isSaveAs ? '保存' : '只有API创建者才能更新'"
          :disabled="userName !== creator && !isSuperuser && isSaveAs"
          @click="save = !save"
          >Save
        </el-button>

        <el-button
          style="margin-left: 0"
          size="medium"
          slot="append"
          type="success"
          :title="'另存为'"
          @click="handleSaveAs"
          >Save As
        </el-button>

        <el-button
          style="margin-left: 0"
          size="medium"
          type="primary"
          @click="reverseStatus"
          v-loading="loading"
          :disabled="loading"
          >Send
        </el-button>
      </div>

      <div>
        <el-input
          style="width: 60%; margin-top: 10px; min-width: 500px"
          placeholder="请输入接口请求地址"
          v-model="url"
          clearable
        >
          <el-select style="width: 100px" slot="prepend" v-model="method">
            <el-option v-for="item of httpOptions" :label="item.label" :value="item.label" :key="item.value">
            </el-option>
          </el-select>
          <template slot="prepend">
            <span style="margin-left: 20px">
              {{ config.base_url }}
            </span></template
          >
        </el-input>

        <el-tooltip effect="dark" content="循环次数" placement="bottom">
          <el-input-number v-model="times" controls-position="right" :min="1" :max="100" style="width: 120px">
          </el-input-number>
        </el-tooltip>
      </div>
    </div>

    <div class="request">
      <el-dialog v-if="dialogTableVisible" :visible.sync="dialogTableVisible" width="70%">
        <report :summary="summary"></report>
      </el-dialog>

      <el-tabs style="margin-left: 20px" v-model="activeTag">
        <el-tab-pane label="Header" name="first">
          <span slot="label">
            Header
            <el-badge slot="label" :value="handleBadgeValue(response ? response.body.header : [], 'key')"></el-badge>
          </span>
          <headers :save="save" v-on:header="handleHeader" :header="response ? response.body.header : []"> </headers>
        </el-tab-pane>

        <el-tab-pane label="Request" name="second">
          <request :save="save" v-on:request="handleRequest" :request="response ? response.body.request : []">
          </request>
        </el-tab-pane>

        <el-tab-pane label="Extract" name="third">
          <span slot="label">
            Extract
            <el-badge slot="label" :value="handleBadgeValue(response ? response.body.extract : [], 'key')"></el-badge>
          </span>
          <extract :save="save" v-on:extract="handleExtract" :extract="response ? response.body.extract : []">
          </extract>
        </el-tab-pane>

        <el-tab-pane label="Validate" name="fourth">
          <span slot="label">
            Validate
            <el-badge
              slot="label"
              :value="handleBadgeValue(response ? response.body.validate : [], 'actual')"
            ></el-badge>
          </span>
          <validate :save="save" v-on:validate="handleValidate" :validate="response ? response.body.validate : []">
          </validate>
        </el-tab-pane>

        <el-tab-pane label="Variables" name="five">
          <span slot="label">
            Variables
            <el-badge slot="label" :value="handleBadgeValue(response ? response.body.variables : [], 'key')"></el-badge>
          </span>
          <variables :save="save" v-on:variables="handleVariables" :variables="response ? response.body.variables : []">
          </variables>
        </el-tab-pane>

        <el-tab-pane label="Hooks" name="six">
          <span slot="label"
            >Hooks
            <el-badge slot="label" :value="handleHooksBadge(response ? response.body.hooks : [])"></el-badge>
          </span>
          <hooks :save="save" v-on:hooks="handleHooks" :hooks="response ? response.body.hooks : []"></hooks>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import Headers from "../../../httprunner/components/Headers";
import Request from "../../../httprunner/components/Request";
import Extract from "../../../httprunner/components/Extract";
import Validate from "../../../httprunner/components/Validate";
import Variables from "../../../httprunner/components/Variables";
import Hooks from "../../../httprunner/components/Hooks";
import Report from "../../../reports/DebugReport";

export default {
  components: { Headers, Request, Extract, Validate, Variables, Hooks, Report },
  props: {
    host: { require: false },
    nodeId: { require: false },
    project: { require: false },
    config: { require: false },
    response: { require: false },
    isSaveAs: Boolean
  },
  methods: {
    reverseStatus() {
      this.save = !this.save;
      this.run = true;
    },

    handleHeader(header) {
      this.header = header;
    },
    handleRequest(request) {
      this.request = request;
    },
    handleValidate(validate) {
      this.validate = validate;
    },
    handleExtract(extract) {
      this.extract = extract;
    },
    handleVariables(variables) {
      this.variables = variables;
    },

    // 计算标记的数值
    handleBadgeValue(arr, countKey) {
      let res = 0;
      for (const v of arr) {
        if (v[countKey]) {
          res += 1;
        }
      }
      return res;
    },
    // 计算hook数值
    handleHooksBadge(hook) {
      let res = 0;
      for (const hookElement of hook) {
        if (hookElement["setup"]) {
          res += 1;
        }
        if (hookElement["teardown"]) {
          res += 1;
        }
      }
      return res;
    },
    handleHooks(hooks) {
      this.hooks = hooks;

      if (!this.run) {
        if (this.id === "") {
          this.addAPI();
        } else {
          this.updateAPI();
        }
      } else {
        this.runAPI();
        this.run = false;
      }
    },
    handleSaveAs() {
      this.save = !this.save;
      this.id = "";
    },
    validateData() {
      if (this.url === "") {
        this.$notify.error({
          title: "url错误",
          message: "接口请求地址不能为空",
          duration: 1500
        });
        return false;
      }

      if (this.name === "") {
        this.$notify.error({
          title: "name错误",
          message: "接口名称不能为空",
          duration: 1500
        });
        return false;
      }
      return true;
    },
    updateAPI() {
      if (this.validateData()) {
        this.$api
          .updateAPI(this.id, {
            header: this.header,
            request: this.request,
            extract: this.extract,
            validate: this.validate,
            variables: this.variables,
            hooks: this.hooks,
            url: this.url,
            method: this.method,
            name: this.name,
            times: this.times
          })
          .then((resp) => {
            if (resp.success) {
              this.$emit("addSuccess");
            } else {
              this.$message.error({
                message: resp.msg,
                duration: this.$store.state.duration
              });
            }
          });
      }
    },

    runAPI() {
      if (this.validateData()) {
        this.loading = true;
        this.$api
          .runSingleAPI({
            header: this.header,
            request: this.request,
            extract: this.extract,
            validate: this.validate,
            variables: this.variables,
            hooks: this.hooks,
            url: this.url,
            method: this.method,
            name: this.name,
            times: this.times,
            project: this.project,
            config: this.config.name,
            host: this.host
          })
          .then((resp) => {
            this.summary = resp;
            this.dialogTableVisible = true;
            this.loading = false;
          })
          .catch((resp) => {
            this.loading = false;
          });
      }
    },

    addAPI() {
      if (this.validateData()) {
        this.$api
          .addAPI({
            header: this.header,
            request: this.request,
            extract: this.extract,
            validate: this.validate,
            variables: this.variables,
            hooks: this.hooks,
            url: this.url,
            method: this.method,
            name: this.name,
            times: this.times,
            // 另存为时，使用response的值
            nodeId: this.response.relation || this.nodeId,
            project: this.response.project || this.project
          })
          .then((resp) => {
            if (resp.success) {
              this.$emit("addSuccess");
            } else {
              this.$message.error({
                message: resp.msg,
                duration: this.$store.state.duration
              });
            }
          });
      }
    }
  },

  watch: {
    response: function () {
      this.name = this.response.body.name;
      this.method = this.response.body.method;
      this.url = this.response.body.url;
      this.times = this.response.body.times;
      this.id = this.response.id;
      this.creator = this.response.creator;
    }
  },
  data() {
    return {
      isSuperuser: this.$store.state.is_superuser,
      userName: this.$store.state.user,
      loading: false,
      times: 1,
      name: "",
      url: "",
      id: "",
      creator: "",
      header: [],
      request: [],
      extract: [],
      validate: [],
      variables: [],
      hooks: [],
      method: "GET",
      dialogTableVisible: false,
      save: false,
      run: false,
      summary: {},
      activeTag: "second",
      httpOptions: [
        {
          label: "GET"
        },
        {
          label: "POST"
        },
        {
          label: "PUT"
        },
        {
          label: "DELETE"
        },
        {
          label: "HEAD"
        },
        {
          label: "OPTIONS"
        },
        {
          label: "PATCH"
        }
      ]
    };
  },
  name: "ApiBody"
};
</script>

<style scoped>
.request {
  margin-top: 15px;
  border: 1px solid #ddd;
}
</style>
