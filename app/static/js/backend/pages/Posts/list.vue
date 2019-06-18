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
                <router-link :to="{name: 'CreatePost'}" class="btn btn-sm btn-success">
                    <i class="far fa-pencil"/> Create new post
                </router-link>
            </div>
        </template>
        <template v-slot:body>
            <el-table :ref="tableRef" v-loading="loading" :data="posts" class="w-100" @sort-change="orderBy"
                      @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" width="40"/>
                <el-table-column label="#" prop="id" width="60" sortable="custom"/>
                <el-table-column label="Title" prop="title" sortable="custom">
                    <template slot-scope="scope">
                        <el-tooltip v-if="scope.row.title.length > maxTitleLength" class="item" effect="dark"
                                    :content="scope.row.title" placement="top-start"
                        >
                            <span>{{ scope.row.title | truncate(maxTitleLength) }}</span>
                        </el-tooltip>
                        <span v-else>{{ scope.row.title }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Category" prop="category.name" sortable="custom"/>
                <el-table-column label="Author" prop="author.name" sortable="custom"/>
                <el-table-column label="Created" align="center" width="160" prop="created_at" sortable="custom">
                    <template slot-scope="scope">
                        <time :datetime="scope.row.created_at">{{ scope.row.created_at|formatDate }}
                        </time>
                    </template>
                </el-table-column>
                <el-table-column label="Updated" align="center" width="160" prop="updated_at" sortable="custom">
                    <template slot-scope="scope">
                        <time :datetime="scope.row.updated_at">{{ scope.row.updated_at|formatDate }}
                        </time>
                    </template>
                </el-table-column>
                <el-table-column align="right">
                    <template slot="header" slot-scope="scope">
                        <el-input v-model="params.search"
                                  size="mini"
                                  placeholder="Type to search post title"
                                  clearable
                                  @change="searchData"
                        />
                    </template>
                    <template slot-scope="scope">
                        <template v-if="!lockedPosts.find(el => el.post_id === scope.row.id)">
                            <router-link :to="{name: 'EditPost', params: {postId: scope.row.id}}"
                                         class="btn btn-sm btn-outline-secondary"
                            >
                                <i class="far fa-edit"/>
                            </router-link>
                            <button class="btn btn-sm btn-outline-danger" @click.prevent="remove(scope.row)">
                                <i class="far fa-trash-alt"/>
                            </button>
                        </template>
                        <template v-else>
                            <router-link :to="{name: 'EditPost', params: {postId: scope.row.id}}"
                                         class="btn btn-sm btn-outline-secondary"
                            >
                                <i class="fas fa-eye"/>
                            </router-link>
                            <el-tooltip v-if="currentUser.role.moderate || currentUser.role.admin"
                                        class="item" effect="dark" content="Forcefully unlock"
                                        placement="right-start"
                            >
                                <button class="btn btn-sm btn-outline-primary"
                                        @click.prevent="unlock(scope.row)"
                                >
                                    <i class="fas fa-unlock-alt"/>
                                </button>
                            </el-tooltip>
                            <el-tooltip v-else class="item" effect="dark" content="Locked"
                                        placement="right-start"
                            >
                                <button class="btn btn-sm btn-ghost-danger" :disabled="true">
                                    <i class="fas fa-lock-alt"/>
                                </button>
                            </el-tooltip>
                        </template>
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
    import IndexPartial             from "../../components/IndexPartial"
    import {mapActions, mapGetters} from "vuex"
    import {isEmpty}                from "lodash"
    import Post                     from "../../models/Post"

    export default {
        name: "ListPosts",

        extends: IndexPartial,

        data() {
            return {
                title:          "Posts",
                posts:          [],
                maxTitleLength: 30
            }
        },

        computed: {
            ...mapGetters("post", ["created", "updated", "deleted", "lockedPosts", "notifyAboutForcedUnlock"]),

            ...mapGetters("user", ["currentUser"]),
        },

        watch: {
            created() {
                /**
                 * Update the posts table when a new post is created
                 */
                this.getData()
            },

            updated() {
                /**
                 * Update the posts table when a post gets updated
                 */
                this.getData()
            },

            deleted() {
                /**
                 * Update the posts table when a post gets deleted
                 */
                this.getData()
            },

            notifyAboutForcedUnlock(forcedUnlock) {
                if (forcedUnlock && forcedUnlock.by_user_id !== this.currentUser.id) {
                    this.$alert("A moderator or administrator has forcefully unlocked " +
                                "an article you were recently editing. Please be advised " +
                                "that now other people can edit that article.",
                                "Article unlocked", {
                                    type:              "info",
                                    confirmButtonText: "OK",
                                    callback:          action => {
                                        this.clearForcedUnlockNotification()
                                    }
                                })
                }
            }
        },

        created() {
            if (!this.lockedPosts.length) {
                this.listLockedPosts()
            }
        },

        methods: {
            ...mapActions("post", ["getPosts", "deletePost", "deletePosts", "unlockPost", "listLockedPosts", "clearForcedUnlockNotification"]),

            getData() {
                this.$router.replace({name: "Posts", query: this.params})

                return new Promise((resolve, reject) => {
                    this.getPosts({params: this.params})
                        .then(({data}) => {
                            this.$set(this, "posts", data.results.map(post => new Post(post)))
                            this.$set(this, "totalCount", data.count)
                            resolve()
                        })
                        .catch(() => {
                            reject()
                        })
                })
            },

            edit(post) {
                this.$router.push({name: "EditPost", params: {postId: post.id}})
            },

            unlock(post) {
                this.$confirm(`Are you sure you want to forcefully unlock ${post.title}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                        this.unlockPost({post, forced: true})
                    })
                    .catch(() => {
                        this.info("Post not forcefully unlocked.")
                    })
            },

            bulkRemove() {
                this._bulkRemove(this.deletePosts, "post")
            },

            remove(post) {
                this.$confirm(`Are you sure you want to delete ${post.title}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deletePost(post.id)
                                  .then(() => {
                                      this.getData()
                                      this.success("Post successfully deleted")
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the post: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("Post not deleted")
                    })
            },

            primary: items => items.find(el => el.primary === true) || items[0]
        },

        beforeRouteUpdate(to, from, next) {
            if (isEmpty(to.query)) {
                this.getPosts({params: {}})
                    .then(({data}) => {
                        this.$set(this, "posts", data.results.map(post => new Post(post)))
                        this.$set(this, "totalCount", data.count)
                    })
            }

            next()
        }
    }
</script>