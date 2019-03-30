<template>
    <div class="row">
        <div class="col-sm-12">
            <div class="card">
                <div class="card-header">
                    <slot name="header"/>
                </div>
                <div class="card-body">
                    <slot name="body"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Card",
    }
</script>