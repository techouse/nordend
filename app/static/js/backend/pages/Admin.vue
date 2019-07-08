<template>
    <div id="admin" class="app">
        <header class="app-header navbar">
            <button class="navbar-toggler sidebar-toggler d-lg-none mr-auto" type="button"
                    data-toggle="sidebar-show"
                    @click.prevent="toggleNanoXs"
            >
                <span class="navbar-toggler-icon"/>
            </button>
            <a class="navbar-brand" href="#">
                <img class="navbar-brand-full" src="/static/images/admin/admin.png" width="48"
                     height="48"
                     alt="Administration"
                >
                <img class="navbar-brand-minimized" src="/static/images/admin/admin.png"
                     width="48"
                     height="48" alt="Administration"
                >
            </a>
            <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button"
                    data-toggle="sidebar-lg-show"
                    @click.prevent="toggleNano"
            >
                <span class="navbar-toggler-icon"/>
            </button>
            <ul class="nav navbar-nav ml-auto mr-4">
                <el-dropdown v-if="currentUser" size="medium" split-button
                             type="primary" @command="handleDropdownCommand"
                             @click="$router.push({name: 'EditUser', params: {userId: currentUser.id}})"
                >
                    <i class="el-icon-user-solid el-icon--right"/>
                    <span class="d-none d-sm-inline">
                        {{ currentUser.name || currentUser.email }}
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item icon="el-icon-lock" :command="logout">
                            Logout
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </ul>
        </header>
        <div class="app-body">
            <div class="sidebar">
                <nav class="sidebar-nav ps">
                    <ul class="nav">
                        <li class="nav-item">
                            <router-link :to="{name: 'Dashboard'}" class="nav-link">
                                <i class="nav-icon icon-speedometer"/> Dashboard
                            </router-link>
                        </li>
                        <li v-if="currentUserIsAuthor"
                            class="nav-item">
                            <router-link :to="{name: 'Posts'}" class="nav-link">
                                <i class="nav-icon icon-notebook"/> Posts
                            </router-link>
                        </li>
                        <li v-if="currentUserIsAuthor"
                            class="nav-item">
                            <router-link :to="{name: 'Images'}" class="nav-link">
                                <i class="nav-icon icon-camera"/> Images
                            </router-link>
                        </li>
                        <li v-if="currentUserIsStaff" class="nav-item">
                            <router-link :to="{name: 'Categories'}" class="nav-link">
                                <i class="nav-icon icon-tag"/> Categories
                            </router-link>
                        </li>
                        <li v-if="currentUserIsStaff" class="nav-item">
                            <router-link :to="{name: 'Users'}" class="nav-link">
                                <i class="nav-icon icon-people"/> Users
                            </router-link>
                        </li>
                        <li v-if="currentUserIsAdmin" class="nav-item">
                            <router-link :to="{name: 'Roles'}" class="nav-link">
                                <i class="nav-icon icon-graduation"/> Roles
                            </router-link>
                        </li>
                    </ul>
                </nav>
                <button class="sidebar-minimizer brand-minimizer" type="button" @click.prevent="toggleMini"/>
            </div>
            <main class="main">
                <el-breadcrumb class="breadcrumb" separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item v-for="(crumb, index) in breadcrumbs" :key="index" :to="crumb">
                        {{ crumb.meta.breadcrumb }}
                    </el-breadcrumb-item>
                </el-breadcrumb>
                <div class="container-fluid">
                    <div id="content" class="animated fadeIn">
                        <router-view/>
                    </div>
                </div>
            </main>
        </div>
        <footer class="app-footer">
            <div>
                <span>&copy;2018–{{ currentYear }} <a href="https://github.com/techouse"
                                                      target="_blank">Klemen Tušar</a></span>
            </div>
            <div class="ml-auto d-none d-md-block">
                <span>Shamelessly powered by</span>
                <a href="http://flask.pocoo.org" target="_blank">Flask</a> and
                <a href="https://vuejs.org" target="_blank">Vue.js</a>.
            </div>
        </footer>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import {getYear}                from "date-fns"
    import User                     from "../models/User"

    export default {
        name: "Admin",

        computed: {
            ...mapGetters("user", ["currentUser",
                                   "currentUserIsAdmin",
                                   "currentUserIsStaff",
                                   "currentUserIsAuthor",
            ]),

            ...mapGetters("csrf", ["csrf"]),

            breadcrumbs() {
                return this.$route.matched.filter(route => route.meta && route.meta.breadcrumb)
            },

            currentYear() {
                return getYear(new Date())
            },
        },

        mounted() {
            /**
             * Having this inside mounted prevents getting the user 2x after login
             */
            if (!this.currentUser) {
                this.autoLogin()
                    .then(({userId}) => {
                        this.getUser(userId)
                            .then(({data}) => {
                                this.setCurrentUser(new User(data))
                            })
                    })
            }
        },

        methods: {
            ...mapActions("user", ["getUser", "setCurrentUser"]),

            ...mapActions("auth", ["autoLogin", "logout"]),

            toggleNanoXs() {
                // body
                const body = document.body

                if (body.classList.contains("sidebar-lg-show")) {
                    body.classList.remove("sidebar-lg-show")
                } else {
                    body.classList.add("sidebar-lg-show")
                }

                if (body.classList.contains("sidebar-show")) {
                    body.classList.remove("sidebar-show")
                } else {
                    body.classList.add("sidebar-show")
                }
            },

            toggleNano() {
                // body
                const body = document.body

                if (body.classList.contains("sidebar-lg-show")) {
                    body.classList.remove("sidebar-lg-show")
                } else {
                    body.classList.add("sidebar-lg-show")
                }

                if (body.classList.contains("sidebar-show")) {
                    body.classList.remove("sidebar-show")
                }
            },

            toggleMini() {
                // body
                const body              = document.body,
                      miniBodyClassList = ["brand-minimized",
                                           "sidebar-minimized"]

                miniBodyClassList.forEach(_class => {
                    if (body.classList.contains(_class)) {
                        body.classList.remove(_class)
                    } else {
                        body.classList.add(_class)
                    }
                })

                // .sidebar-nav
                const sidebarNav = document.querySelector(".sidebar-nav")

                if (sidebarNav.classList.contains("ps")) {
                    sidebarNav.classList.remove("ps")
                } else {
                    sidebarNav.classList.add("ps")
                }

                // .navbar-brand
                const navbarBrandFull      = document.querySelector(".navbar-brand-full"),
                      navbarBrandMinimized = document.querySelector(".navbar-brand-minimized")

                if (window.getComputedStyle(navbarBrandFull).display === "none") {
                    navbarBrandFull.style.display = "block"
                } else {
                    navbarBrandFull.style.display = "none"
                }

                if (window.getComputedStyle(navbarBrandMinimized).display === "none") {
                    navbarBrandMinimized.style.display = "block"
                } else {
                    navbarBrandMinimized.style.display = "none"
                }
            },

            handleDropdownCommand(command) {
                command()
            }
        }
    }
</script>