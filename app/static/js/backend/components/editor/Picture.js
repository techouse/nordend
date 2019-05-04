import {Image}      from "tiptap-extensions"
import {mapActions} from "vuex"
import Photo        from "../../models/Image"

export default class Picture extends Image {
    get name() {
        return "picture"
    }

    get schema() {
        return {
            inline:     true,
            attrs:      {
                src:       {
                    default: null
                },
                alt:       {
                    default: null,
                },
                title:     {
                    default: null,
                },
                "data-id": {
                    default: null
                },
                sources:   {
                    default: []
                },
                href:      {
                    default: null
                }
            },
            group:      "inline",
            selectable: true,
            draggable:  true,
            parseDOM:   [
                {
                    tag: "span.picture",
                    getAttrs(dom) {
                        return {
                            "data-id": dom.getElementsByTagName("picture")[0].dataset["id"],
                            src:       dom.getElementsByTagName("img")[0].getAttribute("src"),
                            title:     dom.getElementsByTagName("img")[0].getAttribute("title"),
                            alt:       dom.getElementsByTagName("img")[0].getAttribute("alt"),
                            sources:   [...dom.getElementsByTagName("source")].map(source => {
                                return {
                                    media:       source.getAttribute("media"),
                                    srcset:      source.getAttribute("srcset"),
                                    "data-size": source.dataset["size"]
                                }
                            }),
                            href:      dom.getElementsByTagName("a").length
                                       ? dom.getElementsByTagName("a")[0].getAttribute("href")
                                       : null
                        }
                    },
                },
            ],
            toDOM(node) {
                const wrapper = [
                    "span",
                    {class: "picture"}
                ]

                const anchor = [
                    "a",
                    {
                        href: node.attrs.href,
                        rel:  "noopener noreferrer nofollow"
                    }
                ]

                const picture = [
                    "picture",
                    {
                        "data-id": node.attrs["data-id"],
                    },
                    ...node.attrs.sources.map(source => ["source", source]),
                    [
                        "img",
                        {
                            src:   node.attrs.src,
                            title: node.attrs.title,
                            alt:   node.attrs.alt
                        }
                    ]
                ]

                return node.attrs.href ? [...wrapper, [...anchor, picture]]
                                       : [...wrapper, picture]
            }
        }
    }

    get view() {
        return {
            props:    ["node", "updateAttrs", "editable"],
            data() {
                return {
                    popoverVisible: false,
                    photo:          new Photo()
                }
            },
            computed: {
                dataId() {
                    return this.node.attrs["data-id"]
                },
                src:     {
                    get() {
                        return this.node.attrs.src
                    },
                    set(src) {
                        this.updateAttrs({src})
                    }
                },
                title:   {
                    get() {
                        return this.node.attrs.title
                    },
                    set(title) {
                        this.updateAttrs({title})
                    }
                },
                alt:     {
                    get() {
                        return this.node.attrs.alt
                    },
                    set(alt) {
                        this.updateAttrs({alt})
                    }
                },
                href:    {
                    get() {
                        return this.node.attrs.href
                    },
                    set(href) {
                        this.updateAttrs({href})
                    }
                },
                sources: {
                    get() {
                        return this.node.attrs.sources.map(source => Number(source["data-size"]))
                    },
                    set(sources) {
                        this.updateAttrs({
                                             sources: sources.map(size => Number(size))
                                                             .filter(size => size >= 440) // Minimum size for srcset
                                                             .sort((a, b) => a - b)
                                                             .map(size => {
                                                                 return {
                                                                     media:       Photo.getMediaBreakPoint(size),
                                                                     srcset:      `${this.photo.public_path}/${size}.jpg`,
                                                                     "data-size": size
                                                                 }
                                                             })
                                         })
                    }
                },
                formRef() {
                    return `picture_${this.node.attrs["data-id"] || this.node.attrs["src"]}`
                }
            },
            watch:    {
                popoverVisible(visible) {
                    if (visible && !this.photo.id) {
                        this.getImage(this.dataId)
                            .then(({data}) => this.$set(this, "photo", new Photo(data)))
                            .catch(() => this.error("Could not load image data"))
                    }
                }
            },
            methods:  {
                ...mapActions("alert", ["error"]),
                ...mapActions("image", ["getImage"])
            },
            template: `
                <div :style="{lineHeight: 0, fontSize: 0}">
                    <el-popover placement="top"
                                width="600"
                                trigger="click"
                                title="Picture details"
                                :disabled="!editable"
                                @show="popoverVisible = true"
                                @hide="popoverVisible = false">
                        <el-form :ref="formRef" label-position="right">
                            <el-form-item :style="{marginBottom: '10px'}">
                                <el-input v-model="href" type="url" size="small" placeholder="Enter url ...">
                                    <template slot="prepend">Url</template>
                                </el-input>
                            </el-form-item>
                            <el-form-item :style="{marginBottom: '10px'}">
                                <el-input v-model="title" size="small" placeholder="Enter title ...">
                                    <template slot="prepend">Title</template>
                                </el-input>
                            </el-form-item>
                            <el-form-item :style="{marginBottom: '10px'}">
                                <el-input v-model="alt" size="small" placeholder="Enter alt ...">
                                    <template slot="prepend">Alt</template>
                                </el-input>
                            </el-form-item>
                            <el-form-item :style="{marginBottom: 0}" label="Responsive sizes">
                                <el-checkbox-group size="small" v-model="sources">
                                    <el-checkbox-button v-for="size in photo.sizes" 
                                                        :label="size"
                                                        :key="size">
                                        {{ size }}px
                                    </el-checkbox-button>
                                </el-checkbox-group>
                            </el-form-item>
                        </el-form>
                        <picture slot="reference" 
                                :data-id="dataId"
                                :style="{outline: popoverVisible ? 'thin dashed dimgrey' : 'none'}">
                            <source v-for="source in sources" 
                                    :key="source.srcset" 
                                    :media="source.media" 
                                    :srcset="source.srcset"
                                    :data-size="source['data-size']">
                            <img :src="src" :title="title" :alt="alt">
                        </picture>
                    </el-popover>
                </div>
            `
        }
    }
}
