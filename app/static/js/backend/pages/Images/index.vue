<template>
    <card>
        <template v-slot:header>
            <b>{{ title }}</b>
        </template>
        <template v-slot:body>
            <el-row v-for="(imageRow, rowIndex) in arrayChunk(images, imagesPerRow)" :key="rowIndex" :gutter="20">
                <el-col v-for="image in imageRow" :key="image.id" :span="24/imagesPerRow">
                    <el-card :body-style="{ padding: '0', textAlign: 'center' }">
                        <el-image :style="{width: '100%', height: '100%'}"
                                  :src="`${image.public_path}/${thumbnailSize}.jpg`"
                                  fit="cover">
                            <div slot="error" class="image-slot">
                                <i class="el-icon-picture-outline"></i>
                            </div>
                        </el-image>
                        <div style="padding: 14px;">
                            <span>{{ image.title || image.original_filename }}</span>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </template>
    </card>
</template>

<script>
    import IndexPartial from "../../components/IndexPartial"
    import {mapActions} from "vuex"
    // alias Image to Picture in order not to interfere with JavaScript's native Image object
    import Picture      from "../../models/Image"

    export default {
        name: "Images",

        extends: IndexPartial,

        data() {
            return {
                title:         "Images",
                images:        [],
                imagesPerRow:  4,
                thumbnailSize: 280
            }
        },

        methods: {
            ...mapActions("image", ["getImages"]),

            getData() {
                this.$router.replace({name: "Images", query: this.params})

                this.getImages({params: this.params})
                    .then(({data}) => {
                        this.$set(this, "images", data.results.map(image => new Picture(image)))
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