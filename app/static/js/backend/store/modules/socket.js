import io from "socket.io-client"

const state = {
    socket: null
}

const getters = {
    socket: (state) => state.socket
}

const mutations = {
    setSocket(state, user) {
        state.socket = io.connect(`${location.protocol}//${document.domain}:${location.port}/user.${user.id}.ws`)
                         .on("post_updated", ({data}) => {
                             // TODO all actions for the user
                             console.log(data)
                         })
    }
}

const actions = {
    connect: ({commit}, user) => commit("setSocket", user)
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}