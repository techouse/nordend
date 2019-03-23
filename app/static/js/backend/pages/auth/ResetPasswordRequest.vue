<template>
    <div class="col-md-6">
        <div class="card mx-4">
            <form action="" method="post" class="card-body p-4">
                <h1>Reset Password</h1>
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">@</span>
                    </div>
                    <input name="email" type="email" class="form-control" placeholder="E-mail">
                </div>
                <p>
                    <input type="submit" class="btn btn-block btn-success" value="Submit">
                </p>
            </form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ResetPasswordRequest"
    }
</script>