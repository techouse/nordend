import api                                                                from "../../services/api"
import router                                                             from "../../router"
import {parse, subMinutes, differenceInMinutes, differenceInMilliseconds} from "date-fns"

const state = {
    remember:             0,
    userId:               null,
    permissions:          0,
    token:                null,
    expiration:           0,
    authRefresher:        null,
    authRefreshThreshold: 15,
}

const getters = {
    userId: state => state.userId,

    token: state => state.token,

    remember: state => state.remember,

    isAuthenticated: state => state.token !== null && state.userId !== null && +new Date() < state.expiration
}

const mutations = {
    setRemember(state, remember = 0) {
        state.remember = Number(remember)
        localStorage.setItem("remember", state.remember)
    },

    setAuthData(state, {userId, permissions, token, expiration, refresher}) {
        state.userId = userId
        state.permissions = permissions
        state.token = token
        state.expiration = expiration
        state.authRefresher = refresher

        if (state.remember) {
            localStorage.setItem("userId", userId)
            localStorage.setItem("permissions", permissions)
            localStorage.setItem("token", token)
            localStorage.setItem("expiration", expiration)
        } else {
            sessionStorage.setItem("userId", userId)
            sessionStorage.setItem("permissions", permissions)
            sessionStorage.setItem("token", token)
            sessionStorage.setItem("expiration", expiration)
        }
    },

    setAuthRefresher(state, refresher) {
        state.authRefresher = refresher
    },

    setPublicRegistrationEnabled(state, enabled) {
        state.publicRegistrationEnabled = enabled
    },

    clearAuthData(state) {
        state.remember = false
        state.userId = null
        state.permissions = null
        state.token = null
        state.expiration = 0
        if (state.authRefresher !== null) {
            window.clearTimeout(state.authRefresher)
            state.authRefresher = null
        }

        localStorage.removeItem("remember")
        localStorage.removeItem("userId")
        sessionStorage.removeItem("userId")
        localStorage.removeItem("permissions")
        sessionStorage.removeItem("permissions")
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

    login({commit, dispatch}, {email, password, recaptcha_token, totp}) {
        dispatch("alert/clear", null, {root: true})

        return new Promise((resolve, reject) => {
            api.post("login", {recaptcha_token, totp}, {
                   auth:    {
                       username: email,
                       password: password
                   },
                   headers: {
                       common: {
                           "X-CSRF-TOKEN": window.csrfToken
                       }
                   }
               })
               .then(response => {
                   const data = response.data
                   if (data.token) {
                       const jwtData = JSON.parse(atob(data.token.split(".")[0]))
                       const jwtUser = JSON.parse(atob(data.token.split(".")[1]))

                       const authData = {
                           userId:      jwtUser && "id" in jwtUser ? Number(jwtUser.id) : null,
                           permissions: jwtUser && "permissions" in jwtUser ? Number(jwtUser.permissions) : 0,
                           token:       data.token,
                           expiration:  jwtData ? Number(jwtData.exp) * 1000 : 0
                       }

                       window.csrfToken = null
                       commit("setAuthData", authData)
                       dispatch("refreshToken")

                       return resolve(authData)
                   }
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }
                   return reject(error)
               })
        })
    },

    autoLogin({state, commit, dispatch}) {
        return new Promise((resolve, reject) => {
            const remember = localStorage.getItem("remember") || 0
            commit("setRemember", remember)

            const userId      = state.remember ? Number(localStorage.getItem("userId")) : Number(sessionStorage.getItem("userId")),
                  permissions = state.remember ? Number(localStorage.getItem("permissions")) : Number(sessionStorage.getItem("permissions")),
                  token       = state.remember ? localStorage.getItem("token") : sessionStorage.getItem("token"),
                  expiration  = state.remember ? Number(localStorage.getItem("expiration")) : Number(sessionStorage.getItem("expiration"))

            if (+new Date() >= expiration || !token || !userId) {
                reject()
                return
            } else if (differenceInMinutes(expiration, +new Date()) <= state.authRefreshThreshold + 1) {
                api.post("login", {}, {
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
                               userId:      jwtUser && "id" in jwtUser ? Number(jwtUser.id) : null,
                               permissions: jwtUser && "permissions" in jwtUser ? Number(jwtUser.permissions) : 0,
                               token:       data.token,
                               expiration:  jwtData ? Number(jwtData.exp) * 1000 : 0
                           }

                           commit("setAuthData", authData)
                           dispatch("refreshToken")

                           return resolve(authData)
                       }
                   })
                   .catch(() => {
                       dispatch("logout")
                   })
            } else {
                const authData = {
                    userId,
                    permissions,
                    token,
                    expiration
                }

                commit("setAuthData", authData)
                dispatch("refreshToken")

                return resolve(authData)
            }
        })
    },

    logout({state, commit, dispatch}) {
        dispatch("socket/leave", state.token, {root: true})
            .then(() => {
                dispatch("csrf/getCsrf", {}, {root: true})  // needed in order to get a new CSRF token
                    .then(() => {
                        commit("post/clearLockedPosts", {}, {root: true})
                        commit("clearAuthData")
                        router.replace({name: "Login"})
                    })
            })
    },

    refreshToken({state, commit, dispatch}) {
        const refresher = setTimeout(() => {
                                         dispatch("csrf/getCsrf", {}, {root: true}).then(() => {
                                             if (window.reCAPTCHASiteKey) {
                                                 grecaptcha.ready(() => {
                                                     grecaptcha.execute(window.reCAPTCHASiteKey, {action: "refresh_token"})
                                                               .then(token => {
                                                                   api.post("login", {recaptcha_token: token}, {
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
                                                                                  userId:      jwtUser && "id" in jwtUser ? Number(jwtUser.id) : null,
                                                                                  permissions: jwtUser && "permissions" in jwtUser ? Number(jwtUser.permissions) : 0,
                                                                                  token:       data.token,
                                                                                  expiration:  jwtData ? Number(jwtData.exp) * 1000 : 0
                                                                              }

                                                                              commit("setAuthData", authData)
                                                                              dispatch("refreshToken")
                                                                          }
                                                                      })
                                                                      .catch(() => {
                                                                          dispatch("logout")
                                                                      })
                                                               })
                                                 })
                                             } else {
                                                 api.post("login", {}, {
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
                                                                userId:      jwtUser && "id" in jwtUser ? Number(jwtUser.id) : null,
                                                                permissions: jwtUser && "permissions" in jwtUser ? Number(jwtUser.permissions) : 0,
                                                                token:       data.token,
                                                                expiration:  jwtData ? Number(jwtData.exp) * 1000 : 0
                                                            }

                                                            commit("setAuthData", authData)
                                                            dispatch("refreshToken")
                                                        }
                                                    })
                                                    .catch(() => {
                                                        dispatch("logout")
                                                    })
                                             }
                                         })
                                     },
                                     Math.max(differenceInMilliseconds(subMinutes(parse(state.expiration), state.authRefreshThreshold), new Date()), 1000))

        commit("setAuthRefresher", refresher)
    },

    setPublicSocketHooks({dispatch, rootGetters}) {
        const token = rootGetters["auth/token"]
        dispatch("socket/getPublicSocket", {}, {root: true}).then(socket => {
            socket.on("connect", () => {
                      socket.emit("authenticate", {token})
                  })
                  .on("authenticated", ({data}) => {
                      // TODO maybe do something else
                      dispatch("console/log", data, {root: true})

                      window.addEventListener("beforeunload", () => {
                          socket.emit("leave", {token})
                      })
                  })
                  .on("left", ({data}) => {
                      // TODO maybe do something else
                      dispatch("console/log", data, {root: true})
                  })
        })
    },

    setPrivateSocketHooks({dispatch, rootGetters}) {
        const token = rootGetters["auth/token"]
        dispatch("socket/getPrivateSocket", {}, {root: true}).then(socket => {
            socket.on("connect", () => {
                      socket.emit("authenticate", {token})
                  })
                  .on("authenticated", ({data}) => {
                      // TODO maybe do something else
                      dispatch("console/log", data, {root: true})

                      window.addEventListener("beforeunload", () => {
                          socket.emit("leave", {token})
                      })
                  })
                  .on("left", ({data}) => {
                      // TODO maybe do something else
                      dispatch("console/log", data, {root: true})
                  })
        })
    },

    setAdminSocketHooks({dispatch, rootGetters}) {
        const token = rootGetters["auth/token"]
        dispatch("socket/getAdminSocket", {}, {root: true}).then(socket => {
            socket.on("connect", () => {
                      socket.emit("authenticate", {token})
                  })
                  .on("authenticated", ({data}) => {
                      // TODO maybe do something else
                      dispatch("console/log", data, {root: true})

                      window.addEventListener("beforeunload", () => {
                          socket.emit("leave", {token})
                      })
                  })
                  .on("left", ({data}) => {
                      // TODO maybe do something else
                      dispatch("console/log", data, {root: true})
                  })
        })
    },

    checkIfPublicRegistrationEnabled({dispatch}) {
        return new Promise((resolve, reject) => {
            api.get("register", {
                   headers: {
                       common: {
                           "X-CSRF-TOKEN": window.csrfToken
                       }
                   }
               })
               .then(response => resolve(response))
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }

                   return reject(error)
               })
        })
    },

    verifyPasswordResetToken({dispatch}, token) {
        return new Promise((resolve, reject) => {
            api.post("reset_password", {token: token}, {
                   headers: {
                       common: {
                           "X-CSRF-TOKEN": window.csrfToken
                       }
                   }
               })
               .then(response => resolve(response))
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }

                   return reject(error)
               })
        })
    },

    confirmUserViaToken({dispatch}, token) {
        return new Promise((resolve, reject) => {
            api.post("confirm", {token: token}, {
                   headers: {
                       common: {
                           "X-CSRF-TOKEN": window.csrfToken
                       }
                   }
               })
               .then(response => {
                   dispatch("alert/success", response.data.message, {root: true})

                   return resolve(response)
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }

                   return reject(error)
               })
        })
    },

    sendAnotherConfirmationEmail({dispatch}, token) {
        return new Promise((resolve, reject) => {
            api.put("confirm", {token: token}, {
                   headers: {
                       common: {
                           "X-CSRF-TOKEN": window.csrfToken
                       }
                   }
               })
               .then(response => {
                   dispatch("alert/success", response.data.message, {root: true})

                   return resolve(response)
               })
               .catch(error => {
                   try {
                       dispatch("alert/error", error.response.data.message, {root: true})
                   } catch (e) {
                       console.log(error)
                   }

                   return reject(error)
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