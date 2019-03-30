<template>
    <error>
        <template v-slot:error_code>
            500
        </template>
        <template v-slot:title>
            Houston, we have a problem!
        </template>
        <template v-slot:content>
            The page you are looking for is temporarily unavailable.
        </template>
    </error>
</template>

<script>
    import Error from "../../components/Error"

    export default {
        name: "Error500",

        components: {Error}
    }
</script>