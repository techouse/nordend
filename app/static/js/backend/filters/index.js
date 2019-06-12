import Vue             from "vue"
import {format, parse} from "date-fns"

Vue.filter("formatDate", (value, formatString = "YYYY-MM-DD HH:mm:ss") => format(parse(value), formatString))

Vue.filter("truncate", (text = "", length = 30, clamp = "...") => {
    if (text.length <= length) {
        return text
    }

    let tcText = text.slice(0, length - clamp.length),
        last = tcText.length - 1

    while (last > 0 && tcText[last] !== " " && tcText[last] !== clamp[0]) {
        last -= 1
    }

    // Fix for case when text dont have any `space`
    last = last || length - clamp.length
    tcText = tcText.slice(0, last)

    return tcText + clamp
})

Vue.filter("truncate_middle", (fullStr, strLen, separator = "...") => {
    if (fullStr.length <= strLen) {
        return fullStr
    }

    const sepLen = separator.length
    const charsToShow = strLen - sepLen
    const frontChars = Math.ceil(charsToShow / 2)
    const backChars = Math.floor(charsToShow / 2)

    return fullStr.substr(0, frontChars) + separator + fullStr.substr(fullStr.length - backChars)
})