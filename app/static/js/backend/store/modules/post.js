import {create, destroy, get, update} from "../../services"

const state = {
    created:                 0,
    createdId:               null,
    createdIds:              [],
    updated:                 0,
    updatedId:               null,
    updatedIds:              [],
    deleted:                 0,
    deletedId:               null,
    deletedIds:              [],
    lockedPosts:             [],
    unlockedPosts:           [],
    notifyAboutForcedUnlock: false
}

const getters = {
    created:                 state => state.created,
    createdId:               state => state.createdId,
    createdIds:              state => state.createdIds,
    updated:                 state => state.updated,
    updatedId:               state => state.updatedId,
    updatedIds:              state => state.updatedIds,
    deleted:                 state => state.deleted,
    deletedId:               state => state.deletedId,
    deletedIds:              state => state.deletedIds,
    lockedPosts:             state => state.lockedPosts,
    unlockedPosts:           state => state.unlockedPosts,
    notifyAboutForcedUnlock: state => state.notifyAboutForcedUnlock,
}

const mutations = {
    setCreated:                 (state, {post_id, by_user_id}) => {
        state.created++
        state.createdId = post_id
        state.createdIds.push({post_id, by_user_id})
    },
    popCreatedIds:              (state) => {
        state.createdIds.pop()
    },
    setUpdated:                 (state, {post_id, by_user_id}) => {
        state.updated++
        state.updatedId = post_id
        state.updatedIds.push({post_id, by_user_id})
    },
    popUpdatedIds:              (state) => {
        state.updatedIds.pop()
    },
    setDeleted:                 (state, {post_id, by_user_id}) => {
        state.deleted++
        state.deletedId = post_id
        state.deletedIds.push({post_id, by_user_id})
    },
    popDeletedIds:              (state) => {
        state.deletedIds.pop()
    },
    setLockedPosts:             (state, ids) => {
        state.lockedPosts = ids
    },
    clearLockedPosts:           state => {
        state.lockedPosts = []
    },
    lockPost:                   (state, {post_id, by_user_id, timestamp, expires}) => {
        if (!state.lockedPosts.find(el => el.post_id === post_id)) {
            state.lockedPosts.push({post_id, by_user_id, timestamp: new Date(timestamp), expires: new Date(expires)})
        }
    },
    unlockPost:                 (state, post_id) => {
        if (state.lockedPosts.find(el => el.post_id === post_id)) {
            state.lockedPosts.splice(state.lockedPosts.findIndex(el => el.post_id === post_id), 1)
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

    getLatestCreated: ({state, commit}) => new Promise(resolve => {
        const latest = state.createdIds[state.createdIds.length - 1]
        commit("popCreatedIds")
        return resolve(latest)
    }),

    getLatestUpdated: ({state, commit}) => new Promise(resolve => {
        const latest = state.updatedIds[state.updatedIds.length - 1]
        commit("popUpdatedIds")
        return resolve(latest)
    }),

    getLatestDeleted: ({state, commit}) => new Promise(resolve => {
        const latest = state.deletedIds[state.deletedIds.length - 1]
        commit("popDeletedIds")
        return resolve(latest)
    }),

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
            socket.on("post.created", ({data, by_user_id, timestamp}) => {
                      commit("setCreated", {post_id: data.id, by_user_id})
                      dispatch("console/log", `Post titled ${data.title} created`, {root: true})
                  })
                  .on("post.updated", ({data, by_user_id, timestamp}) => {
                      commit("setUpdated", {post_id: data.id, by_user_id})
                      dispatch("console/log", `Post titled ${data.title} updated`, {root: true})
                  })
                  .on("post.deleted", ({data, by_user_id, timestamp}) => {
                      commit("setDeleted", {post_id: data.id, by_user_id})
                      dispatch("console/log", `Post with ID ${data.id} deleted`, {root: true})
                  })
                  .on("post.locked", ({data, by_user_id, timestamp, expires}) => {
                      commit("lockPost", {post_id: data.id, by_user_id, timestamp, expires})
                      dispatch("console/log", `Post with ID ${data.id} locked`, {root: true})
                  })
                  .on("post.unlocked", ({data, forced, notify_user_id, by_user_id, timestamp}) => {
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
    },
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}