<template>

    <el-container class="login">
        <el-header>
            <el-row>
                <el-col
                    :span="4"
                    :offset="1"
                >
                    <div>

                    </div>
                </el-col>
            </el-row>
        </el-header>
        <el-main style="padding: 0px">
            <el-row>
                <el-col :span="7">
                    <div class="bottom-left">
                        <img src="~@/assets/images/bottom-left.png">
                    </div>

                </el-col>
                <el-col :span="24">
                    <div>
                        <div id="form-title">{{ this.$store.state.FasterRunner }}自动化测试平台</div>
                        <form id="submit-form">
                            <div id="form-content">
                                <div id="form-msg">登录账号</div>
                                <div id="form-inputs">
                                    <div class="form-input-div">
                                        <i class="iconfont"
                                           style="position: absolute; bottom: 250px; padding-left: 10px">&#xe61c;</i>
                                        <input placeholder="用户名" type="text" id="email" v-model="loginForm.username">
                                        <div class="err_msg" id="email_err" v-html="usernameInvalid"
                                             @mouseover="usernameInvalid=''"></div>
                                    </div>
                                    <div class="form-input-div">
                                        <i class="iconfont"
                                           style="position: absolute; bottom: 190px; padding-left: 10px">&#xe652;</i>
                                        <input placeholder="密码" type="password" id="pwd" v-model="loginForm.password">
                                        <div class="err_msg" id="pwd_err" v-html="passwordInvalid"
                                             @mouseover="passwordInvalid= ''"></div>
                                    </div>
                                    <div class="form-submit">
                                        <button type="button" class="btn btn-primary" id="submitBtn"
                                                @click="submitForm">立即登录
                                        </button>
                                    </div>
                                </div>
                                <div class="form-foot">
                                    <span>注册功能已经关闭，创建用户请联系管理员</span>
                                </div>

                            </div>
                        </form>

                    </div>

                </el-col>
                <el-col :span="7">
                    <div class="bottom-right">
                        <img src="~@/assets/images/bottom-right.png">
                    </div>
                </el-col>
            </el-row>

        </el-main>
    </el-container>

</template>

<script>

export default {
    name: "Login",

    data() {
        return {
            loginForm: {
                username: '',
                password: '',
            },
            usernameInvalid: '',
            passwordInvalid: ''
        };
    },

    methods: {
        validateUserName() {
            if (this.loginForm.username.replace(/(^\s*)/g, "") === '') {
                this.usernameInvalid = "用户名不能为空";
                return false;
            }
            return true
        },
        validatePassword() {
            if (this.loginForm.password.replace(/(^\s*)/g, "") === '') {
                this.passwordInvalid = "密码不能为空";
                return false;
            }
            return true;
        },
        handleLoginSuccess(resp) {
            if (resp.success) {
                this.$router.push({name: 'ProjectList'});
                this.$store.commit("isLogin", resp.token);
                this.$store.commit("setUser", resp.user);
                this.$store.commit("setIsSuperuser", resp.is_superuser);
                this.$store.commit("setRouterName", 'ProjectList');
                this.$store.commit("setShowHots", resp.show_hosts);
                this.setLocalValue("token", resp.token);
                this.setLocalValue("user", resp.user);
                this.setLocalValue("routerName", 'ProjectList');
                this.setLocalValue("is_superuser", resp.is_superuser);
                this.setLocalValue("show_hosts", resp.show_hosts);
            } else {
                this.$message.error({
                    message: resp.msg,
                    duration: 2000,
                    center: true
                })
            }
        },
        submitForm() {
            if (this.validateUserName() && this.validatePassword()) {
                this.$api.login(this.loginForm).then(resp => {
                    this.handleLoginSuccess(resp)
                })
            }
        }
    }
}
</script>

<style scoped>

</style>
