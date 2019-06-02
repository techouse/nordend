<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <div class="card">
                    <div class="card-header">
                        <b>Edit image</b> <i>{{ title }}</i>
                        <div v-if="image.id" class="card-header-actions">
                            <button class="btn btn-sm btn-danger" @click.prevent="remove">
                                Delete image
                            </button>
                        </div>
                    </div>
                    <div class="card-body edit-image">
                        <tui-image-editor v-if="image.id"
                                          :ref="refName"
                                          :include-ui="useDefaultUI"
                                          :options="options"
                        />
                    </div>
                    <div class="card-footer">
                        <el-button type="success" @click="submit">
                            Save
                        </el-button>
                        <el-button type="danger" @click="$router.push({name: 'Images'})">
                            Cancel
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {ImageEditor}         from "@toast-ui/vue-image-editor"
    import {mapActions}          from "vuex"
    import Photo                 from "../../models/Image"
    import CreatePartial         from "../../components/CreatePartial"
    import {white as whiteTheme} from "../../components/image_editor/theme"

    export default {
        name: "EditImage",

        components: {
            "tui-image-editor": ImageEditor
        },

        extends: CreatePartial,

        props: {
            imageId: {
                type:     [String, Number],
                required: true
            }
        },

        data() {
            return {
                refName:      "editor",
                image:        new Photo(),
                useDefaultUI: true,
                options:      {
                    includeUI:       {
                        theme:           whiteTheme,
                        loadImage:       {
                            path: null,
                            name: null
                        },
                        initMenu:        "filter",
                        menuBarPosition: "right"
                    },
                    cssMaxWidth:     700,
                    cssMaxHeight:    500,
                    usageStatistics: false,
                }
            }
        },

        computed: {
            title() {
                /**
                 * Since not all images have a title
                 */
                return this.image.title || this.image.original_filename
            },
            path() {
                /**
                 * In order to prevent the browser from crashing and the Universe unraveling before our very eyes try
                 * and pick a sensible maximum image size. If the image is larger than 1920px pick the 1920px version
                 * otherwise pick the original.
                 */
                return this.image.sizes.includes(1920)
                       ? `${this.image.public_path}/1920.jpg`
                       : `${this.image.public_path}/original.jpg`
            }
        },

        mounted() {
            this.getImage(this.imageId)
                .then(({data}) => {
                    this.$set(this, "image", new Photo(data))

                    this.$set(this.options.includeUI, "loadImage", {
                        path: this.path,
                        name: this.title
                    })
                })
        },

        methods: {
            ...mapActions("image", ["getImage", "updateImage", "deleteImage"]),

            remove() {
                this.$confirm(`Are you sure you want to delete ${this.title}?`, "Warning", {
                        confirmButtonText: "Yes",
                        cancelButtonText:  "No",
                        type:              "warning"
                    })
                    .then(() => {
                              this.deleteImage(this.image.id)
                                  .then(() => {
                                      this.$router.push({name: "Images"})
                                      this.success(`Image ${this.title} successfully deleted`)
                                  })
                                  .catch(() => {
                                      this.error(`There was an error deleting the image: ${this.alert.message}`)
                                  })
                          }
                    )
                    .catch(() => {
                        this.info("Image not deleted")
                    })
            },

            submit() {
                this.$set(this.image, "data_url", this.$refs[this.refName].invoke("toDataURL", {format: "png"}))

                if (this.image.data_url) {
                    this.updateImage(this.image)
                        .then(() => {
                            this.success("Image successfully updated")
                        })
                        .catch(() => {
                            this.error(`There was an error updating the image: ${this.alert.message}`)
                        })
                } else {
                    this.error("The image data is invalid!")
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .card-body {
        width: 100%;
        height: 800px;
    }
</style>