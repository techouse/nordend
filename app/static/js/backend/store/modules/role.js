import api from "../../components/api"

const state = {}

const getters = {}

const mutations = {}

const actions = {
    getRole({dispatch}, id) {
        return new Promise((resolve, reject) => {
            api.get(`/roles/${id}`)
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

    getRoles({dispatch}, params = {}) {
        return new Promise((resolve, reject) => {
            api.get("/roles/", params)
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
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}