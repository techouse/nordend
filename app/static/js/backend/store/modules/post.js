import {create, destroy, get, update} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getPost: (context, id) => get(context, `/posts/${id}`),

    getPosts: (context, params = {}) => get(context, "/posts/", params),

    createPost: (context, post) => create(context, "/posts/", post),

    updatePost: (context, post) => update(context, `/posts/${post.id}`, post),

    deletePost: (context, id) => destroy(context, `/posts/${id}`)
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}