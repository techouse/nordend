require("../bootstrap")
require("@coreui/coreui")

import Vue     from "vue"
import Element from "element-ui"
import router  from "./router"
import store   from "./store"
import api     from "./components/api"
import App     from "./App"

let token = document.head.querySelector("meta[name=\"csrf-token\"]")

if (token) {
    api.defaults.headers.common["X-CSRF-TOKEN"] = token.content
} else {
    console.error("CSRF token not found!")
}

Vue.prototype.$http = api

Vue.use(Element)

new Vue(
    {
        el:     "#app",
        router,
        store,
        render: h => h(App)
    }
)