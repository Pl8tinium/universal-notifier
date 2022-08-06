import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/getplugins': 'http://localhost:5000',
			'/editplugins': 'http://localhost:5000',
		},
	},
};

export default config;
