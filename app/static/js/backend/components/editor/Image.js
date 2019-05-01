import {Image as TTImage} from "tiptap-extensions"

export default class Image extends TTImage {
    get schema() {
        return {
            inline:    true,
            attrs:     {
                src:       {},
                alt:       {
                    default: null,
                },
                title:     {
                    default: null,
                },
                "data-id": {
                    default: null
                },
                srcset:    {
                    default: null
                },
                sizes:     {
                    default: null
                }
            },
            group:     "inline",
            draggable: true,
            parseDOM:  [
                {
                    tag:      "img[src]",
                    getAttrs: dom => ({
                        src:       dom.getAttribute("src"),
                        title:     dom.getAttribute("title"),
                        alt:       dom.getAttribute("alt"),
                        "data-id": dom.dataset["id"],
                        srcset:    dom.getAttribute("srcset"),
                        sizes:     dom.getAttribute("sizes")
                    }),
                },
            ],
            toDOM:     node => ["img", node.attrs],
        }
    }
}
