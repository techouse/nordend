import {Node}       from "tiptap"
import {mapActions} from "vuex"

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
                this.$set(this, "youTubeId", this.parseYouTubeUrl(this.node.attrs.src))
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
                        this.$set(this, "youTubeId", this.parseYouTubeUrl(src))
                        if (this.youTubeId) {
                            this.updateAttrs(
                                {
                                    src: this.node.attrs.start ? `https://www.youtube.com/embed/${this.youTubeId}?start=${this.node.attrs.start}`
                                                               : `https://www.youtube.com/embed/${this.youTubeId}`
                                }
                            )
                        }
                    },
                }
            },
            methods:  {
                ...mapActions("alert", ["error"]),

                parseYouTubeUrl(url) {
                    const re = /^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(\?\S*)?$/
                    const matches = url.match(re)
                    return matches ? matches[1] : false
                },
            },
            template: `
                <div class="iframe">
                    <iframe :src="src" 
                            :data-start="start"
                            :width="width"
                            :height="height"
                            class="youtube" 
                            frameborder="0" 
                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen />
                    <input class="iframe__input" @paste.stop type="url" v-model="url" v-if="editable" required />
                </div>
            `,
        }
    }
}