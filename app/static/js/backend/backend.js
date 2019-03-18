require("../bootstrap")
require("@coreui/coreui")

import Vue     from "vue"
import App     from "./App"
import router  from "./router"
import Element from "element-ui"
import api     from "./components/api"

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
        render: h => h(App)
    }
)