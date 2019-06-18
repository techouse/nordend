import {create, destroy, get, update} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getImage: (context, id) => get(context, `/images/${id}`),

    getImages: (context, params = {}) => get(context, "/images/", params),

    createImage: (context, image) => create(context, "/images/", image),

    updateImage: (context, image) => update(context, `/images/${image.id}`, image),

    deleteImage: (context, id) => destroy(context, `/images/${id}`),

    deleteImages: (context, ids) => destroy(context, "/images/", {ids}),
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}