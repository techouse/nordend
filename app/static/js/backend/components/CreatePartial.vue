<script>
    import {mapActions, mapGetters} from "vuex"

    export default {
        name: "CreatePartial",

        data() {
            return {
                labelWidth: "140px",
                formRef:    "create-form",
                rules:      {},
                loading:    false
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
            },

            goBack() {
                this.$router.go(-1)
            }
        }
    }
</script>

<style lang="scss" scoped>
    .el-form-item__content {
        & > div:first-child {
            width: calc(100% - 140px);
        }
    }
</style>