<template>
    <modal v-if="show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            Upload images
        </template>
        <template v-slot:body>
            <el-upload ref="image_upload"
                       v-loading="loading"
                       :element-loading-text="loadingText"
                       class="text-center"
                       action="/api/v1/images/"
                       :show-file-list="false"
                       :on-success="handleImageSuccess"
                       :before-upload="beforeImageUpload"
                       :headers="uploadHeaders"
                       :limit="uploadLimit"
                       :on-exceed="handleUploadLimitExceeded"
                       drag
                       multiple
            >
                <div>
                    <i class="el-icon-upload"/>
                    <div class="el-upload__text">
                        Drop image files here or <em>click to upload</em>
                    </div>
                    <div slot="tip" class="el-upload__tip">
                        jpg/png/gif/bmp files with a size less than 2MB
                    </div>
                </div>
            </el-upload>
        </template>
        <template v-slot:footer>
            <button class="btn btn-danger" @click.prevent="closeModal" :disabled="loading">
                Close
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import Modal                    from "../../components/Modal"
    import Photo                    from "../../models/Image"

    export default {
        name: "CreateImage",

        components: {
            "modal": Modal
        },

        data() {
            return {
                loading:            false,
                completedCount:     0,
                totalImages:        0,
                photo:              new Photo(),
                imageUrl:           "",
                previewImageUrl:    "",
                show:               false,
                uploadHeaders:      {},
                minimumImageWidth:  100,
                minimumImageHeight: 100,
                uploadLimit:        10,
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),

            loadingText() {
                if (this.completedCount && this.totalImages) {
                    return `Uploading image ${this.completedCount + 1} of ${this.totalImages} ...`
                } else {
                    return "Uploading ..."
                }
            }
        },

        methods: {
            ...mapActions("alert", ["error", "success", "warning"]),

            findClosest(x, arr) {
                const indexArr = arr.map(k => Math.abs(k - x))
                const min = Math.min.apply(Math, indexArr)
                return arr[indexArr.indexOf(min)]
            },

            showModal() {
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
                this.$set(this, "imageUrl", "")
            },

            handleImageSuccess(response, file, fileList) {
                const complete = !fileList.some(file => file.percentage < 100)
                this.$set(this, "totalImages", fileList.length)
                this.$set(this, "completedCount", fileList.filter(file => file.percentage === 100).length)

                this.$set(this, "photo", new Photo(response))
                this.success(`Image ${this.photo.original_filename} uploaded successfully!`)

                if (complete) {
                    this.$set(this, "loading", false)
                    this.$emit("success", true)
                    this.closeModal()
                }
            },

            beforeImageUpload(file) {
                this.$set(this, "loading", true)
                this.$set(this.uploadHeaders, "Authorization", `Bearer ${this.token}`)

                return new Promise((resolve, reject) => {
                    if (!["image/jpeg", "image/png", "image/gif", "image/bmp"].includes(file.type)) {
                        this.error("Photo must be of type JPG, PNG, GIF or BMP.")
                        this.$set(this, "loading", false)
                        return reject(false)
                    }

                    if (file.size / 1024 / 1024 > 2) {
                        this.error("Photo can not exceed 2 MB in size.")
                        this.$set(this, "loading", false)
                        return reject(false)
                    }

                    if (this.minimumImageWidth > 0 || this.minimumImageHeight > 0) {
                        try {
                            let img = new Image()

                            img.onload = () => {
                                const width  = img.naturalWidth,
                                      height = img.naturalHeight

                                window.URL.revokeObjectURL(img.src)

                                if (width >= this.minimumImageWidth && height >= this.minimumImageHeight) {
                                    return resolve(true)
                                } else {
                                    this.error(`Photo too small. It must be at least ${this.minimumImageWidth}px wide and ${this.minimumImageHeight}px high!`)
                                    this.$set(this, "loading", false)
                                    return reject(false)
                                }
                            }

                            img.src = window.URL.createObjectURL(file)
                        } catch (exception) {
                            this.error(exception)
                            this.$set(this, "loading", false)
                            return reject(exception)
                        }
                    } else {
                        return resolve(true)
                    }
                })
            },

            handleUploadLimitExceeded(files, fileList) {
                this.warning(`Please do not try to upload more than ${this.uploadLimit} images at once!`)

                this.$refs.image_upload.clearFiles()
            }
        }
    }
</script>