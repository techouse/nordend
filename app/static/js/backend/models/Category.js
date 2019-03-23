export default class Category {
    constructor(values = {}) {
        this.id = null
        this.slug = null
        this.name = null

        Object.assign(this, values)
    }

    mappedForSubmission() {
        return {
            slug: this.slug,
            name: this.name
        }
    }
}