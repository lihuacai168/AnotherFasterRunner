export default {

    isLogin(state, value) {
        state.token = value
    },

    setUser(state, value) {
        state.user = value
    },
    setRouterName(state, value) {
        state.routerName = value
    },
    setProjectName(state, value) {
        if (value !== '' ){
            value = ' / ' + value.replaceAll('/', '').replaceAll(' ', '')
        }
        state.projectName = value
    },

    setIsSuperuser(state, value) {
        state.is_superuser = value
    },
    setShowHots(state, value) {
        state.show_hosts = value
    }
}
