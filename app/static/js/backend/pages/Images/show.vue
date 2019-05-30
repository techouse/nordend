<template>
    <modal v-if="image && show" :class="{show: show}" @close="closeModal">
        <template v-slot:title>
            {{ title | truncate(30) }}
        </template>
        <template v-slot:body>
            <el-image :src="src" lazy>
                <div slot="error" class="image-slot">
                    <i class="el-icon-picture-outline"></i>
                </div>
            </el-image>
        </template>
    </modal>
</template>

<script>
    import Modal from "../../components/Modal"

    export default {
        name: "ShowImage",

        components: {
            "modal": Modal
        },

        props: {
            image: {
                default: null
            }
        },

        data() {
            return {
                show: false
            }
        },

        computed: {
            src() {
                /**
                 * In order to prevent the browser from crashing and the Universe unraveling before our very eyes try
                 * and pick a sensible maximum image size. If the image is larger than 1920px pick the 1920px version
                 * otherwise pick the original.
                 */
                return this.image.sizes.includes(1920)
                       ? `${this.image.public_path}/1920.jpg`
                       : `${this.image.public_path}/original.jpg`
            },
            title() {
                return this.image.title || this.image.original_filename
            }
        },

        methods: {
            showModal() {
                this.$set(this, "show", true)
            },

            closeModal() {
                this.$set(this, "show", false)
            },
        }
    }
</script>