<template>
    <modal v-if="show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            Embed YouTube video
        </template>
        <template v-slot:body>
            <el-form ref="youtube_form" :model="form" :rules="rules" label-width="120px">
                <el-form-item label="YouTube URL" prop="url">
                    <el-input v-model="form.url" type="url" required/>
                </el-form-item>
                <el-form-item label="Start at">
                    <el-time-picker v-model="start"
                                    :picker-options="{format: 'HH:mm:ss'}"
                                    placeholder="Start at"
                                    :disabled="!youTubeUrlValid"
                                    @change="changeStart">
                    </el-time-picker>
                </el-form-item>
                <el-form-item label="Width" prop="width">
                    <el-input-number v-model="form.width"
                                     :min="426"
                                     :max="3840"
                                     :disabled="!youTubeUrlValid"
                                     required
                                     @change="changeWidth"
                    />
                </el-form-item>
                <el-form-item label="Height" prop="height">
                    <el-input-number v-model="form.height"
                                     :min="240"
                                     :max="2160"
                                     :disabled="!youTubeUrlValid"
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
            <button class="btn btn-success" :disabled="!form.url" @click.prevent="insertYouTubeVideo">
                Embed
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions}   from "vuex"
    import Modal          from "../Modal"
    import {
        getHours,
        getMinutes,
        getSeconds,
        setHours,
        setMinutes,
        setSeconds
    }                     from "date-fns"
    import {getYouTubeId} from "./YouTube"

    export default {
        name: "EmbedYouTube",

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
                    width:  640,
                    height: 360
                },
                rules:       {
                    url:    [
                        {validator: this.validateYouTubeUrl, trigger: "blur"},
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
            youTubeUrlValid() {
                return this.form.url ? getYouTubeId(this.form.url) : false
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

            validateYouTubeUrl(rule, value, callback) {
                if (!value) {
                    callback(new Error("Please input a YouTube URL"))
                } else if (!getYouTubeId(value)) {
                    callback(new Error("The YouTube URL is invalid."))
                } else {
                    callback()
                }
            },

            validateWidth(rule, value, callback) {
                if (Number(value) <= 0) {
                    callback(new Error("Please input a YouTube video width"))
                } else if (Number(value) < 426 || Number(value) > 3840) {
                    callback(new Error("Please input a YouTube video width between 426 and 3840"))
                } else {
                    callback()
                }
            },

            validateHeight(rule, value, callback) {
                if (Number(value) <= 0) {
                    callback(new Error("Please input a YouTube video height"))
                } else if (Number(value) < 240 || Number(value) > 2160) {
                    callback(new Error("Please input a YouTube video height between 240 and 2160"))
                } else {
                    callback()
                }
            },

            insertYouTubeVideo() {
                this.$refs["youtube_form"].validate((valid) => {
                    if (valid) {
                        const data = {
                            command: this.command,
                            data:    {
                                src:    `https://www.youtube.com/embed/${getYouTubeId(this.form.url)}`,
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
                    } else {
                        this.error("The YouTube URL is invalid!")
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