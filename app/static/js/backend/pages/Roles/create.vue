<template>
    <card-form :ref="formRef" :form-ref="formRef" :loading="loading" :model="role" :rules="rules" :label-width="labelWidth">
        <template v-slot:header>
            <el-page-header :content="title" @back="goBack" />
            <div v-if="role.id" class="card-header-actions">
                <button class="btn btn-sm btn-danger" @click.prevent="remove">
                    Delete role
                </button>
            </div>
        </template>
        <template v-slot:body>
            <el-form-item label="Name" prop="name">
                <el-input v-model="role.name" type="string" required />
            </el-form-item>
            <el-form-item label="Permissions">
                <el-checkbox v-model="role.follow" label="Follow" />
                <el-checkbox v-model="role.comment" label="Comment" />
                <el-checkbox v-model="role.write" label="Write" />
                <el-checkbox v-model="role.moderate" label="Moderate" />
                <el-checkbox v-model="role.admin" label="Admin" />
            </el-form-item>
        </template>
        <template v-slot:footer>
            <el-button type="success" @click="submit">
                Submit
            </el-button>
            <el-button type="danger" @click="$router.push({name: 'Roles'})">
                Cancel
            </el-button>
        </template>
    </card-form>
</template>

<script>
    import CreatePartial from "../../components/CreatePartial"
    import Role          from "../../models/Role"
    import {mapActions}  from "vuex"

    export default {
        name: "CreateRole",

        extends: CreatePartial,

        data() {
            return {
                formRef: "create-role-form",
                role:    new Role(),
                rules:   {
                    name: [
                        {required: true, message: "Please enter a name", trigger: "blur"},
                        {min: 1, max: 255, message: "Length should be between 1 and 255 characters", trigger: "blur"}
                    ],
                },
            }
        },

        computed: {
            title() {
                return "Create new role"
            }
        },

        methods: {
            ...mapActions("role", ["createRole"]),


            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.createRole(this.role)
                            .then(({data}) => {
                                this.success("Role successfully created")
                                this.$router.push({name: "EditRole", params: {roleId: data.id}})
                            })
                            .catch(() => {
                                this.error(`There was an error creating the role: ${this.alert.message}`)
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