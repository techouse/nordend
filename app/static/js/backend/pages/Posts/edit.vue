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
                formRef:       "edit-post-form",
                post:          new Post(),
                postWasLocked: false
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),

            ...mapGetters("post", ["lockedPosts", "updatedId", "updatedIds", "notifyAboutUnlock", "notifyAboutForcedUnlock", "forcefullyUnlockedPost"]),

            postIsLocked() {
                const lock = this.lockedPosts.find(el => el.post_id === this.post.id)

                return lock &&
                       lock.expires >= new Date() &&
                       this.currentUser &&
                       lock.by_user_id !== this.currentUser.id
            },

            editable() {
                return !this.readonly && !this.postIsLocked && !this.postWasLocked
            },

            title() {
                return this.post.title
            }
        },

        watch: {
            notifyAboutUnlock(unlock) {
                if (unlock) {
                    this.clearUnlockNotification()

                    if (unlock.post_id === this.post.id) {
                        if (unlock.by_user_id !== this.currentUser.id) {
                            this.$alert(
                                "This post has just been unlocked! You may now edit it.",
                                {
                                    type:              "info",
                                    confirmButtonText: "OK",
                                }
                            )

                            this.$set(this, "postWasLocked", false)
                        }
                    }
                }
            },

            forcefullyUnlockedPost(forcedUnlock) {
                if (forcedUnlock) {
                    if (forcedUnlock.post_id === this.post.id) {
                        this.$set(this, "postWasLocked", false)
                    }
                }
            },

            notifyAboutForcedUnlock(forcedUnlock) {
                if (forcedUnlock) {
                    this.clearForcedUnlockNotification()

                    if (forcedUnlock.by_user_id !== this.currentUser.id) {
                        const message = `A moderator or administrator has forcefully unlocked
                                         ${this.post.id === forcedUnlock.post_id ? "the" : "an"}
                                         article you were recently editing. In case the article was
                                         also taken over you will not be able to edit it until the
                                         lock persists.`

                        this.$alert(message, {
                            type:              this.post.id === forcedUnlock.post_id ? "warning" : "info",
                            confirmButtonText: "OK"
                        })
                    }
                }
            },

            updatedIds: {
                handler(updatedIds) {
                    if (updatedIds.length > 0) {
                        this.getLatestUpdated()
                            .then(({post_id, by_user_id}) => {
                                if (post_id === this.post.id && by_user_id !== this.currentUser.id) {
                                    this.$set(this, "loading", true)

                                    this.getPost(this.postId)
                                        .then(({data}) => {
                                            this.$set(this, "post", new Post(data))
                                            this.$set(this, "loading", false)
                                            this.editor.setContent(this.post.body)
                                        })
                                        .catch(() => {
                                            this.$set(this, "loading", false)
                                        })
                                }
                            })
                    }
                },
                deep: true
            },

            editable(editable) {
                if (editable) {
                    console.log("lock in watcher")

                    this.$set(this, "postWasLocked", false)

                    this.lockPost(this.post)
                        .then(() => {
                            this.$set(this.post, "locked_by", this.currentUser)

                            window.addEventListener("beforeunload", () => {
                                this.unlockPost({post: this.post})
                            })
                        })
                }
            }
        },

        created() {
            this.$set(this, "loading", true)
        },

        mounted() {
            this.getPost(this.postId)
                .then(({data}) => {
                    this.$set(this, "post", new Post(data))
                    this.$set(this, "loading", false)

                    this.$set(this, "postWasLocked", this.post.locked &&
                                                     this.post.lock_expires >= new Date() &&
                                                     this.currentUser &&
                                                     this.post.locked_by &&
                                                     this.post.locked_by.id !== this.currentUser.id)
                    if (!this.postWasLocked) {
                        console.log("lock on mounted")
                        this.lockPost(this.post)
                            .then(() => {
                                window.addEventListener("beforeunload", () => {
                                    this.unlockPost({post: this.post})
                                })
                            })
                    } else {
                        console.log('fuq')
                    }
                    this.editor.setContent(this.post.body)
                })
                .catch(() => {
                    this.$set(this, "loading", false)
                })
        },

        beforeDestroy() {
            this.unlockPost({post: this.post})
            this.editor.destroy()
        },

        methods: {
            ...mapActions("post", ["getPost", "updatePost", "deletePost", "lockPost", "unlockPost",
                                   "clearForcedUnlockNotification", "getLatestUpdated", "clearUnlockNotification"]),

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
            this.getPost(to.params.postId)
                .then(({data}) => {
                    this.$set(this, "post", new Post(data))
                })
            next()
        }
    }
</script>