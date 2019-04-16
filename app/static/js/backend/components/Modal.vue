<template>
    <div class="modal fade" role="dialog" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">
                        <slot name="title" />
                    </h4>
                    <button class="close" data-dismiss="modal" aria-label="Close" @click.prevent="$emit('close')">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <slot name="body" />
                </div>
                <div class="modal-footer">
                    <slot name="footer" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Modal",
    }
</script>

<style lang="scss" scoped>
    .modal {
        overflow-y: auto !important;
        overflow-x: hidden;

        &.show {
            display: block;
        }

        background: rgba(0, 0, 0, .5);
    }
</style>