<template>
    <div class="col-md-8">
        <div class="card-group">
            <div class="card p-4">
                <form method="post" action="" class="card-body">
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
                        <input class="form-control" type="email" placeholder="E-mail">
                    </div>
                    <div class="input-group mb-4">
                        <div class="input-group-prepend">
                            <span class="input-group-text">
                                <i class="icon-lock" />
                            </span>
                        </div>
                        <input class="form-control" type="password" placeholder="Password">
                    </div>
                    <input type="checkbox" name="remember_me">
                    <label>Remember me</label>
                    <div class="row">
                        <div class="col-6">
                            <input class="btn btn-primary px-4" type="submit" value="Submit">
                        </div>
                        <div class="col-6 text-right">
                            <router-link class="btn btn-link px-0" type="button" :to="{name: 'ResetPasswordRequest'}">
                                Forgot your password?
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
                        <router-link class="btn btn-primary active mt-3" type="button" :to="{name: 'Register'}">
                            Register Now!
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Login"
    }
</script>

<style scoped>

</style>