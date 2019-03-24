<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <div class="card">
                    <div class="card-header">
                        <b>Users</b>
                        <div class="card-header-actions">
                            <router-link :to="{name: 'CreateUser'}" class="btn btn-sm btn-primary">
                                Create new user
                            </router-link>
                        </div>
                    </div>
                    <div class="card-body">
                        <el-table :data="users" class="w-100">
                            <el-table-column label="#" prop="id" width="50"/>
                            <el-table-column label="Name" prop="name"/>
                            <el-table-column label="E-mail" prop="email"/>
                            <el-table-column label="Role" prop="role.name" align="center" width="120"/>
                            <el-table-column label="Confirmed" align="center" width="100">
                                <template slot-scope="scope">
                                    <i v-if="scope.row.confirmed" class="fas fa-check text-success"></i>
                                    <i v-else class="fas fa-times text-danger"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="Created" align="center" width="160">
                                <template slot-scope="scope">
                                    <time :datetime="scope.row.created_at">{{ scope.row.created_at|formattedDate }}
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
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import {parse, format}          from "date-fns"
    import {isEmpty}                from "lodash"
    import User                     from "../../models/User"

    export default {
        name: "Users",

        filters: {
            formattedDate(datetime) {
                return format(parse(datetime), "YYYY-MM-DD HH:mm:ss")
            }
        },

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
                users:      [],
                params:     {
                    search:   this.search,
                    page:     this.page,
                    per_page: this.perPage
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
            this.params = {
                search:   this.search,
                page:     this.page,
                per_page: this.perPage
            }
        },

        methods: {
            ...mapActions("user", ["getUsers", "deleteUser"]),

            ...mapActions("alert", ["error", "success", "info", "warning"]),

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
            },

            searchData() {
                this.$set(this.params, "page", 1)

                this.getData()
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