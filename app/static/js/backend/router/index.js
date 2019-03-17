import Vue                  from "vue"
import Router               from "vue-router"
// PAGES
import Dashboard            from "../pages/Dashboard"
import Login                from "../pages/auth/Login"
import Posts                from "../pages/Posts"
import Users                from "../pages/Users"
import Categories           from "../pages/Categories"
import Roles                from "../pages/Roles"
import NotFound             from "../pages/NotFound"
import Register             from "../pages/auth/Register"
import ResetPassword        from "../pages/auth/ResetPassword"
import ResetPasswordRequest from "../pages/auth/ResetPasswordRequest"

const routerOptions = [
    {
        path:      "/auth/login",
        component: Login,
        name:      "Login",
        meta:      {
            guest: true
        }
    },
    {
        path:      "/auth/register",
        component: Register,
        name:      "Register",
        meta:      {
            guest: true
        }
    },
    {
        path:      "/auth/reset_password/:token",
        component: ResetPassword,
        name:      "ResetPassword",
        props:     true,
        meta:      {
            guest: true
        }
    },
    {
        path:      "/auth/reset_password_request",
        component: ResetPasswordRequest,
        name:      "ResetPasswordRequest",
        meta:      {
            guest: true
        }
    },
    {
        path:      "/",
        component: Dashboard,
        name:      "Dashboard",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/posts",
        component: Posts,
        name:      "Posts",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/users",
        component: Users,
        name:      "Users",
        meta:      {
            requiresAuth: true,
            is_admin:     true
        }
    },
    {
        path:      "/categories",
        component: Categories,
        name:      "Categories",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/roles",
        component: Roles,
        name:      "Roles",
        meta:      {
            requiresAuth: true,
            is_admin:     true
        }
    },
    {
        path:      "*",
        component: NotFound,
        name:      "NotFound"
    }
]

Vue.use(Router)

export default new Router({
                              routes: routerOptions,
                              base:   "/admin/",
                              mode:   "history",
                              beforeRouteEnter(to, from, next) {
                                  // called before the route that renders this component is confirmed.
                                  // does NOT have access to `this` component instance,
                                  // because it has not been created yet when this guard is called!
                              },
                          })