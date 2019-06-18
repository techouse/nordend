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
                tableRef:          "listTable",
                loading:           false,
                multipleSelection: [],
                params:            {
                    search:   this.search,
                    page:     this.page,
                    per_page: this.perPage,
                    sort:     null
                },
                pageSizes:         [12, 24, 48, 96],
                totalCount:        0
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"]),
        },

        created() {
            this.$set(this, "loading", true)
            this.getData()
                .then(() => {
                    this.$set(this, "loading", false)
                })
                .catch(() => {
                    this.$set(this, "loading", false)
                })
        },

        mounted() {
            this.$set(this.params, "search", this.search)
            this.$set(this.params, "page", this.page)
            this.$set(this.params, "per_page", this.perPage)
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
            },

            toggleSelection(rows) {
                if (rows && Array.isArray(rows)) {
                    rows.forEach(row => {
                        this.$refs[this.tableRef].toggleRowSelection(row)
                    })
                } else {
                    this.$refs[this.tableRef].clearSelection()
                }
            },

            handleSelectionChange(val) {
                this.$set(this, "multipleSelection", val)
            },

            bulkRemove() {
                console.error("Not implemented. You must implement bulkRemove in the child component!")
            },

            handleBulkCommand(command) {
                command()
            }
        }
    }
</script>