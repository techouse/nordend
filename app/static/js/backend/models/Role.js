export default class Role {
    constructor(values = {}) {
        this.id = null
        this.name = null
        this.default = false
        this.permissions = 0

        Object.assign(this, values)
    }

    mappedForSubmission() {
        return {
            name:        this.name,
            default:     this.default,
            permissions: this.permissions
        }
    }
}