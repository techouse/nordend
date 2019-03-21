import api                                           from "../../components/api"
import router                                        from "../../router"
import {parse, subMinutes, differenceInMilliseconds} from "date-fns"

const state = {
    userId:        null,
    token:         null,
    expiration:    0,
    authRefresher: null
}

const getters = {
    userId(state) {
        return state.userId
    },

    token(state) {
        return state.token
    },

    isAuthenticated(state) {
        return state.token !== null && +new Date() < Number(state.expiration)
    }
}

const mutations = {
    setAuthData(state, {userId, token, expiration, refresher}) {
        state.userId = userId
        state.token = token
        state.expiration = expiration
        state.authRefresher = refresher

        localStorage.setItem("userId", userId)
        localStorage.setItem("token", token)
        localStorage.setItem("expiration", expiration)
    },

    setAuthRefresher(state, refresher) {
        state.authRefresher = refresher
    },

    clearAuthData(state) {
        state.userId = null
        state.token = null
        state.expiration = 0
        if (state.authRefresher !== null) {
            window.clearTimeout(state.authRefresher)
            state.authRefresher = null
        }

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

                       const authData = {
                           userId:     (jwtUser && "id" in jwtUser) ? Number(jwtUser.id) : null,
                           token:      data.token,
                           expiration: jwtData ? Number(jwtData.exp) * 1000 : 0
                       }

                       commit("setAuthData", authData)
                       dispatch("refreshToken")

                       resolve(authData)
                   }
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

    autoLogin({commit, dispatch}) {
        return new Promise((resolve, reject) => {
            const userId = Number(localStorage.getItem("userId"))
            const token = localStorage.getItem("token")
            const expiration = Number(localStorage.getItem("expiration"))

            if (+new Date() >= expiration || !token || !userId) {
                reject()
                return
            }

            const authData = {
                userId:     userId,
                token:      token,
                expiration: expiration
            }

            commit("setAuthData", authData)
            dispatch("refreshToken")

            resolve(authData)
        })
    },

    logout({commit}) {
        commit("clearAuthData")
        router.replace({name: "Login"})
    },

    refreshToken({state, commit, dispatch}) {
        const refresher = setTimeout(() => {
                                         api.post("/login/", {}, {
                                                auth: {
                                                    username: state.token,
                                                    password: ""
                                                }
                                            })
                                            .then(response => {
                                                const data = response.data
                                                if (data.token) {
                                                    const jwtData = JSON.parse(atob(data.token.split(".")[0]))
                                                    const jwtUser = JSON.parse(atob(data.token.split(".")[1]))

                                                    const authData = {
                                                        userId:     (jwtUser && "id" in jwtUser) ? Number(jwtUser.id) : null,
                                                        token:      data.token,
                                                        expiration: jwtData ? Number(jwtData.exp) * 1000 : 0
                                                    }

                                                    commit("setAuthData", authData)
                                                }
                                            })
                                            .catch(error => {
                                                try {
                                                    dispatch("alert/error", error.response.data.message, {root: true})
                                                } catch (e) {
                                                    console.log(error)
                                                }
                                            })
                                     },
                                     differenceInMilliseconds(subMinutes(parse(state.expiration), 1), new Date()))

        commit("setAuthRefresher", refresher)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}