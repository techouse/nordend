<template>
    <div class="row">
        <div class="col-sm-12">
            <div :id="id" :ref="cardRef" class="card">
                <div class="card-header">
                    <slot name="header"/>
                </div>
                <div class="card-body">
                    <slot name="body"/>
                </div>
                <div class="card-footer">
                    <slot name="footer"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Card",

        props: {
            cardRef: {
                type: String,
                default: "card"
            },
            id: {
                type:    String,
                default: "card"
            }
        },

        data() {
            return {
                width: 0,
                height: 0
            }
        },

        mounted() {
            this.handleWindowResize()
            window.addEventListener("resize", this.handleWindowResize)
        },

        methods: {
            handleWindowResize() {
                this.$set(this, "width", document.getElementById(this.id).clientWidth)
                this.$set(this, "height", document.getElementById(this.id).clientHeight)
            }
        }
    }
</script>