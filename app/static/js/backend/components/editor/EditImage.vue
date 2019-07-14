<template>
    <modal :class="{show: image}" modal-class="modal-xxl" @close="closeModal">
        <template v-slot:title>
            Edit image <i>{{ title }}</i>
        </template>
        <template v-slot:body>
            <div class="edit-image-within-editor edit-image">
                <tui-image-editor v-if="image.id"
                                  :ref="refName"
                                  :include-ui="useDefaultUI"
                                  :options="options"
                />
            </div>
        </template>
        <template v-slot:footer>
            <button class="btn btn-danger" @click.prevent="closeModal">
                Cancel
            </button>
            <button class="btn btn-success" @click.prevent="submit">
                Save
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions}          from "vuex"
    import Photo                 from "../../models/Image"
    import Modal                 from "../Modal"
    import {white as whiteTheme} from "../../components/image_editor/theme"

    export default {
        name: "EditImageWithinEditor",

        components: {
            "modal":            Modal,
            "tui-image-editor": () => import(/* webpackChunkName: "vue-image-editor" */ "@toast-ui/vue-image-editor").then(({ImageEditor}) => ImageEditor),
        },

        props: {
            image: {
                required: true
            }
        },

        data() {
            return {
                refName:      "editor",
                show:         false,
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
                    cssMaxWidth:     1024,
                    cssMaxHeight:    1024,
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

        created() {
            this.$set(this.options.includeUI, "loadImage", {
                path: this.path,
                name: this.title
            })
        },

        methods: {
            ...mapActions("alert", ["error", "success"]),

            ...mapActions("image", ["getImage", "updateImage", "deleteImage"]),

            ...mapActions("postImage", {
                hideImageEditor:     "hideEditor",
                emitFinishedEditing: "storeEditedImage"
            }),

            showModal() {
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
                this.hideImageEditor()
            },

            submit() {
                this.$set(this.image, "data_url", this.$refs[this.refName].invoke("toDataURL", {format: "png"}))

                if (this.image.data_url) {
                    this.updateImage(this.image)
                        .then(({data}) => {
                            this.emitFinishedEditing(new Photo(data))
                            this.success("Image successfully updated")
                            this.closeModal()
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
    .edit-image-within-editor {
        width: 100%;
        height: 800px;
    }
</style>