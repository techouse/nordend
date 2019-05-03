<template>
    <modal v-if="show" :class="{show: show}" modal-class="modal-lg" @close="closeModal">
        <template v-slot:title>
            Select image size image
        </template>
        <template v-slot:body>
            <el-row :gutter="12">
                <el-col v-for="size in sizes" :key="size.size" :span="8">
                    <el-card :body-style="{padding: '0px'}" shadow="hover">
                        <el-image :style="{width: '100%', height: '100%'}"
                                  :src="`${photo.public_path}/220.jpg`"
                                  fit="cover"
                        />
                        <div style="padding: 14px;">
                            <span>Image width: {{ size.size }}px</span>
                            <div class="bottom clearfix">
                                <el-button type="primary" size="small" class="button" @click="useImageSize(size)">
                                    Use
                                </el-button>
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </template>
    </modal>
</template>

<script>
    import {mapActions} from "vuex"
    import Modal        from "../Modal"
    import Photo        from "../../models/Image"

    export default {
        name: "EditImage",

        components: {
            "modal": Modal
        },

        data() {
            return {
                command: null,
                show:    false,
                photo:   new Photo()
            }
        },

        computed: {
            sizes() {
                if (this.photo.sizes.length && this.photo.width) {
                    return this.photo.sizes
                               .map(size => Number(size))
                               .filter(size => size >= 440) // Minimum size for srcset
                               .sort((a, b) => a - b)
                               .map(size => {
                                   return {url: `${this.photo.public_path}/${size}.jpg`, size: size}
                               })
                               .concat([{url: `${this.photo.public_path}/original.jpg`, size: this.photo.width}])
                }

                return []
            }
        },

        methods: {
            ...mapActions("alert", ["error"]),
            ...mapActions("image", ["getImage"]),

            showModal(command, pictureId) {
                this.$set(this, "command", command)
                this.getImage(pictureId)
                    .then(({data}) => {
                        this.$set(this, "photo", new Photo(data))
                        this.$set(this, "show", true)
                    })
                    .catch(() => this.error("Error loading image"))
            },

            closeModal() {
                this.$set(this, "show", false)
            },

            useImageSize(size) {
                const data = {
                    command: this.command,
                    data:    {
                        src:       size.url,
                        alt:       this.photo.original_title,
                        title:     this.photo.original_title,
                        "data-id": this.photo.id,
                        sources:   this.photo.sizes
                                       .map(size => Number(size))
                                       .filter(size => size >= 440) // Minimum size for srcset
                                       .sort((a, b) => a - b)
                                       .map(size => {
                                           return {
                                               media:  Photo.getMediaBreakPoint(size),
                                               srcset: `${this.photo.public_path}/${size}.jpg`
                                           }
                                       })
                    }
                }

                this.$emit("onConfirm", data)
                this.closeModal()
            }
        }
    }
</script>

<style scoped>

</style>