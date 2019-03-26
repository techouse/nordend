import api from "./api"

export const get = (context, url, params = {}) => new Promise((resolve, reject) => {
    api.get(url, params)
       .then(response => {
           resolve(response)
       })
       .catch(error => {
           try {
               context.dispatch("alert/error", error.response.data.message, {root: true})
           } catch (e) {
               console.error(error)
           }
           reject(error)
       })
})

export const create = (context, url, model) => new Promise((resolve, reject) => {
    api({
            method: "post",
            url:    url,
            data:   typeof model.mappedForSubmission === "function" ? model.mappedForSubmission() : model
        })
        .then(response => {
            resolve(response)
        })
        .catch(error => {
            try {
                context.dispatch("alert/error", error.response.data.message, {root: true})
            } catch (e) {
                console.error(error)
            }
            reject(error)
        })
})

export const update = (context, url, model) => new Promise((resolve, reject) => {
    api({
            method: "patch",
            url:    url,
            data:   typeof model.mappedForSubmission === "function" ? model.mappedForSubmission() : model
        })
        .then(response => {
            resolve(response)
        })
        .catch(error => {
            try {
                context.dispatch("alert/error", error.response.data.message, {root: true})
            } catch (e) {
                console.error(error)
            }
            reject(error)
        })
})

export const destroy = (context, url) => new Promise((resolve, reject) => {
    api.delete(url)
       .then(response => {
           resolve(response)
       })
       .catch(error => {
           try {
               context.dispatch("alert/error", error.response.data.message, {root: true})
           } catch (e) {
               console.error(error)
           }
           reject(error)
       })
})