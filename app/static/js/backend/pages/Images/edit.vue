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
                    <div class="card-body">
                        <tui-image-editor v-if="image.id"
                                          ref="editor"
                                          :include-ui="useDefaultUI"
                                          :options="options"
                        />
                    </div>
                    <div class="card-footer">
                        <el-button type="success" @click="submit">
                            Submit
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
                return this.image.title || this.image.original_filename
            },
        },

        mounted() {
            this.getImage(this.imageId)
                .then(({data}) => {
                    this.$set(this, "image", new Photo(data))

                    this.$set(this.options.includeUI, "loadImage", {
                        path: `${this.image.public_path}/original.jpg`,
                        name: this.title
                    })
                })
        },

        methods: {
            ...mapActions("image", ["getImage"]),

            remove() {

            },

            submit() {

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