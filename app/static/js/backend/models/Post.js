import User     from "./User"
import Category from "./Category"

export default class Post {
    constructor(values = {}) {
        this.id = null
        this.slug = null
        this.title = null
        this.body = null
        this.body_html = null
        this.author_id = null
        this.author = null
        this.category_id = null
        this.category = null
        this.created_at = null
        this.updated_at = null
        this.locked = false
        this.locked_since = null
        this.lock_expires = null
        this.locked_by = null

        Object.assign(this, values)

        if (this.author) {
            this.author = new User(this.author)
        }

        if (this.category) {
            this.category = new Category(this.category)
        }

        if (this.created_at) {
            this.created_at = new Date(this.created_at)
        }

        if (this.updated_at) {
            this.updated_at = new Date(this.updated_at)
        }

        if (this.locked_since) {
            this.locked_since = new Date(this.locked_since)
        }

        if (this.lock_expires) {
            this.lock_expires = new Date(this.lock_expires)
        }

        if (this.locked_by) {
            this.locked_by = new User(this.locked_by)
        }
    }

    mappedForSubmission() {
        return {
            slug:        this.slug,
            title:       this.title,
            body:        this.body,
            category_id: this.category_id
        }
    }
}