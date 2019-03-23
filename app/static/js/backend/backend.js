require("../bootstrap")

import Vue     from "vue"
import router  from "./router"
import store   from "./store"
import api     from "./components/api"
import App     from "./App"

const csrfToken = document.head.querySelector("meta[name=\"csrf-token\"]")

if (csrfToken) {
    api.defaults.headers.common["X-CSRF-TOKEN"] = csrfToken.content
} else {
    console.error("CSRF token not found!")
}

Vue.prototype.$http = api

new Vue(
    {
        el:     "#app",
        router,
        store,
        render: h => h(App)
    }
)