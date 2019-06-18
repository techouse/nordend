import {create, destroy, get, update} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getRole: (context, id) => get(context, `/roles/${id}`),

    getRoles: (context, params = {}) => get(context, "/roles/", params),

    createRole: (context, role) => create(context, "/roles/", role),

    updateRole: (context, role) => update(context, `/roles/${role.id}`, role),

    deleteRole: (context, id) => destroy(context, `/roles/${id}`),

    deleteRoles: (context, ids) => destroy(context, "/roles/", {ids}),
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}