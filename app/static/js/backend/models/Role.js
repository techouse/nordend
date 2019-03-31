export default class Role {
    constructor(values = {}) {
        this.id = null
        this.name = null
        this.default = false
        this.permissions = 0
        this.follow = false
        this.comment = false
        this.write = false
        this.moderate = false
        this.admin = false

        Object.assign(this, values)
    }

    mappedForSubmission() {
        let permissions = 0
        if (this.follow) permissions += 1
        if (this.comment) permissions += 2
        if (this.write) permissions += 4
        if (this.moderate) permissions += 8
        if (this.admin) permissions += 16

        return {
            name:        this.name,
            default:     this.default,
            permissions: permissions
        }
    }
}