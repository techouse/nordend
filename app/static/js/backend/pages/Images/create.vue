<template>
    <modal v-if="show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            Upload image
        </template>
        <template v-slot:body>
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
                    <i class="el-icon-upload" />
                    <div class="el-upload__text">
                        Drop image file here or <em>click to upload</em>
                    </div>
                    <div slot="tip" class="el-upload__tip">
                        jpg/png/gif/bmp file with a size less than 2MB
                    </div>
                </div>
            </el-upload>
        </template>
        <template v-slot:footer>
            <button class="btn btn-danger" @click.prevent="closeModal">
                Close
            </button>
        </template>
    </modal>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import Modal                    from "../../components/Modal"
    import Photo                    from "../../models/Image"

    export default {
        name: "CreateImage",

        components: {
            "modal": Modal
        },

        data() {
            return {
                loading:         false,
                photo:           new Photo(),
                imageUrl:        "",
                previewImageUrl: "",
                show:            false,
                uploadHeaders:   {}
            }
        },

        computed: {
            ...mapGetters("auth", ["token"]),
        },

        methods: {
            ...mapActions("alert", ["error", "success"]),

            findClosest(x, arr) {
                const indexArr = arr.map(k => Math.abs(k - x))
                const min = Math.min.apply(Math, indexArr)
                return arr[indexArr.indexOf(min)]
            },

            showModal() {
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
                this.$set(this, "imageUrl", "")
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

                this.success(`Image ${this.photo.original_filename} uploaded successfully!`)
                this.$emit("success", true)

                this.closeModal()
            },

            beforeImageUpload(file) {
                this.$set(this, "loading", true)
                this.$set(this.uploadHeaders, "Authorization", `Bearer ${this.token}`)

                if (!["image/jpeg", "image/png", "image/gif", "image/bmp"].includes(file.type)) {
                    this.error("Photo must be of type JPG, PNG, GIF or BMP.")
                    this.$set(this, "loading", false)
                    return false
                }

                if (file.size / 1024 / 1024 > 2) {
                    this.error("Photo can not exceed 2 MB in size.")
                    this.$set(this, "loading", false)
                    return false
                }

                return true
            },
        }
    }
</script>