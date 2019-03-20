import api    from "../../components/api"
import router from "../../router"

const state = {
    userId:     null,
    token:      null,
    expiration: 0
}

const getters = {
    isAuthenticated(state) {
        return state.token !== null && +new Date() < Number(state.expiration)
    }
}

const mutations = {
    setAuthData(state, {userId, token, expiration}) {
        state.userId = userId
        state.token = token
        state.expiration = expiration

        localStorage.setItem("userId", userId)
        localStorage.setItem("token", token)
        localStorage.setItem("expiration", expiration)
    },

    clearAuthData(state) {
        state.userId = null
        state.token = null
        state.expiration = 0

        localStorage.removeItem("userId")
        localStorage.removeItem("token")
        localStorage.removeItem("expiration")
    }
}

const actions = {
    login({commit, dispatch}, {email, password}) {
        dispatch("alert/clear", null, {root: true})

        return new Promise((resolve, reject) => {
            api.post("/login/", {}, {
                   auth: {
                       username: email,
                       password: password
                   }
               })
               .then(response => {
                   const data = response.data
                   if (data.token) {
                       const jwtData = JSON.parse(atob(data.token.split(".")[0]))
                       const jwtUser = JSON.parse(atob(data.token.split(".")[1]))

                       commit("setAuthData", {
                           userId:     (jwtUser && "id" in jwtUser) ? Number(jwtUser.id) : null,
                           token:      data.token,
                           expiration: jwtData ? Number(jwtData.exp) * 1000 : 0
                       })

                       dispatch("user/get", (jwtUser && "id" in jwtUser) ? Number(jwtUser.id) : null, {root: true})

                       resolve(response)
                   }
               })
               .catch(error => {
                   dispatch("alert/error", error.response.data.message, {root: true})
                   reject(error)
               })
        })
    },

    autoLogin({commit, dispatch}) {
        return new Promise((resolve, reject) => {
            const userId = Number(localStorage.getItem("userId"))
            const token = localStorage.getItem("token")
            const expiration = Number(localStorage.getItem("expiration"))

            if (+new Date() >= expiration || !token || !userId) {
                reject()
                return
            }

            commit("setAuthData", {
                userId:     userId,
                token:      token,
                expiration: expiration
            })

            dispatch("user/get", userId, {root: true})

            resolve({
                        userId:     userId,
                        token:      token,
                        expiration: expiration
                    })
        })
    },

    logout({commit}) {
        commit("clearAuthData")
        router.replace({name: "Login"})
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}