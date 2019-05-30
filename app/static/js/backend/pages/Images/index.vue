<template>
    <card>
        <template v-slot:header>
            <b>{{ title }}</b>
            <div class="card-header-actions">
                <button class="btn btn-sm btn-primary" @click.prevent="upload">
                    Upload new image
                </button>
            </div>
        </template>
        <template v-slot:body>
            <el-row :gutter="20">
                <el-col :span="6" :offset="18">
                    <el-input v-model="params.search"
                              placeholder="Type to search images"
                              clearable
                              @change="searchData"
                    >
                        <el-button slot="append" icon="el-icon-search"/>
                    </el-input>
                </el-col>
            </el-row>
            <viewer :images="viewerImages" :options="viewerOptions">
                <template slot-scope="scope">
                    <el-row v-for="(imageRow, rowIndex) in arrayChunk(images, imagesPerRow)" :key="rowIndex"
                            :gutter="20">
                        <el-col v-for="image in imageRow" :key="image.id" :span="24/imagesPerRow">
                            <el-card :body-style="{ padding: '0', textAlign: 'center' }" class="image-card"
                                     shadow="hover">
                                <img :style="{width: '100%', height: '100%'}"
                                     :src="`${image.public_path}/${thumbnailSize}.jpg`"
                                     :data-source="getLargestImageSrc(image)"
                                     :alt="image.original_filename"
                                />
                                <div style="padding: 14px;">
                                    <span>{{ (image.title || image.original_filename) | truncate(20) }}</span>
                                    <div class="bottom clearfix">
                                        <el-button size="mini" @click="edit(image.id)">Edit</el-button>
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                </template>
            </viewer>
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
            <create-image :ref="uploadRefName" @success="getData"/>
        </template>
    </card>
</template>

<script>
    import IndexPartial from "../../components/IndexPartial"
    import {mapActions} from "vuex"
    import Photo        from "../../models/Image"
    import CreateImage  from "./create"

    export default {
        name: "Images",

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
                thumbnailSize: 280,
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
                }
            }
        },

        computed: {
            viewerImages() {
                return this.images.map(image => {
                    return {
                        thumbnail: `${image.public_path}/${this.thumbnailSize}.jpg`,
                        source:    this.getLargestImageSrc(image)
                    }
                })
            }
        },

        methods: {
            ...mapActions("image", ["getImages"]),

            getData() {
                this.$router.replace({name: "Images", query: this.params})

                this.getImages({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "images", data.results.map(image => new Photo(image)))
                        this.$set(this, "totalCount", data.count)
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

            getLargestImageSrc(image) {
                return image.sizes.includes(1920)
                       ? `${image.public_path}/1920.jpg`
                       : `${image.public_path}/original.jpg`
            },
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