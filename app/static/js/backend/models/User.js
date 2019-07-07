export default class User {
    constructor(values = {}) {
        this.id = null
        this.email = null
        this.password = null
        this.password_repeat = null
        this.confirmed = null
        this.name = null
        this.location = null
        this.about_me = null
        this.member_since = null
        this.last_seen = null
        this.created_at = null
        this.updated_at = null
        this.role = null
        this.role_id = null
        this.otp_enabled = false

        Object.assign(this, values)

        if (this.created_at) {
            this.created_at = new Date(this.created_at)
        }

        if (this.updated_at) {
            this.updated_at = new Date(this.updated_at)
        }
    }

    mappedForSubmission() {
        let data = {
            email:     this.email,
            confirmed: Number(this.confirmed),
            name:      this.name,
            location:  this.location,
            about_me:  this.about_me,
            role_id:   this.role_id,
        }
        if (this.password && this.password === this.password_repeat) {
            data["password"] = this.password
        }
        return data
    }
}