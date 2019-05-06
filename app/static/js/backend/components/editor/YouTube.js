import {Node}       from "tiptap"
import {mapActions} from "vuex"
import axios        from "axios"
import {
    getHours,
    getMinutes,
    getSeconds,
    setHours,
    setMinutes,
    setSeconds
}                   from "date-fns"

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
                    loading:        false,
                    popoverVisible: false,
                    youTubeId:      null,
                    aspectRatio:    16 / 9,
                    rules:          {
                        url:    [
                            {validator: this.validateYouTubeUrl, trigger: "blur"},
                        ],
                        width:  [
                            {validator: this.validateWidth, trigger: "blur"}
                        ],
                        height: [
                            {validator: this.validateHeight, trigger: "blur"}
                        ]
                    }
                }
            },
            created() {
                this.$set(this, "youTubeId", getYouTubeId(this.node.attrs.src))
            },
            computed: {
                src() {
                    return this.node.attrs.src
                },
                start: {
                    get() {
                        return setSeconds(setMinutes(setHours(new Date(), 0), 0), Number(this.node.attrs.start))
                    },
                    set(start) {
                        this.updateAttrs(
                            {
                                start: getHours(start) * 3600 + getMinutes(start) * 60 + getSeconds(start)
                            }
                        )
                    }
                },
                width() {
                    return this.node.attrs.width
                },
                height() {
                    return this.node.attrs.height
                },
                url:   {
                    get() {
                        return this.node.attrs.src
                    },
                    set(src) {
                        this.$set(this, "youTubeId", getYouTubeId(src))
                        this.updateAttrs(
                            {
                                src: this.youTubeId ? `https://www.youtube.com/embed/${this.youTubeId}` : src
                            }
                        )
                    },
                },
                imageSrc() {
                    return `https://img.youtube.com/vi/${this.youTubeId}/0.jpg`
                },
                formRef() {
                    return `youtube_${this.node.attrs["src"]}`
                },
                form() {
                    return {
                        url:    this.url,
                        start:  this.start,
                        width:  this.width,
                        height: this.height
                    }
                }
            },
            methods:  {
                ...mapActions("alert", ["error"]),
                showPopover() {
                    this.$set(this, "popoverVisible", true)
                },
                hidePopover() {
                    this.$set(this, "popoverVisible", false)
                    this.$set(this, "loading", false)
                },
                changeWidth(width) {
                    this.updateAttrs({width})
                    this.updateAttrs({height: Math.round(width / this.aspectRatio)})
                },

                changeHeight(height) {
                    this.updateAttrs({height})
                    this.updateAttrs({width: Math.round(height * this.aspectRatio)})
                },

                changeStart(start) {
                    if (start === null) {
                        this.$set(this, "start", setSeconds(setMinutes(setHours(new Date(), 0), 0), 0))
                        this.$set(this.form, "start", null)
                    }
                },

                validateYouTubeUrl(rule, value, callback) {
                    if (!value) {
                        callback(new Error("Please input a YouTube URL"))
                    } else if (!getYouTubeId(value)) {
                        callback(new Error("The YouTube URL is invalid."))
                    } else {
                        callback()
                    }
                },

                validateWidth(rule, value, callback) {
                    if (Number(value) <= 0) {
                        callback(new Error("Please input a YouTube video width"))
                    } else if (Number(value) < 426 || Number(value) > 3840) {
                        callback(new Error("Please input a YouTube video width between 426 and 3840"))
                    } else {
                        callback()
                    }
                },

                validateHeight(rule, value, callback) {
                    if (Number(value) <= 0) {
                        callback(new Error("Please input a YouTube video height"))
                    } else if (Number(value) < 240 || Number(value) > 2160) {
                        callback(new Error("Please input a YouTube video height between 240 and 2160"))
                    } else {
                        callback()
                    }
                },
            },
            template: `
                <span class="youtube">
                    <el-popover placement="top"
                                width="600"
                                trigger="click"
                                title="YouTube video details"
                                :disabled="!editable"
                                @show="showPopover"
                                @hide="hidePopover">
                        <el-form v-if="editable" :model="form" :ref="formRef" :rules="rules" label-placement="right" label-width="120px">
                            <el-form-item label="YouTube URL" prop="url">
                                <el-input type="url" v-model="url" style="width: calc(100% - 120px)"/>
                            </el-form-item>
                            <el-form-item label="Start at" prop="start">
                                <el-time-picker v-model="start"
                                                :picker-options="{format: 'HH:mm:ss'}"
                                                placeholder="Start at"
                                                :disabled="!youTubeId"
                                                @change="changeStart">
                                </el-time-picker>
                            </el-form-item>
                            <el-form-item prop="width" label="Width">
                                <el-input-number :value="width"
                                                 :min="426"
                                                 :max="3840"
                                                 :disabled="!youTubeId"
                                                 required
                                                 @change="changeWidth"
                                />
                            </el-form-item>
                            <el-form-item prop="height" label="Height">
                                <el-input-number :value="height"
                                                 :min="240"
                                                 :max="2160"
                                                 :disabled="!youTubeId"
                                                 required
                                                 @change="changeHeight"
                                />
                            </el-form-item>
                        </el-form>
                        <figure slot="reference" :style="{width: width + 'px', position: 'relative'}" title="Click to edit">
                            <img :src="imageSrc" :alt="url" :title="url" :style="{width: width + 'px', height: height + 'px'}">
                            <figcaption><i class="fab fa-youtube"/></figcaption>
                        </figure>
                    </el-popover>
                </span>
            `,
        }
    }
}