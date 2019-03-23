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

        Object.assign(this, values)
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