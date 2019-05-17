<template>
    <div class="col-md-8">
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
                                <i class="icon-user" />
                            </span>
                        </div>
                        <input v-model="email" class="form-control" type="email" placeholder="E-mail">
                    </div>
                    <div class="input-group mb-4">
                        <div class="input-group-prepend">
                            <span class="input-group-text">
                                <i class="icon-lock" />
                            </span>
                        </div>
                        <input v-model="password" class="form-control" type="password" placeholder="Password">
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

<script>
    import {mapActions, mapGetters} from "vuex"
    import User                     from "../../models/User"

    export default {
        name: "Login",

        data() {
            return {
                email:    null,
                password: null,
                remember: false
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"]),

            csrfToken() {
                return window.csrfToken
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
                    this.login({email: this.email, password: this.password})
                        .then(({userId}) => {
                            this.getUser(userId)
                                .then(({data}) => {
                                    this.setCurrentUser(new User(data))

                                    this.$router.push({name: "Dashboard"})
                                })
                        })
                        .catch(error => {
                            try {
                                const response = error.response
                                if (response.status === 403) {
                                    this.$router.push({name: "Unconfirmed", params: {token: response.data.token}})
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