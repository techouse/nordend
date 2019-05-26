<template>
    <card>
        <template v-slot:header>
            <b>{{ title }}</b>
        </template>
        <template v-slot:body>
            TODO images go here
        </template>
    </card>
</template>

<script>
    import IndexPartial from "../../components/IndexPartial"

    export default {
        name: "Images",

        extends: IndexPartial,

        data() {
            return {
                title:      "Images",
            }
        },

         methods: {
            getData() {

            }
         }
    }
</script>