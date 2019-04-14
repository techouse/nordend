export default class Photo {
    constructor(values = {}) {
        this.id = null
        this.title = null
        this.author_id = null
        this.public_path = null
        this.original_filename = null
        this.sizes = {}
        this.created_at = null

        Object.assign(this, values)
    }
}