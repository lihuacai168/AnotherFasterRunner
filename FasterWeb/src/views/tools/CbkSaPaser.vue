<script>
import { Base64 } from "js-base64";
import pako from "pako";
import websocket from "../../restful/websocket";
import { baseUrl } from "../../restful/api";

export default {
  data() {
    return {
      table: false,
      resultDialog: false,
      jsonViewDialog: false,
      jsonViewTmp: "",
      textArea: "",
      tableSearch: "",
      onlyCustomEvent: false,
      socketBaseUrl: baseUrl.replace("http", "ws"),
      debugCodeImg: "https://m.caibeike.com/qr.html?l=logo&c=https//sa-viewer-{}.caibeike.net/salog/sa",
      debugImgUrl: "",
      resultData: [
        // {
        //   index: 1,
        //   date: new Date().toLocaleTimeString(),
        //   source: "App",
        //   result: JSON.stringify({ test: "这是演示数据，王小虎:上海市普陀区金沙江路 1518 弄" }),
        //   eventName: "test event name",
        //   remark: "",
        // },
      ],
      jsonOptions: {
        onModeChange(newMode, oldMode) {
          if (newMode === "view") {
            self.$refs.jsonEditor[0].editor.expandAll();
          }
        },
        onEvent: function (node, event) {
          if (event.type === "click") {
            let value = node.value;
            // 当前点击的位置有value，复制value
            if (value) {
              self.jsonPathOrValue = value;
            } else {
              // 当前点击的位置是key，复制key的jsonpath
              let arr = node.path;
              arr.unshift("content");
              value = arr.join(".");
            }
            navigator.clipboard
              .writeText(value)
              .then(() => console.log("复制json value成功"))
              .catch(() => console.log("复制json value失败"));
          }
        },
        mode: "view",
        modes: ["view", "code"], // allowed modes
      },
      gridData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
      ],
    };
  },
  methods: {
    zipDateParse(urlsBase64) {
      if (urlsBase64.lenth === 0) {
        return [];
      }
      urlsBase64.forEach((url) => {
        try {
          if (!url.includes("salog/sa.gif")) {
            return;
          }
          if (!url.includes("data")) {
            return;
          }
          const arrayTmp = url.split("&");
          if (arrayTmp.lenth !== 3) {
            return;
          }
          const valueData = arrayTmp[1].split("=");
          if (valueData.lenth !== 2) {
            return;
          }
          this.$message.info({ message: this.h5Desc(valueData[1]) + "\n\r" });
        } catch (error) {
          this.$message.error({ message: error });
        }
      });
    },

    h5Desc(param) {
      // return window.decodeURIComponent(self.textArea);
      //   return window.atob(window.decodeURIComponent(param));
      return Base64.decode(window.decodeURIComponent(param));
    },
    appDesc(param) {
      //   const decode = Base64.decode(param);
      //   return ungzip(decode);
      const gzipData = new Uint8Array(
        Base64.atob(param)
          .split("")
          .map((char) => char.charCodeAt(0))
      );
      return pako.inflate(gzipData, { to: "string" });
    },

    addResultData(decodeStr, source = "App", event = "") {
      this.resultData.unshift({
        date: new Date().toLocaleTimeString(),
        index: this.resultData.length + 1,
        result: decodeStr,
        remark: "",
        eventName: event,
        source: source,
      });
    },
    h5Decode(saType) {
      if (this.textArea === undefined || this.textArea === "") {
        this.$message.warning({ message: "请输入正确的内容~" });
        return;
      }
      const saList = this.textArea.split("\n");
      try {
        if (saType === "H5") {
          saList.map((saLine) => {
            const decode = this.h5Desc(saLine.split("&")[1].split("=")[1]);
            const eventName = JSON.parse(decode).event;
            this.addResultData(decode, "H5", eventName);
          });
        } else if (saType === "App") {
          saList.map((saLine) => {
            // const decode = this.appDesc(saLine);
            // this.addResultData(decode);
            const decodeList = JSON.parse(this.appDesc(saLine));
            decodeList.map((decode) => {
              const eventName = decode.event;
              this.addResultData(JSON.stringify(decode), "App", eventName);
            });
          });
        }
      } catch (error) {
        this.$message.error({ message: "格式不正确,无法解码！" });
      }
    },
    saLogLink() {
      websocket.initWebSocket("/api/tools/salog/link");
      console.log();
    },
    appDecode(msg) {
      if (msg.length < 100) {
        this.$message.warning({ message: "内容过短：" + msg });
        return;
      }
      msg = window.decodeURIComponent(msg);
      try {
        if (msg.includes("eyJkaXN")) {
          const decode = Base64.decode(msg);
          if ("event" in JSON.parse(decode)) {
            const eventName = JSON.parse(decode).event;
            this.addResultData(decode, "H5", eventName);
          } else {
            this.addResultData(decode, "H5");
          }
        } else if (msg.includes("H4sIAAAAAAAA")) {
          // const decode = this.appDesc(saLine);
          // this.addResultData(decode);
          const decodeList = JSON.parse(this.appDesc(msg));
          decodeList.map((decode) => {
            const eventName = decode.event;
            this.addResultData(JSON.stringify(decode), "App", eventName);
          });
        }
      } catch (error) {
        this.$message.error({ message: "格式不正确,无法解码！" });
      }
    },
    init: function () {
      this.textArea = "";
      if (typeof WebSocket === "undefined") {
        this.$message.error({ message: "您的浏览器不支持socket" });
      } else {
        if (this.socket !== undefined) {
          this.socket.close();
        }
        // 实例化socket
        this.socket = new WebSocket(this.socketBaseUrl + "/api/tools/salog/link");
        // 监听socket连接
        this.socket.onopen = this.open;
        // 监听socket错误信息
        this.socket.onerror = this.error;
        // 监听socket消息
        this.socket.onmessage = this.getMessage;
      }
    },
    open: function () {
      console.log("socket连接成功");
    },
    error: function () {
      console.log("连接错误");
    },
    getMessage: function (msg) {
      const data = msg.data;
      if (data.includes("userId")) {
        const userId = data.split("-")[1];
        console.log(data, userId, typeof userId);
        this.debugCodeImg =
          "https://m.caibeike.com/qr.html?l=logo&c=https%3A%2F%2Fsa-viewer-{}.caibeike.net%2Fsalog%2Fsa".replace(
            "{}",
            userId
          );
        this.debugImgUrl = "sa-viewer-{}.caibeike.net".replace("{}", userId);
        this.resultDialog = true;
      } else {
        this.appDecode(data);
      }
    },
    send: function (params) {
      this.socket.send(params);
    },
    close: function () {
      console.log("socket已经关闭");
    },
    handleJsonView(index) {
      this.jsonViewTmp = JSON.parse(index.result);
      this.jsonViewDialog = true;
      console.log(index);
    },
    onError() {
      console.log("error");
    },
    //复制
    handleCopyText(url) {
      // 创建一个 Input标签
      const cInput = document.createElement("input");
      cInput.value = url;
      document.body.appendChild(cInput);
      cInput.select(); // 选取文本域内容;
      // 执行浏览器复制命令
      // 复制命令会将当前选中的内容复制到剪切板中（这里就是创建的input标签）
      // Input要在正常的编辑状态下原生复制方法才会生效
      document.execCommand("Copy");
      this.$message.success("复制成功:" + url);
      /// 复制成功后再将构造的标签 移除
      cInput.remove();
    },
  },
  destroyed() {
    this.socket.onclose = this.close;
    this.socket.close();
  },
  computed: {
    height() {
      return (window.screen.height - 464).toString() + "px";
    },
    tableHeight() {
      return (document.body.clientHeight - 210).toString();
    },
  },
};
</script>

<template>
  <el-main style="height: 100%">
    <el-button type="text" @click="table = true" v-if="false">嵌套表格的演示Drawer</el-button>

    <el-input
      type="textarea"
      clearable
      v-model="textArea"
      :autosize="{ minRows: 2, maxRows: 4 }"
      placeholder="请输入APP/H5埋点请求"
    ></el-input>
    <p>&nbsp;</p>
    <el-button type="info" size="small" @click="h5Decode('H5')">H5解码</el-button>
    <el-button type="success" size="small" @click="h5Decode('App')">APP解码</el-button>
    <el-button type="primary" size="small" @click="init()">自动跟踪</el-button>
    <el-button size="small" @click="resultData = []">清空</el-button>
    <el-button type="text" @click="resultDialog = true" v-if="false">打开弹窗</el-button>
    <el-checkbox v-model="onlyCustomEvent" style="position: absolute; right: 200px; padding: 7px 15px">
      仅自定义埋点
    </el-checkbox>
    <el-input
      v-model="tableSearch"
      clearable
      placeholder="请输入事件名进行搜索"
      style="width: 180px; position: absolute; right: 20px"
      size="small"
    ></el-input>
    <p>&nbsp;</p>

    <el-table
      :data="
        resultData
          .filter((data) => !tableSearch || data.eventName.toLowerCase().includes(tableSearch.toLowerCase()))
          .filter((data) => !(onlyCustomEvent && data.eventName.includes('$')))
      "
      border
      style="padding: 5px"
      :max-height="tableHeight"
    >
      <el-table-column property="index" label="序号" width="60"></el-table-column>
      <el-table-column property="date" label="时间" width="90"></el-table-column>
      <el-table-column property="source" label="客户端" width="70"></el-table-column>
      <el-table-column property="eventName" label="事件名" min-width="100"></el-table-column>
      <el-table-column property="result" label="解码文本" :show-overflow-tooltip="true">
        <template v-slot="scope">
          <span style="cursor: pointer; height: 40px" @click="handleJsonView(scope.row)">
            {{ scope.row.result }}
          </span>
        </template>
      </el-table-column>
      <el-table-column property="remark" label="操作" width="100">
        <template v-slot="scope">
          <el-button icon="el-icon-search" circle size="mini" @click="handleJsonView(scope.row)"></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="jsonViewDialog">
      <v-jsoneditor
        ref="jsonEditor"
        v-model="this.jsonViewTmp"
        :options="jsonOptions"
        :plus="true"
        :height="height"
        @error="onError"
      >
      </v-jsoneditor>
    </el-dialog>

    <el-drawer title="示例表格代码!" :visible.sync="table" direction="rtl" size="50%">
      <el-table :data="gridData" border style="padding: 5px">
        <el-table-column property="date" label="日期" width="150"></el-table-column>
        <el-table-column property="name" label="姓名" width="200"></el-table-column>
        <el-table-column property="address" label="地址"></el-table-column>
      </el-table>
    </el-drawer>
    <el-dialog title="请扫描二维码" :visible.sync="resultDialog" direction="rtl" width="340px">
      <el-input :readonly="true" v-model="debugImgUrl" style="margin-bottom: 10px">
        <el-button slot="append" @click="handleCopyText(debugImgUrl)" icon="el-icon-document-copy"></el-button>
      </el-input>
      <div style="text-align: center"><img :src="debugCodeImg" alt="调试二维码" /></div>
      <div style="text-align: center; margin-top: 10px">
        <a href="http://cbkbuy.cn/vi6jIv" target="_blank" title="知识库链接">如何设置？</a>
      </div>
    </el-dialog>
  </el-main>
</template>

<style>
.el-tooltip__popper {
  max-width: 50%;
}
</style>
