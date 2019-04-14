<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <el-form :ref="formRef" :model="post" :rules="rules" :label-width="labelWidth" class="card">
                    <div class="card-header">
                        <b>{{ title }}</b> <i>{{ post.title }}</i>
                        <div v-if="post.id" class="card-header-actions">
                            <el-button class="btn btn-sm btn-danger" @click="remove">
                                Delete post
                            </el-button>
                        </div>
                    </div>
                    <div class="card-body">
                        <el-form-item label="Title" prop="title">
                            <el-input v-model="post.title" type="string" required />
                        </el-form-item>
                        <el-form-item label="Category" prop="category_id">
                            <el-select v-model="post.category_id" placeholder="Post category" required>
                                <el-option v-for="category in categories"
                                           :key="category.id"
                                           :label="category.name"
                                           :value="category.id"
                                />
                            </el-select>
                        </el-form-item>
                        <el-form-item label="Content">
                            <div class="editor">
                                <editor-menu-bar :editor="editor">
                                    <div slot-scope="{ commands, isActive }" class="menubar">
                                        <el-button-group>
                                            <el-tooltip class="item" effect="dark" content="Bold" placement="top-start">
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.bold() }"
                                                           @click="commands.bold"
                                                >
                                                    <i class="fas fa-bold" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Italic"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.italic() }"
                                                           @click="commands.italic"
                                                >
                                                    <i class="fas fa-italic" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Strikethrough"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.strike() }"
                                                           @click="commands.strike"
                                                >
                                                    <i class="fas fa-strikethrough" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Underline"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.underline() }"
                                                           @click="commands.underline"
                                                >
                                                    <i class="fas fa-underline" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Code" placement="top-start">
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.code() }"
                                                           @click="commands.code"
                                                >
                                                    <i class="fas fa-code" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Paragraph"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.paragraph() }"
                                                           @click="commands.paragraph"
                                                >
                                                    <i class="fas fa-paragraph" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Heading 1"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                                                           @click="commands.heading({ level: 1 })"
                                                >
                                                    <span>H1</span>
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Heading 2"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                                                           @click="commands.heading({ level: 2 })"
                                                >
                                                    <span>H2</span>
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Heading 3"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           title="Heading 3"
                                                           :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                                                           @click="commands.heading({ level: 3 })"
                                                >
                                                    <span>H3</span>
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Unordered list"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.bullet_list() }"
                                                           @click="commands.bullet_list"
                                                >
                                                    <i class="fas fa-list-ul" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Ordered list"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.ordered_list() }"
                                                           @click="commands.ordered_list"
                                                >
                                                    <i class="fas fa-list-ol" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Blockquote"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.blockquote() }"
                                                           @click="commands.blockquote"
                                                >
                                                    <i class="fas fa-quote-right" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Code block"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           :class="{ 'is-active': isActive.code_block() }"
                                                           @click="commands.code_block"
                                                >
                                                    <i class="fas fa-laptop-code" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Horizontal ruler"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           @click="commands.horizontal_rule"
                                                >
                                                    <span>–</span>
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Undo" placement="top-start">
                                                <el-button size="mini"
                                                           @click="commands.undo"
                                                >
                                                    <i class="fas fa-undo" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Redo" placement="top-start">
                                                <el-button size="mini"
                                                           title="Redo"
                                                           @click="commands.redo"
                                                >
                                                    <i class="fas fa-redo" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Insert image"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini"
                                                           @click.prevent="showImagePrompt(commands.image)"
                                                >
                                                    <i class="fas fa-image" />
                                                </el-button>
                                            </el-tooltip>
                                        </el-button-group>
                                    </div>
                                </editor-menu-bar>

                                <editor-content class="editor__content" :editor="editor" />
                            </div>
                        </el-form-item>
                    </div>
                    <div class="card-footer">
                        <el-button type="success" @click="submit">
                            Submit
                        </el-button>
                        <el-button type="danger" @click="$router.push({name: 'Posts'})">
                            Cancel
                        </el-button>
                    </div>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapActions}                           from "vuex"
    import {Editor, EditorContent, EditorMenuBar} from "tiptap"
    import {
        Blockquote,
        Bold,
        BulletList,
        Code,
        CodeBlock,
        HardBreak,
        Heading,
        History,
        HorizontalRule,
        Image,
        Italic,
        Link,
        ListItem,
        OrderedList,
        Strike,
        TodoItem,
        TodoList,
        Underline,
    }                                             from "tiptap-extensions"
    import CreatePartial                          from "../../components/CreatePartial"
    import Post                                   from "../../models/Post"
    import Category                               from "../../models/Category"

    export default {
        name: "CreatePost",

        components: {
            EditorContent,
            EditorMenuBar,
        },

        extends: CreatePartial,

        data() {
            return {
                formRef:    "create-post-form",
                title:      "Create post",
                post:       new Post(),
                categories: [],
                rules:      {
                    title:       [
                        {required: true, message: "Please enter a title", trigger: "blur"},
                        {min: 1, max: 255, message: "Length should be between 1 and 255 characters", trigger: "blur"}
                    ],
                    category_id: [
                        {required: true, message: "Please select a category", trigger: "blur"},
                    ],
                },
                editor:     new Editor({
                                           extensions: [
                                               new Blockquote(),
                                               new Bold(),
                                               new BulletList(),
                                               new Code(),
                                               new CodeBlock(),
                                               new HardBreak(),
                                               new Heading({levels: [1, 2, 3]}),
                                               new History(),
                                               new HorizontalRule(),
                                               new Image(),
                                               new Italic(),
                                               new Link(),
                                               new ListItem(),
                                               new OrderedList(),
                                               new Strike(),
                                               new TodoItem(),
                                               new TodoList(),
                                               new Underline(),
                                           ],
                                           content:    null,
                                           onUpdate:   ({getJSON, getHTML}) => {
                                               console.log(getJSON())
                                               this.$set(this.post, "body", getHTML())
                                           }
                                       }),
            }
        },

        created() {
            this.getCategories()
                .then(({data}) => {
                    this.$set(this, "categories", data.results.map(role => new Category(role)))
                })
        },

        beforeDestroy() {
            this.editor.destroy()
        },

        methods: {
            ...mapActions("post", ["createPost"]),

            ...mapActions("category", ["getCategories"]),

            showImagePrompt(command) {
                const src = prompt("Enter the url of your image here")
                if (src !== null) {
                    command({src})
                }
            },

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.createPost(this.post)
                            .then(({data}) => {
                                this.success("Post successfully created")
                                this.$router.push({name: "EditPost", params: {postId: data.id}})
                            })
                            .catch(() => {
                                this.error(`There was an error creating the post: ${this.alert.message}`)
                            })
                    } else {
                        this.error("The form data is invalid!")
                        return false
                    }
                })
            },
        },
    }
</script>