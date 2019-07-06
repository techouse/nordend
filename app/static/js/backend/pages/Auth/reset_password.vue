<template>
    <centered>
        <template v-slot:body>
            <div class="col-md-6">
                <div class="card mx-4">
                    <el-form :ref="formRef" :model="form" :rules="rules" class="card-body p-4">
                        <h1>Reset Your Password</h1>
                        <el-form-item class="input-group mb-3" prop="password">
                            <el-input v-model="form.password" type="password" placeholder="Password">
                                <template slot="prepend">
                                    <i class="icon-lock"/>
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item class="input-group mb-3" prop="password_repeat">
                            <el-input v-model="form.password_repeat" type="password" placeholder="Repeat password">
                                <template slot="prepend">
                                    <i class="icon-lock"/>
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" class="btn btn-block btn-primary" @click.prevent="submit">
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
        name: "ResetPassword",

        components: {
            Centered
        },

        props: {
            token: {
                type:     String,
                required: true
            }
        },

        data() {
            return {
                formRef: "reset-password-form",
                form:    {
                    token:           this.token,
                    password:        null,
                    password_repeat: null,
                    recaptchaToken:  null
                },
                rules:   {
                    password:        [
                        {required: true, message: "Please enter a password", trigger: "blur"},
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback(new Error("Please enter a password"))
                                } else if (value.length > 0 && value.length < 8) {
                                    callback(new Error("Password is too short"))
                                } else {
                                    if (this.form.password_repeat !== "") {
                                        this.$refs[this.formRef].validateField("password_repeat")
                                    }
                                    callback()
                                }
                            },
                            trigger:   "blur"
                        }
                    ],
                    password_repeat: [
                        {required: true, message: "Please re-enter the password", trigger: "blur"},
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback(new Error("Please re-enter the password"))
                                } else if (value !== this.form.password) {
                                    callback(new Error("The password confirmation does not match the password"))
                                } else {
                                    callback()
                                }
                            },
                            trigger:   "blur"
                        }
                    ],
                }
            }
        },

        mounted() {
            if (window.reCAPTCHASiteKey) {
                grecaptcha.ready(() => {
                    grecaptcha.execute(window.reCAPTCHASiteKey, {action: "reset_password"})
                              .then(token => {
                                  this.$set(this.form, "recaptchaToken", token)
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

                        api.patch("reset_password", this.form, {
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