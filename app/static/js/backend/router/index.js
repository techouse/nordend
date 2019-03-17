import Vue        from "vue"
import Router     from "vue-router"
// PAGES
import Dashboard  from "../pages/Dashboard"
import Login      from "../pages/Login"
import Posts      from "../pages/Posts"
import Users      from "../pages/Users"
import Categories from "../pages/Categories"
import Roles      from "../pages/Roles"
import NotFound   from "../pages/NotFound"

const routerOptions = [
    {path: "/", component: Dashboard, name: "Dashboard"},
    {path: "/login", component: Login, name: "Login"},
    {path: "/posts", component: Posts, name: "Posts"},
    {path: "/users", component: Users, name: "Users"},
    {path: "/categories", component: Categories, name: "Categories"},
    {path: "/roles", component: Roles, name: "Roles"},
    {path: "*", component: NotFound, name: "NotFound"}
]

Vue.use(Router)

export default new Router({
                              routes: routerOptions,
                              base:   "/admin/",
                              mode:   "history"
                          })