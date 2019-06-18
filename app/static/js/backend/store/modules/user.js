import {create, destroy, get, update} from "../../services"

const state = {
    user: null
}

const getters = {
    currentUser: state => state.user
}

const mutations = {
    setUser: (state, user) => state.user = user,
}

const actions = {
    setCurrentUser: ({commit, dispatch}, user) => {
        commit("setUser", user)

        dispatch("csrf/getCsrf", {}, {root: true})

        dispatch("socket/connect", user, {root: true})
    },

    getUser: (context, id) => get(context, `/users/${id}`),

    getUsers: (context, params = {}) => get(context, "/users/", params),

    createUser: (context, user) => create(context, "/users/", user),

    updateUser: (context, user) => update(context, `/users/${user.id}`, user),

    deleteUser: (context, id) => destroy(context, `/users/${id}`),

    deleteUsers: (context, ids) => destroy(context, "/users/", {ids}),
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}