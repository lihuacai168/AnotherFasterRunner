<template>
  <el-container class="login">
    <el-header>
      <el-row>
        <el-col :span="4" :offset="1">
          <div></div>
        </el-col>
      </el-row>
    </el-header>
    <el-main style="padding: 0px">
      <el-row>
        <el-col :span="7">
          <div class="bottom-left">
            <img src="~@/assets/images/bottom-left.png" />
          </div>
        </el-col>
        <el-col :span="24">
          <div>
            <div id="form-title">{{ this.$store.state.FasterRunner }}</div>
            <form id="submit-form">
              <div id="form-content">
                <div id="form-msg">注册账号</div>
                <div id="form-inputs">
                  <div class="form-input-div">
                    <i class="iconfont" style="position: absolute; bottom: 375px; padding-left: 10px">&#xe61c;</i>
                    <input placeholder="用户名" type="text" id="user" v-model="registerForm.username" />
                    <div class="err_msg" id="user_err" v-html="usernameInvalid" @mouseover="usernameInvalid = ''"></div>
                  </div>
                  <div class="form-input-div">
                    <i class="iconfont" style="position: absolute; bottom: 312px; padding-left: 10px">&#xe652;</i>
                    <input placeholder="密码" type="password" id="pwd" v-model="registerForm.password" />
                    <div class="err_msg" id="pwd_err" v-html="passwordInvalid" @mouseover="passwordInvalid = ''"></div>
                  </div>
                  <div class="form-input-div">
                    <i class="iconfont" style="position: absolute; bottom: 250px; padding-left: 10px">&#xe652;</i>
                    <input placeholder="确认密码" type="password" id="repwd" v-model="registerForm.repwd" />
                    <div class="err_msg" id="repwd_err" v-html="repwdInvalid" @mouseover="repwdInvalid = ''"></div>
                  </div>
                  <div class="form-input-div">
                    <i class="iconfont" style="position: absolute; bottom: 190px; padding-left: 10px">&#xe668;</i>
                    <input placeholder="邮箱" type="email" id="email" v-model="registerForm.email" />
                    <div class="err_msg" id="email_err" v-html="emailInvalid" @mouseover="emailInvalid = ''"></div>
                  </div>
                  <div class="form-submit">
                    <button type="button" class="btn btn-primary" id="submitBtn" @click="submitForm">立即注册</button>
                  </div>
                </div>
                <div class="form-foot">
                  <span>已有账户，<router-link to="/fastrunner/login">立即登陆</router-link></span>
                </div>
              </div>
            </form>
          </div>
        </el-col>
        <el-col :span="7">
          <div class="bottom-right">
            <img src="~@/assets/images/bottom-right.png" />
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      registerForm: {
        username: "",
        password: "",
        repwd: "",
        email: ""
      },
      passwordInvalid: "",
      usernameInvalid: "",
      repwdInvalid: "",
      emailInvalid: ""
    };
  },
  methods: {
    validateUser() {
      const uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
      if (!uPattern.test(this.registerForm.username)) {
        this.usernameInvalid = "用户名4到16位,只能是字母,数字,下划线,连字符";
        return false;
      }
      return true;
    },

    validatePassword() {
      const pPattern = /^[a-zA-Z\d_]{6,}$/;
      if (!pPattern.test(this.registerForm.password)) {
        this.passwordInvalid = "密码至少6位数";
        return false;
      }
      return true;
    },

    validateRepwd() {
      if (this.registerForm.password !== this.registerForm.repwd) {
        this.repwdInvalid = "确认密码和密码不一致";
        return false;
      }
      return true;
    },

    validateEmail() {
      const ePattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
      if (!ePattern.test(this.registerForm.email)) {
        this.emailInvalid = "邮箱格式不正确";
        return false;
      }
      return true;
    },

    handleRegisterSuccess(resp) {
      if (resp["success"]) {
        this.$router.push("/fastrunner/login");
      } else {
        this.$message.error({
          message: resp["msg"],
          duration: 2000,
          center: true
        });
      }
    },
    submitForm(formName) {
      if (this.validateUser() && this.validatePassword() && this.validateRepwd() && this.validateEmail()) {
        this.$api.register(this.registerForm).then((resp) => {
          this.handleRegisterSuccess(resp);
        });
      }
    }
  }
};
</script>

<style scoped></style>
