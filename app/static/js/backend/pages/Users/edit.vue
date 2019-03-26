<script>
    import CreateUser   from "./create"
    import {mapActions} from "vuex"
    import User         from "../../models/User"

    export default {
        name: "EditUser",

        extends: CreateUser,

        props: {
            userId: {
                type:     [String, Number],
                required: true
            }
        },

        data() {
            return {
                formRef: "edit-user-form",
                title:   "Edit user",
                user:    new User(),
                rules:   {
                    email:           [
                        {required: true, message: "Please enter email address", trigger: "blur"},
                        {type: "email", message: "Please enter a valid email address", trigger: "blur"},
                    ],
                    password:        [
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback()
                                } else if (value.length > 0 && value.length < 8) {
                                    callback(new Error("Password is too short"))
                                } else {
                                    if (this.user.password_repeat !== "") {
                                        this.$refs[this.formRef].validateField("password_repeat")
                                    }
                                    callback()
                                }
                            },
                            trigger:   "blur"
                        }
                    ],
                    password_repeat: [
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback()
                                } else if (value !== this.user.password) {
                                    callback(new Error("The password confirmation does not match the password"))
                                } else {
                                    callback()
                                }
                            },
                            trigger:   "blur"
                        }],
                    role_id:         [
                        {required: true, message: "Please select a role", trigger: "blur"},
                    ],
                    confirmed:       [
                        {required: true, message: "Please confirm or reject the user", trigger: "blur"},
                    ],
                    name:            [
                        {required: true, message: "Please enter a name", trigger: "blur"},
                        {min: 3, max: 255, message: "Length should be between 3 and 255 characters", trigger: "blur"}
                    ],
                    location:        [
                        {max: 255, message: "Length should not exceed 255 characters", trigger: "blur"}
                    ],
                    about_me:        [],
                }
            }
        },

        created() {
            this.getUser(this.userId)
                .then(({data}) => {
                    this.$set(this, "user", new User(data))
                })
        },

        methods: {
            ...mapActions("user", ["updateUser"]),

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.updateUser(this.user)
                            .then(() => {
                                this.$set(this.user, "password", null)
                                this.$set(this.user, "password_repeat", null)
                                this.success("User successfully updated")
                            })
                            .catch(() => {
                                this.error(`There was an error updating the user: ${this.alert.message}`)
                            })
                    } else {
                        this.error("The form data is invalid!")
                        return false
                    }
                })
            },

            remove() {
                this.$confirm(`Are you sure you want to delete ${this.user.name}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteUser(this.user.id)
                                  .then(() => {
                                      this.$router.push({name: "Users"})
                                      this.success("User successfully deleted")
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the user: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("User not deleted")
                    })
            }
        },

        beforeRouteUpdate(to, from, next) {
            this.getUser(to.params.userId)
                .then(({data}) => {
                    this.$set(this, "user", new User(data))
                })
            next()
        }
    }
</script>