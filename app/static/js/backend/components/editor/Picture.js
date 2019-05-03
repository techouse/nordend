import {Image} from "tiptap-extensions"

export default class Picture extends Image {
    get name() {
        return "picture"
    }

    get schema() {
        return {
            inline:    true,
            attrs:     {
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
            group:     "inline",
            draggable: true,
            parseDOM:  [
                {
                    tag:      "picture",
                    getAttrs: dom => ({
                        "data-id": dom.dataset["id"],
                        src:       dom.getElementsByTagName("img")[0].getAttribute("src"),
                        title:     dom.getElementsByTagName("img")[0].getAttribute("title"),
                        alt:       dom.getElementsByTagName("img")[0].getAttribute("alt"),
                        sources:   [...dom.getElementsByTagName("source")].map(source => {
                            return {
                                media:       source.getAttribute("media"),
                                srcset:      source.getAttribute("srcset")
                            }
                        })
                    }),
                },
            ],
            toDOM:     node => [
                "picture",
                {"data-id": node.attrs["data-id"]},
                ...node.attrs.sources.map(source => ["source", source]),
                [
                    "img",
                    {
                        src:       node.attrs.src,
                        title:     node.attrs.title,
                        alt:       node.attrs.alt
                    }
                ]
            ],
        }
    }
}
