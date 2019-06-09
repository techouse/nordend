<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <el-form :ref="formRef" v-loading="loading" :model="category" :rules="rules" :label-width="labelWidth" class="card">
                    <div class="card-header">
                        <el-page-header :content="title" @back="goBack" />
                        <div v-if="category.id" class="card-header-actions">
                            <button class="btn btn-sm btn-danger" @click.prevent="remove">
                                Delete category
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <el-form-item label="Name" prop="name">
                            <el-input v-model="category.name" type="string" required/>
                        </el-form-item>
                    </div>
                    <div class="card-footer">
                        <el-button type="success" @click="submit">
                            Submit
                        </el-button>
                        <el-button type="danger" @click="$router.push({name: 'Categories'})">
                            Cancel
                        </el-button>
                    </div>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import CreatePartial from "../../components/CreatePartial"
    import Category      from "../../models/Category"
    import {mapActions}  from "vuex"

    export default {
        name: "CreateCategory",

        extends: CreatePartial,

        data() {
            return {
                formRef:    "create-category-form",
                category:   new Category(),
                rules:      {
                    name: [
                        {required: true, message: "Please enter a name", trigger: "blur"},
                        {min: 1, max: 255, message: "Length should be between 1 and 255 characters", trigger: "blur"}
                    ],
                },
            }
        },

        computed: {
            title() {
                return "Create new category"
            }
        },

        methods: {
            ...mapActions("category", ["createCategory"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.createCategory(this.category)
                            .then(({data}) => {
                                this.success("Category successfully created")
                                this.$router.push({name: "EditCategory", params: {categoryId: data.id}})
                            })
                            .catch(() => {
                                this.error(`There was an error creating the category: ${this.alert.message}`)
                            })
                    } else {
                        this.error("The form data is invalid!")
                        return false
                    }
                })
            }
        }
    }
</script>