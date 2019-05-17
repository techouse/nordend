import {create, destroy, get, update} from "../../services"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getPost: (context, id) => get(context, `/posts/${id}`),

    getPosts: (context, params = {}) => get(context, "/posts/", params),

    createPost: (context, post) => create(context, "/posts/", post),

    updatePost: (context, post) => update(context, `/posts/${post.id}`, post),

    deletePost: (context, id) => destroy(context, `/posts/${id}`),

    setPublicSocketHooks: ({rootGetters}) => {
        rootGetters["socket/publicSocket"].on("post.created", ({data}) => {
                                              console.log("post.created", data)
                                          })
                                          .on("post.updated", ({data}) => {
                                              console.log("post.updated", data)
                                          })
                                          .on("post.deleted", ({data}) => {
                                              console.log("post.deleted", data)
                                          })
    },

    setPrivateSocketHooks: ({commit, rootGetters}, user) => {
        // TODO add some private stuff maybe
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}