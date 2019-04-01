<template>
    <div id="app">
        <auth v-if="isAuthPage" />
        <error v-else-if="isErrorPage && !isAuthenticated" />
        <admin v-else />
    </div>
</template>

<script>
    import {mapGetters, mapActions} from "vuex"
    import Auth                     from "./pages/Auth"
    import Admin                    from "./pages/Admin"
    import Error                    from "./pages/Errors"

    export default {
        name: "App",

        components: {
            Auth,
            Admin,
            Error
        },

        computed: {
            ...mapGetters("alert", ["alert"]),

            ...mapGetters("auth", ["isAuthenticated"]),

            isAuthPage() {
                return "meta" in this.$route && "auth" in this.$route.meta && this.$route.meta.auth === true
            },

            isErrorPage() {
                return "meta" in this.$route && "error" in this.$route.meta && this.$route.meta.error === true
            }
        },

        watch: {
            alert: {
                handler(alert) {
                    if (alert && alert.message && alert.type) {
                        this.$message(alert)
                        this.clearAlert()
                    }
                },
                deep: true
            }
        },

        methods: {
            ...mapActions("alert", {
                clearAlert: "clear"
            })
        }
    }
</script>
