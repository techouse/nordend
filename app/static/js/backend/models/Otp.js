export default class Otp {
    constructor(values = {}) {
        this.secret = null
        this.uri = null
        this.recaptcha_token = null
        this.totp = null

        Object.assign(this, values)
    }

    mappedForSubmission() {
        return {
            recaptcha_token: this.recaptcha_token,
            totp:            this.totp
        }
    }
}