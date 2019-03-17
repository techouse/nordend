<template>
    <div id="app" class="app header-fixed sidebar-fixed aside-menu-fixed sidebar-lg-show">
        <header class="app-header navbar">
            <button class="navbar-toggler sidebar-toggler d-lg-none mr-auto" type="button" data-toggle="sidebar-show">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="#">
                <img class="navbar-brand-full" src="/static/images/admin.png" width="48"
                     height="48"
                     alt="Administration">
                <img class="navbar-brand-minimized" src="/static/images/admin.png"
                     width="48"
                     height="48" alt="Administration">
            </a>
            <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button" data-toggle="sidebar-lg-show">
                <span class="navbar-toggler-icon"></span>
            </button>
            <ul class="nav navbar-nav ml-auto">
                <li class="nav-item dropdown">
                    <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-haspopup="true"
                       aria-expanded="false">
                        <img class="img-avatar" alt="example@example.com">
                    </a>
                    <div class="dropdown-menu dropdown-menu-right">
                        <div class="dropdown-header text-center">
                            <strong>Settings</strong>
                        </div>
                        <a class="dropdown-item" href="#">
                            <i class="fa fa-user"></i> Profile
                        </a>
                        <a class="dropdown-item" href="#">
                            <i class="fa fa-wrench"></i> Settings
                        </a>
                        <a class="dropdown-item" href="#">
                            <i class="fa fa-lock"></i> Logout
                        </a>
                    </div>
                </li>
            </ul>
        </header>
        <div class="app-body">
            <div class="sidebar">
                <nav class="sidebar-nav">
                    <ul class="nav">
                        <li class="nav-title">Menu</li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Dashboard'}" class="nav-link">
                                <i class="nav-icon icon-speedometer"></i> Dashboard
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Posts'}" class="nav-link">
                                <i class="nav-icon icon-notebook"></i> Posts
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Categories'}" class="nav-link">
                                <i class="nav-icon icon-tag"></i> Categories
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Users'}" class="nav-link">
                                <i class="nav-icon icon-people"></i> Users
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link :to="{name: 'Roles'}" class="nav-link">
                                <i class="nav-icon icon-graduation"></i> Roles
                            </router-link>
                        </li>
                    </ul>
                </nav>
                <button class="sidebar-minimizer brand-minimizer" type="button"></button>
            </div>
            <main class="main">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a :href="$route.fullPath">{{ $route.name }}</a>
                    </li>
                </ol>
                <div class="container-fluid">
                    <div id="content" class="animated fadeIn">
                        <router-view/>
                    </div>
                </div>
            </main>
        </div>
        <footer class="app-footer">
            <div class="ml-auto">
                <span>Shamelessly powered by</span>
                <a href="http://flask.pocoo.org" target="_blank">Flask</a> & <a href="https://vuejs.org">Vue.js</a>
            </div>
        </footer>
    </div>
</template>

<script>
    export default {
        name: "App"
    }
</script>

<style scoped>

</style>