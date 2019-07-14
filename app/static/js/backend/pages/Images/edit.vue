<template>
    <card-form :ref="formRef" :form-ref="formRef" :model="image" :rules="rules" :label-width="labelWidth">
        <template v-slot:header>
            <el-page-header :content="title" @back="goBack"/>
            <div v-if="image.id" class="card-header-actions">
                <el-button class="btn btn-sm btn-danger" @click.prevent="remove">
                    Delete image
                </el-button>
            </div>
        </template>
        <template v-slot:body>
            <el-form-item label="Title" prop="title">
                <el-input v-model="image.title" type="text" maxlength="255" show-word-limit required/>
            </el-form-item>
            <el-row class="image-tags">
                <el-col :span="24">
                    <el-form-item label="Tags">
                        <el-tag v-for="tag in image.tags"
                                :key="tag.id"
                                :closable="true"
                                :disable-transitions="false"
                                @close="handleTagRemove(tag)"
                        >
                            <i class="fal fa-tag"/> {{ tag.name }}
                        </el-tag>
                        <el-input v-if="tagInputVisible"
                                  ref="saveImageTagInput"
                                  v-model="newTagName"
                                  class="input-new-tag"
                                  size="mini"
                                  @change="handleTagConfirm"
                                  @blur="handleTagConfirm"
                        />
                        <el-button v-else class="button-new-tag" size="small" @click="showTagInput">
                            <i class="fal fa-tags"/> Add new tag
                        </el-button>
                    </el-form-item>
                </el-col>
            </el-row>
            <div ref="edit-image" class="edit-image">
                <tui-image-editor v-if="image.id"
                                  :ref="refName"
                                  :include-ui="useDefaultUI"
                                  :options="options"
                                  @objectActivated="handleObjectActivated"
                                  @objectScaled="handleObjectScaled"
                                  @objectMoved="handleObjectMoved"
                                  @redoStackChanged="handleRedoStackChanged"
                                  @undoStackChanged="handleUndoStackChanged"
                />
            </div>
        </template>
        <template v-slot:footer>
            <el-button type="success" @click="submit">
                Update current image
            </el-button>
            <el-button type="primary" @click="create">
                Save as new image
            </el-button>
        </template>
    </card-form>
</template>

<script>
    import {mapActions}          from "vuex"
    import MD5                   from "crypto-js/md5"
    import Photo                 from "../../models/Image"
    import CardForm              from "../../components/CardForm"
    import CreatePartial         from "../../components/CreatePartial"
    import {white as whiteTheme} from "../../components/image_editor/theme"
    import Tag                   from "../../models/Tag"

    export default {
        name: "EditImage",

        components: {
            "tui-image-editor": () => import(/* webpackChunkName: "vue-image-editor" */ "@toast-ui/vue-image-editor").then(({ImageEditor}) => ImageEditor),
            CardForm
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
                formRef:         "image-edit-form",
                refName:         "editor",
                labelWidth:      "80px",
                image:           new Photo(),
                useDefaultUI:    true,
                options:         {
                    includeUI:       {
                        theme:           whiteTheme,
                        loadImage:       {
                            path: null,
                            name: null
                        },
                        initMenu:        "filter",
                        menuBarPosition: "right"
                    },
                    cssMaxWidth:     1024,
                    cssMaxHeight:    1024,
                    usageStatistics: false,
                },
                aspectRatio:     0,
                editorWidth:     0,
                actionStack:     [],
                undo:            0,
                redo:            0,
                tagInputVisible: false,
                newTagName:      "",
                imageDataUrl:    ""
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
            },
            cssMaxWidth() {
                const width = Math.min(this.editorWidth - 248 - 64, 1024)
                return width > 0 ? width : 1024
            },
            imageHeight() {
                return Math.floor(this.cssMaxWidth / this.aspectRatio)
            },
            latestAction() {
                return this.actionStack.length > 0 ? this.actionStack[this.actionStack.length - 1] : null
            }
        },

        watch: {
            cssMaxWidth: {
                handler(current, previous) {
                    this.$set(this.options, "cssMaxWidth", current)
                    if (this.$refs[this.refName] !== undefined) {
                        this.$refs[this.refName].invoke("ui.resizeEditor", {
                            imageSize: {
                                newHeight: Math.floor(current / this.aspectRatio),
                                newWidth:  current
                            }
                        })
                    }
                },
                immediate: true
            },

            aspectRatio(aspectRatio) {
                if (this.$refs[this.refName] !== undefined) {
                    this.$refs[this.refName].invoke("ui.resizeEditor", {
                        imageSize: {
                            newHeight: Math.floor(this.cssMaxWidth / aspectRatio),
                            newWidth:  this.cssMaxWidth
                        }
                    })
                }
            },

            latestAction: {
                handler(latestAction) {
                    if (latestAction.committed && latestAction.action.type === "cropzone") {
                        this.$set(this, "aspectRatio", latestAction.action.width / latestAction.action.height)
                    }
                },
                deep: true
            },

            redo(current, previous) {
                if (current > previous) {
                    let latestAction = this.latestAction
                    if (latestAction) {
                        latestAction.committed = false
                        this.$set(this.actionStack, this.actionStack.findIndex(el => el.action.id === this.latestAction.action.id), latestAction)

                        if (this.undo === 0) {
                            if (latestAction.action.type === "cropzone") {
                                this.$set(this, "aspectRatio", this.image.width / this.image.height)
                            }
                        } else {
                            if (latestAction.action.type === "cropzone") {
                                this.$set(this, "aspectRatio", latestAction.action.width / latestAction.action.height)
                            }
                        }
                    }
                }

                if (current === 0 && this.undo === 0) {
                    this.$set(this, "aspectRatio", this.image.width / this.image.height)
                }
            },

            undo(current, previous) {
                if (current > previous) {
                    let latestAction = this.latestAction
                    if (latestAction) {
                        latestAction.committed = true
                        this.$set(this.actionStack, this.actionStack.findIndex(el => el.action.id === this.latestAction.action.id), latestAction)

                        if (latestAction.action.type === "cropzone") {
                            this.$set(this, "aspectRatio", latestAction.action.width / latestAction.action.height)
                        }
                    }
                }

                if (current === 0 && this.redo === 0) {
                    this.$set(this, "aspectRatio", this.image.width / this.image.height)
                }
            }
        },

        mounted() {
            this.getEditorWidth()
            window.addEventListener("resize", this.getEditorWidth)

            this.getImage(this.imageId)
                .then(({data}) => {
                    this.$set(this, "image", new Photo(data))

                    this.$set(this, "aspectRatio", this.image.width / this.image.height)

                    this.$set(this.options.includeUI, "loadImage", {
                        path: this.path,
                        name: this.title
                    })

                    // wait 500ms before grabbing the initial image data url
                    setTimeout(() => {
                        this.$set(this, "imageDataUrl", MD5(this.getImageData()).toString())
                    }, 500)
                })
        },

        methods: {
            ...mapActions("image", ["getImage", "createImage", "updateImage", "deleteImage"]),

            ...mapActions("tag", ["getTags", "createTag"]),

            handleObjectMoved(props) {
                console.log("object moved")
            },

            handleObjectScaled(props) {
                console.log("object scaled")
            },

            handleObjectActivated(props) {
                this.actionStack.push({action: props, committed: false})
            },

            handleRedoStackChanged(length) {
                this.$set(this, "redo", length)
            },

            handleUndoStackChanged(length) {
                this.$set(this, "undo", length)
            },

            getEditorWidth() {
                this.$set(this, "editorWidth", this.$refs["edit-image"].clientWidth)
            },

            handleTagRemove(tag) {
                if (this.image.tags.length > 0 && this.image.tag_ids.length > 0) {
                    this.image.tags.splice(this.image.tags.findIndex(el => Number(el.id) === Number(tag.id)), 1)
                    this.image.tag_ids.splice(this.image.tag_ids.findIndex(el => Number(el) === Number(tag.id)), 1)
                }
            },

            handleTagConfirm() {
                const name = this.newTagName
                if (name) {
                    const exists = this.image.tags.some(tag => tag.name.toLowerCase() === name.trim().toLowerCase())

                    if (!exists) {
                        this.getTags({params: {name}})
                            .then(({data}) => {
                                if (data.results.length > 0) {
                                    const tag = new Tag(data.results.shift())
                                    this.image.tags.push(tag)
                                    this.image.tag_ids.push(tag.id)
                                } else {
                                    this.createTag({name})
                                        .then(({data}) => {
                                            const tag = new Tag(data)
                                            this.image.tags.push(tag)
                                            this.image.tag_ids.push(tag.id)
                                        })
                                }
                            })
                    } else {
                        this.warning(`A tag with the name ${name} is already associated with this image.`)
                    }
                }
                this.$set(this, "tagInputVisible", false)
                this.$set(this, "newTagName", "")
            },

            showTagInput() {
                this.$set(this, "tagInputVisible", true)
                this.$nextTick(_ => {
                    this.$refs.saveImageTagInput.$refs.input.focus()
                })
            },

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

            getImageData() {
                return this.$refs[this.refName].invoke("toDataURL", {format: "png"})
            },

            submit() {
                const currentImageDataUrl = this.getImageData()
                if (MD5(currentImageDataUrl).toString() !== this.imageDataUrl) {
                    this.$set(this.image, "data_url", currentImageDataUrl)
                }

                this.updateImage(this.image)
                    .then(() => {
                        this.$set(this, "imageDataUrl", MD5(currentImageDataUrl).toString())
                        this.$set(this.image, "data_url", null)
                        this.success("Image successfully updated")
                    })
                    .catch(() => {
                        this.error(`There was an error updating the image: ${this.alert.message}`)
                    })
            },

            create() {
                const currentImageDataUrl = this.getImageData()
                this.$set(this.image, "data_url", currentImageDataUrl)

                if (this.image.data_url) {
                    this.createImage(this.image)
                        .then(({data}) => {
                            this.$set(this, "image", new Photo(data))
                            this.$set(this, "imageDataUrl", MD5(currentImageDataUrl).toString())
                            this.$router.push({name: "EditImage", params: {imageId: this.image.id}})
                            this.$refs[this.refName].invoke("loadImageFromURL", this.path, this.title)

                            this.success("Successfully saved edited image as new image")
                        })
                        .catch((err) => {
                            if (this.alert.message) {
                                this.error(`There was an error creating the image: ${this.alert.message}`)
                            } else {
                                this.error(`There was an error creating the image: ${err}`)
                            }
                        })
                } else {
                    this.error("The image data is invalid!")
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .edit-image {
        width: 100%;
        height: (1024px + 64px);
    }

    .el-form-item__content {
        & > div:first-child {
            width: calc(100% - 80px);
        }
    }
</style>