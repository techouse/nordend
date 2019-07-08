<template>
    <card-form :ref="formRef" :form-ref="formRef" :loading="loading" :model="user" :rules="rules"
               :label-width="labelWidth">
        <template v-slot:header>
            <el-page-header :content="title" @back="goBack"/>
            <div v-if="user.id" class="card-header-actions">
                <button class="btn btn-sm btn-danger" @click.prevent="remove">
                    Delete user
                </button>
            </div>
        </template>
        <template v-slot:body>
            <div class="row">
                <div class="col-sm-6">
                    <el-form-item label="E-mail" prop="email">
                        <el-input v-model="user.email" type="email" required/>
                    </el-form-item>
                    <el-form-item label="Password" prop="password">
                        <el-input v-model="user.password" type="password" :required="!user.id"/>
                    </el-form-item>
                    <el-form-item label="Repeat password" prop="password_repeat">
                        <el-input v-model="user.password_repeat" type="password" :required="!user.id"/>
                    </el-form-item>
                    <el-form-item label="Role" prop="role_id">
                        <el-select v-model="user.role_id" placeholder="User role" required>
                            <el-option v-for="role in roles"
                                       :key="role.id"
                                       :label="role.name"
                                       :value="role.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Confirmed" prop="confirmed">
                        <el-switch v-model="user.confirmed"
                                   active-color="#13ce66"
                                   inactive-color="#ff4949"
                                   active-text="Yes"
                                   inactive-text="No"
                                   required
                        />
                    </el-form-item>
                    <el-form-item v-if="displayOtpButtons" label="2 Factor Auth">
                        <el-button v-if="user.otp_enabled" type="danger" plain round @click="disableOtp">
                            Disable 2FA
                        </el-button>
                        <el-button v-else type="success" plain round @click="enableOtp">
                            Enable 2FA
                        </el-button>
                    </el-form-item>
                </div>
                <div class="col-sm-6">
                    <el-form-item label="Name" prop="name">
                        <el-input v-model="user.name" type="text" required/>
                    </el-form-item>
                    <el-form-item label="Location" prop="location">
                        <el-input v-model="user.location" type="text"/>
                    </el-form-item>
                    <el-form-item label="About" prop="about_me">
                        <el-input v-model="user.about_me"
                                  type="textarea"
                                  :autosize="{ minRows: 8, maxRows: 16}"
                        />
                    </el-form-item>
                </div>
            </div>
            <enable-otp :ref="generateOtpRef" :user="user" @success="handleOtpEnabled"/>
        </template>
        <template v-slot:footer>
            <el-button type="success" @click="submit">
                Submit
            </el-button>
        </template>
    </card-form>
</template>

<script>
    import CreatePartial            from "../../components/CreatePartial"
    import User                     from "../../models/User"
    import Role                     from "../../models/Role"
    import EnableOtp                from "./OTP/enable"
    import {mapActions, mapGetters} from "vuex"

    export default {
        name: "CreateUser",

        components: {
            EnableOtp
        },

        extends: CreatePartial,

        data() {
            return {
                formRef:        "create-user-form",
                generateOtpRef: "generate-otp",
                user:           new User(),
                roles:          [],
                rules:          {
                    email:           [
                        {required: true, message: "Please enter email address", trigger: "blur"},
                        {type: "email", message: "Please enter a valid email address", trigger: "blur"},
                    ],
                    password:        [
                        {required: true, message: "Please enter a password", trigger: "blur"},
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback(new Error("Please enter a password"))
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
                        {required: true, message: "Please re-enter the password", trigger: "blur"},
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback(new Error("Please re-enter the password"))
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

        computed: {
            title() {
                return "Create new user"
            },

            displayOtpButtons() {
                return false
            }
        },

        created() {
            this.getRoles()
                .then(({data}) => {
                    this.$set(this, "roles", data.results.map(role => new Role(role)))
                })
        },

        mounted() {
            if (!this.user.role_id) {
                this.$set(this.user, "role_id", 1)
            }
        },

        methods: {
            ...mapActions("user", ["createUser"]),

            ...mapActions("user", {
                disableOtpAction: "disableOtp"
            }),

            ...mapActions("role", ["getRoles"]),

            enableOtp() {
                this.$refs[this.generateOtpRef].showModal()
            },

            disableOtp() {
                this.$confirm("Are you sure you want to disable 2 Factor Authentication?", "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                        this.disableOtpAction(this.user)
                            .then(({data}) => {
                                this.$set(this.user, "otp_enabled", false)
                                this.success("2 Factor Authentication successfully disabled!")
                            })
                            .catch(error => {
                                this.error(`There was an disabling enabling 2 Factor Authentication: ${this.alert.message}`)
                            })
                    })
                    .catch(() => {
                        this.info("2 Factor Authentication not disabled!")
                    })
            },

            handleOtpEnabled() {
                this.$set(this.user, "otp_enabled", true)
            },

            submit() {
                this.$refs[this.formRef].validate((valid) => {
                    if (valid) {
                        this.createUser(this.user)
                            .then(({data}) => {
                                this.success("User successfully created")
                                this.$router.push({name: "EditUser", params: {userId: data.id}})
                            })
                            .catch(() => {
                                this.error(`There was an error creating the user: ${this.alert.message}`)
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