require("./bootstrap")
require("@coreui/coreui")

import Vue from "vue"

const app = new Vue(
    {
        el: "#app",

        methods: {
            sendDeleteRequest(url) {
                axios.delete(url)
                     .then(() => {
                         window.location.reload(true)
                     })
            }
        }
    }
)