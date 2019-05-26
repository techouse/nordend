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
            },
            sort:    {
                type:     String,
                required: false,
                default:  ""
            }
        },

        data() {
            return {
                params:     {
                    search:   this.search,
                    page:     this.page,
                    per_page: this.per_page,
                    sort:     null
                },
                pageSizes:  [12, 24, 48, 96],
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
            this.$set(this.params, "sort", this.sort)
        },

        methods: {
            ...mapActions("alert", ["error", "success", "info", "warning"]),

            getData() {
                console.warn("Implement getData in a child component!")
            },

            searchData() {
                this.$set(this.params, "page", 1)

                this.getData()
            },

            orderBy({prop, order}) {
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