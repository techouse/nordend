require("../bootstrap")

import Vue    from "vue"
import Viewer from "v-viewer"
import router from "./router"
import store  from "./store"
import api    from "./services/api"
import App    from "./App"
import {
    Breadcrumb,
    BreadcrumbItem,
    Button,
    ButtonGroup,
    Card,
    Checkbox,
    Col,
    Container,
    DatePicker,
    Dropdown,
    DropdownItem,
    DropdownMenu,
    Form,
    FormItem,
    Image,
    Input,
    InputNumber,
    Loading,
    Menu,
    MenuItem,
    Message,
    MessageBox,
    Notification,
    Option,
    PageHeader,
    Pagination,
    Popover,
    Row,
    Select,
    Switch,
    Table,
    TableColumn,
    TabPane,
    Tabs,
    Tag,
    TimePicker,
    Tooltip,
    Upload,
}             from "element-ui"

// Set Axios as default resource handler
Vue.prototype.$http = api

// ElementUI
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Button)
Vue.use(ButtonGroup)
Vue.use(Card)
Vue.use(Checkbox)
Vue.use(Col)
Vue.use(Container)
Vue.use(DatePicker)
Vue.use(Dropdown)
Vue.use(DropdownItem)
Vue.use(DropdownMenu)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Image)
Vue.use(Input)
Vue.use(InputNumber)
Vue.use(Loading.directive)
Vue.use(Menu)
Vue.use(MenuItem)
Vue.use(Option)
Vue.use(PageHeader)
Vue.use(Pagination)
Vue.use(Popover)
Vue.use(Row)
Vue.use(Select)
Vue.use(Switch)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(TabPane)
Vue.use(Tabs)
Vue.use(Tag)
Vue.use(TimePicker)
Vue.use(Tooltip)
Vue.use(Upload)

Vue.prototype.$loading = Loading.service
Vue.prototype.$msgbox = MessageBox
Vue.prototype.$alert = MessageBox.alert
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$prompt = MessageBox.prompt
Vue.prototype.$notify = Notification
Vue.prototype.$message = Message


// V-Viewer
Vue.use(Viewer)

// Set all the custom filters
import "./filters"

new Vue(
    {
        el:     "#app",
        router,
        store,
        render: h => h(App)
    }
)