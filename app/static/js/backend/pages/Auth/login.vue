<template>
    <centered>
        <template v-slot:logo>
            <div class="col-md-8 text-center mb-4">
                <img width="224" src="/static/images/admin/logo_full.svg">
            </div>
        </template>
        <template v-slot:body>
            <div v-if="otpEnabled" class="col-md-8">
                <div class="card mx-4">
                    <el-form :model="otpForm" :rules="otpRules" class="card-body p-4">
                        <h4>Please enter the code from your authentication app</h4>
                        <el-form-item class="input-group mb-3" prop="totp">
                            <el-input v-model="otpForm.totp" placeholder="Please enter 6-digit one time password"
                                      :max="6" :min="6" :maxlength="6" required show-word-limit
                            >
                                <template slot="prepend">
                                    <i class="fal fa-key"/>
                                </template>
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
            <div v-else class="col-md-8">
                <div class="card-group">
                    <div class="card p-4">
                        <form class="card-body" @submit.prevent="submit">
                            <h1>Login</h1>
                            <p class="text-muted">
                                Sign In to your account
                            </p>
                            <div class="input-group mb-3">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="icon-user"/>
                                    </span>
                                </div>
                                <input v-model="email" class="form-control" type="email" placeholder="E-mail" required>
                            </div>
                            <div class="input-group mb-4">
                                <div class="input-group-prepend">
                                    <span class="input-group-text">
                                        <i class="icon-lock"/>
                                    </span>
                                </div>
                                <input v-model="password" class="form-control" type="password"
                                       placeholder="Password" required
                                >
                            </div>
                            <input v-model="remember" type="checkbox" name="remember_me" @change="rememberChanged">
                            <label>Remember me</label>
                            <div class="row">
                                <div class="col-6">
                                    <input class="btn btn-primary px-4" type="submit" value="Submit">
                                </div>
                                <div class="col-6 text-right">
                                    <router-link tag="button" class="btn btn-link px-0" type="button"
                                                 :to="{name: 'ResetPasswordRequest'}"
                                    >
                                        Forgot password?
                                    </router-link>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="card text-white bg-primary py-5 d-md-down-none" style="width:44%">
                        <div class="card-body text-center">
                            <div>
                                <h2>Sign up</h2>
                                <p>Not a user yet?</p>
                                <router-link tag="button" class="btn btn-primary active mt-3" type="button"
                                             :to="{name: 'Register', params: {csrfToken: csrfToken}}"
                                >
                                    Register Now!
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </centered>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import Centered                 from "../../components/Centered"
    import User                     from "../../models/User"

    export default {
        name: "Login",

        components: {
            Centered
        },

        data() {
            return {
                currentUser:     new User(),
                email:           null,
                password:        null,
                remember:        false,
                recaptcha_token: null,
                otpEnabled:      false,
                otpForm:         {
                    totp: null
                },
                otpRules:        {
                    totp: [
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback(new Error("Please fill the verification field!"))
                                } else {
                                    if (value.length !== 6) {
                                        callback(new Error("One time password must be exactly 6-digits long"))
                                    } else if (!value.match(/^\d+$/)) {
                                        callback(new Error("Please fill the verification with digits only!"))
                                    }
                                    callback()
                                }
                            },
                            trigger:   "blur"
                        }
                    ]
                }
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"]),

            csrfToken() {
                return window.csrfToken
            }
        },

        created() {
            this.$set(this, "remember", true)
            this.rememberChanged()
        },

        mounted() {
            if (window.reCAPTCHASiteKey) {
                grecaptcha.ready(() => {
                    grecaptcha.execute(window.reCAPTCHASiteKey, {action: "login"})
                              .then(token => {
                                  this.$set(this, "recaptcha_token", token)
                              })
                })
            }
        },

        methods: {
            ...mapActions("auth", [
                "login",
                "rememberMe"
            ]),

            ...mapActions("user", ["getUser", "setCurrentUser"]),

            rememberChanged() {
                this.rememberMe(this.remember)
            },

            submit() {
                if (this.email && this.password) {
                    this.login({
                                   email:           this.email,
                                   password:        this.password,
                                   recaptcha_token: this.recaptcha_token,
                                   totp:            this.otpForm.totp
                               })
                        .then(({userId}) => {
                            this.getUser(userId)
                                .then(({data}) => {
                                    this.$set(this, "currentUser", new User(data))

                                    this.setCurrentUser(this.currentUser)

                                    this.$router.push({name: "Dashboard"})
                                })
                        })
                        .catch(error => {
                            if (window.reCAPTCHASiteKey) {
                                grecaptcha.ready(() => {
                                    grecaptcha.execute(window.reCAPTCHASiteKey, {action: "login"})
                                              .then(token => {
                                                  this.$set(this, "recaptcha_token", token)
                                              })
                                })
                            }

                            try {
                                const response = error.response
                                if (response.status === 403) {
                                    this.$router.push({name: "Unconfirmed", params: {token: response.data.token}})
                                } else if (response.status === 412) {
                                    this.$set(this, "otpEnabled", true)
                                }
                            } catch (e) {
                                console.log(error)
                            }
                        })
                }
            }
        }
    }
</script>