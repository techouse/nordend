import Vue   from "vue"
import Vuex  from "vuex"
import auth  from "./modules/auth"
import role  from "./modules/role"
import user  from "./modules/user"
import alert from "./modules/alert"

Vue.use(Vuex)

export default new Vuex.Store(
    {
        modules: {
            auth,
            alert,
            role,
            user
        }
    }
)