<template>
    <modal v-if="show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            Upload image
        </template>
        <template v-slot:body>
            <el-tabs v-model="activeTab" @tab-click="handleTabChange">
                <el-tab-pane label="File" name="file">
                    <el-upload v-loading="loading"
                               element-loading-text="Uploading image..."
                               drag
                               class="text-center"
                               action="/api/v1/images/"
                               :show-file-list="false"
                               :on-success="handleImageSuccess"
                               :before-upload="beforeImageUpload"
                               :headers="uploadHeaders"
                    >
                        <img v-if="imageUrl" class="preview-img" :src="previewImageUrl">
                        <div v-else>
                            <i class="el-icon-upload"/>
                            <div class="el-upload__text">
                                Drop image file here or <em>click to upload</em>
                            </div>
                            <div slot="tip" class="el-upload__tip">
                                jpg/png/gif/bmp file with a size less than 2MB
                            </div>
                        </div>
                    </el-upload>
                </el-tab-pane>
                <el-tab-pane label="URL" name="url">
                    <el-input v-model="imageUrl"
                              placeholder="Type or paste URL"
                              clearable
                    />
                </el-tab-pane>
            </el-tabs>
        </template>
        <template v-slot:footer>
            <button class="btn btn-danger" @click.prevent="closeModal">
                Cancel
            </button>
            <button class="btn btn-success" @click.prevent="insertImage">
                Insert
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import Modal                    from "../Modal"
    import Photo                    from "../../models/Photo"

    export default {
        name: "UploadImage",

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
                loading:         false,
                photo:           new Photo(),
                imageUrl:        "",
                previewImageUrl: "",
                command:         null,
                show:            false,
                activeTab:       "file",
                uploadHeaders:   {},
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),
        },

        methods: {
            ...mapActions("alert", ["error"]),

            findClosest(x, arr) {
                const indexArr = arr.map(k => Math.abs(k - x))
                const min = Math.min.apply(Math, indexArr)
                return arr[indexArr.indexOf(min)]
            },

            showModal(command) {
                this.$set(this, "command", command)
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
                this.$set(this, "activeTab", "file")
                this.$set(this, "imageUrl", "")
            },

            handleTabChange(tab, event) {
                // console.log(tab, event)
            },

            handleImageSuccess(response, file) {
                this.$set(this, "loading", false)
                this.$set(this, "photo", new Photo(response))
                this.$set(this, "imageUrl", `${this.photo.public_path}/original.jpg`)
                let closestSize = this.findClosest(360, this.photo.sizes || [])
                if (!closestSize || closestSize < 360) {
                    closestSize = "original"
                }
                this.$set(this, "previewImageUrl", `${this.photo.public_path}/${closestSize}.jpg`)
            },

            beforeImageUpload(file) {
                this.$set(this, "loading", true)
                this.$set(this.uploadHeaders, "Authorization", `Bearer ${this.token}`)

                if (!["image/jpeg", "image/png", "image/gif", "image/bmp"].includes(file.type)) {
                    this.error("Image must be of type JPG, PNG, GIF or BMP.")
                    return false
                }

                if (file.size / 1024 / 1024 > 2) {
                    this.error("Image can not exceed 2 MB in size.")
                    return false
                }

                return true
            },

            insertImage() {
                const data = {
                    command: this.command,
                    data:    {
                        src:   this.imageUrl,
                        alt:   this.photo.original_title,
                        title: this.photo.original_title,
                    }
                }

                this.$emit("onConfirm", data)
                this.closeModal()
            },
        }
    }
</script>

<style lang="scss" scoped>
    .modal {
        .preview-img {
            width: 100%;
        }
    }
</style>

<style lang="scss">
    .el-upload {
        .el-upload-dragger {
            height: auto !important;
            min-height: 180px;
            max-width: 360px;
        }
    }
</style>