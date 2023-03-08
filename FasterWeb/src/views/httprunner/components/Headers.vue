<template>
  <el-table
    highlight-current-row
    :data="tableData"
    :height="height"
    style="width: 100%"
    :border="false"
    @cell-mouse-enter="cellMouseEnter"
    @cell-mouse-leave="cellMouseLeave"
    :cell-style="{ paddingTop: '4px', paddingBottom: '4px' }"
  >
    <el-table-column label="标签" width="190">
      <template v-slot="scope">
        <el-autocomplete
          clearable
          v-model="scope.row.key"
          :fetch-suggestions="querySearch"
          size="medium"
          placeholder="头部标签"
          style="margin-left: 5px"
        >
        </el-autocomplete>
      </template>
    </el-table-column>

    <el-table-column label="内容" min-width="280" style="margin-left: 5px">
      <template v-slot="scope">
        <el-input clearable v-model="scope.row.value" placeholder="头部内容" size="medium"></el-input>
      </template>
    </el-table-column>

    <el-table-column label="描述" width="180">
      <template v-slot="scope">
        <el-input clearable v-model="scope.row.desc" placeholder="头部信息简要描述" size="medium"></el-input>
      </template>
    </el-table-column>

    <el-table-column width="120">
      <template v-slot="scope">
        <el-row v-show="scope.row === currentRow">
          <el-button
            icon="el-icon-circle-plus-outline"
            size="mini"
            circle
            type="info"
            style="margin-left: 5px"
            @click="handleEdit(scope.$index, scope.row)"
          >
          </el-button>
          <el-button
            icon="el-icon-delete"
            size="mini"
            circle
            type="danger"
            v-show="scope.$index !== 0"
            style="margin-left: 5px"
            @click="handleDelete(scope.$index, scope.row)"
          >
          </el-button>
        </el-row>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  props: {
    save: Boolean,
    header: {
      require: false,
    },
  },
  methods: {
    querySearch(queryString, cb) {
      let headerOptions = this.headerOptions;
      let results = queryString ? headerOptions.filter(this.createFilter(queryString)) : headerOptions;
      cb(results);
    },

    createFilter(queryString) {
      return (headerOptions) => {
        return headerOptions.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
      };
    },

    cellMouseEnter(row) {
      this.currentRow = row;
    },

    cellMouseLeave(row) {
      this.currentRow = "";
    },

    handleEdit(index, row) {
      this.tableData.push({
        key: "",
        value: "",
        desc: "",
      });
    },

    handleDelete(index, row) {
      this.tableData.splice(index, 1);
    },

    // 头部信息格式化
    parseHeader() {
      let header = {
        header: {},
        desc: {},
      };
      for (let content of this.tableData) {
        if (content["key"] !== "" && content["value"] !== "") {
          header.header[content["key"]] = content["value"];
          header.desc[content["key"]] = content["desc"];
        }
      }
      return header;
    },
  },
  watch: {
    save: function () {
      this.$emit("header", this.parseHeader(), this.tableData);
    },

    header: function () {
      if (this.header.length !== 0) {
        this.tableData = this.header;
      }
    },
  },
  computed: {
    height() {
      return window.screen.height - 440;
    },
  },
  data() {
    return {
      headerOptions: [
        {
          value: "Accept",
        },
        {
          value: "Accept-Charset",
        },
        {
          value: "Accept-Language",
        },
        {
          value: "Accept-Datetime",
        },
        {
          value: "Authorization",
        },
        {
          value: "Cache-Control",
        },
        {
          value: "Connection",
        },
        {
          value: "Cookie",
        },
        {
          value: "Content-Length",
        },
        {
          value: "Content-MD5",
        },
        {
          value: "Content-Type",
        },
        {
          value: "Expect",
        },
        {
          value: "Date",
        },
        {
          value: "From",
        },
        {
          value: "Host",
        },
        {
          value: "If-Match",
        },
        {
          value: "If-Modified-Since",
        },
        {
          value: "If-None-Match",
        },
        {
          value: "If-Range",
        },
        {
          value: "If-Unmodified-Since",
        },
        {
          value: "Max-Forwards",
        },
        {
          value: "Origin",
        },
        {
          value: "Pragma",
        },
        {
          value: "Proxy-Authorization",
        },
        {
          value: "Range",
        },
        {
          value: "Referer",
        },
        {
          value: "TE",
        },
        {
          value: "User-Agent",
        },
        {
          value: "Upgrade",
        },
        {
          value: "Via",
        },
        {
          value: "Warning",
        },
      ],

      currentRow: "",
      tableData: [{ key: "", value: "", desc: "" }],
    };
  },
  name: "Header",
};
</script>

<style scoped></style>
