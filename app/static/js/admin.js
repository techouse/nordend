require("./bootstrap")

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