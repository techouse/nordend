import api  from "../../components/api"
import User from "../../models/User"

const state = {
    user:  null
}

const getters = {
    user(state) {
        return state.user
    }
}

const mutations = {
    setUser(state, user) {
        state.user = user
    }
}

const actions = {
    getUser({commit, dispatch}, id) {
        return new Promise((resolve, reject) => {
            api.get(`/users/${id}`)
               .then(response => {
                   commit("setUser", new User(response.data))

                   resolve(response)
               })
               .catch(error => {
                   dispatch("alert/error", error.response.data.message, {root: true})
                   reject(error)
               })
        })
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}