<script>
    import {mapActions, mapGetters} from "vuex"
    import Card                     from "./Card"

    export default {
        name: "IndexPartial",

        components: {Card},

        props: {
            search:  {
                type:     String,
                required: false,
                default:  ""
            },
            page:    {
                type:     Number,
                required: false,
                default:  1
            },
            perPage: {
                type:     Number,
                required: false,
                default:  12
            }
        },

        data() {
            return {
                params:     {
                    search:   this.search,
                    page:     this.page,
                    per_page: this.perPage,
                    sort:     null
                },
                pageSizes:  [12, 24, 50, 100],
                totalCount: 0
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"]),
        },

        created() {
            this.getData()
        },

        mounted() {
            this.$set(this.params, "search", this.search)
            this.$set(this.params, "page", this.page)
            this.$set(this.params, "per_page", this.per_page)
        },

        methods: {
            ...mapActions("alert", ["error", "success", "info", "warning"]),

            getData() {},

            searchData() {
                this.$set(this.params, "page", 1)

                this.getData()
            },

            sort({prop, order}) {
                if (prop && order) {
                    const direction = order === "descending" ? "-" : ""
                    this.$set(this.params, "sort", `${direction}${prop}`)
                } else {
                    this.$set(this.params, "sort", null)
                }

                this.getData()
            }
        }
    }
</script>