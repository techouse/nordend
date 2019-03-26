import Vue             from "vue"
import {format, parse} from "date-fns"

Vue.filter("formatDate", (value, formatString = "YYYY-MM-DD HH:mm:ss") => format(parse(value), formatString))