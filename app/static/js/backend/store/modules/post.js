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
    notifyAboutUnlock:       null,
    forcefullyUnlockedPost:  null,
    notifyAboutForcedUnlock: null
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
    notifyAboutUnlock:       state => state.notifyAboutUnlock,
    forcefullyUnlockedPost:  state => state.forcefullyUnlockedPost,
    notifyAboutForcedUnlock: state => state.notifyAboutForcedUnlock,
}

const mutations = {
    setCreated:                 (state, {post_id, by_user_id, timestamp}) => {
        state.created++
        state.createdId = post_id
        state.createdIds.push({post_id, by_user_id, timestamp: new Date(timestamp)})
    },
    popCreatedIds:              state => {
        state.createdIds.pop()
    },
    setUpdated:                 (state, {post_id, by_user_id, timestamp}) => {
        state.updated++
        state.updatedId = post_id
        state.updatedIds.push({post_id, by_user_id, timestamp: new Date(timestamp)})
    },
    popUpdatedIds:              state => {
        state.updatedIds.pop()
    },
    setDeleted:                 (state, {post_id, by_user_id, timestamp}) => {
        state.deleted++
        state.deletedId = post_id
        state.deletedIds.push({post_id, by_user_id, timestamp: new Date(timestamp)})
    },
    popDeletedIds:              state => {
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
    unlockPost:                 (state, {post_id}) => {
        if (state.lockedPosts.find(el => el.post_id === post_id)) {
            state.lockedPosts.splice(state.lockedPosts.findIndex(el => el.post_id === post_id), 1)
        }
    },
    setNotifyAboutUnlock:       (state, unlock) => {
        state.notifyAboutUnlock = unlock
    },
    setForcefullyUnlockedPost:  (state, unlock) => {
        state.forcefullyUnlockedPost = unlock
    },
    setNotifyAboutForcedUnlock: (state, forcedUnlock) => {
        state.notifyAboutForcedUnlock = forcedUnlock
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

    notifyAboutUnlock: ({commit, rootGetters}, {post_id, by_user_id, timestamp}) => {
        if (rootGetters["user/currentUser"].id !== by_user_id) {
            commit("setNotifyAboutUnlock", {post_id, by_user_id, timestamp})
        }
    },

    clearUnlockNotification: ({commit}) => {
        commit("setNotifyAboutUnlock", null)
    },

    forcefullyUnlockPost: ({commit, rootGetters}, {post_id, notify_user_id, by_user_id, timestamp}) => {
        if (rootGetters["user/currentUser"].id === by_user_id) {
            commit("setForcefullyUnlockedPost", {post_id, notify_user_id, by_user_id, timestamp})
        }
    },

    notifyAboutForcedUnlock: ({commit, rootGetters}, {post_id, notify_user_id, by_user_id, timestamp}) => {
        if (rootGetters["user/currentUser"].id === notify_user_id) {
            commit("setNotifyAboutForcedUnlock", {post_id, notify_user_id, by_user_id, timestamp})
        }
    },

    clearForcedUnlockNotification: ({commit}) => {
        commit("setNotifyAboutForcedUnlock", null)
    },

    setPublicSocketHooks: ({commit, dispatch}) => {
        dispatch("socket/getPublicSocket", {}, {root: true}).then(socket => {
            socket.on("post.created", ({data, by_user_id, timestamp}) => {
                      commit("setCreated", {post_id: data.id, by_user_id, timestamp})
                      dispatch("console/log", `Post titled ${data.title} created`, {root: true})
                  })
                  .on("post.updated", ({data, by_user_id, timestamp}) => {
                      commit("setUpdated", {post_id: data.id, by_user_id, timestamp})
                      dispatch("console/log", `Post titled ${data.title} updated`, {root: true})
                  })
                  .on("post.deleted", ({data, by_user_id, timestamp}) => {
                      commit("setDeleted", {post_id: data.id, by_user_id, timestamp})
                      dispatch("console/log", `Post with ID ${data.id} deleted`, {root: true})
                  })
                  .on("post.locked", ({data, by_user_id, timestamp, expires}) => {
                      commit("lockPost", {post_id: data.id, by_user_id, timestamp, expires})
                      dispatch("console/log", `Post with ID ${data.id} locked`, {root: true})
                  })
                  .on("post.unlocked", ({data, forced, notify_user_id, by_user_id, timestamp}) => {
                      commit("unlockPost", {post_id: data.id, by_user_id, timestamp})
                      if (forced) {
                          dispatch("forcefullyUnlockPost", {post_id: data.id, notify_user_id, by_user_id, timestamp})
                          dispatch("notifyAboutForcedUnlock", {post_id: data.id, notify_user_id, by_user_id, timestamp})
                      } else {
                          dispatch("notifyAboutUnlock", {post_id: data.id, by_user_id, timestamp})
                      }
                      dispatch("console/log", `Post with ID ${data.id} unlocked`, {root: true})
                  })
                  .on("post.list.locked", ({data}) => {
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