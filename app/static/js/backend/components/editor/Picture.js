import {Image} from "tiptap-extensions"

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
                }
            },
            group:      "inline",
            selectable: false,
            draggable:  true,
            parseDOM:   [
                {
                    tag:      "picture",
                    getAttrs: dom => ({
                        "data-id": dom.dataset["id"],
                        src:       dom.getElementsByTagName("img")[0].getAttribute("src"),
                        title:     dom.getElementsByTagName("img")[0].getAttribute("title"),
                        alt:       dom.getElementsByTagName("img")[0].getAttribute("alt"),
                        sources:   [...dom.getElementsByTagName("source")].map(source => {
                            return {
                                media:  source.getAttribute("media"),
                                srcset: source.getAttribute("srcset")
                            }
                        })
                    }),
                },
            ],
            toDOM:      node => [
                "picture",
                {"data-id": node.attrs["data-id"]},
                ...node.attrs.sources.map(source => ["source", source]),
                [
                    "img",
                    {
                        src:   node.attrs.src,
                        title: node.attrs.title,
                        alt:   node.attrs.alt
                    }
                ]
            ],
        }
    }

    get view() {
        return {
            props:    ["node", "updateAttrs", "editable"],
            data() {
                return {
                    popoverVisible: false
                }
            },
            computed: {
                dataId() {
                    return this.node.attrs["data-id"]
                },
                src:   {
                    get() {
                        return this.node.attrs.src
                    },
                    set(src) {
                        this.updateAttrs({src})
                    }
                },
                title: {
                    get() {
                        return this.node.attrs.title
                    },
                    set(title) {
                        this.updateAttrs({title})
                    }
                },
                alt:   {
                    get() {
                        return this.node.attrs.alt
                    },
                    set(alt) {
                        this.updateAttrs({alt})
                    }
                },
                sources() {
                    return this.node.attrs.sources
                },
                formRef() {
                    return `picture_${this.node.attrs["data-id"]}`
                }
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
                        <el-form :ref="formRef">
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
                        </el-form>
                        <picture slot="reference" 
                                :data-id="dataId" 
                                :style="{outline: popoverVisible ? 'thin dashed dimgrey' : 'none'}">
                            <source v-for="source in sources" 
                                    :key="source.srcset" 
                                    :media="source.media" 
                                    :srcset="source.srcset">
                            <img :src="src" :title="title" :alt="alt">
                        </picture>
                    </el-popover>
                </div>
            `
        }
    }
}
