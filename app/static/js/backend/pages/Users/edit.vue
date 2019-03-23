<template>
    <div>
        <div class="row">
            <div class="col-sm-12">
                <div class="card">
                    <div class="card-header">
                        <b>Edit user</b> <i>{{ user.name }}</i>
                        <div class="card-header-actions">
                            <a class="btn btn-sm btn-danger" href="#">
                                Delete
                            </a>
                        </div>
                    </div>
                    <div class="card-body">
                        Edit user here {{ userId }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapActions} from "vuex"
    import User         from "../../models/User"

    export default {
        name: "User",

        props: {
            userId: {
                type: [String, Number],
                required: true
            }
        },

        data() {
            return {
                user: null
            }
        },

        created() {
            this.getUser(this.userId)
                .then(({data}) => {
                    this.$set(this, "user", new User(data))
                })
        },

        methods: {
            ...mapActions("user", ["getUser"])
        }
    }
</script>