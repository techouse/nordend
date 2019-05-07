<template>
    <el-input v-model="sourceCode"
              type="textarea"
              autosize
              placeholder="Please write some content HTML here ..."
    />
</template>

<script>
    export default {
        name: "SourceCode",

        props: {
            value: {
                type: String
            }
        },

        computed: {
            sourceCode: {
                get() {
                    return this.value
                },
                set(sourceCode) {
                    this.$emit("input", sourceCode)
                    this.$emit("onUpdate")
                }
            }
        }
    }
</script>