import api                                           from "../../components/api"
import router                                        from "../../router"
import {parse, subMinutes, differenceInMilliseconds} from "date-fns"

const state = {
    remember:      0,
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
    setRemember(state, remember = 0) {
        state.remember = Number(remember)
        localStorage.setItem("remember", state.remember)
    },

    setAuthData(state, {userId, token, expiration, refresher}) {
        state.userId = userId
        state.token = token
        state.expiration = expiration
        state.authRefresher = refresher

        if (state.remember) {
            localStorage.setItem("userId", userId)
            localStorage.setItem("token", token)
            localStorage.setItem("expiration", expiration)
        } else {
            sessionStorage.setItem("userId", userId)
            sessionStorage.setItem("token", token)
            sessionStorage.setItem("expiration", expiration)
        }
    },

    setAuthRefresher(state, refresher) {
        state.authRefresher = refresher
    },

    clearAuthData(state) {
        state.remember = false
        state.userId = null
        state.token = null
        state.expiration = 0
        if (state.authRefresher !== null) {
            window.clearTimeout(state.authRefresher)
            state.authRefresher = null
        }

        localStorage.removeItem("remember")
        localStorage.removeItem("userId")
        sessionStorage.removeItem("userId")
        localStorage.removeItem("token")
        sessionStorage.removeItem("token")
        localStorage.removeItem("expiration")
        sessionStorage.removeItem("expiration")
    }
}

const actions = {
    rememberMe({commit}, remember) {
        commit("setRemember", remember)
    },

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

    autoLogin({state, commit, dispatch}) {
        return new Promise((resolve, reject) => {
            const remember = localStorage.getItem("remember") || 0
            commit("setRemember", remember)

            const userId = state.remember ? Number(localStorage.getItem("userId")) : Number(sessionStorage.getItem("userId")),
                  token = state.remember ? localStorage.getItem("token") : sessionStorage.getItem("token"),
                  expiration = state.remember ? Number(localStorage.getItem("expiration")) : Number(sessionStorage.getItem("expiration"))

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
                                                    dispatch("refreshToken")
                                                }
                                            })
                                            .catch(() => {
                                                dispatch("logout")
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