<template>
  <div>
    <div>
      <div>
        <el-input style="width: 60%; min-width: 500px" placeholder="请输入接口名称" v-model="name" clearable>
          <template slot="prepend">接口信息录入</template>
        </el-input>
        <el-button
          slot="append"
          type="success"
          size="medium"
          @click="save = !save"
          :disabled="disabledSave"
          :title="disabledSave ? '不能修改其他人的用例' : '保存用例步骤'"
          >Save
        </el-button>

        <el-button style="margin-left: 0" size="medium" slot="append" type="danger" @click="esc = !esc"
          >Back
        </el-button>

        <!-- <el-button
                     type="primary"
                     @click="handleRun"
                     v-loading="loading"
                 >Run
                 </el-button>-->
      </div>
      <div>
        <el-input
          class="input-with-select"
          placeholder="请输入接口请求地址"
          v-model="url"
          clearable
          style="width: 60%; min-width: 500px"
        >
          <el-select slot="prepend" v-model="method" size="small">
            <el-option v-for="item of httpOptions" :label="item.label" :value="item.label" :key="item.value">
            </el-option>
          </el-select>
        </el-input>

        <el-tooltip effect="dark" content="循环次数" placement="bottom" style="width: 10%">
          <el-input-number v-model="times" controls-position="right" :min="1" :max="100" style="width: 120px">
          </el-input-number>
        </el-tooltip>
      </div>
      <el-dialog v-if="dialogTableVisible" :visible.sync="dialogTableVisible" width="70%">
        <report :summary="summary"></report>
      </el-dialog>
    </div>

    <div class="request">
      <el-tabs style="margin-left: 20px" v-model="activeTag">
        <el-tab-pane label="Header" name="first">
          <span slot="label">
            Header
            <el-badge slot="label" :value="handleBadgeValue(response.body.header, 'key')"></el-badge>
          </span>
          <headers :save="save" v-on:header="handleHeader" :header="header"> </headers>
        </el-tab-pane>

        <el-tab-pane label="Request" name="second">
          <request :save="save" v-on:request="handleRequest" :request="request"> </request>
        </el-tab-pane>

        <el-tab-pane label="Extract" name="third">
          <span slot="label">
            Extract
            <el-badge slot="label" :value="handleBadgeValue(response.body.extract, 'key')"></el-badge>
          </span>
          <extract :save="save" v-on:extract="handleExtract" :extract="extract"> </extract>
        </el-tab-pane>

        <el-tab-pane label="Validate" name="fourth">
          <span slot="label">
            Validate
            <el-badge slot="label" :value="handleBadgeValue(response.body.validate, 'actual')"></el-badge>
          </span>
          <validate :save="save" v-on:validate="handleValidate" :validate="validate"> </validate>
        </el-tab-pane>

        <el-tab-pane label="Variables" name="five">
          <span slot="label">
            Variables
            <el-badge slot="label" :value="handleBadgeValue(response.body.variables, 'key')"></el-badge>
          </span>
          <variables :save="save" v-on:variables="handleVariables" :variables="variables"> </variables>
        </el-tab-pane>

        <el-tab-pane label="Hooks" name="six">
          <span slot="label">
            Hooks
            <el-badge slot="label" :value="handleHooksBadge(response.body.hooks)"></el-badge>
          </span>
          <hooks :save="save" v-on:hooks="handleHooks" :hooks="hooks"> </hooks>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import Headers from "../../../httprunner/components/Headers.vue";
import Request from "../../../httprunner/components/Request.vue";
import Extract from "../../../httprunner/components/Extract.vue";
import Validate from "../../../httprunner/components/Validate.vue";
import Variables from "../../../httprunner/components/Variables.vue";
import Hooks from "../../../httprunner/components/Hooks.vue";
import Report from "../../../reports/DebugReport.vue";

export default {
  components: {
    Headers,
    Request,
    Extract,
    Validate,
    Variables,
    Hooks,
    Report
  },

  props: {
    response: {
      require: true
    },
    host: {
      require: true
    },
    disabledSave: {
      type: Boolean,
      require: true
    }
  },
  methods: {
    /*  handleRun() {
              this.run = true;
              this.save = !this.save;
          },
*/
    handleHeader(header, value) {
      this.header = value;
      this.tempBody.header = header;
    },
    handleRequest(request, value) {
      this.request = value;
      this.tempBody.request = request;
    },
    handleValidate(validate, value) {
      this.validate = value;
      this.tempBody.validate = validate;
    },
    handleExtract(extract, value) {
      this.extract = value;
      this.tempBody.extract = extract;
    },
    handleVariables(variables, value) {
      this.variables = value;
      this.tempBody.variables = variables;
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
    handleHooks(hooks, value) {
      this.hooks = value;

      this.tempBody.hooks = hooks;
      this.tempBody.url = this.url;
      this.tempBody.method = this.method;
      this.tempBody.name = this.name;
      this.tempBody.times = this.times;

      if (this.validateData()) {
        const body = {
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
        };
        this.$emit("getNewBody", body, this.tempBody);
        this.run = false;
      }
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
    }
  },

  watch: {
    esc() {
      this.$emit("escEdit");
    }
  },
  data() {
    return {
      loading: false,
      run: false,
      esc: false,
      times: this.response.body.times,
      name: this.response.body.name,
      url: this.response.body.url,
      header: [],
      request: [],
      extract: [],
      validate: [],
      variables: [],
      hooks: [],
      tempBody: {},
      method: this.response.body.method,
      save: false,
      summary: {},
      dialogTableVisible: false,
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
  name: "TestBody",
  mounted() {
    this.header = this.response.body.header;
    this.request = this.response.body.request;
    this.extract = this.response.body.extract;
    this.validate = this.response.body.validate;
    this.variables = this.response.body.variables;
    this.hooks = this.response.body.hooks;
  }
};
</script>

<style scoped>
.el-select {
  width: 125px;
}

.input-with-select {
  width: 600px;
  margin-top: 10px;
}

.request {
  margin-top: 15px;
  border: 1px solid #ddd;
}
</style>
