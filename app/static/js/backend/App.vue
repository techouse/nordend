<template>
    <div id="app">
        <auth v-if="isAuthPage"/>
        <admin v-else-if="isAdministrationPage"/>
        <error v-else-if="isErrorPage"/>
        <div v-else/>
    </div>
</template>

<script>
    import {mapGetters, mapActions} from "vuex"

    export default {
        name: "App",

        components: {
            "auth":  () => import(/* webpackChunkName: "auth" */ "./pages/Auth"),
            "admin": () => import(/* webpackChunkName: "admin" */ "./pages/Admin"),
            "error": () => import(/* webpackChunkName: "errors" */ "./pages/Errors")
        },

        computed: {
            ...mapGetters("alert", ["alert"]),

            ...mapGetters("auth", ["isAuthenticated"]),

            isAuthPage() {
                return "meta" in this.$route && "auth" in this.$route.meta && this.$route.meta.auth === true
            },

            isErrorPage() {
                return "meta" in this.$route && "error" in this.$route.meta && this.$route.meta.error === true
            },

            isAdministrationPage() {
                return "meta" in this.$route && "requiresAuth" in this.$route.meta && this.$route.meta.requiresAuth === true
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
