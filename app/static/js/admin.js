require("./bootstrap")
require("@coreui/coreui")

import Vue from "vue"

const app = new Vue(
    {
        el: "#app",
        data() {
            return {
                message: "Hi"
            }
        }
    }
)