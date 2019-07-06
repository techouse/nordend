import User     from "./User"
import Category from "./Category"
import Photo    from "./Image"
import Tag      from "./Tag"

export default class Post {
    constructor(values = {}) {
        this.id = null
        this.slug = null
        this.title = null
        this.sub_title = null
        this.body = null
        this.body_html = null
        this.author = null
        this.author_id = null
        this.authors = []
        this.author_ids = []
        this.category = null
        this.category_id = null
        this.additional_categories = []
        this.additional_category_ids = []
        this.tags = []
        this.tag_ids = []
        this.related = []
        this.related_ids = []
        this.image = null
        this.images = []
        this.draft = true
        this.published = false
        this.published_at = null
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

        if (this.authors) {
            this.authors = this.authors
                               .filter(el => el.primary === false)
                               .map(el => el.user)
            this.author_ids = this.authors.map(el => el.id)
        }

        if (this.category) {
            this.category = new Category(this.category)
            this.category_id = this.category.id
        }

        if (this.additional_categories) {
            this.additional_categories = this.additional_categories
                                             .map(el => el.category)
            this.additional_category_ids = this.additional_categories.map(el => el.id)
        }

        if (this.tags) {
            this.tags = this.tags.map(el => new Tag(el.tag))
            this.tag_ids = this.tags.map(el => el.id)
        }

        if (this.related) {
            this.related = this.related.map(el => new Post(el))
            this.related_ids = this.related.map(el => el.id)
        }

        if (this.image) {
            this.image = new Photo(this.image)
        }

        if (this.published_at) {
            this.published_at = new Date(this.published_at)
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
            slug:                    this.slug,
            title:                   this.title,
            sub_title:               this.sub_title,
            body:                    this.body,
            category_id:             this.category_id,
            additional_category_ids: this.additional_category_ids,
            tag_ids:                 this.tag_ids,
            related_ids:             this.related_ids,
            draft:                   this.draft,
            image_id:                this.image ? this.image.id : null,
            published:               this.published_at instanceof Date ? this.published_at.toISOString() : null
        }
    }
}