<script>
    import {mapActions, mapGetters} from "vuex"

    export default {
        name: "CreatePartial",

        data() {
            return {
                labelWidth: "140px",
                formRef:    "create-form",
                rules:      {}
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"]),

            title() {
                return "Create"
            }
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

<style lang="scss" scoped>
    .el-form-item__content {
        &>div:first-child {
            width: calc(100% - 140px);
        }
    }
</style>