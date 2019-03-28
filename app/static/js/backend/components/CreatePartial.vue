<script>
    import {mapActions, mapGetters} from "vuex"

    export default {
        name: "CreatePartial",

        data() {
            return {
                formRef: "create-form",
                title:   "Create",
                rules:   {}
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"])
        },

        methods: {
            ...mapActions("alert", ["error", "success", "info", "warning"]),

            submit() {
            },

            remove() {
            }
        }
    }
</script>