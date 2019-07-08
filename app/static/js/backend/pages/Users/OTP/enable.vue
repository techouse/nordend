<template>
    <modal v-if="show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            2 Factor Authentication Setup
        </template>
        <template v-slot:body>
            <p>
                Please scan the QR code below using an authenticator app on your smart phone and enter the
                generated 6-digit code in to the verification field below.
            </p>
            <b class="text-danger">
                For security purposes please write down the 16-character code below and store it in a safe
                place! After you have done so please tick the checkbox below.
                <u>If you do not comply will not be able to continue!</u>
            </b>
            <pre class="text-center" :style="{fontSize: '1.5rem'}">{{ otp.secret }}</pre>
            <el-checkbox v-model="form.codeSafelyStored">
                I hereby confirm that I have stored the code in a safe place.
            </el-checkbox>
            <qrcode-vue :value="otp.uri" :size="size" level="H" class="text-center mb-2"/>
            <el-form ref="form" :model="form" :rules="rules" label-width="120px">
                <el-form-item label="Verification" prop="totp">
                    <el-input id="totp_input" v-model="form.totp" placeholder="Please enter 6-digit one time password"
                              :max="6" :min="6" :disabled="!form.codeSafelyStored" :maxlength="6" required
                              show-word-limit
                    />
                </el-form-item>
            </el-form>
        </template>
        <template v-slot:footer>
            <button class="btn btn-danger" @click.prevent="closeModal">
                Cancel
            </button>
            <button class="btn btn-success" :disabled="!totpEntered" @click.prevent="submit">
                Submit
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import Modal                    from "../../../components/Modal"
    import User                     from "../../../models/User"
    import Otp                      from "../../../models/Otp"
    import QrcodeVue                from "qrcode.vue"

    export default {
        name: "EnableOtp",

        components: {
            Modal,
            QrcodeVue
        },

        props: {
            user: {
                type:     User,
                required: true
            }
        },

        data() {
            return {
                show:  false,
                otp:   new Otp(),
                size:  280,
                form:  {
                    codeSafelyStored: false,
                    totp:             null
                },
                rules: {
                    totp: [
                        {
                            validator: (rule, value, callback) => {
                                if (!value) {
                                    callback(new Error("Please fill the verification field!"))
                                } else {
                                    if (value.length !== 6) {
                                        callback(new Error("One time password must be exactly 6-digits long"))
                                    } else if (!value.match(/^\d+$/)) {
                                        callback(new Error("Please fill the verification with digits only!"))
                                    }
                                    callback()
                                }
                            },
                            trigger:   "blur"
                        }
                    ]
                }
            }
        },

        computed: {
            ...mapGetters("alert", ["alert"]),

            totpEntered() {
                return this.form.totp && this.form.totp.length === 6
            }
        },

        beforeDestroy() {
            this.$set(this, "otp", new Otp())
            this.$set(this.form, "totp", null)
        },

        methods: {
            ...mapActions("user", ["generateOtp", "enableOtp"]),

            ...mapActions("alert", ["error", "success"]),

            showModal() {
                this.generateOtp(this.user)
                    .then(({data}) => {
                        this.$set(this, "otp", new Otp(data))
                        if (window.reCAPTCHASiteKey) {
                            grecaptcha.ready(() => {
                                grecaptcha.execute(window.reCAPTCHASiteKey, {action: "enable_otp"})
                                          .then(token => {
                                              this.$set(this.otp, "recaptcha_token", token)
                                          })
                            })
                        }
                        this.$set(this, "show", true)
                    })
                    .catch(error => {
                        this.closeModal()
                        this.error(`There when requesting a 2 Factor Authentication ability: ${this.alert.message}`)
                    })
            },

            closeModal() {
                this.$set(this, "show", false)
                this.$set(this, "otp", new Otp())
                this.$set(this.form, "totp", null)
            },

            submit() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$set(this.otp, "totp", this.form.totp)
                        this.enableOtp({user: this.user, otp: this.otp})
                            .then(({data}) => {
                                this.$emit("success", true)
                                this.success("2 Factor Authentication successfully enabled!")
                                this.closeModal()
                            })
                            .catch(error => {
                                this.error(`There was an error enabling 2 Factor Authentication: ${this.alert.message}`)
                            })
                    } else {
                        this.error("Form data invalid!")
                        return false
                    }
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .el-form-item__content {
        & > div:first-child {
            width: calc(100% - 140px);
        }
    }
</style>