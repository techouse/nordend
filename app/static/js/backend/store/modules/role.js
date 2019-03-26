import {get} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getRole: (context, id) => get(context, `/roles/${id}`),

    getRoles: (context, params = {}) => get(context, "/roles/", params)
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}