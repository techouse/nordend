<template>
    <editor ref="sourceCodeEditor"
            v-model="sourceCode"
            lang="html"
            theme="chrome"
            width="auto"
            height="500"
            @init="editorInit"
    />
</template>

<script>
    import Editor from "vue2-ace-editor"
    import {html} from "js-beautify"

    export default {
        name: "SourceCode",

        components: {
            editor: Editor
        },

        props: {
            value: {
                type: String
            }
        },

        data() {
            return {
                sourceCode:      null,
                beautifyOptions: {
                    indent_size:      4,
                    html:             {
                        end_with_newline: true,
                        indent_inner_html: true,
                        preserve_newlines: true,
                        js:               {
                            indent_size: 2
                        },
                        css:              {
                            indent_size: 2
                        }
                    },
                    css:              {
                        indent_size: 1
                    },
                    js:               {
                        preserve_newlines: true
                    },
                    wrap_line_length: 140,
                },
            }
        },

        watch: {
            sourceCode(value) {
                this.$emit("input", value)
                this.$emit("onUpdate")
            }
        },

        created() {
            this.$set(this, "sourceCode", html(this.value, this.beautifyOptions))
        },

        methods: {
            editorInit: function () {
                require("brace/ext/language_tools") //language extension prerequsite...
                require("brace/mode/html")
                require("brace/mode/javascript")    //language
                require("brace/mode/css")
                require("brace/theme/chrome")
                require("brace/snippets/javascript") //snippet
            },
        }
    }
</script>