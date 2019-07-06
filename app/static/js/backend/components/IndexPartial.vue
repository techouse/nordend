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
            this.updateData()
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

            updateData(image) {
                this.$set(this, "loading", true)

                this.getData()
                    .then(() => {
                        this.$set(this, "loading", false)
                    })
                    .catch(() => {
                        this.$set(this, "loading", false)
                    })
            },

            searchData() {
                this.$set(this.params, "page", 1)

                this.updateData()
            },

            orderBy({prop, order}) {
                if (prop && order) {
                    const direction = order === "descending" ? "-" : ""
                    this.$set(this.params, "sort", `${direction}${prop}`)
                } else {
                    this.$set(this.params, "sort", null)
                }

                this.updateData()
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

            _bulkRemove(callback, singularLabel = "record", pluralLabel = null) {
                if (typeof callback !== "function") {
                    console.error("Invalid callback function provided!")
                    return
                }
                const count = this.multipleSelection.length
                const label = count > 1 ? pluralLabel || `${singularLabel}s` : singularLabel

                this.$confirm(`Are you sure you want to delete ${count} ${label}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                        const ids = this.multipleSelection.map(el => el.id)
                        callback(ids)
                            .then(() => {
                                this.updateData()
                                this.success(`${count} ${label} successfully deleted`)
                                this.$set(this, "multipleSelection", this.multipleSelection.filter(el => !ids.includes(el.id)))
                            })
                            .catch(() => {
                                this.error(`There was an error deleting the ${count} ${label}: ${this.alert.message}`)
                            })
                    })
                    .catch(() => {
                        this.info(`${count} ${label} were not deleted.`)
                    })
            },

            remove(item = null) {
                console.error("Not implemented. You must implement remove in the child component!")
            },

            _remove(callback, model, label = "record") {
                if (typeof callback !== "function") {
                    console.error("Invalid callback function provided!")
                    return
                }

                if (typeof model !== "object" || model.id === undefined) {
                    console.error("Invalid model provided!")
                    return
                }

                this.$confirm(`Are you sure you want to delete ${label}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              callback(model.id)
                                  .then(() => {
                                      this.updateData()
                                      this.success(`${label} successfully deleted`)
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the ${label}: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info(`${this.capitalize(label)} not deleted`)
                    })
            },

            handleBulkCommand(command) {
                command()
            },

            capitalize: s => {
                if (typeof s !== "string") return ""
                return s.charAt(0).toUpperCase() + s.slice(1)
            }
        }
    }
</script>