<template>
    <modal v-if="show" :class="{show: show}" modal-class="modal-lg" @close="closeModal">
        <template v-slot:title>
            Select image size image
        </template>
        <template v-slot:body>
            <el-row :gutter="12">
                <el-col v-for="(size, index) in sizes" :key="size.size" :span="8">
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
                    return this.photo.sizes.sort()
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

            showModal(command, photoId) {
                this.$set(this, "command", command)
                this.getImage(photoId)
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
                console.log(size)

                const data = {
                    command: this.command,
                    data:    {
                        src:       size.url,
                        alt:       this.photo.original_title,
                        title:     this.photo.original_title,
                        "data-id": this.photo.id,
                        // srcset:    this.photo.sizes.sort()
                        //                .map(size => `${this.photo.public_path}/${size}.jpg ${size}w`)
                        //                .concat([`${this.photo.public_path}/original.jpg ${this.photo.width}w`])
                        //                .join(", "),
                        // sizes:     this.photo.sizes
                        //                .map(size => {
                        //                    for (let bp of Object.values(this.mediaBreakPoints)) {
                        //                        if (bp.fits(size)) {
                        //                            return `${bp.mediaQuery} ${size}px`
                        //                        }
                        //                    }
                        //                })
                        //                .join(", ")
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