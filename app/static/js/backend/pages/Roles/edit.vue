<script>
    import CreateRole   from "./create"
    import Role         from "../../models/Role"
    import {mapActions} from "vuex"

    export default {
        name: "EditRole",

        extends: CreateRole,

        props: {
            roleId: {
                type:     [String, Number],
                required: true
            }
        },

        data() {
            return {
                formRef:  "edit-role-form",
                title:    "Edit role",
                role: new Role(),
            }
        },

        created() {
            this.getRole(this.roleId)
                .then(({data}) => {
                    this.$set(this, "role", new Role(data))
                })
        },

        methods: {
            ...mapActions("role", ["getRole", "updateRole", "deleteRole"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.updateRole(this.role)
                            .then(() => {
                                this.success("Role successfully updated")
                            })
                            .catch(() => {
                                this.error(`There was an error updating the role: ${this.alert.message}`)
                            })
                    } else {
                        this.error("The form data is invalid!")
                        return false
                    }
                })
            },

            remove() {
                this.$confirm(`Are you sure you want to delete ${this.role.name}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteRole(this.role.id)
                                  .then(() => {
                                      this.$router.push({name: "Roles"})
                                      this.success("Role successfully deleted")
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the role: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("Role not deleted")
                    })
            }
        }
    }
</script>