import {create, destroy, get, update} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getTag: (context, id) => get(context, `/tags/${id}`),

    getTags: (context, params = {}) => get(context, "/tags/", params),

    createTag: (context, tag) => create(context, "/tags/", tag),

    updateTag: (context, tag) => update(context, `/tags/${tag.id}`, tag),

    deleteTag: (context, id) => destroy(context, `/tags/${id}`)
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}