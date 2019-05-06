import {Node}       from "tiptap"
import {mapActions} from "vuex"
import axios        from "axios"

export function getYouTubeId(url) {
    const re = /^(https?:\/\/)?((www\.)?(youtube(-nocookie)?|youtube.googleapis)\.com.*(v\/|v=|vi=|vi\/|e\/|embed\/|user\/.*\/u\/\d+\/)|youtu\.be\/)([_0-9a-z-]+)/i
    const matches = url.match(re)
    return matches ? matches[7] : false
}

export function getYouTubeInfo(id) {
    return new Promise((resolve, reject) => {
        const youTubeInfo = data => data

        axios.get("https://noembed.com/embed", {
                 params: {
                     format:   "json",
                     url:      `http://www.youtube.com/watch?v=${id}`,
                     callback: "youTubeInfo"
                 }
             })
             .then(({data}) => resolve(eval(data)))
             .catch(error => reject(error))
    })
}

export default class YouTube extends Node {
    get name() {
        return "youtube"
    }

    get schema() {
        return {
            attrs:      {
                src:    {
                    default: null
                },
                start:  {
                    default: 0
                },
                width:  {
                    default: 640
                },
                height: {
                    default: 360
                }
            },
            group:      "block",
            selectable: false,
            parseDOM:   [
                {
                    tag: "iframe.youtube",
                    getAttrs(dom) {
                        return {
                            src:    dom.getAttribute("src"),
                            start:  Number(dom.dataset["start"]),
                            width:  Number(dom.getAttribute("width")),
                            height: Number(dom.getAttribute("height"))
                        }
                    }
                }
            ],
            toDOM(node) {
                return [
                    "iframe",
                    {
                        class:           "youtube",
                        src:             node.attrs.start ? `${node.attrs.src}?start=${node.attrs.start}`
                                                          : node.attrs.src,
                        "data-start":    node.attrs.start,
                        width:           node.attrs.width,
                        height:          node.attrs.height,
                        frameborder:     0,
                        allowfullscreen: "true",
                        allow:           "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                        // You can set the width and height here also
                    }
                ]
            }
        }
    }

    commands({type}) {
        return attrs => (state, dispatch) => {
            const {selection} = state
            const position = selection.$cursor ? selection.$cursor.pos : selection.$to.pos
            const node = type.create(attrs)
            const transaction = state.tr.insert(position, node)
            dispatch(transaction)
        }
    }

    get view() {
        return {
            props:    ["node", "updateAttrs", "editable"],
            data() {
                return {
                    youTubeId: null
                }
            },
            created() {
                this.$set(this, "youTubeId", getYouTubeId(this.node.attrs.src))
            },
            computed: {
                src() {
                    return this.node.attrs.src
                },
                start() {
                    return this.node.attrs.start
                },
                width() {
                    return this.node.attrs.width
                },
                height() {
                    return this.node.attrs.height
                },
                url: {
                    get() {
                        return this.node.attrs.start ? `https://www.youtube.com/watch?v=${this.youTubeId}&t=${this.node.attrs.start}`
                                                     : `https://www.youtube.com/watch?v=${this.youTubeId}`
                    },
                    set(src) {
                        this.$set(this, "youTubeId", getYouTubeId(src))
                        if (this.youTubeId) {
                            this.updateAttrs(
                                {
                                    src: this.node.attrs.start ? `https://www.youtube.com/embed/${this.youTubeId}?start=${this.node.attrs.start}`
                                                               : `https://www.youtube.com/embed/${this.youTubeId}`
                                }
                            )
                        }
                    },
                },
                imageSrc() {
                    return `https://img.youtube.com/vi/${this.youTubeId}/0.jpg`
                }
            },
            methods:  {
                ...mapActions("alert", ["error"]),
            },
            template: `
                <el-card :body-style="{ padding: 0 }" :style="{width: width + 'px'}">
                    <el-image :src="imageSrc" :style="{width: width + 'px', height: height + 'px'}" :alt="src" fit="cover">
                        <div slot="placeholder" class="image-slot">
                            Loading<span class="dot">...</span>
                        </div>
                        <div slot="error" class="image-slot">
                            <i class="el-icon-picture-outline"></i>
                        </div>
                    </el-image>
                    <div style="padding: 14px;">
                        <input class="iframe__input" @paste.stop type="url" v-model="url" v-if="editable" required />
                    </div>
                </el-card>
            `,
        }
    }
}