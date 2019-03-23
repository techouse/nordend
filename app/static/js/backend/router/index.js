import Vue                  from "vue"
import Router               from "vue-router"
import store                from "../store"
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
        path:     "/",
        redirect: {name: "Dashboard"}
    },
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
        path:      "/dashboard",
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

const router = new Router(
    {
        routes:               routerOptions,
        base:                 "/admin/",
        mode:                 "history",
        linkExactActiveClass: "active"
    }
)

router.beforeEach((to, from, next) => {
    const remember   = Number(localStorage.getItem("remember")),
          userId     = remember ? localStorage.getItem("userId") : sessionStorage.getItem("userId"),
          token      = remember ? localStorage.getItem("token") : sessionStorage.getItem("token"),
          expiration = remember ? Number(localStorage.getItem("expiration")) : Number(sessionStorage.getItem("expiration"))

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (+new Date() >= expiration || !token || !userId) {
            store.commit("auth/clearAuthData")
            next({name: "Login", params: {nextUrl: to.fullPath}})
        } else {
            next()
        }
    } else if (to.matched.some(record => record.meta.guest)) {
        if (+new Date() >= expiration || !token || !userId) {
            next()
        } else {
            next({name: "Dashboard", params: {nextUrl: to.fullPath}})
        }
    } else {
        next()
    }
})

export default router