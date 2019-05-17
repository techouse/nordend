import {get} from "../../services"

const state = {
    csrf: null
}

const getters = {
    csrf: (state) => state.csrf
}

const mutations = {
    setCsrf: (state, token) => {
        state.csrf = token
        window.csrfToken = token
    }
}

const actions = {
    getCsrf(context) {
        get(context, "/csrf").then(({data}) => {
            context.commit("setCsrf", data)
        })
    },
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}