<template>
  <el-container>
    <el-header style="background: #f7f7f7; padding: 0; height: 50px">
      <div class="apiData">
        <div style="padding-top: 10px; margin-left: 10px">
          <el-button type="primary" size="small" icon="el-icon-circle-plus" @click="dialogVisible = true">
            添加数据库
          </el-button>

          <el-button
            style="margin-left: 50px"
            type="info"
            round
            size="small"
            icon="el-icon-d-arrow-left"
            :disabled="dataBaseData.previous === null"
            @click="getPagination(dataBaseData.previous)"
          >
            上一页
          </el-button>

          <el-button
            type="info"
            round
            size="small"
            :disabled="dataBaseData.next === null"
            @click="getPagination(dataBaseData.next)"
          >
            下一页
            <i class="el-icon-d-arrow-right"></i>
          </el-button>

          <el-dialog title="添加数据库" :visible.sync="dialogVisible" width="40%" align="center">
            <div style="padding-bottom: 10px; cursor: pointer" id="db_type">
              <el-radio-group v-model="dataBaseForm.type">
                <el-radio v-for="item in tags" :key="item.value" :label="item.value">{{ item.name }} </el-radio>
              </el-radio-group>
            </div>

            <el-form :model="dataBaseForm" :rules="rules" ref="dataBaseForm" label-width="100px">
              <el-form-item label="数据库名称" prop="name">
                <el-input v-model="dataBaseForm.name"></el-input>
              </el-form-item>

              <el-form-item label="访问地址" prop="name">
                <el-input v-model="dataBaseForm.server"></el-input>
              </el-form-item>

              <el-form-item label="登陆账号" prop="account">
                <el-input v-model="dataBaseForm.account"></el-input>
              </el-form-item>

              <el-form-item label="登陆密码" prop="password">
                <el-input v-model="dataBaseForm.password"></el-input>
              </el-form-item>

              <el-form-item label="简要描述" prop="desc">
                <el-input v-model="dataBaseForm.desc"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="handleConfirm('dataBaseForm')">确 定</el-button>
            </span>
          </el-dialog>
        </div>
      </div>
    </el-header>

    <el-container>
      <el-main style="padding: 0; margin-left: 10px">
        <el-table
          :data="dataBaseData.results"
          border
          stripe
          highlight-current-row
          style="width: 100%"
          :show-header="dataBaseData.results.length > 0"
        >
          <el-table-column label="数据库名称" width="250" align="center">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.type === 1" type="">Sql Server</el-tag>
              <el-tag v-if="scope.row.type === 2" type="success">MySQL</el-tag>
              <el-tag v-if="scope.row.type === 3" type="warning">Oracle</el-tag>
              <el-tag v-if="scope.row.type === 4" type="danger">Mongodb</el-tag>
              <el-tag v-if="scope.row.type === 5" type="info">InfluxDB</el-tag>
              <span style="margin-left: 10px; font-size: 18px; font-weight: bold">{{ scope.row.name }}</span>
            </template>
          </el-table-column>

          <el-table-column label="访问地址" width="200" align="center">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag type="info" style="font-size: 16px">{{ scope.row.server }}</el-tag>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="用户名/密码" width="250" align="center">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag type="info" style="font-size: 16px">{{ scope.row.desc }}</el-tag>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="描述" width="300" align="center">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag type="info" style="font-size: 16px">{{ scope.row.desc }}</el-tag>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <el-button size="medium" @click="handleEdit(scope.$index, scope.row)">编辑 </el-button>

              <el-dialog title="编辑数据库" :visible.sync="editVisible" width="40%" align="center">
                <el-form :model="dataBaseForm" :rules="rules" ref="dataBaseForm" label-width="100px">
                  <el-form-item label="数据库名称" prop="name">
                    <el-input v-model="dataBaseForm.name"></el-input>
                  </el-form-item>

                  <el-form-item label="访问地址" prop="name">
                    <el-input v-model="dataBaseForm.server"></el-input>
                  </el-form-item>

                  <el-form-item label="登陆账号" prop="account">
                    <el-input v-model="dataBaseForm.account"></el-input>
                  </el-form-item>

                  <el-form-item label="登陆密码" prop="password">
                    <el-input v-model="dataBaseForm.password"></el-input>
                  </el-form-item>

                  <el-form-item label="简要描述" prop="desc">
                    <el-input v-model="dataBaseForm.desc"></el-input>
                  </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="dialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="handleConfirm('dataBaseForm')">确 定</el-button>
                </span>
              </el-dialog>

              <el-button size="medium" type="danger" @click="handleDelete(scope.$index, scope.row)">删除 </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      editVisible: false,
      dialogVisible: false,
      dataBaseData: {
        results: [],
      },
      dataBaseForm: {
        name: "",
        desc: "",
        server: "",
        account: "",
        password: "",
        type: 2,
        id: "",
      },
      tags: [
        { name: "Sql Server", value: 1 },
        { name: "MySQL", value: 2 },
        { name: "Oracle", value: 3 },
        { name: "Mongodb", value: 4 },
        { name: "InfluxDB", value: 5 },
      ],
      rules: {
        name: [
          { required: true, message: "请输入数据库名称", trigger: "blur" },
          { min: 1, max: 50, message: "最多不超过50个字符", trigger: "blur" },
        ],
        server: [
          { required: true, message: "请输入数据库访问地址", trigger: "blur" },
          { min: 1, max: 50, message: "最多不超过50个字符", trigger: "blur" },
        ],
        account: [
          { required: true, message: "请输入登陆账号", trigger: "blur" },
          { min: 1, max: 50, message: "最多不超过50个字符", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入登陆密码", trigger: "blur" },
          { min: 1, max: 50, message: "最多不超过50个字符", trigger: "blur" },
        ],
        desc: [
          { required: true, message: "请简要描述下该数据库", trigger: "blur" },
          { min: 1, max: 100, message: "最多不超过100个字符", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    handleEdit(index, row) {
      this.editVisible = true;
      this.dataBaseForm.name = row["name"];
      this.dataBaseForm.desc = row["desc"];
      this.dataBaseForm.id = row["id"];
      this.dataBaseForm.server = row["server"];
      this.dataBaseForm.type = row["type"];
      this.dataBaseForm.account = row["account"];
      this.dataBaseForm.password = row["password"];
    },
    handleDelete(index, row) {
      this.$confirm("此操作将永久删除该数据库, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        this.$api
          .deleteDataBase(row["id"])
          .then((resp) => {
            this.success("数据库删除成功");
            this.getDataBaseList();
          })
          .catch((resp) => {
            this.failure(resp);
          });
      });
    },
    handleConfirm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.dialogVisible = false;
          this.editVisible = false;
          let obj;

          if (this.dataBaseForm.id === "") {
            obj = this.$api.addDataBase(this.dataBaseForm);
          } else {
            obj = this.$api.updateDataBase(this.dataBaseForm.id, this.dataBaseForm);
          }
          obj
            .then((resp) => {
              if (resp["name"] === this.dataBaseForm.name) {
                this.success(resp["name"] + "数据库操作成功");
                this.getDataBaseList();
              }

              this.dataBaseForm.name = "";
              this.dataBaseForm.desc = "";
              this.dataBaseForm.id = "";
              this.dataBaseForm.account = "";
              this.dataBaseForm.password = "";
              this.dataBaseForm.server = "";
              this.dataBaseForm.type = 2;
            })
            .catch((resp) => {
              this.failure(resp);
            });
        } else {
          if (this.dataBaseForm.id !== "") {
            this.editVisible = true;
          } else {
            this.dialogVisible = true;
          }
          return false;
        }
      });
    },
    success(resp) {
      this.$notify({
        message: resp,
        type: "success",
        duration: this.$store.state.duration,
      });
    },
    failure(resp) {
      this.$notify.error({
        message: resp,
        duration: this.$store.state.duration,
      });
    },
    getDataBaseList() {
      this.$api.getDataBaseList().then((resp) => {
        this.dataBaseData = resp;
      });
    },
    getPagination(url) {
      this.$api.getPagination(url).then((resp) => {
        this.dataBaseData = resp;
      });
    },
  },
  mounted() {
    this.getDataBaseList();
  },
  name: "DataBase",
};
</script>

<style scoped></style>
