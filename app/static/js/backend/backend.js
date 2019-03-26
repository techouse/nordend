require("../bootstrap")
require("@coreui/coreui")

import Vue       from "vue"
import ElementUI from "element-ui"
import router    from "./router"
import store     from "./store"
import api       from "./services/api"
import App       from "./App"

// Set Axios as default resource handler
Vue.prototype.$http = api

// ElementUI
Vue.use(ElementUI)

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