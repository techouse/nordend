import io from "socket.io-client"

const state = {
    broadcastRoom: "broadcast",
    publicSocket:  null,
    privateSocket: null
}

const getters = {
    publicSocket:  (state) => state.publicSocket,
    privateSocket: (state) => state.privateSocket
}

const mutations = {
    setPublicSocket(state, token) {
        // TODO add public actions
        state.publicSocket = io.connect(`${location.protocol}//${document.domain}:${location.port}/${state.broadcastRoom}`)
                               .on("connect", () => {
                                   state.publicSocket.emit("authenticate", {token})
                               })
                               .on("authenticated", ({data}) => {
                                   console.log(data)
                                   window.onbeforeunload = function () {
                                       state.publicSocket.emit("leave", {token})
                                   }
                               })
                               .on("left", ({data}) => {
                                   console.log(data)
                               })
                               .on("post_updated", ({data}) => {
                                   console.log(data)
                               })
    },

    setPrivateSocket(state, {user, token}) {
        // TODO add private actions
        state.privateSocket = io.connect(`${location.protocol}//${document.domain}:${location.port}/private.${state.broadcastRoom}`)
                                .on("connect", () => {
                                    state.privateSocket.emit("authenticate", {token})
                                })
                                .on("authenticated", ({data}) => {
                                    console.log(data)
                                    window.onbeforeunload = function () {
                                        state.privateSocket.emit("leave", {token})
                                    }
                                })
                                .on("left", ({data}) => {
                                    console.log(data)
                                })
    }
}

const actions = {
    connect: ({commit, rootGetters}, user) => {
        commit("setPublicSocket", rootGetters["auth/token"])
        commit("setPrivateSocket", {user, token: rootGetters["auth/token"]})
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