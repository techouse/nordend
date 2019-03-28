<template>
    <card>
        <template v-slot:header>
            <b>{{ title }}</b>
            <div class="card-header-actions">
                <router-link :to="{name: 'CreateUser'}" class="btn btn-sm btn-primary">
                    Create new user
                </router-link>
            </div>
        </template>
        <template v-slot:body>
            <el-table :data="users" class="w-100" @sort-change="orderBy">
                <el-table-column label="#" prop="id" width="60" sortable="custom" />
                <el-table-column label="Name" prop="name" sortable="custom" />
                <el-table-column label="E-mail" prop="email" sortable="custom" />
                <el-table-column label="Role" prop="role.name" sort-by="role_id" align="center" width="120" sortable="custom" />
                <el-table-column label="Confirmed" align="center" width="130" prop="confirmed" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.confirmed" class="fas fa-check text-success" />
                        <i v-else class="fas fa-times text-danger" />
                    </template>
                </el-table-column>
                <el-table-column label="Created" align="center" width="160" prop="created_at" sortable="custom">
                    <template slot-scope="scope">
                        <time :datetime="scope.row.created_at">{{ scope.row.created_at|formatDate }}
                        </time>
                    </template>
                </el-table-column>
                <el-table-column align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input v-model="params.search"
                                  size="mini"
                                  placeholder="Type to search name or email address"
                                  clearable
                                  @change="searchData"
                        />
                    </template>
                    <template slot-scope="scope">
                        <router-link :to="{name: 'EditUser', params: {userId: scope.row.id}}"
                                     class="btn btn-sm btn-outline-secondary"
                        >
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
    import {isEmpty}    from "lodash"
    import User         from "../../models/User"

    export default {
        name: "Users",

        extends: IndexPartial,

        data() {
            return {
                title: "Users",
                users: []
            }
        },

        methods: {
            ...mapActions("user", ["getUsers", "deleteUser"]),

            getData() {
                this.$router.replace({name: "Users", query: this.params})

                this.getUsers({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "users", data.results.map(user => new User(user)))
                        this.$set(this, "totalCount", data.count)
                    })
            },

            show(user) {
                this.$router.push({name: "ShowUser", params: {userId: user.id}})
            },

            edit(user) {
                this.$router.push({name: "EditUser", params: {userId: user.id}})
            },

            remove(user) {
                this.$confirm(`Are you sure you want to delete ${user.name}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteUser(user.id)
                                  .then(() => {
                                      this.getData()
                                      this.success("User successfully deleted")
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the user: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("User not deleted")
                    })
            }
        },

        beforeRouteUpdate(to, from, next) {
            if (isEmpty(to.query)) {
                this.getUsers({params: {}})
                    .then(({data}) => {
                        this.$set(this, "users", data.results.map(user => new User(user)))
                        this.$set(this, "totalCount", data.count)
                    })
            }

            next()
        }
    }
</script>