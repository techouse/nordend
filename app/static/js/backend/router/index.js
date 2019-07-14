import Vue    from "vue"
import Router from "vue-router"
import store  from "../store"
import Role   from "../models/Role"

// PAGES
// Dashboard
const Dashboard = () => import(/* webpackChunkName: "dashboard" */ "../pages/Dashboard")
// Auth
const Auth = () => import(/* webpackChunkName: "auth" */ "../pages/Auth")
const Login = () => import(/* webpackChunkName: "auth-login" */ "../pages/Auth/login")
const Register = () => import(/* webpackChunkName: "auth-register" */ "../pages/Auth/register")
const ResetPassword = () => import(/* webpackChunkName: "auth-reset-password" */ "../pages/Auth/reset_password")
const ResetPasswordRequest = () => import(/* webpackChunkName: "auth-reset-password-request" */ "../pages/Auth/reset_password_request")
const Unconfirmed = () => import(/* webpackChunkName: "auth-unconfirmed" */ "../pages/Auth/unconfirmed")
// Posts
const Posts = () => import(/* webpackChunkName: "posts" */ "../pages/Posts")
const ListPosts = () => import(/* webpackChunkName: "posts-list" */ "../pages/Posts/list")
const CreatePost = () => import(/* webpackChunkName: "posts-create" */ "../pages/Posts/create")
const EditPost = () => import(/* webpackChunkName: "posts-edit" */ "../pages/Posts/edit")
// Users
const Users = () => import(/* webpackChunkName: "users" */ "../pages/Users")
const ListUsers = () => import(/* webpackChunkName: "users-list" */ "../pages/Users/list")
const CreateUser = () => import(/* webpackChunkName: "users-create" */ "../pages/Users/create")
const EditUser = () => import(/* webpackChunkName: "users-edit" */ "../pages/Users/edit")
// Categories
const Categories = () => import(/* webpackChunkName: "categories" */ "../pages/Categories")
const ListCategories = () => import(/* webpackChunkName: "categories-list" */ "../pages/Categories/list")
const CreateCategory = () => import(/* webpackChunkName: "categories-create" */ "../pages/Categories/create")
const EditCategory = () => import(/* webpackChunkName: "categories-edit" */ "../pages/Categories/edit")
// Roles
const Roles = () => import(/* webpackChunkName: "roles" */ "../pages/Roles")
const ListRoles = () => import(/* webpackChunkName: "roles-list" */ "../pages/Roles/list")
const CreateRole = () => import(/* webpackChunkName: "roles-create" */ "../pages/Roles/create")
const EditRole = () => import(/* webpackChunkName: "roles-edit" */ "../pages/Roles/edit")
// Images
const Images = () => import(/* webpackChunkName: "pages" */ "../pages/Images")
const ListImages = () => import(/* webpackChunkName: "pages-list" */ "../pages/Images/list")
const EditImage = () => import(/* webpackChunkName: "pages-edit" */ "../pages/Images/edit")
// Errors
const Error404 = () => import(/* webpackChunkName: "error-404" */ "../pages/Errors/404")

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
            requiresAuth: true,
            breadcrumb:   "Dashboard"
        }
    },
    {
        path:      "/posts/",
        component: Posts,
        meta:      {
            requiresAuth: true,
            breadcrumb:   "Posts"
        },
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
                    requiresAuth: true,
                }
            },
            {
                path:      ":postId(\\d+)/",
                component: EditPost,
                props:     true,
                name:      "EditPost",
                meta:      {
                    requiresAuth:   true,
                    requiresAuthor: true,
                    breadcrumb:     "Edit"
                }
            },
            {
                path:      "new/",
                component: CreatePost,
                name:      "CreatePost",
                meta:      {
                    requiresAuth:   true,
                    requiresAuthor: true,
                    breadcrumb:     "Create"
                }
            },
        ]
    },
    {
        path:      "/users/",
        component: Users,
        meta:      {
            requiresAuth: true,
            breadcrumb:   "Users"
        },
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
                    requiresStaff: true,
                }
            },
            {
                path:      ":userId(\\d+)/",
                component: EditUser,
                props:     true,
                name:      "EditUser",
                meta:      {
                    requiresAuth:          true,
                    requiresMyselfOrStaff: true,
                    breadcrumb:            "Edit"
                }
            },
            {
                path:      "new/",
                component: CreateUser,
                name:      "CreateUser",
                meta:      {
                    requiresAuth:  true,
                    requiresStaff: true,
                    breadcrumb:    "Create"
                }
            },
        ]
    },
    {
        path:      "/categories/",
        component: Categories,
        meta:      {
            requiresAuth:   true,
            requiresAuthor: true,
            breadcrumb:     "Categories"
        },
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
                    requiresAuth:   true,
                    requiresAuthor: true,
                }
            },
            {
                path:      ":categoryId(\\d+)/",
                component: EditCategory,
                props:     true,
                name:      "EditCategory",
                meta:      {
                    requiresAuth:   true,
                    requiresAuthor: true,
                    breadcrumb:     "Edit"
                }
            },
            {
                path:      "new/",
                component: CreateCategory,
                name:      "CreateCategory",
                meta:      {
                    requiresAuth:   true,
                    requiresAuthor: true,
                    breadcrumb:     "Create"
                }
            },
        ]
    },
    {
        path:      "/roles/",
        component: Roles,
        meta:      {
            requiresAuth:  true,
            requiresAdmin: true,
            breadcrumb:    "Roles"
        },
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
                    requiresAdmin: true,
                }
            },
            {
                path:      ":roleId(\\d+)/",
                component: EditRole,
                props:     true,
                name:      "EditRole",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true,
                    breadcrumb:    "Edit"
                }
            },
            {
                path:      "new/",
                component: CreateRole,
                name:      "CreateRole",
                meta:      {
                    requiresAuth:  true,
                    requiresAdmin: true,
                    breadcrumb:    "Create"
                }
            },
        ]
    },
    {
        path:      "/images/",
        component: Images,
        meta:      {
            requiresAuth:   true,
            requiresAuthor: true,
            breadcrumb:     "Images"
        },
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
                    requiresAuth:   true,
                    requiresAuthor: true,
                }
            },
            {
                path:      ":imageId(\\d+)/",
                component: EditImage,
                props:     true,
                name:      "EditImage",
                meta:      {
                    requiresAuth:   true,
                    requiresAuthor: true,
                    breadcrumb:     "Edit"
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
    const remember    = Number(localStorage.getItem("remember")),
          userId      = remember ? Number(localStorage.getItem("userId")) : Number(sessionStorage.getItem("userId")),
          token       = remember ? localStorage.getItem("token") : sessionStorage.getItem("token"),
          expiration  = remember ? Number(localStorage.getItem("expiration")) : Number(sessionStorage.getItem("expiration")),
          permissions = remember ? Number(localStorage.getItem("permissions")) : Number(sessionStorage.getItem("permissions")),
          role        = Role.createFromPermissions(permissions)

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (+new Date() >= expiration || !token || !userId) {
            store.commit("auth/clearAuthData")
            next({name: "Login"})
        } else {
            if (to.matched.some(record => record.meta.requiresAuthor)) {
                if (role.write) {
                    next()
                } else {
                    next({name: "Dashboard"})
                }
            } else if (to.matched.some(record => record.meta.requiresMyselfOrStaff)) {
                if (("userId" in to.params && to.params.userId === userId) || role.moderate) {
                    next()
                } else {
                    next({name: "Dashboard"})
                }
            } else if (to.matched.some(record => record.meta.requiresStaff)) {
                if (role.moderate) {
                    next()
                } else {
                    next({name: "Dashboard"})
                }
            } else if (to.matched.some(record => record.meta.requiresAdmin)) {
                if (role.admin) {
                    next()
                } else {
                    next({name: "Dashboard"})
                }
            } else {
                next()
            }
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