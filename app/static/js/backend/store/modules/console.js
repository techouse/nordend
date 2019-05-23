import {format} from "date-fns"

const state = {
    format: "YYYY-MM-DD HH:mm:ss Z"
}

const actions = {
    log:   ({state}, message) => console.log(`[${format(new Date(), state.format)}] ${message}`),
    warn:  ({state}, message) => console.warn(`[${format(new Date(), state.format)}] ${message}`),
    error: ({state}, message) => console.error(`[${format(new Date(), state.format)}] ${message}`),
    info:  ({state}, message) => console.info(`[${format(new Date(), state.format)}] ${message}`),
}

export default {
    namespaced: true,
    state,
    actions
}