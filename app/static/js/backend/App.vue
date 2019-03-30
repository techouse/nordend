<template>
    <div id="app">
        <auth v-if="$route.path.startsWith('/auth/')" />
        <admin v-else />
    </div>
</template>

<script>
    import {mapGetters, mapActions} from "vuex"
    import Auth                     from "./pages/Auth"
    import Admin                    from "./pages/Admin"

    export default {
        name: "App",

        components: {
            Auth,
            Admin
        },

        computed: {
            ...mapGetters("alert", ["alert"])
        },

        methods: {
            ...mapActions("alert", {
                clearAlert: "clear"
            })
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
        }
    }
</script>
