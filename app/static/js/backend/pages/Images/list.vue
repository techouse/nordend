<template>
    <card>
        <template v-slot:header>
            <el-page-header class="no-back" :content="title"/>
            <div class="card-header-actions">
                <template v-if="images.length">
                    <button class="btn btn-pill btn-sm"
                            :class="selectMode ? 'btn-outline-danger' : 'btn-outline-primary'"
                            @click.prevent="toggleSelect"
                    >
                        <template v-if="selectMode">
                            <i class="fal fa-times-square"/> Cancel select
                        </template>
                        <template v-else>
                            <i class="fal fa-check-double"/> Toggle select
                        </template>
                    </button>
                    <button v-if="selectMode" class="btn btn-pill btn-sm btn-outline-info"
                            @click.prevent="selectAllImages"
                    >
                        <i class="fal fa-object-group"/> Select all
                    </button>
                    <el-dropdown v-if="multipleSelection.length" @command="handleBulkCommand">
                        <button class="btn btn-sm btn-outline-secondary">
                            Bulk actions <i class="el-icon-arrow-down el-icon--right"/>
                        </button>
                        <el-dropdown-menu slot="dropdown" size="mini">
                            <el-dropdown-item icon="fal fa-trash-alt" :command="bulkRemove">
                                Delete selection
                            </el-dropdown-item>
                            <el-dropdown-item icon="fal fa-snowplow" :command="clearSelection" divided>
                                Clear selection
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </template>
                <button class="btn btn-sm btn-success" @click.prevent="upload">
                    <i class="far fa-images"/> Upload new images
                </button>
            </div>
        </template>
        <template v-slot:body>
            <el-row v-if="images.length" :gutter="20">
                <el-col :span="9" :style="{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}">
                    <el-menu :default-active="params.sort" mode="horizontal" @select="handleSortSelect">
                        <el-menu-item v-for="item in sortByOptions" :key="item.value" :index="item.value">
                            {{ item.label }}
                            <i class="fal" :class="sortDirection ? 'fa-chevron-up' : 'fa-chevron-down'"/>
                        </el-menu-item>
                    </el-menu>
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
                                :gutter="20"
                        >
                            <el-col v-for="image in imageRow" :key="image.id" :span="24/imagesPerRow">
                                <el-card :body-style="{ padding: '0', textAlign: 'center', position: 'relative' }"
                                         class="image-card"
                                         shadow="hover"
                                >
                                    <img :src="getThumbnailSrc(image)"
                                         :data-source="getLargestImageSrc(image)"
                                         :alt="image.original_filename"
                                         class="image-viewer-thumbnail"
                                    >
                                    <template v-if="selectMode">
                                        <el-tooltip class="item" effect="dark"
                                                    :content="imageSelected(image) ? 'Deselect' : 'Select'"
                                                    placement="top"
                                                    :style="{position: 'absolute', left: '2px', top: '2px'}"
                                        >
                                            <el-button v-if="imageSelected(image)" type="primary" size="mini"
                                                       icon="fas fa-check" circle @click="deselectImage(image)"
                                            />
                                            <el-button v-else type="default" size="mini" icon="el-icon-minus"
                                                       circle @click="selectImage(image)"
                                            />
                                        </el-tooltip>
                                    </template>
                                    <div style="padding: 14px;">
                                        <template v-if="imageTitle(image).length > 20">
                                            <el-tooltip class="item" effect="dark" :content="imageTitle(image)"
                                                        placement="top"
                                            >
                                                <span>{{ imageTitle(image) | truncateMiddle(20) }}</span>
                                            </el-tooltip>
                                        </template>
                                        <template v-else>
                                            <span>{{ imageTitle(image) }}</span>
                                        </template>
                                        <div class="bottom clearfix">
                                            <el-button-group>
                                                <el-tooltip class="item" effect="dark" content="Edit in image editor"
                                                            placement="bottom"
                                                >
                                                    <el-button size="mini" @click="edit(image.id)">
                                                        <i class="fas fa-paint-brush"/>
                                                    </el-button>
                                                </el-tooltip>
                                                <el-tooltip class="item" effect="dark" content="Delete"
                                                            placement="bottom"
                                                >
                                                    <el-button type="danger" size="mini" icon="el-icon-delete-solid"
                                                               @click="remove(image)"
                                                    />
                                                </el-tooltip>
                                            </el-button-group>
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
                               @size-change="updateData"
                               @current-change="updateData"
                />
            </div>
            <create-image :ref="uploadRefName" @success="updateData"/>
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
                    "button":     false,
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
                sortDirection: true,
                selectMode:    false
            }
        },

        computed: {
            viewerImages() {
                return this.images.map(image => ({
                    thumbnail: this.getThumbnailSrc(image),
                    source:    this.getLargestImageSrc(image)
                }))
            },
            sortByOptions() {
                return [
                    {value: "created_at", label: "Date uploaded"},
                    {value: "original_filename", label: "Title"},
                ].map(option => ({
                    label: option.label,
                    value: this.sortDirection ? option.value.replace(/^-/, "") : `-${option.value}`
                }))
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

            if (!this.params.sort) {
                this.$set(this.params, "sort", "-created_at")
                this.$set(this, "sortDirection", false)
            }
        },

        methods: {
            ...mapActions("image", ["getImages", "deleteImage", "deleteImages"]),

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

            bulkRemove() {
                this._bulkRemove(this.deleteImages, "image")
            },

            remove(image) {
                this._remove(this.deleteImage, image, image.title || image.original_filename)
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

            handleSortSelect(key, keyPath) {
                console.log(key)
                const currentSort = this.params.sort
                this.$set(this.params, "sort", key)
                if (key.replace(/^-/, "") === currentSort.replace(/^-/, "")) {
                    this.$set(this, "sortDirection", currentSort[0] === "-")
                    this.handleSortDirectionChange(this.sortDirection)
                }
            },

            handleSortDirectionChange(order) {
                const direction = order === false ? "-" : ""
                const prop = this.params.sort ? this.params.sort.replace(/^-|\+/, "") : null
                this.$set(this.params, "sort", prop ? `${direction}${prop}` : null)
            },

            toggleSelect() {
                this.$set(this, "selectMode", !this.selectMode)

                if (!this.selectMode && this.multipleSelection.length > 0) {
                    this.clearSelection()
                }
            },

            clearSelection() {
                this.$set(this, "multipleSelection", [])
            },

            selectImage(image) {
                if (!this.imageSelected(image)) {
                    this.multipleSelection.push(image)
                }
            },

            selectAllImages() {
                this.images
                    .filter(img => this.multipleSelection.findIndex(el => el.id !== img.id))
                    .forEach(img => {
                        this.multipleSelection.push(img)
                    })
            },

            deselectImage(image) {
                if (this.imageSelected(image)) {
                    this.multipleSelection.splice(this.multipleSelection.findIndex(img => img.id === image.id), 1)
                }
            },

            imageSelected(image) {
                return this.multipleSelection.find(img => img.id === image.id)
            },

            imageTitle(image) {
                return image.title || image.original_filename || ""
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