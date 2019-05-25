import {create, destroy, get, update} from "../../services"

const state = {
    created:                 0,
    createdId:               null,
    updated:                 0,
    updatedId:               null,
    deleted:                 0,
    deletedId:               null,
    lockedPosts:             [],
    gotLockedPosts:          false,
    notifyAboutForcedUnlock: false
}

const getters = {
    created:                 state => state.created,
    createdId:               state => state.createdId,
    updated:                 state => state.updated,
    updatedId:               state => state.updatedId,
    deleted:                 state => state.deleted,
    deletedId:               state => state.deletedId,
    lockedPosts:             state => state.lockedPosts,
    gotLockedPosts:          state => state.gotLockedPosts,
    notifyAboutForcedUnlock: state => state.notifyAboutForcedUnlock,
}

const mutations = {
    setCreated:       (state, id) => {
        state.created++
        state.createdId = id
    },
    setUpdated:       (state, id) => {
        state.updated++
        state.updatedId = id
    },
    setDeleted:       (state, id) => {
        state.deleted++
        state.deletedId = id
    },
    setLockedPosts:   (state, ids) => {
        state.lockedPosts = ids
        state.gotLockedPosts = true
    },
    clearLockedPosts: state => {
        state.lockedPosts = []
        state.gotLockedPosts = false
    },
    lockPost:         (state, id) => {
        if (!state.lockedPosts.includes(id)) {
            state.lockedPosts.push(id)
        }
    },
    unlockPost:       (state, id) => {
        if (state.lockedPosts.includes(id)) {
            state.lockedPosts.splice(state.lockedPosts.indexOf(id), 1)
        }
    },
    setNotifyAboutForcedUnlock: (state, id) => {
        state.notifyAboutForcedUnlock = id
    }
}

const actions = {
    getPost: (context, id) => get(context, `/posts/${id}`),

    getPosts: (context, params = {}) => get(context, "/posts/", params),

    createPost: (context, post) => create(context, "/posts/", post),

    updatePost: (context, post) => update(context, `/posts/${post.id}`, post),

    deletePost: (context, id) => destroy(context, `/posts/${id}`),

    listLockedPosts: ({dispatch, rootGetters}) => {
        dispatch("socket/getPublicSocket", {}, {root: true}).then(socket => {
            socket.emit("post.list.locked", {token: rootGetters["auth/token"]})
        })
    },

    clearLockedPosts: ({commit}) => {
        commit("clearLockedPosts")
    },

    lockPost: ({dispatch, rootGetters}, post) => {
        dispatch("socket/getPublicSocket", {}, {root: true}).then(socket => {
            socket.emit("post.lock", {
                post_id: post.id,
                token:   rootGetters["auth/token"]
            })
        })
    },

    unlockPost: ({dispatch, rootGetters}, {post, forced = false}) => {
        dispatch("socket/getPublicSocket", {}, {root: true}).then(socket => {
            socket.emit("post.unlock", {
                post_id: post.id,
                forced:  forced,
                token:   rootGetters["auth/token"]
            })
        })
    },

    notifyAboutForcedUnlock: ({commit, rootGetters}, {post, notify_user_id}) => {
        if (rootGetters["user/currentUser"].id === notify_user_id) {
            commit("setNotifyAboutForcedUnlock", post.id)
        }
    },

    clearForcedUnlockNotification: ({commit}) => {
        commit("setNotifyAboutForcedUnlock", false)
    },

    setPublicSocketHooks: ({commit, dispatch}) => {
        dispatch("socket/getPublicSocket", {}, {root: true}).then(socket => {
            socket.on("post.created", ({data, timestamp}) => {
                      commit("setCreated", data.id)
                      dispatch("console/log", `Post titled ${data.title} created`, {root: true})
                  })
                  .on("post.updated", ({data, timestamp}) => {
                      commit("setUpdated", data.id)
                      dispatch("console/log", `Post titled ${data.title} updated`, {root: true})
                  })
                  .on("post.deleted", ({data, timestamp}) => {
                      commit("setDeleted", data.id)
                      dispatch("console/log", `Post with ID ${data.id} deleted`, {root: true})
                  })
                  .on("post.locked", ({data, timestamp}) => {
                      commit("lockPost", data.id)
                      dispatch("console/log", `Post with ID ${data.id} locked`, {root: true})
                  })
                  .on("post.unlocked", ({data, forced, notify_user_id, timestamp}) => {
                      commit("unlockPost", data.id)
                      if (forced) {
                          dispatch("notifyAboutForcedUnlock", {post: data, notify_user_id: notify_user_id})
                      }
                      dispatch("console/log", `Post with ID ${data.id} unlocked`, {root: true})
                  })
                  .on("post.list.locked", ({data, timestamp}) => {
                      if (data.length > 0) {
                          commit("setLockedPosts", data)
                          dispatch("console/log", "Set locked post IDs", {root: true})
                      }
                  })
        })
    },

    setPrivateSocketHooks: ({commit, dispatch}, user) => {
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