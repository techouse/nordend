<template>
    <modal v-if="show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            Embed Vimeo video
        </template>
        <template v-slot:body>
            <el-form ref="vimeo_form" :model="form" :rules="rules" label-width="120px">
                <el-form-item label="Vimeo URL" prop="url">
                    <el-input v-model="form.url" type="url" required/>
                </el-form-item>
                <el-form-item label="Start at">
                    <el-time-picker v-model="start"
                                    :picker-options="{format: 'HH:mm:ss'}"
                                    placeholder="Start at"
                                    :disabled="!vimeoUrlValid"
                                    @change="changeStart">
                    </el-time-picker>
                </el-form-item>
                <el-form-item label="Width" prop="width">
                    <el-input-number v-model="form.width"
                                     :min="426"
                                     :max="3840"
                                     :disabled="!vimeoUrlValid"
                                     required
                                     @change="changeWidth"
                    />
                </el-form-item>
                <el-form-item label="Height" prop="height">
                    <el-input-number v-model="form.height"
                                     :min="240"
                                     :max="2160"
                                     :disabled="!vimeoUrlValid"
                                     required
                                     @change="changeHeight"
                    />
                </el-form-item>
            </el-form>
        </template>
        <template v-slot:footer>
            <button class="btn btn-danger" @click.prevent="closeModal">
                Cancel
            </button>
            <button class="btn btn-success" :disabled="!form.url" @click.prevent="insertVimeoVideo">
                Embed
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions}               from "vuex"
    import Modal                      from "../Modal"
    import {
        getHours,
        getMinutes,
        getSeconds,
        setHours,
        setMinutes,
        setSeconds
    }                                 from "date-fns"
    import {getVimeoId, getVimeoInfo} from "./Vimeo"

    export default {
        name: "EmbedVimeo",

        components: {
            "modal": Modal
        },

        props: {
            postId: {
                type:    [String, Number],
                default: null
            }
        },

        data() {
            return {
                command:     null,
                show:        false,
                aspectRatio: 16 / 9,
                start:       setSeconds(setMinutes(setHours(new Date(), 0), 0), 0),
                form:        {
                    url:    null,
                    title:  null,
                    width:  640,
                    height: 360
                },
                rules:       {
                    url:    [
                        {validator: this.validateVimeoUrl, trigger: "blur"},
                    ],
                    width:  [
                        {validator: this.validateWidth, trigger: "blur"}
                    ],
                    height: [
                        {validator: this.validateHeight, trigger: "blur"}
                    ]
                }
            }
        },

        computed: {
            vimeoUrlValid() {
                return this.form.url ? getVimeoId(this.form.url) : false
            },
            startSeconds() {
                const seconds = getHours(this.start) * 3600 + getMinutes(this.start) * 60 + getSeconds(this.start)
                return seconds > 0 ? seconds : null
            }
        },

        methods: {
            ...mapActions("alert", ["error"]),

            showModal(command) {
                this.$set(this, "command", command)
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
            },

            changeWidth(width) {
                this.$set(this.form, "height", Math.round(width / this.aspectRatio))
            },

            changeHeight(height) {
                this.$set(this.form, "width", Math.round(height * this.aspectRatio))
            },

            changeStart(start) {
                if (start === null) {
                    this.$set(this, "start", setSeconds(setMinutes(setHours(new Date(), 0), 0), 0))
                    this.$set(this.form, "start", null)
                }
            },

            validateVimeoUrl(rule, value, callback) {
                if (!value) {
                    callback(new Error("Please input a Vimeo URL"))
                } else if (!getVimeoId(value)) {
                    callback(new Error("The Vimeo URL is invalid."))
                } else {
                    callback()
                }
            },

            validateWidth(rule, value, callback) {
                if (Number(value) <= 0) {
                    callback(new Error("Please input a Vimeo video width"))
                } else if (Number(value) < 426 || Number(value) > 3840) {
                    callback(new Error("Please input a Vimeo video width between 426 and 3840"))
                } else {
                    callback()
                }
            },

            validateHeight(rule, value, callback) {
                if (Number(value) <= 0) {
                    callback(new Error("Please input a Vimeo video height"))
                } else if (Number(value) < 240 || Number(value) > 2160) {
                    callback(new Error("Please input a Vimeo video height between 240 and 2160"))
                } else {
                    callback()
                }
            },

            insertVimeoVideo() {
                this.$refs["vimeo_form"].validate((valid) => {
                    if (valid) {
                        getVimeoInfo(getVimeoId(this.form.url))
                            .then(response => {
                                const data = {
                                    command: this.command,
                                    data:    {
                                        src:    `https://player.vimeo.com/video/${getVimeoId(this.form.url)}`,
                                        title:  response.title,
                                        thumb:  response.thumbnail_large,
                                        start:  this.startSeconds,
                                        width:  this.form.width,
                                        height: this.form.height
                                    }
                                }

                                this.$emit("onConfirm", data)

                                this.$set(this, "form", {
                                    url:    null,
                                    width:  640,
                                    height: 360
                                })

                                this.closeModal()
                            })
                            .catch(() => {
                                this.error("The Vimeo video does not exist!")
                            })
                    } else {
                        this.error("The Vimeo URL is invalid!")
                    }
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .el-form-item__content {
        & > div:first-child {
            width: calc(100% - 120px);
        }
    }
</style>