const Permission = {
    follow:   1,
    comment:  2,
    write:    4,
    moderate: 8,
    admin:    16
}

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
        if (this.follow) permissions += Permission.follow
        if (this.comment) permissions += Permission.comment
        if (this.write) permissions += Permission.write
        if (this.moderate) permissions += Permission.moderate
        if (this.admin) permissions += Permission.admin

        return {
            name:        this.name,
            default:     this.default,
            permissions: permissions
        }
    }

    static createFromPermissions(permissions = 0) {
        return new Role(
            {
                permissions,
                follow:   (permissions & Permission.follow) === Permission.follow,
                comment:  (permissions & Permission.comment) === Permission.comment,
                write:    (permissions & Permission.write) === Permission.write,
                moderate: (permissions & Permission.moderate) === Permission.moderate,
                admin:    (permissions & Permission.admin) === Permission.admin
            }
        )
    }
}