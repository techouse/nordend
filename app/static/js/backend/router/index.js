import Vue                  from "vue"
import Router               from "vue-router"
import store                from "../store"
// PAGES
// Dashboard
import Dashboard            from "../pages/Dashboard"
// Auth
import Auth                 from "../pages/Auth"
import Login                from "../pages/Auth/login"
import Register             from "../pages/Auth/register"
import ResetPassword        from "../pages/Auth/reset_password"
import ResetPasswordRequest from "../pages/Auth/reset_password_request"
import Unconfirmed          from "../pages/Auth/unconfirmed"
// Posts
import Posts                from "../pages/Posts"
import ListPosts            from "../pages/Posts/list"
import CreatePost           from "../pages/Posts/create"
import EditPost             from "../pages/Posts/edit"
// Users
import Users                from "../pages/Users"
import ListUsers            from "../pages/Users/list"
import CreateUser           from "../pages/Users/create"
import EditUser             from "../pages/Users/edit"
// Categories
import Categories           from "../pages/Categories"
import ListCategories       from "../pages/Categories/list"
import CreateCategory       from "../pages/Categories/create"
import EditCategory         from "../pages/Categories/edit"
// Roles
import Roles                from "../pages/Roles"
import ListRoles            from "../pages/Roles/list"
import CreateRole           from "../pages/Roles/create"
import EditRole             from "../pages/Roles/edit"
// Images
import Images               from "../pages/Images"
import ListImages           from "../pages/Images/list"
import EditImage            from "../pages/Images/edit"
// Errors
import Error404             from "../pages/Errors/404"

const routerOptions = [
    {
        path:     "/",
        redirect: {name: "Dashboard"}
    },
    {
        path:      "/auth/",
        component: Auth,
        children:  [
            {
                path:      "login/",
                component: Login,
                name:      "Login",
                meta:      {
                    auth:  true,
                    guest: true
                }
            },
            {
                path:      "register/:csrfToken",
                component: Register,
                name:      "Register",
                props:     true,
                meta:      {
                    auth:         true,
                    registration: true
                }
            },
            {
                path:      "unconfirmed/:token",
                component: Unconfirmed,
                name:      "Unconfirmed",
                props:     true,
                meta:      {
                    auth: true
                }
            },
            {
                path:      "confirm/:token",
                component: Login,
                name:      "ConfirmRegistration",
                props:     true,
                meta:      {
                    auth:    true,
                    confirm: true
                }
            },
            {
                path:      "reset_password/:token",
                component: ResetPassword,
                name:      "ResetPassword",
                props:     true,
                meta:      {
                    auth:          true,
                    passwordReset: true
                }
            },
            {
                path:      "reset_password_request/",
                component: ResetPasswordRequest,
                name:      "ResetPasswordRequest",
                meta:      {
                    auth:  true,
                    guest: true
                }
            },
        ]
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
        children:  [
            {
                path:      "",
                component: ListPosts,
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
                path:      ":postId/",
                component: EditPost,
                props:     true,
                name:      "EditPost",
                meta:      {
                    requiresAuth: true
                }
            },
            {
                path:      "new/",
                component: CreatePost,
                props:     true,
                name:      "CreatePost",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true
                }
            },
        ]
    },
    {
        path:      "/users/",
        component: Users,
        children:  [
            {
                path:      "",
                component: ListUsers,
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
                path:      ":userId/",
                component: EditUser,
                props:     true,
                name:      "EditUser",
                meta:      {
                    requiresAuth: true
                }
            },
            {
                path:      "new/",
                component: CreateUser,
                props:     true,
                name:      "CreateUser",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true
                }
            },
        ]
    },
    {
        path:      "/categories/",
        component: Categories,
        children:  [
            {
                path:      "",
                component: ListCategories,
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
                path:      ":categoryId/",
                component: EditCategory,
                props:     true,
                name:      "EditCategory",
                meta:      {
                    requiresAuth: true
                }
            },
            {
                path:      "new/",
                component: CreateCategory,
                props:     true,
                name:      "CreateCategory",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true
                }
            },
        ]
    },
    {
        path:      "/roles/",
        component: Roles,
        children:  [
            {
                path:      "",
                component: ListRoles,
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
                path:      ":roleId/",
                component: EditRole,
                props:     true,
                name:      "EditRole",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true
                }
            },
            {
                path:      "new/",
                component: CreateRole,
                props:     true,
                name:      "CreateRole",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true
                }
            },
        ]
    },
    {
        path:      "/images/",
        component: Images,
        children:  [
            {
                path:      "",
                component: ListImages,
                name:      "Images",
                props:     route => ({
                    search:  route.query.search,
                    page:    Number(route.query.page) || 1,
                    perPage: Number(route.query.per_page) || 12,
                    sort:    route.query.sort
                }),
                meta:      {
                    requiresAuth: true,
                }
            },
            {
                path:      ":imageId/",
                component: EditImage,
                props:     true,
                name:      "EditImage",
                meta:      {
                    requiresAuth: true,
                }
            },
        ]
    },
    {
        path:      "*",
        component: Error404,
        name:      "Error404",
        meta:      {
            error: true
        }
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
            next({name: "Login"})
        } else {
            next()
        }
    } else if (to.matched.some(record => record.meta.guest)) {
        if (+new Date() >= expiration || !token || !userId) {
            next()
        } else {
            next({name: "Dashboard"})
        }
    } else if (to.matched.some(record => record.meta.passwordReset)) {
        if (+new Date() < expiration && token && userId) {
            next({name: "Dashboard"})
        } else {
            store.dispatch("auth/verifyPasswordResetToken", to.params.token)
                 .then(() => {
                     next()
                 })
                 .catch(() => {
                     store.commit("auth/clearAuthData")
                     next({name: "Login"})
                 })
        }
    } else if (to.matched.some(record => record.meta.registration)) {
        if (+new Date() < expiration && token && userId) {
            next({name: "Dashboard"})
        } else if (to.params.csrfToken !== window.csrfToken) {
            store.commit("auth/clearAuthData")
            next({name: "Login"})
        } else {
            store.dispatch("auth/checkIfPublicRegistrationEnabled")
                 .then(() => {
                     next()
                 })
                 .catch(() => {
                     store.commit("auth/clearAuthData")
                     next({name: "Login"})
                 })
        }
    } else if (to.matched.some(record => record.meta.confirm)) {
        if (+new Date() < expiration && token && userId) {
            next({name: "Dashboard"})
        } else if (!to.params.token) {
            store.commit("auth/clearAuthData")
            next({name: "Login"})
        } else {
            store.dispatch("auth/confirmUserViaToken", to.params.token)
            next({name: "Login"})
        }
    } else {
        next()
    }
})

export default router