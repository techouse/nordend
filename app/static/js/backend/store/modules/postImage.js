import Photo from "../../models/Image"

const state = {
    image:         null,
    editedImage:   null,
    editorVisible: false
}

const getters = {
    image:         state => state.image,
    editorVisible: state => state.editorVisible,
    editedImage:   state => state.editedImage,
}

const mutations = {
    setImage:         (state, image) => {
        state.image = image
    },
    setEditorVisible: (state, visible = true) => {
        state.editorVisible = visible
    },
    setEditedImage:   (state, image) => {
        state.editedImage = image
    }
}

const actions = {
    showEditor: ({commit, dispatch}, imageId) => {
        commit("setEditedImage", null)
        dispatch("image/getImage", imageId, {root: true})
            .then(({data}) => {
                commit("setImage", new Photo(data))
                commit("setEditorVisible", true)
            })
    },

    hideEditor: ({commit}) => {
        commit("setEditorVisible", false)
        commit("setImage", false)
    },

    storeEditedImage({commit}, image) {
        commit("setEditedImage", image)
    },

    clearEditedImage({commit}) {
        commit("setEditedImage", null)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}