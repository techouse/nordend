import Vue             from "vue"
import {format, parse} from "date-fns"

Vue.filter("formatDate", (value, formatString = "YYYY-MM-DD HH:mm:ss") => format(parse(value), formatString))

Vue.filter("truncate", (fullStr, strLen, separator = "...") => {
    if (fullStr.length <= strLen) {
        return fullStr
    }

    const sepLen = separator.length
    const charsToShow = strLen - sepLen
    const frontChars = Math.ceil(charsToShow / 2)
    const backChars = Math.floor(charsToShow / 2)

    return fullStr.substr(0, frontChars) + separator + fullStr.substr(fullStr.length - backChars)
})