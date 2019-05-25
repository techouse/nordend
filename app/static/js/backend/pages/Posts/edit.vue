<script>
    import CreatePost               from "./create"
    import Post                     from "../../models/Post"
    import {mapActions, mapGetters} from "vuex"

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
                post:    new Post(),
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),

            ...mapGetters("user", ["currentUser"]),

            editable() {
                return !this.readonly && (!this.post.locked || this.post.locked && this.post.locked_by && this.post.locked_by.id === this.currentUser.id)
            },

            title() {
                return this.editable ? "Edit post" : "View post"
            }
        },

        mounted() {
            this.getPost(this.postId)
                .then(({data}) => {
                    this.$set(this, "post", new Post(data))
                    if (this.editable) {
                        this.lockPost(this.post)
                            .then(() => {
                                window.addEventListener("beforeunload", () => {
                                    this.unlockPost(this.post)
                                })
                            })
                    }
                    this.editor.setContent(this.post.body)
                })
        },

        beforeDestroy() {
            this.editor.destroy()
            if (this.editable) {
                this.unlockPost(this.post)
            }
        },

        methods: {
            ...mapActions("post", ["getPost", "updatePost", "deletePost", "lockPost", "unlockPost"]),

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