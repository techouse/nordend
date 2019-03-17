require("../bootstrap")
require("@coreui/coreui")

import Vue     from "vue"
import App     from "./App"
import router  from "./router"
import Element from "element-ui"

Vue.use(Element)

new Vue(
    {
        el:     "#app",
        router,
        render: h => h(App)
    }
)