<template>
    <div class="app header-fixed sidebar-fixed aside-menu-fixed sidebar-lg-show">
        <header class="app-header navbar">
            <button class="navbar-toggler sidebar-toggler d-lg-none mr-auto" type="button"
                    data-toggle="sidebar-show"
            >
                <span class="navbar-toggler-icon" />
            </button>
            <a class="navbar-brand" href="#">
                <img class="navbar-brand-full" src="/static/images/admin.png" width="48"
                     height="48"
                     alt="Administration"
                >
                <img class="navbar-brand-minimized" src="/static/images/admin.png"
                     width="48"
                     height="48" alt="Administration"
                >
            </a>
            <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button"
                    data-toggle="sidebar-lg-show"
            >
                <span class="navbar-toggler-icon" />
            </button>
            <ul class="nav navbar-nav ml-auto">
                <li v-if="currentUser" class="nav-item dropdown">
                    <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-haspopup="true"
                       aria-expanded="false"
                    >
                        <img class="img-avatar" :alt="currentUser.name || currentUser.email">
                    </a>
                    <div class="dropdown-menu dropdown-menu-right">
                        <div class="dropdown-header text-center">
                            <strong>Settings</strong>
                        </div>
                        <router-link :to="{name: 'EditUser', params: {userId: currentUser.id}}" class="dropdown-item">
                            <i class="fa fa-user" /> Profile
                        </router-link>
                        <a class="dropdown-item" href="#" @click.prevent="logout">
                            <i class="fa fa-lock" /> Logout
                        </a>
                    </div>
                </li>
            </ul>
        </header>
        <div class="app-body">
            <div class="sidebar">
                <nav class="sidebar-nav">
                    <ul class="nav">
                        <li class="nav-item">
                            <router-link :to="{name: 'Dashboard'}" class="nav-link">
                                <i class="nav-icon icon-speedometer" /> Dashboard
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Posts'}" class="nav-link">
                                <i class="nav-icon icon-notebook" /> Posts
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Categories'}" class="nav-link">
                                <i class="nav-icon icon-tag" /> Categories
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Users'}" class="nav-link">
                                <i class="nav-icon icon-people" /> Users
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Roles'}" class="nav-link">
                                <i class="nav-icon icon-graduation" /> Roles
                            </router-link>
                        </li>
                    </ul>
                </nav>
                <button class="sidebar-minimizer brand-minimizer" type="button" />
            </div>
            <main class="main">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <router-link :to="{path: $route.currentRoute}">{{ $route.name }}</router-link>
                    </li>
                </ol>
                <div class="container-fluid">
                    <div id="content" class="animated fadeIn">
                        <router-view />
                    </div>
                </div>
            </main>
        </div>
        <footer class="app-footer">
            <div class="ml-auto">
                <span>Shamelessly powered by</span>
                <a href="http://flask.pocoo.org" target="_blank">Flask</a>,
                <a href="https://vuejs.org">Vue.js</a> and
                <a href="https://getbootstrap.com" target="_blank">Bootstrap</a>.
            </div>
        </footer>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from "vuex"
    import User                     from "../models/User"

    export default {
        name: "Admin",

        computed: {
            ...mapGetters("user", ["currentUser"])
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

            ...mapActions("auth", [
                "autoLogin",
                "logout"
            ])
        }
    }
</script>