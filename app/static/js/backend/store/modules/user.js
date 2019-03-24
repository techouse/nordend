import api  from "../../components/api"
import User from "../../models/User"

const state = {
    user: null
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
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }
                   reject(error)
               })
        })
    },

    getUsers({dispatch}, params = {}) {
        return new Promise((resolve, reject) => {
            api.get("/users/", params)
               .then(response => {
                   resolve(response)
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }
                   reject(error)
               })
        })
    },

    createUser({dispatch}, user) {
        return new Promise((resolve, reject) => {
            api.post("/users/", user.mappedForSubmission())
               .then(response => {
                   resolve(response)
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }
                   reject(error)
               })
        })
    },

    updateUser({dispatch}, user) {
        return new Promise((resolve, reject) => {
            api.patch(`/users/${user.id}`, user.mappedForSubmission())
               .then(response => {
                   resolve(response)
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }
                   reject(error)
               })
        })
    },

    deleteUser({dispatch}, id) {
        return new Promise((resolve, reject) => {
            api.delete(`/users/${id}`)
               .then(response => {
                   resolve(response)
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }
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