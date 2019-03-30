<template>
    <error>
        <template v-slot:error_code>
            404
        </template>
        <template v-slot:title>
            Oops! You're lost.
        </template>
        <template v-slot:content>
            The page you are looking for was not found.
        </template>
    </error>
</template>

<script>
    import Error from "../../components/Error"

    export default {
        name: "Error404",

        components: {Error}
    }
</script>