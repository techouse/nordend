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
            selectable: false,
            draggable:  true,
            parseDOM:   [
                {
                    tag: "span.picture",
                    getAttrs(dom) {
                        const pictures = dom.getElementsByTagName("picture")
                        const img = dom.getElementsByTagName("img")[0]
                        const anchors = dom.getElementsByTagName("a")

                        return {
                            "data-id": pictures.length
                                       ? pictures[0].dataset["id"]
                                       : img.dataset["id"],
                            src:       img.getAttribute("src"),
                            title:     img.getAttribute("title"),
                            alt:       img.getAttribute("alt"),
                            sources:   [...dom.getElementsByTagName("source")].map(source => {
                                return {
                                    media:       source.getAttribute("media"),
                                    srcset:      source.getAttribute("srcset"),
                                    "data-size": source.dataset["size"]
                                }
                            }),
                            href:      anchors.length
                                       ? anchors[0].getAttribute("href")
                                       : null
                        }
                    },
                },
            ],
            toDOM(node) {
                const span = [
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

                const img = [
                    "img",
                    {
                        src:       node.attrs.src,
                        title:     node.attrs.title,
                        alt:       node.attrs.alt,
                        "data-id": node.attrs["data-id"],
                    }
                ]

                const picture = [
                    "picture",
                    {
                        "data-id": node.attrs["data-id"],
                    },
                    ...node.attrs.sources.map(source => ["source", source]),
                    img
                ]

                const image = node.attrs.sources.length > 1 ? picture : img

                return node.attrs.href ? [...span, [...anchor, image]]
                                       : [...span, image]
            }
        }
    }

    get view() {
        return {
            props:    ["node", "updateAttrs", "view"],
            data() {
                return {
                    loading:        false,
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
                sourceObjects() {
                    return this.sources
                               .map(size => Number(size))
                               .filter(size => size >= 440) // Minimum size for srcset
                               .sort((a, b) => a - b)
                               .map(size => {
                                   return {
                                       media:       Photo.getMediaBreakPoint(size),
                                       srcset:      `${this.photo.public_path}/${size}.jpg`,
                                       "data-size": size
                                   }
                               })
                },
                formRef() {
                    return `picture_${this.node.attrs["data-id"] || this.node.attrs["src"]}`
                }
            },
            watch:    {
                popoverVisible(visible) {
                    if (visible && !this.photo.id && this.dataId) {
                        this.$set(this, "loading", true)

                        this.getImage(this.dataId)
                            .then(({data}) => {
                                this.$set(this, "photo", new Photo(data))
                                this.$set(this, "loading", false)
                            })
                            .catch(() => this.error("Could not load image data"))
                    }
                }
            },
            methods:  {
                ...mapActions("alert", ["error"]),

                ...mapActions("image", ["getImage"]),

                togglePopover() {
                    this.$set(this, "popoverVisible", !this.popoverVisible)
                },

                closePopover() {
                    this.$set(this, "popoverVisible", false)
                },

                toggleImageEditor() {
                    // TODO
                    console.log("not yet implemented")
                }
            },
            template: `
                <span :style="{lineHeight: 0, fontSize: 0, display: 'inline-block', position: 'relative'}" class="picture">
                    <el-popover placement="top"
                                width="600"
                                trigger="manual"
                                title="Picture details"
                                v-model="popoverVisible"
                                :disabled="!view.editable">
                        <el-tooltip class="item" effect="dark" content="Close image details" placement="top-start">
                            <el-button type="danger" icon="el-icon-close" circle class="close-popover" size="mini"
                                       @click="closePopover" />
                        </el-tooltip>
                        <el-form v-loading="loading" :ref="formRef" label-position="right">
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
                            <el-form-item v-if="photo.id && photo.sizes.length > 1" 
                                          :style="{marginBottom: 0}" 
                                          label="Responsive sizes">
                                <el-checkbox-group size="small" v-model="sources">
                                    <el-checkbox-button v-for="size in photo.sizes" 
                                                        :label="size"
                                                        :key="size">
                                        {{ size }}px
                                    </el-checkbox-button>
                                </el-checkbox-group>
                            </el-form-item>
                        </el-form>
                        <template slot="reference">
                            <picture v-if="sources.length > 1"
                                     :data-id="dataId"
                                     :style="{outline: popoverVisible ? 'thin dashed dimgrey' : 'none', 
                                              position: 'relative', 
                                              zIndex: '1 !important'}">
                                <source v-for="source in sourceObjects" 
                                        :key="source.srcset" 
                                        :media="source.media"
                                        :data-size="source['data-size']">
                                <img :src="src" :title="title" :alt="alt" :data-id="dataId">
                            </picture>
                            <img v-else
                                 :src="src" 
                                 :title="title" 
                                 :alt="alt"
                                 :data-id="dataId"
                                 :style="{outline: popoverVisible ? 'thin dashed dimgrey' : 'none', 
                                          position: 'relative', 
                                          zIndex: 1}">
                            <el-button-group class="image-edit-buttons" 
                                             :style="{display: 'none',
                                                      position: 'absolute !important', 
                                                      top: '5px !important', 
                                                      left: '5px !important', 
                                                      zIndex: '3 !important'}">
                                <el-tooltip class="item" effect="dark" content="Edit in image editor" placement="top-start">
                                    <el-button type="default" size="mini" @click="toggleImageEditor">
                                        <i class="fas fa-paint-brush"/>
                                    </el-button>
                                </el-tooltip>
                                <el-tooltip class="item" effect="dark" 
                                            :content="popoverVisible ? 'Close image details' : 'Edit image details'" 
                                            placement="top-start">
                                    <el-button :type="popoverVisible ? 'danger' : 'default'" size="mini" @click="togglePopover">
                                        <i class="fas fa-edit"/>
                                    </el-button>
                                </el-tooltip>
                            </el-button-group>
                        </template>
                    </el-popover>
                </span>
            `
        }
    }
}
