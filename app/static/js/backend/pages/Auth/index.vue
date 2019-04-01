<template>
    <div class="app flex-row align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <router-view/>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Auth",
    }
</script>