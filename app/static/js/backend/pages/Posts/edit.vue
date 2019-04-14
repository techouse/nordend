<script>
    import CreatePost   from "./create"
    import Post         from "../../models/Post"
    import {mapActions} from "vuex"

    export default {
        name: "EditPost",

        extends: CreatePost,

        props: {
            postId: {
                type:     [String, Number],
                required: true
            }
        },

        data() {
            return {
                formRef: "edit-post-form",
                title:   "Edit post",
                post:    new Post(),
            }
        },

        mounted() {
            this.getPost(this.postId)
                .then(({data}) => {
                    this.$set(this, "post", new Post(data))
                    this.editor.setContent(this.post.body)
                })
        },

        methods: {
            ...mapActions("post", ["getPost", "updatePost", "deletePost"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.updatePost(this.post)
                            .then(() => {
                                this.success("Post successfully updated")
                            })
                            .catch(() => {
                                this.error(`There was an error updating the post: ${this.alert.message}`)
                            })
                    } else {
                        this.error("The form data is invalid!")
                        return false
                    }
                })
            },

            remove() {
                this.$confirm(`Are you sure you want to delete ${this.post.title}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deletePost(this.post.id)
                                  .then(() => {
                                      this.$router.push({name: "Posts"})
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
            }
        },

        beforeRouteUpdate(to, from, next) {
            this.getUser(to.params.postId)
                .then(({data}) => {
                    this.$set(this, "post", new Post(data))
                })
            next()
        }
    }
</script>