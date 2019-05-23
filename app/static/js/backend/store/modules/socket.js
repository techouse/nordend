import io from "socket.io-client"

const state = {
    broadcastRoom: "broadcast",
    publicSocket:  null,
    privateSocket: null,
    adminSocket:   null,
}

const getters = {
    publicSocket:  state => state.publicSocket,
    privateSocket: state => state.privateSocket,
    adminSocket:   state => state.adminSocket
}

const mutations = {
    setPublicSocket(state) {
        state.publicSocket = io.connect(`${location.protocol}//${document.domain}:${location.port}/${state.broadcastRoom}`)
    },

    setPrivateSocket(state) {
        state.privateSocket = io.connect(`${location.protocol}//${document.domain}:${location.port}/private.${state.broadcastRoom}`)
    },

    setAdminSocket(state) {
        state.adminSocket = io.connect(`${location.protocol}//${document.domain}:${location.port}/admin.${state.broadcastRoom}`)
    },
}

const actions = {
    connect: ({commit, dispatch}, user) => {
        commit("setPublicSocket")
        dispatch("auth/setPublicSocketHooks", {}, {root: true}).then(() => {
            dispatch("post/setPublicSocketHooks", {}, {root: true})
        })

        commit("setPrivateSocket")
        dispatch("auth/setPrivateSocketHooks", {}, {root: true}).then(() => {
            dispatch("post/setPrivateSocketHooks", user, {root: true})
        })

        commit("setAdminSocket")
        dispatch("auth/setAdminSocketHooks", {}, {root: true}).then(() => {
            // TODO dispatch other admin socket stuff
        })
    },
    leave:   ({state}, token) => {
        if (state.publicSocket) {
            state.publicSocket.emit("leave", {token})
        }
        if (state.privateSocket) {
            state.privateSocket.emit("leave", {token})
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}