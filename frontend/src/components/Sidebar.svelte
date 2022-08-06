<script lang="ts"> 
     export let display = 'home';
</script>

<style>
    .main-sidebar {
        height: 100%;
        display: grid;
        justify-items: center;
        align-items: center;
    }
</style>

<div class="main-sidebar">
    <button on:click={() => display = 'home'}>Home</button>
    <button on:click={() => display = 'settings'}>Settings</button>
</div>