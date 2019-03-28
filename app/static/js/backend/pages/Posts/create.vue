<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <el-form :ref="formRef" :model="post" :rules="rules" label-width="160px" class="card">
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
                        <vue-editor v-model="post.body"/>
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
    import {mapActions}  from "vuex"
    import {VueEditor}   from "vue2-editor"
    import CreatePartial from "../../components/CreatePartial"
    import Post          from "../../models/Post"
    import Category      from "../../models/Category"

    export default {
        name: "CreatePost",

        components: {
            VueEditor
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
            }
        }
    }
</script>