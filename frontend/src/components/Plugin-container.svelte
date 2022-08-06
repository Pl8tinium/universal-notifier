<script lang="ts">
    import Plugin from '../models/plugin';
    export let plugin: Plugin;
    import * as emoji from 'node-emoji';


</script>

<style>
    .main-plugin {
        height: 400px;
        width: 300px;
        background-color: rgb(172, 172, 172);
        display: grid;
    }

</style>

{#if plugin.active}
    <div class="main-plugin">
        <p>Name: {plugin.name}</p>
        <p>Website: {plugin.website}</p>
        <p>Check interval: {plugin.checkInterval}</p>
        <p>Last checked: {plugin.lastChecked}</p>
        <p>State: {plugin.state ?  emoji.get('alien'): emoji.get('japanese_goblin')}</p>
    </div>
{/if}