<template>
    <card>
        <template v-slot:header>
            <b>{{ title }}</b>
            <div class="card-header-actions">
                <router-link :to="{name: 'CreateCategory'}" class="btn btn-sm btn-primary">
                    Create new category
                </router-link>
            </div>
        </template>
        <template v-slot:body>
            <el-table :data="categories" class="w-100" @sort-change="orderBy">
                <el-table-column label="#" prop="id" width="50" sortable="custom"/>
                <el-table-column label="Name" prop="name" sortable="custom"/>
                <el-table-column label="Slug" prop="slug" sortable="custom"/>
                <el-table-column align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input v-model="params.search"
                                  size="mini"
                                  placeholder="Type to search category title"
                                  clearable
                                  @change="searchData"
                        />
                    </template>
                    <template slot-scope="scope">
                        <router-link :to="{name: 'EditCategory', params: {categoryId: scope.row.id}}"
                                     class="btn btn-sm btn-outline-secondary">
                            Edit
                        </router-link>
                        <button class="btn btn-sm btn-outline-danger" @click="remove(scope.row)">
                            Delete
                        </button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="d-flex justify-content-center mt-2">
                <el-pagination :current-page.sync="params.page"
                               :page-sizes="pageSizes"
                               :page-size.sync="params.per_page"
                               :total="totalCount"
                               layout="prev, pager, next, sizes"
                               background
                               @size-change="getData"
                               @current-change="getData"
                />
            </div>
        </template>
    </card>
</template>

<script>
    import IndexPartial from "../../components/IndexPartial"
    import {mapActions} from "vuex"
    import Category     from "../../models/Category"
    import {isEmpty}    from "lodash"

    export default {
        name: "Categories",

        extends: IndexPartial,

        data() {
            return {
                title:      "Categories",
                categories: []
            }
        },

        methods: {
            ...mapActions("category", ["getCategories", "deleteCategory"]),

            getData() {
                this.$router.replace({name: "Categories", query: this.params})

                this.getCategories({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "categories", data.results.map(category => new Category(category)))
                        this.$set(this, "totalCount", data.count)
                    })
            },

            show(category) {
                this.$router.push({name: "ShowCategories", params: {categoryId: category.id}})
            },

            edit(category) {
                this.$router.push({name: "EditCategories", params: {categoryId: category.id}})
            },

            remove(category) {
                this.$confirm(`Are you sure you want to delete ${category.name}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteCategory(category.id)
                                  .then(() => {
                                      this.getData()
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
            },
        },

        beforeRouteUpdate(to, from, next) {
            if (isEmpty(to.query)) {
                this.getCategories({params: {}})
                    .then(({data}) => {
                        this.$set(this, "categories", data.results.map(category => new Category(category)))
                        this.$set(this, "totalCount", data.count)
                    })
            }

            next()
        }
    }
</script>