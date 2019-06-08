<template>
    <div class="app flex-row align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <slot name="body" />
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Centered"
    }
</script>