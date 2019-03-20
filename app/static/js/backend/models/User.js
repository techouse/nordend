export default class User {
    constructor(values = {}) {
        this.id = null
        this.email = null
        this.password = null
        this.confirmed = null
        this.name = null
        this.location = null
        this.about_me = null
        this.member_since = null
        this.last_seen = null
        this.created_at = null
        this.updated_at = null
        this.role = null

        Object.assign(this, values)
    }

    mappedForSubmission() {
        let data = {
            email:     this.email,
            confirmed: this.confirmed,
            name:      this.name,
            location:  this.location,
            about_me:  this.about_me,
            role_id:   this.role.id,
        }
        if (this.password) {
            data["password"] = this.password
        }
    }
}