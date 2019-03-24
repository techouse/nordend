<template>
    <div id="app">
        <auth v-if="$route.path.startsWith('/auth/')"/>
        <admin v-else/>
    </div>
</template>

<script>
    import {mapGetters} from "vuex"
    import Auth         from "./pages/auth/Auth"
    import Admin        from "./pages/Admin"

    export default {
        name: "App",

        components: {
            Auth,
            Admin,
        },

        computed: {
            ...mapGetters("alert", ["alert"])
        },

        watch: {
            alert: {
                handler(alert) {
                    if (alert && alert.message && alert.type) {
                        this.$message(alert)
                    }
                },
                deep: true
            }
        }
    }
</script>
