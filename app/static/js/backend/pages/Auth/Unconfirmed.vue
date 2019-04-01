<template>
    <div class="col-md-8">
        <div class="card mx-8">
            <div class="card-body p-8">
                <h1 class="text-center">Confirm your account</h1>
                <h3 class="text-danger text-center">You have not confirmed your account yet!</h3>
                <p>
                    Before you can access this site you need to confirm your account.
                    Check your inbox, you should have received an email with a confirmation link.
                </p>
                <p class="text-center">
                    <el-button type="primary" @click.prevent="send">
                        Send me another confirmation e-mail
                    </el-button>
                </p>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapActions} from "vuex"

    export default {
        name: "Unconfirmed",

        props: {
            token: {
                required: true,
                type:     String
            }
        },

        methods: {
            ...mapActions("auth", ["sendAnotherConfirmationEmail"]),

            ...mapActions("alert", ["success"]),

            send() {
                this.sendAnotherConfirmationEmail(this.token)
                    .then(({data}) => {
                        this.success(data.message)
                    })

                this.$router.push({name: "Login"})
            }
        }
    }
</script>