export default class Image {
    constructor(values = {}) {
        this.id = null
        this.title = null
        this.author_id = null
        this.public_path = null
        this.original_filename = null
        this.sizes = []
        this.created_at = null
        this.data_url = null

        Object.assign(this, values)

        if (this.created_at) {
            this.created_at = new Date(this.created_at)
        }

        if (this.sizes.length > 0) {
            this.sizes = this.sizes
                             .map(size => Number(size))
                             .filter(size => size >= 440) // Minimum size for srcset
                             .sort((a, b) => a - b)
        }
    }

    mappedForSubmission() {
        return {
            title:             this.title,
            author_id:         this.author_id,
            original_filename: this.original_filename,
            data_url:          this.data_url
        }
    }

    static getMediaBreakPoint(size = 0) {
        switch (true) {
            case Number(size) >= 1200:
                // Extra large devices (large desktops, 1200px and up)
                return "(min-width: 1200px)"
            case Number(size) >= 992 && Number(size) < 1200:
                // Large devices (desktops, 992px and up)
                return "(min-width: 992px) and (max-width: 1199.98px)"
            case Number(size) >= 768 && Number(size) < 992:
                // Medium devices (tablets, 768px and up)
                return "(min-width: 768px) and (max-width: 991.98px)"
            case Number(size) >= 576 && Number(size) < 768:
                // Small devices (landscape phones, 576px and up)
                return "(min-width: 576px) and (max-width: 767.98px)"
            case Number(size) < 576:
            default:
                // Extra small devices (portrait phones, less than 576px)
                return "(max-width: 575.98px)"
        }
    }
}