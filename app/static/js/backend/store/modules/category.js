import {create, destroy, get, update} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getCategory: (context, id) => get(context, `/categories/${id}`),

    getCategories: (context, params = {}) => get(context, "/categories/", params),

    createCategory: (context, category) => create(context, "/categories/", category),

    updateCategory: (context, category) => update(context, `/categories/${category.id}`, category),

    deleteCategory: (context, id) => destroy(context, `/categories/${id}`),

    deleteCategories: (context, ids) => destroy(context, "/categories/", {ids}),
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}