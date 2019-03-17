<template>
    <div id="app">
        <auth v-if="$route.path.startsWith('/auth/')"/>
        <admin v-else/>
    </div>
</template>

<script>
    import Auth  from "./pages/auth/Auth"
    import Admin from "./pages/Admin"

    export default {
        name: "App",

        components: {
            Auth,
            Admin,
        }
    }
</script>

<style scoped>

</style>