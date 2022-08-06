<script lang="ts">
    import Plugin from '../models/plugin';
    export let plugins: Array<Plugin>;
    let editPlugins: Array<Plugin> = plugins;

    function updatePlugin(plugin: Plugin) {
        fetch('http://127.0.0.1:5173/editplugins', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(plugin),
            })
        .then((data) => {
            if (data.ok) {
                alert("Success")
            }
            else {
                alert("Error")
                location.reload()
            }
        })
    }
</script>

<style>
    .main-settings {
        width: 100%;
        height: 100%;
        background-color: rgb(172, 172, 172);
        display: grid;
    }

</style>

<div class="main-settings">
    <table>
        <tr>
            <th>Name</th>
            <th>Website</th>
            <th>Check interval</th>
            <th>Script</th>
            <th>Active</th>
        </tr>
        {#each editPlugins as plugin}
            <tr>
                <td><input bind:value={plugin.name}></td>
                <td><input bind:value={plugin.website}></td>
                <td><input type=number bind:value={plugin.checkInterval}></td>
                <td><input bind:value={plugin.script}></td>
                <td><input type=checkbox bind:checked={plugin.active}></td>
                <td><button on:click={() => updatePlugin(plugin)}>Update</button></td>
            </tr>
        {/each}
    </table>
    <button on:click={() => editPlugins = [...editPlugins, new Plugin()]}>Add new</button>
</div>