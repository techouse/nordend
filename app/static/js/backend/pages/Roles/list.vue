<template>
    <card>
        <template v-slot:header>
            <el-page-header class="no-back" :content="title"/>
            <div class="card-header-actions">
                <el-dropdown v-if="multipleSelection.length" @command="handleBulkCommand">
                    <button class="btn btn-sm btn-outline-secondary">
                        Bulk actions <i class="el-icon-arrow-down el-icon--right"></i>
                    </button>
                    <el-dropdown-menu slot="dropdown" size="mini">
                        <el-dropdown-item icon="fal fa-trash-alt" :command="bulkRemove">
                            Delete selection
                        </el-dropdown-item>
                        <el-dropdown-item icon="fal fa-snowplow" :command="toggleSelection" divided>
                            Clear selection
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <router-link :to="{name: 'CreateRole'}" class="btn btn-sm btn-success">
                    <i class="far fa-graduation-cap"/> Create new role
                </router-link>
            </div>
        </template>
        <template v-slot:body>
            <el-table :ref="tableRef" v-loading="loading" :data="roles" class="w-100" @sort-change="orderBy"
                      @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="40"/>
                <el-table-column label="#" prop="id" width="60" sortable="custom"/>
                <el-table-column label="Name" prop="name" sortable="custom"/>
                <el-table-column label="Default" prop="default" align="center" width="120" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.default" class="fas fa-check text-success"/>
                        <i v-else class="fas fa-times text-danger"/>
                    </template>
                </el-table-column>
                <el-table-column label="Follow" prop="follow" align="center" width="120" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.follow" class="fas fa-check text-success"/>
                        <i v-else class="fas fa-times text-danger"/>
                    </template>
                </el-table-column>
                <el-table-column label="Comment" prop="comment" align="center" width="120" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.comment" class="fas fa-check text-success"/>
                        <i v-else class="fas fa-times text-danger"/>
                    </template>
                </el-table-column>
                <el-table-column label="Write" prop="write" align="center" width="120" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.write" class="fas fa-check text-success"/>
                        <i v-else class="fas fa-times text-danger"/>
                    </template>
                </el-table-column>
                <el-table-column label="Moderate" prop="moderate" align="center" width="120" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.moderate" class="fas fa-check text-success"/>
                        <i v-else class="fas fa-times text-danger"/>
                    </template>
                </el-table-column>
                <el-table-column label="Admin" prop="admin" align="center" width="120" sortable="custom">
                    <template slot-scope="scope">
                        <i v-if="scope.row.admin" class="fas fa-check text-success"/>
                        <i v-else class="fas fa-times text-danger"/>
                    </template>
                </el-table-column>
                <el-table-column align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input v-model="params.search"
                                  size="mini"
                                  placeholder="Type to search role title"
                                  clearable
                                  @change="searchData"
                        />
                    </template>
                    <template slot-scope="scope">
                        <router-link :to="{name: 'EditRole', params: {roleId: scope.row.id}}"
                                     class="btn btn-sm btn-outline-secondary"
                        >
                            <i class="far fa-edit"/>
                        </router-link>
                        <button class="btn btn-sm btn-outline-danger" @click="remove(scope.row)">
                            <i class="far fa-trash-alt"/>
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
    import Role         from "../../models/Role"
    import {isEmpty}    from "lodash"

    export default {
        name: "ListRoles",

        extends: IndexPartial,

        data() {
            return {
                title: "Roles",
                roles: []
            }
        },

        methods: {
            ...mapActions("role", ["getRoles", "deleteRole", "deleteRoles"]),

            getData() {
                this.$router.replace({name: "Roles", query: this.params})

                return new Promise((resolve, reject) => {
                    this.getRoles({params: this.params})
                        .then(({data}) => {
                            this.$set(this, "roles", data.results.map(role => new Role(role)))
                            this.$set(this, "totalCount", data.count)
                            resolve()
                        })
                        .catch(() => {
                            reject()
                        })
                })
            },

            edit(role) {
                this.$router.push({name: "EditRole", params: {roleId: role.id}})
            },

            bulkRemove() {
                this._bulkRemove(this.deleteRoles, "role")
            },

            remove(role) {
                this._remove(this.deleteRole, role, role.name)
            },
        },

        beforeRouteUpdate(to, from, next) {
            if (isEmpty(to.query)) {
                this.getRoles({params: {}})
                    .then(({data}) => {
                        this.$set(this, "roles", data.results.map(role => new Role(role)))
                        this.$set(this, "totalCount", data.count)
                    })
            }

            next()
        }
    }
</script>