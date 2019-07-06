<template>
    <modal v-if="show" :class="{show: show}" :modal-class="modalClass" @close="closeModal">
        <template v-slot:title>
            {{ activeTab === "file" ? 'Upload' : 'Select' }} {{ multiple && activeTab === "file" ? 'images' : 'image' }}
        </template>
        <template v-slot:body>
            <template v-if="gallery">
                <el-tabs v-model="activeTab">
                    <el-tab-pane label="File" name="file">
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
                                   :on-change="handleChange"
                                   drag
                                   :multiple="multiple"
                        >
                            <div>
                                <i class="el-icon-upload"/>
                                <div class="el-upload__text">
                                    Drop image {{ multiple ? 'files' : 'file' }} here or <em>click to upload</em>
                                </div>
                                <div slot="tip" class="el-upload__tip">
                                    jpg/png/gif/bmp files with a size less than 2MB
                                </div>
                            </div>
                        </el-upload>
                    </el-tab-pane>
                    <el-tab-pane label="Gallery" name="gallery">
                        <el-row v-for="(imageRow, rowIndex) in arrayChunk(images, imagesPerRow)" :key="rowIndex"
                                v-loading="loading" :gutter="20"
                        >
                            <el-col v-for="image in imageRow" :key="image.id" :span="24/imagesPerRow">
                                <div @click.prevent="handleImageGallerySelect(image)">
                                    <el-card :body-style="{ padding: '0', textAlign: 'center' }"
                                             :class="{selected: photo.id === image.id}" class="image-card"
                                             shadow="hover"
                                    >
                                        <img :src="getThumbnailSrc(image)" class="image-list-thumbnail">
                                        <div style="padding: 14px;">
                                            <span>{{ (image.title || image.original_filename) | truncateMiddle(20) }}</span>
                                        </div>
                                    </el-card>
                                </div>
                            </el-col>
                        </el-row>
                        <div class="d-flex justify-content-center mt-2">
                            <el-pagination :current-page.sync="params.page"
                                           :page-sizes="pageSizes"
                                           :page-size.sync="params.per_page"
                                           :total="totalCount"
                                           layout="prev, pager, next, sizes"
                                           background
                                           @size-change="getData"
                                           @current-change="getData"
                            />
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </template>
            <template v-else>
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
                           :on-change="handleChange"
                           drag
                           :multiple="multiple"
                >
                    <div>
                        <i class="el-icon-upload"/>
                        <div class="el-upload__text">
                            Drop image {{ multiple ? 'files' : 'file' }} here or <em>click to upload</em>
                        </div>
                        <div slot="tip" class="el-upload__tip">
                            jpg/png/gif/bmp files with a size less than 2MB
                        </div>
                    </div>
                </el-upload>
            </template>
        </template>
        <template v-slot:footer>
            <button v-if="activeTab === 'gallery'" class="btn btn-success" @click.prevent="selectImage"
                    :disabled="loading">
                Select
            </button>
            <button v-else class="btn btn-danger" @click.prevent="closeModal" :disabled="loading">
                Close
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import Modal                    from "../../components/Modal"
    import Photo                    from "../../models/Image"
    import {uniqBy}                 from "lodash"

    export default {
        name: "CreateImage",

        components: {
            "modal": Modal
        },

        props: {
            multiple: {
                type:    Boolean,
                default: true
            },
            gallery:  {
                type:    Boolean,
                default: false
            }
        },

        data() {
            return {
                loading:            false,
                completedCount:     0,
                totalImages:        0,
                photo:              new Photo(),
                show:               false,
                uploadHeaders:      {},
                minimumImageWidth:  100,
                minimumImageHeight: 100,
                uploadLimit:        10,

                imageUrl:     "",
                activeTab:    "file",
                imagesPerRow: 6,
                images:       [],
                params:       {
                    search:   this.search,
                    page:     this.page,
                    per_page: this.per_page,
                    sort:     null
                },
                pageSizes:    [12, 24, 48, 96],
                totalCount:   0,
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),

            modalClass() {
                return this.activeTab === "gallery" ? "modal-xl" : ""
            },

            loadingText() {
                if (this.totalImages > 1) {
                    return `Uploading image ${this.completedCount + 1} of ${this.totalImages} ...`
                } else {
                    return "Uploading image ..."
                }
            }
        },

        mounted() {
            this.$set(this.params, "search", null)
            this.$set(this.params, "page", 1)
            this.$set(this.params, "per_page", 12)
            this.$set(this.params, "sort", null)

            this.getData()
        },

        methods: {
            ...mapActions("alert", ["error", "success", "warning"]),

            ...mapActions("image", ["getImages"]),

            arrayChunk(array, chunk_size) {
                return array.reduce(
                    (segments, _, index) =>
                        index % chunk_size === 0
                        ? [...segments, array.slice(index, index + chunk_size)]
                        : segments,
                    []
                )
            },

            getThumbnailSrc(image) {
                if (image.thumbnail_sizes.length > 0) {
                    for (let size of [280, 220]) {
                        if (image.thumbnail_sizes.includes(size)) {
                            return `${image.public_path}/${size}.jpg`
                        }
                    }
                }

                return `${image.public_path}/original.jpg`
            },

            getData() {
                this.$set(this, "loading", true)

                this.getImages({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "images", data.results.map(image => new Photo(image)))
                        this.$set(this, "totalCount", data.count)
                        this.$set(this, "loading", false)
                    })
            },

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
                this.$set(this, "completedCount", 0)
                this.$set(this, "totalImages", 0)
                this.$set(this, "photo", new Photo())
                this.$set(this, "uploadHeaders", {})
            },

            handleImageSuccess(response, file, fileList) {
                const complete = !fileList.some(file => file.status === "uploading")
                this.$set(this, "completedCount", fileList.filter(file => file.status === "success").length)

                this.$set(this, "photo", new Photo(response))
                this.success(`Image ${this.photo.original_filename} uploaded successfully!`)

                if (complete) {
                    this.$set(this, "loading", false)
                    this.$emit("success", this.multiple ? uniqBy(fileList.filter(file => file.status === "success")
                                                                         .map(file => new Photo(file.response)),
                                                                 "id")
                                                        : this.photo)
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

            handleImageGallerySelect(image) {
                this.$set(this, "photo", image)
                this.$set(this, "imageUrl", `${this.photo.public_path}/original.jpg`)
            },

            selectImage() {
                this.$emit("success", this.photo)
                this.closeModal()
            },

            handleChange(file, fileList) {
                this.$set(this, "totalImages", fileList.length)
            },

            handleUploadLimitExceeded(files, fileList) {
                this.warning(`Please do not try to upload more than ${this.uploadLimit} images at once!`)

                this.$refs.image_upload.clearFiles()
            }
        }
    }
</script>

<style lang="scss" scoped>
    .modal {
        .el-row {
            margin-bottom: 20px;

            .image-card {
                &:hover {
                    cursor: pointer;
                }

                &.selected {
                    outline: none;
                    border-color: #409eff;
                    box-shadow: 0 0 10px #409eff;
                }
            }

            &:last-of-type {
                margin-bottom: 0;
            }
        }
    }
</style>