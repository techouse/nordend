import {locales}               from "moment/src/locale/extracted"
import DateTimeFormatConverter from "../../utils/DateTimeFormatConverter"

const state = {
    language:     navigator.language,
    momentFormat: navigator.language.toLowerCase() in locales ? locales[navigator.language.toLowerCase()] : locales["en"]
}

const getters = {
    dateFormat: state => DateTimeFormatConverter.momentToElementUi(state.momentFormat.L),
    timeFormat: state => DateTimeFormatConverter.momentToElementUi(state.momentFormat.LTS),
    shortTimeFormat: state => DateTimeFormatConverter.momentToElementUi(state.momentFormat.LT),
}

const mutations = {}

const actions = {}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}