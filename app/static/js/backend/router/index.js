import Vue                  from "vue"
import Router               from "vue-router"
import store                from "../store"
// PAGES
// Dashboard
import Dashboard            from "../pages/Dashboard"
// Auth
import Login                from "../pages/Auth/Login"
import Register             from "../pages/Auth/Register"
import ResetPassword        from "../pages/Auth/ResetPassword"
import ResetPasswordRequest from "../pages/Auth/ResetPasswordRequest"
// Posts
import Posts                from "../pages/Posts"
import CreatePost           from "../pages/Posts/create"
import EditPost             from "../pages/Posts/edit"
// Users
import Users                from "../pages/Users"
import CreateUser           from "../pages/Users/create"
import EditUser             from "../pages/Users/edit"
// Categories
import Categories           from "../pages/Categories"
import CreateCategory       from "../pages/Categories/create"
import EditCategory         from "../pages/Categories/edit"
// Roles
import Roles                from "../pages/Roles"
import CreateRole           from "../pages/Roles/create"
import EditRole             from "../pages/Roles/edit"
// 404
import NotFound             from "../pages/NotFound"

const routerOptions = [
    {
        path:     "/",
        redirect: {name: "Dashboard"}
    },
    {
        path:      "/auth/login/",
        component: Login,
        name:      "Login",
        meta:      {
            guest: true
        }
    },
    {
        path:      "/auth/register/",
        component: Register,
        name:      "Register",
        meta:      {
            guest: true
        }
    },
    {
        path:      "/auth/reset_password/:token/",
        component: ResetPassword,
        name:      "ResetPassword",
        props:     true,
        meta:      {
            guest: true
        }
    },
    {
        path:      "/auth/reset_password_request/",
        component: ResetPasswordRequest,
        name:      "ResetPasswordRequest",
        meta:      {
            guest: true
        }
    },
    {
        path:      "/dashboard/",
        component: Dashboard,
        name:      "Dashboard",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/posts/",
        component: Posts,
        name:      "Posts",
        props:     route => ({
            search:  route.query.search,
            page:    Number(route.query.page) || 1,
            perPage: Number(route.query.per_page) || 12,
            sort:    route.query.sort
        }),
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/posts/:postId/",
        component: EditPost,
        props:     true,
        name:      "EditPost",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/create/post/",
        component: CreatePost,
        props:     true,
        name:      "CreatePost",
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
        }
    },
    {
        path:      "/users/",
        component: Users,
        name:      "Users",
        props:     route => ({
            search:  route.query.search,
            page:    Number(route.query.page) || 1,
            perPage: Number(route.query.per_page) || 12,
            sort:    route.query.sort
        }),
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
        }
    },
    {
        path:      "/users/:userId/",
        component: EditUser,
        props:     true,
        name:      "EditUser",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/create/user/",
        component: CreateUser,
        props:     true,
        name:      "CreateUser",
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
        }
    },
    {
        path:      "/categories/",
        component: Categories,
        name:      "Categories",
        props:     route => ({
            search:  route.query.search,
            page:    Number(route.query.page) || 1,
            perPage: Number(route.query.per_page) || 12,
            sort:    route.query.sort
        }),
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/categories/:categoryId/",
        component: EditCategory,
        props:     true,
        name:      "EditCategory",
        meta:      {
            requiresAuth: true
        }
    },
    {
        path:      "/create/category/",
        component: CreateCategory,
        props:     true,
        name:      "CreateCategory",
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
        }
    },
    {
        path:      "/roles/",
        component: Roles,
        name:      "Roles",
        props:     route => ({
            search:  route.query.search,
            page:    Number(route.query.page) || 1,
            perPage: Number(route.query.per_page) || 12,
            sort:    route.query.sort
        }),
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
        }
    },
    {
        path:      "/roles/:roleId/",
        component: EditRole,
        props:     true,
        name:      "EditRole",
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
        }
    },
    {
        path:      "/create/role/",
        component: CreateRole,
        props:     true,
        name:      "CreateRole",
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true
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
        routes:          routerOptions,
        base:            "/admin/",
        mode:            "history",
        linkActiveClass: "active"
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