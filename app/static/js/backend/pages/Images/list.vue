<template>
    <card>
        <template v-slot:header>
            <el-page-header class="no-back" :content="title"/>
            <div class="card-header-actions">
                <button class="btn btn-sm btn-primary" @click.prevent="upload">
                    Upload new image
                </button>
            </div>
        </template>
        <template v-slot:body>
            <el-row v-if="images.length" :gutter="20">
                <el-col :span="9" :style="{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}">
                    <b>Sort by: </b>
                    <el-select v-model="params.sort" clearable placeholder="Sort by">
                        <el-option v-for="item in sortByOptions"
                                   :key="item.value"
                                   :label="item.label"
                                   :value="item.value"
                        />
                    </el-select>
                    <span>
                        <el-switch v-model="sortDirection"
                                   @change="handleSortDirectionChange"
                        />
                        <span>{{ sortDirection ? "Ascending" : "Descending" }}</span>
                    </span>
                </el-col>
                <el-col :span="6" :offset="9">
                    <el-input v-model="params.search"
                              placeholder="Type to search images"
                              clearable
                              @change="searchData"
                    >
                        <el-button slot="append" icon="el-icon-search"/>
                    </el-input>
                </el-col>
            </el-row>
            <el-container v-loading="loading">
                <viewer v-if="images.length" :images="viewerImages" :options="viewerOptions" class="w-100">
                    <template slot-scope="scope">
                        <el-row v-for="(imageRow, rowIndex) in arrayChunk(images, imagesPerRow)" :key="rowIndex"
                                :gutter="20">
                            <el-col v-for="image in imageRow" :key="image.id" :span="24/imagesPerRow">
                                <el-card :body-style="{ padding: '0', textAlign: 'center' }" class="image-card"
                                         shadow="hover"
                                >
                                    <img :src="getThumbnailSrc(image)"
                                         :data-source="getLargestImageSrc(image)"
                                         :alt="image.original_filename"
                                         class="image-viewer-thumbnail"
                                    >
                                    <div style="padding: 14px;">
                                        <span>{{ (image.title || image.original_filename) | truncate_middle(20) }}</span>
                                        <div class="bottom clearfix">
                                            <el-tooltip class="item" effect="dark" content="Edit in image editor"
                                                        placement="left"
                                            >
                                                <el-button size="mini" circle @click="edit(image.id)">
                                                    <i class="fas fa-paint-brush"/>
                                                </el-button>
                                            </el-tooltip>
                                            <el-tooltip class="item" effect="dark" content="Delete"
                                                        placement="right"
                                            >
                                                <el-button type="danger" size="mini" icon="el-icon-delete-solid" circle
                                                           @click="remove(image.id)"
                                                />
                                            </el-tooltip>
                                        </div>
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </template>
                </viewer>
                <div v-else :style="{width: '100%', textAlign: 'center', opacity: .5}">
                    No images <i class="fal fa-frown"/>
                </div>
            </el-container>
            <div v-if="images.length" class="d-flex justify-content-center mt-2">
                <el-pagination :current-page.sync="params.page"
                               :page-sizes="pageSizes"
                               :page-size.sync="params.per_page"
                               :total="totalCount"
                               layout="prev, pager, next, sizes"
                               background
                               @size-change="getDataWithLoading"
                               @current-change="getDataWithLoading"
                />
            </div>
            <create-image :ref="uploadRefName" @success="getDataWithLoading"/>
        </template>
    </card>
</template>

<script>
    import IndexPartial from "../../components/IndexPartial"
    import {mapActions} from "vuex"
    import Photo        from "../../models/Image"
    import CreateImage  from "./create"

    export default {
        name: "ListImages",

        components: {
            CreateImage
        },

        extends: IndexPartial,

        data() {
            return {
                uploadRefName: "create-image",
                showRefName:   "show-image",
                title:         "Images",
                images:        [],
                imagesPerRow:  6,
                viewerOptions: {
                    "button":     true,
                    "navbar":     false,
                    "title":      true,
                    "toolbar":    true,
                    "tooltip":    true,
                    "movable":    true,
                    "zoomable":   true,
                    "rotatable":  false,
                    "scalable":   false,
                    "transition": true,
                    "fullscreen": true,
                    "keyboard":   true,
                    "url":        "data-source"
                },
                sortDirection: true
            }
        },

        computed: {
            viewerImages() {
                return this.images.map(image => {
                    return {
                        thumbnail: this.getThumbnailSrc(image),
                        source:    this.getLargestImageSrc(image)
                    }
                })
            },
            sortByOptions() {
                return this.sortDirection
                       ? [{value: "title", label: "Title"},
                          {value: "created_at", label: "Date uploaded"},]
                       : [{value: "-title", label: "Title"},
                          {value: "-created_at", label: "Date uploaded"},]
            }
        },

        watch: {
            params: {
                handler() {
                    this.getData()
                },
                deep: true
            }
        },

        mounted() {
            if (this.params.sort && this.params.sort[0] === "-") {
                this.$set(this, "sortDirection", false)
            }
        },

        methods: {
            ...mapActions("image", ["getImages", "deleteImage"]),

            getData() {
                this.$router.replace({name: "Images", query: this.params})

                return new Promise((resolve, reject) => {
                    this.getImages({params: this.params})
                        .then(({data}) => {
                            this.$set(this, "images", data.results.map(image => new Photo(image)))
                            this.$set(this, "totalCount", data.count)
                            resolve()
                        })
                        .catch(() => {
                            reject()
                        })
                })
            },

            getDataWithLoading() {
                this.$set(this, "loading", true)
                this.getData()
                    .then(() => {
                        this.$set(this, "loading", false)
                    })
                    .catch(() => {
                        this.$set(this, "loading", false)
                    })
            },

            arrayChunk(array, chunk_size) {
                return array.reduce(
                    (segments, _, index) =>
                        index % chunk_size === 0
                        ? [...segments, array.slice(index, index + chunk_size)]
                        : segments,
                    []
                )
            },

            edit(imageId) {
                this.$router.push({name: "EditImage", params: {imageId}})
            },

            upload() {
                this.$refs[this.uploadRefName].showModal()
            },

            remove(imageId) {
                this.$confirm("Are you sure you want to delete this image?", "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteImage(imageId)
                                  .then(() => {
                                      this.getData()
                                      this.success("Image successfully deleted")
                                  })
                                  .catch(() => {
                                      this.error("There was an error deleting the image")
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("Image not deleted")
                    })
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

            getLargestImageSrc(image) {
                return image.sizes.includes(1920)
                       ? `${image.public_path}/1920.jpg`
                       : `${image.public_path}/original.jpg`
            },

            handleSortDirectionChange(order) {
                const direction = order === false ? "-" : ""
                const prop = this.params.sort ? this.params.sort.replace(/^-|\+/, "") : null
                this.$set(this.params, "sort", prop ? `${direction}${prop}` : null)
            }
        }
    }
</script>

<style lang="scss" scoped>
    .el-row {
        margin-bottom: 20px;

        &:last-child {
            margin-bottom: 0;
        }
    }
</style>