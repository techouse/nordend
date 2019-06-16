<template>
    <div class="row">
        <div class="col-sm-12">
            <el-form :id="id" :ref="formRef" v-loading="loading" :model="model" :rules="rules"
                     :label-width="labelWidth" class="card"
            >
                <div class="card-header">
                    <slot name="header" />
                </div>
                <div class="card-body">
                    <slot name="body" />
                </div>
                <div class="card-footer">
                    <slot name="footer" />
                </div>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CardForm",

        props: {
            id: {
                type:    String,
                default: "card-form"
            },
            formRef:    {
                type:    String,
                default: "form"
            },
            loading:    {
                type:    Boolean,
                default: false
            },
            model:      {
                type:    Object,
                require: true
            },
            rules:      {
                type:    Object,
                default: () => ({})
            },
            labelWidth: {
                type:    String,
                default: "140px"
            },
        },

        data() {
            return {
                width: 0,
                height: 0
            }
        },

        mounted() {
            this.handleWindowResize()
            window.addEventListener("resize", this.handleWindowResize)
        },

        methods: {
            handleWindowResize() {
                this.$set(this, "width", document.getElementById(this.id).clientWidth)
                this.$set(this, "height", document.getElementById(this.id).clientHeight)
            },

            validate(callback) {
                return this.$refs[this.formRef].validate(callback)
            },

            validateField(callback) {
                return this.$refs[this.formRef].validateField(callback)
            },

            resetFields() {
                return this.$refs[this.formRef].resetFields()
            },

            clearValidate(callback) {
                return this.$refs[this.formRef].clearValidate(callback)
            }
        }
    }
</script>