<template>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="clearfix">
                <h1 class="float-left display-3 mr-4">
                    <slot name="error_code"/>
                </h1>
                <h4 class="pt-3">
                    <slot name="title"/>
                </h4>
                <p class="text-muted">
                    <slot name="content"/>
                </p>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Error"
    }
</script>