<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <el-form :ref="formRef" :model="post" :rules="rules" :label-width="labelWidth" class="card">
                    <div class="card-header">
                        <b>{{ title }}</b> <i>{{ post.title }}</i>
                        <div v-if="post.id" class="card-header-actions">
                            <button class="btn btn-sm btn-danger" @click.prevent="remove">
                                Delete post
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <el-form-item label="Title" prop="title">
                            <el-input v-model="post.title" type="string" required/>
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
                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.bold() }"
                                                @click.prevent="commands.bold"
                                        >
                                            <i class="fas fa-bold"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.italic() }"
                                                @click.prevent="commands.italic"
                                        >
                                            <i class="fas fa-italic"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.strike() }"
                                                @click.prevent="commands.strike"
                                        >
                                            <i class="fas fa-strikethrough"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.underline() }"
                                                @click.prevent="commands.underline"
                                        >
                                            <i class="fas fa-underline"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.code() }"
                                                @click.prevent="commands.code"
                                        >
                                            <i class="fas fa-code"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.paragraph() }"
                                                @click.prevent="commands.paragraph"
                                        >
                                            <i class="fas fa-paragraph"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                                                @click.prevent="commands.heading({ level: 1 })"
                                        >
                                            H1
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                                                @click.prevent="commands.heading({ level: 2 })"
                                        >
                                            H2
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                                                @click.prevent="commands.heading({ level: 3 })"
                                        >
                                            H3
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.bullet_list() }"
                                                @click.prevent="commands.bullet_list"
                                        >
                                            <i class="fas fa-list-ul"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.ordered_list() }"
                                                @click.prevent="commands.ordered_list"
                                        >
                                            <i class="fas fa-list-ol"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.blockquote() }"
                                                @click.prevent="commands.blockquote"
                                        >
                                            <i class="fas fa-quote-right"/>
                                        </button>

                                        <button class="menubar__button"
                                                :class="{ 'is-active': isActive.code_block() }"
                                                @click.prevent="commands.code_block"
                                        >
                                            <i class="fas fa-laptop-code"/>
                                        </button>

                                        <button class="menubar__button"
                                                @click.prevent="commands.horizontal_rule"
                                        >
                                            –
                                        </button>

                                        <button class="menubar__button"
                                                @click.prevent="commands.undo"
                                        >
                                            <i class="fas fa-undo"/>
                                        </button>

                                        <button class="menubar__button"
                                                @click.prevent="commands.redo"
                                        >
                                            <i class="fas fa-redo"/>
                                        </button>
                                    </div>
                                </editor-menu-bar>

                                <editor-content class="editor__content" :editor="editor"/>
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
        Blockquote, CodeBlock, HardBreak, Heading, HorizontalRule,
        OrderedList, BulletList, ListItem, TodoItem, TodoList,
        Bold, Code, Italic, Link, Strike, Underline, History,
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
                                               new BulletList(),
                                               new CodeBlock(),
                                               new HardBreak(),
                                               new Heading({levels: [1, 2, 3]}),
                                               new HorizontalRule(),
                                               new ListItem(),
                                               new OrderedList(),
                                               new TodoItem(),
                                               new TodoList(),
                                               new Bold(),
                                               new Code(),
                                               new Italic(),
                                               new Link(),
                                               new Strike(),
                                               new Underline(),
                                               new History(),
                                           ],
                                           content:    null,
                                           onUpdate:   ({getJSON, getHTML}) => {
                                               const json = getJSON()
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

        methods: {
            ...mapActions("post", ["createPost"]),

            ...mapActions("category", ["getCategories"]),

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

        beforeDestroy() {
            this.editor.destroy()
        },
    }
</script>