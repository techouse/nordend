/**
 * Setting __webpack_public_path__ is a hacky solution but there is no other
 * way changing the URL from which WebPack fetches chunks.
 */
__webpack_public_path__ = ("/static/dist/" + __webpack_public_path__)

try {
    window.Popper = require("popper.js").default
    window.$ = window.jQuery = require("jquery")

    require("bootstrap")
} catch (e) {
}