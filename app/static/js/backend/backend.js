require("../bootstrap")

import Vue       from "vue"
import ElementUI from "element-ui"
import Viewer    from "v-viewer"
import router    from "./router"
import store     from "./store"
import api       from "./services/api"
import App       from "./App"

// Set Axios as default resource handler
Vue.prototype.$http = api

// ElementUI
Vue.use(ElementUI)

// V-Viewer
Vue.use(Viewer)

// Set all the custom filters
import "./filters"

new Vue(
    {
        el:     "#app",
        router,
        store,
        render: h => h(App)
    }
)