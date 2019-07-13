<template>
    <div id="admin" class="app">
        <header class="app-header navbar">
            <button class="navbar-toggler sidebar-toggler d-lg-none mr-auto" type="button"
                    data-toggle="sidebar-show"
                    @click.prevent="toggleNanoXs"
            >
                <span class="navbar-toggler-icon" />
            </button>
            <a class="navbar-brand" href="#">
                <svg enable-background="new 0 0 344.32 47.43"
                     viewBox="0 0 344.32 47.43"
                     class="navbar-brand-full"
                     width="145"
                     height="48"
                     xmlns="http://www.w3.org/2000/svg"
                >
                    <path d="m3.26 46.43c-.4 0-.9-.1-1.3-.3-1-.7-1.3-2.1-.7-3.1l24.6-40.2c.2-.3.4-.6.8-.8 1.1-.6 2.4-.3 3.1.7l7.8 12.8-17.7 30.9z"
                          fill="#4c79ad"
                    />
                    <path d="m16.06 18.73 9.8-16c.2-.3.4-.6.8-.8 1.1-.6 2.4-.3 3.1.7l7.8 12.8-6.7 11.7c-.6-.3-1.2-.7-1.6-1.2-4.3-3.6-8.8-5.9-13.2-7.2z"
                          fill="#ccc"
                    />
                    <path d="m24.96 2.23c1.2-2.1 4.3-2.1 5.5 0l8.1 13.3-.3.5-6.7 11.7-.5.8-10.6 18.8h-17.1c-2.6.1-4.2-2.7-2.9-4.9l14.8-24.2zm4.5 25.4-.1-.1c-4.8-3.4-6.9-5.7-12.9-7.6l-14.4 23.6c-.5.9.1 2 1.2 1.9h.1 16.1zm-2.8-24.4-9.1 15c5.9 1.9 8.1 4.3 12.9 7.7l5.9-10.4-7.5-12.3c-.5-.8-1.8-.8-2.2 0z"
                          fill="#0e0f0f"
                    />
                    <path clip-rule="evenodd"
                          d="m37.46 15.53-17.6 30.9h40.8c1.2 0 2.2-1 2.2-2.2 0-.5-.2-.9-.4-1.3-6.8-9.6-13.6-19.3-20.3-28.9-.7-1-2.1-1.3-3.1-.5-.2.2-.4.3-.5.5z"
                          fill="#4989bd" fill-rule="evenodd"
                    />
                    <path clip-rule="evenodd"
                          d="m37.46 15.53-5.1 8.9c3.5.6 7 2 10.4 5 2.5 2.2 8.9 2.8 12.1 2.4l-12.6-18c-.7-1-2.1-1.3-3.1-.5-.2.2-.4.3-.5.5z"
                          fill="#e6e6e6" fill-rule="evenodd"
                    />
                    <path d="m32.86 25.53-11.3 19.9h39.2c1.9 0 1.2-1.8.5-2.8l-6.9-9.8c-4.2.2-9.5-.1-12.3-2.6-2.6-2.4-5.7-4-9.2-4.7zm7.8-11.5c-.3-.1-.7 0-1 .2-.1 0-.1.1-.2.1s-.1.1-.1.2l-1.1 1.5-4.4 7.7c3.6.8 6.8 2.5 9.5 5 2 1.8 7 2.3 9.7 2.3zm-21.6 31.9 11.8-20.7.7-1.2 5.1-8.9v-.1l1.1-1.6c.1-.1.2-.3.4-.4.1-.1.3-.2.4-.4.7-.5 1.6-.7 2.4-.5.8.1 1.6.6 2.1 1.3l12.6 18 .9 1.3 6.8 9.6c1.5 2.1-.1 5.1-2.6 5.1h-42.5z"
                          fill="#0e0f0f"
                    />
                    <text font-family="Montserrat" font-size="50.3908" font-weight="800"
                          transform="translate(66.0598 42.8315)"
                    >
                        NORDEND
                    </text>
                </svg>
                <svg enable-background="new 0 0 64 64"
                     class="navbar-brand-minimized"
                     viewBox="0 0 64 64"
                     width="48"
                     height="48"
                     xmlns="http://www.w3.org/2000/svg"
                >
                    <path d="m3.3 54.4c-.4 0-.9-.1-1.3-.3-1-.7-1.3-2.1-.7-3.1l24.6-40.2c.2-.3.4-.6.8-.8 1.1-.6 2.4-.3 3.1.7l7.8 12.8-17.7 30.9z"
                          fill="#1379c2"
                    />
                    <path d="m16.1 26.7 9.8-16c.2-.3.4-.6.8-.8 1.1-.6 2.4-.3 3.1.7l7.8 12.8-6.7 11.7c-.6-.3-1.2-.7-1.6-1.2-4.3-3.6-8.8-5.9-13.2-7.2z"
                          fill="#ccc"
                    />
                    <path d="m25 10.2c1.2-2.1 4.3-2.1 5.5 0l8.1 13.3-.3.5-6.7 11.7-.5.8-10.6 18.8h-17.1c-2.6.1-4.2-2.7-2.9-4.9l14.8-24.2zm4.5 25.4-.1-.1c-4.8-3.4-6.9-5.7-12.9-7.6l-14.4 23.6c-.5.9.1 2 1.2 1.9h.1 16.1zm-2.8-24.4-9.1 15c5.9 1.9 8.1 4.3 12.9 7.7l5.9-10.4-7.5-12.3c-.5-.8-1.8-.8-2.2 0z" />
                    <path clip-rule="evenodd"
                          d="m37.5 23.5-17.6 30.9h40.8c1.2 0 2.2-1 2.2-2.2 0-.5-.2-.9-.4-1.3-6.8-9.6-13.6-19.3-20.3-28.9-.7-1-2.1-1.3-3.1-.5-.2.2-.4.3-.5.5z"
                          fill="#358dcc" fill-rule="evenodd"
                    />
                    <path clip-rule="evenodd"
                          d="m37.5 23.5-5.1 8.9c3.5.6 7 2 10.4 5 2.5 2.2 8.9 2.8 12.1 2.4l-12.6-18c-.7-1-2.1-1.3-3.1-.5-.2.2-.4.3-.5.5z"
                          fill="#e6e6e6" fill-rule="evenodd"
                    />
                    <path d="m32.9 33.5-11.3 19.9h39.2c1.9 0 1.2-1.8.5-2.8l-6.9-9.8c-4.2.2-9.5-.1-12.3-2.6-2.6-2.4-5.7-4-9.2-4.7zm7.8-11.5c-.3-.1-.7 0-1 .2-.1 0-.1.1-.2.1s-.1.1-.1.2l-1.1 1.5-4.4 7.7c3.6.8 6.8 2.5 9.5 5 2 1.8 7 2.3 9.7 2.3zm-21.6 31.9 11.8-20.7.7-1.2 5.1-8.9v-.1l1.1-1.6c.1-.1.2-.3.4-.4.1-.1.3-.2.4-.4.7-.5 1.6-.7 2.4-.5.8.1 1.6.6 2.1 1.3l12.6 18 .9 1.3 6.8 9.6c1.5 2.1-.1 5.1-2.6 5.1h-42.5z" />
                </svg>
            </a>
            <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button"
                    data-toggle="sidebar-lg-show"
                    @click.prevent="toggleNano"
            >
                <span class="navbar-toggler-icon" />
            </button>
            <ul class="nav navbar-nav ml-auto mr-4">
                <el-dropdown v-if="currentUser" size="medium" split-button
                             type="primary" @command="handleDropdownCommand"
                             @click="$router.push({name: 'EditUser', params: {userId: currentUser.id}})"
                >
                    <i class="el-icon-user-solid el-icon--right" />
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
                                <i class="nav-icon icon-speedometer" /> Dashboard
                            </router-link>
                        </li>
                        <li v-if="currentUserIsAuthor"
                            class="nav-item"
                        >
                            <router-link :to="{name: 'Posts'}" class="nav-link">
                                <i class="nav-icon icon-notebook" /> Posts
                            </router-link>
                        </li>
                        <li v-if="currentUserIsAuthor"
                            class="nav-item"
                        >
                            <router-link :to="{name: 'Images'}" class="nav-link">
                                <i class="nav-icon icon-camera" /> Images
                            </router-link>
                        </li>
                        <li v-if="currentUserIsStaff" class="nav-item">
                            <router-link :to="{name: 'Categories'}" class="nav-link">
                                <i class="nav-icon icon-tag" /> Categories
                            </router-link>
                        </li>
                        <li v-if="currentUserIsStaff" class="nav-item">
                            <router-link :to="{name: 'Users'}" class="nav-link">
                                <i class="nav-icon icon-people" /> Users
                            </router-link>
                        </li>
                        <li v-if="currentUserIsAdmin" class="nav-item">
                            <router-link :to="{name: 'Roles'}" class="nav-link">
                                <i class="nav-icon icon-graduation" /> Roles
                            </router-link>
                        </li>
                    </ul>
                </nav>
                <button class="sidebar-minimizer brand-minimizer" type="button" @click.prevent="toggleMini" />
            </div>
            <main class="main">
                <el-breadcrumb class="breadcrumb" separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item v-for="(crumb, index) in breadcrumbs" :key="index" :to="crumb">
                        {{ crumb.meta.breadcrumb }}
                    </el-breadcrumb-item>
                </el-breadcrumb>
                <div class="container-fluid">
                    <div id="content" class="animated fadeIn">
                        <router-view />
                    </div>
                </div>
            </main>
        </div>
        <footer class="app-footer">
            <div>
                <span>
                    &copy;2018–{{ currentYear }} <a href="https://github.com/techouse" target="_blank">Klemen Tušar</a>
                </span>
            </div>
            <div class="ml-auto d-none d-md-block">
                <span>Powered by</span>
                <a href="http://flask.pocoo.org" target="_blank">Flask</a> and
                <a href="https://vuejs.org" target="_blank">Vue.js</a>.
                <a href="https://en.wikipedia.org/wiki/Slovenia" target="_blank">
                    <img title="Made in sLOVEnia"
                         alt="Made in sLOVEnia"
                         src="/static/images/admin/sLOVEnia.svg"
                         width="48"
                         height="48"
                    >
                </a>
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