<script lang="ts">
    import Sidebar from '../components/Sidebar.svelte';
    import PluginContainer from '../components/Plugin-container.svelte';
    import PluginSettings from '../components/Plugin-settings.svelte';
    import Plugin from '../models/plugin';
    import { onMount } from 'svelte'

    let display: any;
    let plugins: Array<Plugin> = []

    function fetchPlugins() {
        fetch('http://127.0.0.1:5173/getplugins').then(response => {
            if (!response.ok) {
                throw new Error(response.statusText)
            }
            return response.json()
        })
        .then(response => {
            plugins = Object.values(response);
        })
    }

    //load plugins... do this frequently for updates
    onMount(() => {
        fetchPlugins();
        const fetchInterval = 20000;
        setInterval(fetchPlugins, fetchInterval);
    })
</script>

<style>
    .content {
        grid-area: content;
        padding: 10px;

    }
    
    .home-plugins {
        height: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-evenly;
        align-content: space-around;
    }

	.sidebar {
        grid-area: sidebar;
    }
    
    .main-container {
        height: 100vh;
        width: 100vw;
        display: grid;
        grid-template-columns: 15% auto;
        grid-template-areas: "sidebar content"
    }
</style>

<div class="main-container">
    <div class="sidebar">
        <Sidebar bind:display={display}/>
    </div>
    <div class="content">
        {#if display == 'home'}
            <div class="home-plugins">
                {#each plugins as plugin}
                    <PluginContainer plugin={plugin}/>
                {/each}                
            </div>
        {:else if display == 'settings'}
            <PluginSettings plugins={plugins}/>
        {:else}
            <p>404</p>
        {/if}

    </div>    
</div>

