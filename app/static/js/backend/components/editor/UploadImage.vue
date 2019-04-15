<template>
    <div v-if="show" class="modal fade" role="dialog" tabindex="-1" :class="{show: show}">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">
                        Upload image
                    </h4>
                    <button class="close" data-dismiss="modal" aria-label="Close" @click.prevent="closeModal">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <el-tabs v-model="activeTab" @tab-click="handleTabChange">
                        <el-tab-pane label="File" name="file">
                            <el-upload drag
                                       class="text-center"
                                       action="/api/v1/images/"
                                       :show-file-list="false"
                                       :on-success="handleImageSuccess"
                                       :before-upload="beforeImageUpload"
                                       :headers="uploadHeaders"
                            >
                                <img class="preview-img" v-if="imageUrl" :src="imageUrl">
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
                </div>
                <div class="modal-footer">
                    <button class="btn btn-danger" @click.prevent="closeModal">
                        Cancel
                    </button>
                    <button class="btn btn-success" @click.prevent="insertImage">
                        Insert
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapActions} from "vuex"
    import Photo        from "../../models/Photo"

    export default {
        name: "UploadImage",

        props: {
            postId: {
                type:    [String, Number],
                default: null
            }
        },

        data() {
            return {
                photo:         new Photo(),
                imageUrl:      "",
                command:       null,
                show:          false,
                activeTab:     "file",
                uploadHeaders: {
                    "Authorization": Number(localStorage.getItem("remember"))
                                     ? `Bearer ${localStorage.getItem("token")}`
                                     : `Bearer ${sessionStorage.getItem("token")}`
                },
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
                this.$set(this, "activeTab", "file")
                this.$set(this, "imageUrl", "")
            },

            handleTabChange(tab, event) {
                // console.log(tab, event)
            },

            handleImageSuccess(response, file) {
                this.$set(this, "photo", new Photo(response))
                this.$set(this, "imageUrl", `${response.public_path}/original.jpg`)
            },

            beforeImageUpload(file) {
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
                        src: this.imageUrl,
                        alt: this.photo.original_title,
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
        overflow-y: auto !important;

        &.show {
            display: block;
        }

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