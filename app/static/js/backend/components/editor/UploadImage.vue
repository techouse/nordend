<template>
    <modal v-if="show" :class="{show: show}" :modal-class="modalClass" @close="closeModal">
        <template v-slot:title>
            {{ activeTab === "gallery" ? 'Select' : 'Upload' }} image
        </template>
        <template v-slot:body>
            <el-tabs v-model="activeTab">
                <el-tab-pane label="Gallery" name="gallery">
                    <el-row v-for="(imageRow, rowIndex) in arrayChunk(images, imagesPerRow)" :key="rowIndex"
                            v-loading="loading" :gutter="20"
                    >
                        <el-col v-for="image in imageRow" :key="image.id" :span="24/imagesPerRow">
                            <div @click.prevent="handleImageGallerySelect(image)">
                                <el-card :body-style="{ padding: '0', textAlign: 'center' }"
                                         :class="{selected: photo.id === image.id}" class="image-card" shadow="hover"
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
    import Photo                    from "../../models/Image"

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
                activeTab:       "gallery",
                uploadHeaders:   {},

                imagesPerRow:       6,
                images:             [],
                params:             {
                    search:   this.search,
                    page:     this.page,
                    per_page: this.per_page,
                    sort:     null
                },
                pageSizes:          [12, 24, 48, 96],
                totalCount:         0,
                minimumImageWidth:  100,
                minimumImageHeight: 100,
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),

            modalClass() {
                return this.activeTab === "gallery" ? "modal-xl" : ""
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
            ...mapActions("alert", ["error"]),

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

            showModal(command) {
                this.$set(this, "command", command)
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
                this.$set(this, "activeTab", "file")
                this.$set(this, "imageUrl", "")
            },

            handleImageGallerySelect(image) {
                this.$set(this, "photo", image)
                this.$set(this, "imageUrl", `${this.photo.public_path}/original.jpg`)
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

            insertImage() {
                let sources = [],
                    src     = this.imageUrl

                if (this.photo.id) {
                    sources = this.photo.sizes
                                  .map(size => Number(size))
                                  .filter(size => size >= 440) // Minimum size for srcset
                                  .sort((a, b) => a - b)
                                  .map(size => {
                                      return {
                                          media:       Photo.getMediaBreakPoint(size),
                                          srcset:      `${this.photo.public_path}/${size}.jpg`,
                                          "data-size": size
                                      }
                                  })

                    if (this.photo.sizes.map(size => Number(size)).includes(1920)) {
                        src = `${this.photo.public_path}/1920.jpg`
                    } else {
                        sources = sources.concat([{
                            media:       Photo.getMediaBreakPoint(this.photo.width),
                            srcset:      `${this.photo.public_path}/original.jpg`,
                            "data-size": this.photo.width
                        }])
                    }
                }

                const data = {
                    command: this.command,
                    data:    {
                        src:       src,
                        alt:       this.photo.original_title,
                        title:     this.photo.original_title,
                        "data-id": this.photo.id,
                        sources:   sources
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

<style lang="scss" scoped>
    .el-row {
        margin-bottom: 20px;

        &:last-child {
            margin-bottom: 0;
        }
    }
</style>