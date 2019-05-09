<script>
    import CreatePost   from "./create"
    import {mapActions} from "vuex"
    import {Editor}     from "tiptap"
    import {
        Blockquote,
        Bold,
        BulletList,
        Code,
        CodeBlockHighlight,
        Collaboration,
        HardBreak,
        Heading,
        History,
        HorizontalRule,
        Italic,
        Link,
        ListItem,
        OrderedList,
        Strike,
        Table,
        TableCell,
        TableHeader,
        TableRow,
        TodoItem,
        TodoList,
        Underline,
    }                   from "tiptap-extensions"
    import io           from "socket.io-client"
    import Picture      from "../../components/editor/Picture"
    import YouTube      from "../../components/editor/YouTube"
    import Vimeo        from "../../components/editor/Vimeo"
    import Post         from "../../models/Post"
    // Code highlighting
    import css          from "highlight.js/lib/languages/css"
    import http         from "highlight.js/lib/languages/http"
    import javascript   from "highlight.js/lib/languages/javascript"
    import json         from "highlight.js/lib/languages/json"
    import less         from "highlight.js/lib/languages/less"
    import markdown     from "highlight.js/lib/languages/markdown"
    import perl         from "highlight.js/lib/languages/perl"
    import php          from "highlight.js/lib/languages/php"
    import python       from "highlight.js/lib/languages/python"
    import ruby         from "highlight.js/lib/languages/ruby"
    import scss         from "highlight.js/lib/languages/scss"
    import shell        from "highlight.js/lib/languages/shell"
    import sql          from "highlight.js/lib/languages/sql"
    import swift        from "highlight.js/lib/languages/swift"

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
                loading: true,
                formRef: "edit-post-form",
                title:   "Edit post",
                post:    new Post(),
                socket:  null,
                count:   0,
                editor:  null
            }
        },

        computed: {
            selectedType() {
                if (this.editor) {
                    const selection = this.editor.state.selection
                    return selection.node ? selection.node.type.name : selection.toJSON().type
                }
                return null
            },
            webSocketUrl() {
                /**
                 * It is imperative that this URL matches with the one in Flask's app/api/events/post.py
                 */
                return `${location.protocol}//${document.domain}:${location.port}/posts_ws`
            }
        },

        mounted() {
            this.socket = io.connect(this.webSocketUrl)
                            .on("connect", () => {
                                this.socket.emit("init", {post_id: this.postId})
                            })
                            .on("init", ({data}) => {
                                this.$set(this, "post", new Post(data))
                                this.onInit(data)
                            })
                            .on("update", ({data}) => this.editor.extensions.options.collaboration.update(data))
                            .on("getCount", count => this.setCount(count))
        },

        methods: {
            ...mapActions("post", ["getPost", "updatePost", "deletePost"]),

            onInit({body, updated_at}) {
                this.$set(this, "loading", false)

                if (this.editor) {
                    this.editor.destroy()
                }

                this.$set(this, "editor", new Editor(
                    {
                        editable:   this.editable,
                        extensions: [
                            new Blockquote(),
                            new Bold(),
                            new BulletList(),
                            new Code(),
                            new CodeBlockHighlight(
                                {
                                    languages: {
                                        css,
                                        http,
                                        javascript,
                                        json,
                                        less,
                                        markdown,
                                        perl,
                                        php,
                                        python,
                                        ruby,
                                        scss,
                                        shell,
                                        sql,
                                        swift,
                                    },
                                }
                            ),
                            new HardBreak(),
                            new Heading({levels: [1, 2, 3]}),
                            new History(),
                            new HorizontalRule(),
                            new Italic(),
                            new Link(),
                            new ListItem(),
                            new OrderedList(),
                            new Strike(),
                            new Table(),
                            new TableHeader(),
                            new TableCell(),
                            new TableRow(),
                            new TodoItem(),
                            new TodoList(),
                            new Underline(),
                            // custom extensions
                            new Picture(),
                            new YouTube(),
                            new Vimeo(),
                            // collaboration
                            new Collaboration(
                                {
                                    // the initial version we start with
                                    // version is an integer which is incremented with every change
                                    version:    updated_at,
                                    // debounce changes so we can save some bandwidth
                                    debounce:   250,
                                    // onSendable is called whenever there are changed we have to send to our server
                                    onSendable: data => {
                                        this.socket.emit("update", data)
                                    },
                                }
                            )
                        ],
                        content:    body,
                        onUpdate:   ({getHTML}) => {
                            this.$set(this.post, "body", getHTML())
                        }
                    }
                ))
            },

            setCount(count) {
                this.$set(this, "count", count)
            },

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