<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <div class="card">
                    <div class="card-header">
                        <b>Users</b>
                        <div class="card-header-actions">
                            <a class="btn btn-sm btn-primary" href="#">
                                Create new user
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        <el-table :data="users" class="w-100">
                            <el-table-column label="#" prop="id"/>
                            <el-table-column label="Name" prop="name"/>
                            <el-table-column label="E-mail" prop="email"/>
                            <el-table-column :formatter="$options.filters.formattedDate" label="Created"
                                             prop="created_at"
                            />
                            <el-table-column align="right">
                                <template slot="header" slot-scope="scope">
                                    <el-input v-model="params.search"
                                              size="mini"
                                              placeholder="Type to search name or email address"
                                              clearable
                                              @change="getData"
                                    />
                                </template>
                                <template slot-scope="scope">
                                    <el-button size="mini"
                                               @click="edit(scope.row)"
                                    >
                                        Edit
                                    </el-button>
                                    <el-button size="mini"
                                               type="danger"
                                               @click="remove(scope.row)"
                                    >
                                        Delete
                                    </el-button>
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
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapActions}    from "vuex"
    import {parse, format} from "date-fns"
    import User            from "../../models/User"

    export default {
        name: "Users",

        filters: {
            formattedDate(row, column) {
                return format(parse(row.created_at), "YYYY-MM-DD HH:mm:ss")
            }
        },

        data() {
            return {
                users:      [],
                params:     {
                    search:   "",
                    page:     1,
                    per_page: 12
                },
                pageSizes:  [12, 24, 50, 100],
                totalCount: 0
            }
        },

        created() {
            this.getData()
        },

        methods: {
            ...mapActions("user", ["getUsers", "deleteUser"]),

            getData() {
                this.getUsers({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "users", data.results.map(user => new User(user)))
                        this.$set(this, "totalCount", data.count)
                    })
            },

            edit(user) {
                this.$router.push({name: "EditUser", params: {userId: user.id}})
            },

            remove(user) {
                this.$confirm(`Are you sure you want to delete ${user.name}?`, "Warning", {
                        confirmButtonText: "OK",
                        cancelButtonText:  "Cancel",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteUser(user.id)
                                  .then(() => {
                                      this.getData()
                                      this.$message({
                                                        type:    "success",
                                                        message: "User successfully deleted"
                                                    })
                                  })
                                  .catch(() => {
                                      this.$message({
                                                        type:    "error",
                                                        message: "There was an error deleting the user"
                                                    })
                                  })
                          }
                    )
                    .catch(() => {
                        this.$message({
                                          type:    "info",
                                          message: "User not deleted"
                                      })
                    })
            }
        }
    }
</script>