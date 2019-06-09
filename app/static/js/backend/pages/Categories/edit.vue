<script>
    import CreateCategory from "./create"
    import Category       from "../../models/Category"
    import {mapActions}   from "vuex"

    export default {
        name: "EditCategory",

        extends: CreateCategory,

        props: {
            categoryId: {
                type:     [String, Number],
                required: true
            }
        },

        data() {
            return {
                formRef:  "edit-category-form",
                category: new Category(),
            }
        },

        computed: {
            title() {
                return this.category.name
            }
        },

        created() {
            this.getCategory(this.categoryId)
                .then(({data}) => {
                    this.$set(this, "category", new Category(data))
                })
        },

        methods: {
            ...mapActions("category", ["getCategory", "updateCategory", "deleteCategory"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.updateCategory(this.category)
                            .then(() => {
                                this.success("Category successfully updated")
                            })
                            .catch(() => {
                                this.error(`There was an error updating the category: ${this.alert.message}`)
                            })
                    } else {
                        this.error("The form data is invalid!")
                        return false
                    }
                })
            },

            remove() {
                this.$confirm(`Are you sure you want to delete ${this.category.name}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteCategory(this.category.id)
                                  .then(() => {
                                      this.$router.push({name: "Categorys"})
                                      this.success("Category successfully deleted")
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the category: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("Category not deleted")
                    })
            }
        },
    }
</script>