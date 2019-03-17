<template>
    <div class="col-md-6">
        <div class="card mx-4">
            <form method="post" action="" class="card-body p-4">
                <h1>Register</h1>
                <p class="text-muted">
                    Create your account
                </p>
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">
                            <i class="icon-user" />
                        </span>
                    </div>
                    <input name="name" type="text" class="form-control" placeholder="Name">
                </div>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">@</span>
                    </div>
                    <input name="email" type="email" class="form-control" placeholder="E-mail">
                </div>

                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">
                            <i class="icon-lock" />
                        </span>
                    </div>
                    <input name="password" type="password" class="form-control" placeholder="Password">
                </div>
                <div class="input-group mb-4">
                    <div class="input-group-prepend">
                        <span class="input-group-text">
                            <i class="icon-lock" />
                        </span>
                    </div>
                    <input name="password2" type="password" class="form-control" placeholder="Repeat password">
                </div>
                <input type="submit" class="btn btn-block btn-success" value="Submit">
            </form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Register"
    }
</script>

<style scoped>

</style>