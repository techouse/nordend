import {create, destroy, get, update} from "../../services"

const state = {
    created:   0,
    createdId: null,
    updated:   0,
    updatedId: null,
    deleted:   0,
    deletedId: null
}

const getters = {
    created:   state => state.created,
    createdId: state => state.createdId,
    updated:   state => state.updated,
    updatedId: state => state.updatedId,
    deleted:   state => state.deleted,
    deletedId: state => state.deletedId,
}

const mutations = {
    setCreated: (state, id) => {
        state.created++
        state.createdId = id
    },
    setUpdated: (state, id) => {
        state.updated++
        state.updatedId = id
    },
    setDeleted: (state, id) => {
        state.deleted++
        state.deletedId = id
    },
}

const actions = {
    getPost: (context, id) => get(context, `/posts/${id}`),

    getPosts: (context, params = {}) => get(context, "/posts/", params),

    createPost: (context, post) => create(context, "/posts/", post),

    updatePost: (context, post) => update(context, `/posts/${post.id}`, post),

    deletePost: (context, id) => destroy(context, `/posts/${id}`),

    setPublicSocketHooks: ({commit, dispatch, rootGetters}) => {
        rootGetters["socket/publicSocket"].on("post.created", ({data}) => {
                                              commit("setCreated", data.id)
                                              dispatch("console/log", `Post titled ${data.title} created`, {root: true})
                                          })
                                          .on("post.updated", ({data}) => {
                                              commit("setUpdated", data.id)
                                              dispatch("console/log", `Post titled ${data.title} updated`, {root: true})
                                          })
                                          .on("post.deleted", ({data}) => {
                                              commit("setDeleted", data.id)
                                              dispatch("console/log", `Post with ID ${data.id} deleted`, {root: true})
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