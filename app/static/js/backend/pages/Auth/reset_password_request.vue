<template>
    <centered>
        <template v-slot:logo>
            <div class="col-md-8 text-center mb-4">
                <img width="224" src="/static/images/admin/logo_full.svg">
            </div>
        </template>
        <template v-slot:body>
            <div class="col-md-6">
                <div class="card mx-4">
                    <el-form :ref="formRef" :model="form" :rules="rules" class="card-body p-4">
                        <h1>Reset Password</h1>
                        <el-form-item class="input-group mb-3" prop="email">
                            <el-input v-model="form.email" type="email" placeholder="E-mail" required>
                                <template slot="prepend">@</template>
                            </el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" class="btn btn-block btn-primary" @click="submit">
                                Submit
                            </el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </template>
    </centered>
</template>

<script>
    import {mapActions} from "vuex"
    import Centered     from "../../components/Centered"
    import api          from "../../services/api"

    export default {
        name: "ResetPasswordRequest",

        components: {
            Centered
        },

        data() {
            return {
                formRef: "rest-password-request-form",
                form:    {
                    email:           null,
                    recaptcha_token: null
                },
                rules:   {
                    email: [
                        {required: true, message: "Please input email address", trigger: "blur"},
                        {type: "email", message: "Please input correct email address", trigger: ["blur"]}
                    ]
                }
            }
        },

        mounted() {
            if (window.reCAPTCHASiteKey) {
                grecaptcha.ready(() => {
                    grecaptcha.execute(window.reCAPTCHASiteKey, {action: "reset_password_request"})
                              .then(token => {
                                  this.$set(this.form, "recaptcha_token", token)
                              })
                })
            }
        },

        methods: {
            ...mapActions("alert", ["error", "info", "clear"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.clear()

                        api.post("reset_password_request", this.form, {
                               headers: {
                                   common: {
                                       "X-CSRF-TOKEN": window.csrfToken
                                   },
                               }
                           })
                           .then(({data}) => {
                               this.info(data.message)
                               this.$router.push({name: "Login"})
                           })
                           .catch(error => {
                               try {
                                   this.error(error.response.data.message)
                               } catch (e) {
                                   console.log(error)
                               }
                           })
                    } else {
                        this.error("The provided data is invalid!")
                        return false
                    }
                })
            }
        }
    }
</script>

<style lang="scss">
    .el-form-item__content {
        width: 100%;
    }
</style>