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
                                            <el-tooltip class="item" effect="dark" content="Undo" placement="top-start">
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="commands.undo"
                                                >
                                                    <i class="far fa-undo" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Redo" placement="top-start">
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="commands.redo"
                                                >
                                                    <i class="far fa-redo" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Bold" placement="top-start">
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.bold() }"
                                                           @click="commands.bold"
                                                >
                                                    <i class="far fa-bold" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Italic"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.italic() }"
                                                           @click="commands.italic"
                                                >
                                                    <i class="far fa-italic" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Strikethrough"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.strike() }"
                                                           @click="commands.strike"
                                                >
                                                    <i class="far fa-strikethrough" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Underline"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.underline() }"
                                                           @click="commands.underline"
                                                >
                                                    <i class="far fa-underline" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Code" placement="top-start">
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.code() }"
                                                           @click="commands.code"
                                                >
                                                    <i class="far fa-code" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Paragraph"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.paragraph() }"
                                                           @click="commands.paragraph"
                                                >
                                                    <i class="far fa-paragraph" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Heading 1"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                                                           @click="commands.heading({ level: 1 })"
                                                >
                                                    <i class="far fa-h1" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Heading 2"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                                                           @click="commands.heading({ level: 2 })"
                                                >
                                                    <i class="far fa-h2" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Heading 3"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           title="Heading 3"
                                                           :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                                                           @click="commands.heading({ level: 3 })"
                                                >
                                                    <i class="far fa-h3" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Unordered list"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.bullet_list() }"
                                                           @click="commands.bullet_list"
                                                >
                                                    <i class="far fa-list-ul" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Ordered list"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.ordered_list() }"
                                                           @click="commands.ordered_list"
                                                >
                                                    <i class="far fa-list-ol" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Blockquote"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.blockquote() }"
                                                           @click="commands.blockquote"
                                                >
                                                    <i class="far fa-quote-right" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Code block"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           :class="{ 'is-active': isActive.code_block() }"
                                                           @click="commands.code_block"
                                                >
                                                    <i class="far fa-laptop-code" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Horizontal ruler"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="commands.horizontal_rule"
                                                >
                                                    <i class="far fa-minus" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Insert image"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="openUploadImageModal(commands.picture)"
                                                >
                                                    <i class="fas fa-image" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Insert YouTube video"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="openEmbedYouTubeModal(commands.youtube)"
                                                >
                                                    <i class="fab fa-youtube" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Insert Vimeo video"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="openEmbedVimeoModal(commands.vimeo)"
                                                >
                                                    <i class="fab fa-vimeo" />
                                                </el-button>
                                            </el-tooltip>

                                            <el-tooltip class="item" effect="dark" content="Create table"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :disabled="sourceCodeEditorIsActive"
                                                           @click="commands.createTable({rowsCount: 3, colsCount: 3, withHeaderRow: false })"
                                                >
                                                    <i class="fal fa-table" />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Toggle HTML source code editor"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" :type="sourceCodeEditorIsActive ? 'primary' : 'default'"
                                                           @click="toggleSourceCodeEditor"
                                                >
                                                    <i class="fas fa-hammer" />
                                                </el-button>
                                            </el-tooltip>
                                        </el-button-group>

                                        <el-button-group v-if="isActive.table()">
                                            <el-tooltip class="item" effect="dark" content="Delete table"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.deleteTable">
                                                    <i class="fal fa-table" />
                                                    <i class="fas fa-times-circle text-danger"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Insert column before"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.addColumnBefore">
                                                    <i class="fal fa-th-list" />
                                                    <i class="fas fa-plus-circle text-success"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Insert column after"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.addColumnAfter">
                                                    <i class="fal fa-th-list fa-flip-horizontal" />
                                                    <i class="fas fa-plus-circle text-success"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Delete column"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.deleteColumn">
                                                    <i class="fal fa-th-list" />
                                                    <i class="fas fa-times-circle text-danger"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Insert row before"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.addRowBefore">
                                                    <i class="fal fa-th-list fa-rotate-90" />
                                                    <i class="fas fa-plus-circle text-success"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Insert row after"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.addRowAfter">
                                                    <i class="fal fa-th-list fa-rotate-270" />
                                                    <i class="fas fa-plus-circle text-success"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Delete row"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.deleteRow">
                                                    <i class="fal fa-th-list fa-rotate-90" />
                                                    <i class="fas fa-times-circle text-danger"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Merge cells"
                                                        placement="top-start"
                                            >
                                                <el-button size="mini" @click="commands.toggleCellMerge">
                                                    <i class="fas fa-arrow-alt-circle-right text-primary"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                    <i class="fal fa-columns" />
                                                    <i class="fas fa-arrow-alt-circle-left text-primary"
                                                       :style="{fontSize: '.66rem'}"
                                                    />
                                                </el-button>
                                            </el-tooltip>
                                        </el-button-group>
                                    </div>
                                </editor-menu-bar>

                                <editor-menu-bubble :editor="editor">
                                    <div slot-scope="{ commands, isActive, getMarkAttrs, menu }"
                                         class="menububble"
                                         :class="{ 'is-active': menu.isActive || linkMenuIsActive, 'bg-transparent': bubbleMenuExcludedTypes.includes(selectedType) }"
                                         :style="`left: ${menu.left}px; bottom: ${menu.bottom}px;`"
                                    >
                                        <template />
                                        <form v-if="linkMenuIsActive" class="menububble__form"
                                              @submit.prevent="setLinkUrl(commands.link, linkUrl)"
                                        >
                                            <input ref="linkInput" v-model="linkUrl" class="menububble__input"
                                                   type="text" placeholder="https://" @keydown.esc="hideLinkMenu"
                                            >
                                            <button class="menububble__button" type="button"
                                                    @click.prevent="setLinkUrl(commands.link, null)"
                                            >
                                                <i class="far fa-times-circle" />
                                            </button>
                                        </form>

                                        <template v-else>
                                            <template v-if="selectedType === 'text'">
                                                <button class="menububble__button"
                                                        :class="{ 'is-active': isActive.bold() }"
                                                        @click.prevent="commands.bold"
                                                >
                                                    <i class="far fa-bold" />
                                                </button>

                                                <button class="menububble__button"
                                                        :class="{ 'is-active': isActive.italic() }"
                                                        @click.prevent="commands.italic"
                                                >
                                                    <i class="far fa-italic" />
                                                </button>

                                                <button class="menububble__button"
                                                        :class="{ 'is-active': isActive.strike() }"
                                                        @click.prevent="commands.strike"
                                                >
                                                    <i class="far fa-strikethrough" />
                                                </button>

                                                <button class="menububble__button"
                                                        :class="{ 'is-active': isActive.underline() }"
                                                        @click.prevent="commands.underline"
                                                >
                                                    <i class="far fa-underline" />
                                                </button>

                                                <button class="menububble__button"
                                                        :class="{ 'is-active': isActive.code() }"
                                                        @click.prevent="commands.code"
                                                >
                                                    <i class="far fa-code" />
                                                </button>
                                            </template>

                                            <button v-if="!bubbleMenuExcludedTypes.includes(selectedType)"
                                                    class="menububble__button"
                                                    :class="{ 'is-active': isActive.link() }"
                                                    @click.prevent="showLinkMenu(getMarkAttrs('link'))"
                                            >
                                                <i class="far fa-link" />
                                                <span v-if="isActive.link()" :style="{textIndent: '.5rem'}">
                                                    Update Link
                                                </span>
                                            </button>
                                        </template>
                                    </div>
                                </editor-menu-bubble>

                                <editor-content v-show="!sourceCodeEditorIsActive" class="editor__content" :editor="editor" />

                                <source-code v-if="sourceCodeEditorIsActive"
                                             v-model="post.body"
                                             @onUpdate="editor.setContent(post.body)"
                                />
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
        <upload-image-modal ref="upload-image-modal" :post-id="post.id" @onConfirm="addCommand" />
        <embed-youtube-modal ref="embed-youtube-modal" :post-id="post.id" @onConfirm="addCommand" />
        <embed-vimeo-modal ref="embed-vimeo-modal" :post-id="post.id" @onConfirm="addCommand" />
    </div>
</template>

<script>
    import {mapActions}      from "vuex"
    import {
        Editor,
        EditorContent,
        EditorMenuBar,
        EditorMenuBubble
    }                        from "tiptap"
    import {
        Blockquote,
        Bold,
        BulletList,
        Code,
        CodeBlockHighlight,
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
        TableHeader,
        TableCell,
        TableRow,
        TodoItem,
        TodoList,
        Underline,
    }                        from "tiptap-extensions"
    import Picture           from "../../components/editor/Picture"
    import UploadImageModal  from "../../components/editor/UploadImage"
    import YouTube           from "../../components/editor/YouTube"
    import EmbedYouTubeModal from "../../components/editor/EmbedYouTube"
    import Vimeo             from "../../components/editor/Vimeo"
    import EmbedVimeoModal   from "../../components/editor/EmbedVimeo"
    import SourceCode        from "../../components/editor/SourceCode"
    import CreatePartial     from "../../components/CreatePartial"
    import Post              from "../../models/Post"
    import Category          from "../../models/Category"
    // Code highlighting
    import css               from "highlight.js/lib/languages/css"
    import http              from "highlight.js/lib/languages/http"
    import javascript        from "highlight.js/lib/languages/javascript"
    import json              from "highlight.js/lib/languages/json"
    import less              from "highlight.js/lib/languages/less"
    import markdown          from "highlight.js/lib/languages/markdown"
    import perl              from "highlight.js/lib/languages/perl"
    import php               from "highlight.js/lib/languages/php"
    import python            from "highlight.js/lib/languages/python"
    import ruby              from "highlight.js/lib/languages/ruby"
    import scss              from "highlight.js/lib/languages/scss"
    import shell             from "highlight.js/lib/languages/shell"
    import sql               from "highlight.js/lib/languages/sql"
    import swift             from "highlight.js/lib/languages/swift"

    export default {
        name: "CreatePost",

        components: {
            EditorContent,
            EditorMenuBar,
            EditorMenuBubble,
            "upload-image-modal":  UploadImageModal,
            "embed-youtube-modal": EmbedYouTubeModal,
            "embed-vimeo-modal":   EmbedVimeoModal,
            "source-code":         SourceCode
        },

        extends: CreatePartial,

        props: {
            editable: {
                type:    Boolean,
                default: true
            }
        },

        data() {
            return {
                formRef:                  "create-post-form",
                title:                    "Create post",
                post:                     new Post(),
                categories:               [],
                rules:                    {
                    title:       [
                        {required: true, message: "Please enter a title", trigger: "blur"},
                        {min: 1, max: 255, message: "Length should be between 1 and 255 characters", trigger: "blur"}
                    ],
                    category_id: [
                        {required: true, message: "Please select a category", trigger: "blur"},
                    ],
                },
                editor:                   new Editor(
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
                            new Vimeo()
                        ],
                        content:    "",
                        onUpdate:   ({getJSON, getHTML}) => {
                            console.log(getJSON()) // TODO use me
                            this.$set(this.post, "body", getHTML())
                        }
                    }
                ),
                linkUrl:                  null,
                linkMenuIsActive:         false,
                sourceCodeEditorIsActive: false,
                bubbleMenuExcludedTypes:  [
                    "image",
                    "picture",
                    "youtube",
                    "vimeo"
                ]
            }
        },

        computed: {
            selectedType() {
                const selection = this.editor.state.selection
                return selection.node ? selection.node.type.name : selection.toJSON().type
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

            showLinkMenu(attrs) {
                this.$set(this, "linkUrl", attrs.href)
                this.$set(this, "linkMenuIsActive", true)
                this.$nextTick(() => {
                    this.$refs.linkInput.focus()
                })
            },
            hideLinkMenu() {
                this.$set(this, "linkMenuIsActive", false)
                this.$set(this, "linkUrl", null)
            },
            setLinkUrl(command, url) {
                command({href: url})
                this.hideLinkMenu()
                this.editor.focus()
            },

            openUploadImageModal(command) {
                this.$refs["upload-image-modal"].showModal(command)
            },

            openEmbedYouTubeModal(command) {
                this.$refs["embed-youtube-modal"].showModal(command)
            },

            openEmbedVimeoModal(command) {
                this.$refs["embed-vimeo-modal"].showModal(command)
            },

            toggleSourceCodeEditor() {
                this.$set(this, "sourceCodeEditorIsActive", !this.sourceCodeEditorIsActive)
            },

            addCommand(data) {
                if (data.command !== null) {
                    data.command(data.data)
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