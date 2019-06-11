<template>
    <div class="row">
        <div class="col-sm-12">
            <el-form :ref="formRef" v-loading="loading" :model="model" :rules="rules" :label-width="labelWidth"
                     class="card"
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

        methods: {
            validate(callback) {
                return this.$refs[this.formRef].validate(callback)
            }
        }
    }
</script>