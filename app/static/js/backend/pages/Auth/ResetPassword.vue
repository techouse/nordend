<template>
    <div class="col-md-6">
        <div class="card mx-4">
            <form action="" method="post" class="card-body p-4">
                <h1>Reset Your Password</h1>
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">
                            <i class="icon-lock" />
                        </span>
                    </div>
                    <input name="password" type="password" class="form-control" placeholder="Password">
                    <div />
                </div>
                <div class="input-group mb-4">
                    <div class="input-group-prepend">
                        <span class="input-group-text">
                            <i class="icon-lock" />
                        </span>
                    </div>
                    <input name="password2" type="password" class="form-control" placeholder="Repeat password">
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
        name: "ResetPassword"
    }
</script>