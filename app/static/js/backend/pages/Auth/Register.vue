<template>
    <centered>
        <template v-slot:body>
            <div class="col-md-6">
                <div class="card mx-4">
                    <el-form :ref="formRef" :model="form" :rules="rules" class="card-body p-4">
                        <h1>Register</h1>
                        <p class="text-muted">
                            Create your account
                        </p>
                        <el-form-item class="input-group mb-3" prop="name">
                            <el-input v-model="form.name" type="text" placeholder="Name">
                                <template slot="prepend">
                                    <i class="icon-user"/>
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item class="input-group mb-3" prop="email">
                            <el-input v-model="form.email" placeholder="E-mail">
                                <template slot="prepend">@</template>
                            </el-input>
                        </el-form-item>
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
        name: "Register",

        components: {
            Centered
        },

        props: {
            csrfToken: {
                required: true,
                type:     String
            }
        },

        data() {
            return {
                formRef: "register-form",
                form:    {
                    name:            null,
                    email:           null,
                    password:        null,
                    password_repeat: null
                },
                rules:   {
                    name:            [
                        {required: true, message: "Please input name", trigger: "blur"},
                        {
                            min:     3,
                            max:     255,
                            message: "Please input a name with a length between 3 and 255 characters",
                            trigger: "blur"
                        }
                    ],
                    email:           [
                        {required: true, message: "Please input email address", trigger: "blur"},
                        {type: "email", message: "Please input correct email address", trigger: ["blur"]}
                    ],
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

        created() {
            if (this.csrfToken !== window.csrfToken) {
                this.logout()
            }
        },

        methods: {
            ...mapActions("alert", ["error", "info", "clear"]),

            ...mapActions("auth", ["logout"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.clear()

                        api.post("register", this.form, {
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
                                   if (error.response.status === 409) {
                                       this.$set(this.form, "email", "")
                                   }
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