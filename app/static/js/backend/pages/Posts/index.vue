<template>
    <card>
        <template v-slot:header>
            <b>{{ title }}</b>
            <div class="card-header-actions">
                <router-link :to="{name: 'CreatePost'}" class="btn btn-sm btn-primary">
                    Create new post
                </router-link>
            </div>
        </template>
        <template v-slot:body>
            <el-table :data="posts" class="w-100" @sort-change="orderBy">
                <el-table-column label="#" prop="id" width="60" sortable="custom"/>
                <el-table-column label="Title" prop="title" sortable="custom"/>
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
                        <template v-if="!lockedPosts.includes(scope.row.id)">
                            <router-link :to="{name: 'EditPost', params: {postId: scope.row.id}}"
                                         class="btn btn-sm btn-outline-secondary"
                            >
                                <i class="fas fa-edit"></i>
                            </router-link>
                            <button class="btn btn-sm btn-outline-danger" @click.prevent="remove(scope.row)">
                                <i class="far fa-trash-alt"></i>
                            </button>
                        </template>
                        <template v-else>
                            <router-link :to="{name: 'EditPost', params: {postId: scope.row.id, readonly: false}}"
                                         class="btn btn-sm btn-outline-secondary"
                            >
                                <i class="fas fa-eye"></i>
                            </router-link>
                            <button class="btn btn-sm btn-danger" :disabled="true">
                                <i class="fas fa-lock-alt"></i>
                            </button>
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
        name: "Posts",

        extends: IndexPartial,

        data() {
            return {
                title: "Posts",
                posts: []
            }
        },

        computed: {
            ...mapGetters("post", ["created", "updated", "deleted", "gotLockedPosts", "lockedPosts"])
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
            lockedPosts: {
                handler(ids) {
                    console.log('locked posts changed')
                },
                deep: true
            }
        },

        created() {
            if (!this.gotLockedPosts) {
                this.listLockedPosts()
            }
        },

        methods: {
            ...mapActions("post", ["getPosts", "deletePost", "listLockedPosts"]),

            getData() {
                this.$router.replace({name: "Posts", query: this.params})

                this.getPosts({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "posts", data.results.map(post => new Post(post)))
                        this.$set(this, "totalCount", data.count)
                    })
            },

            edit(post) {
                this.$router.push({name: "EditPost", params: {postId: post.id}})
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