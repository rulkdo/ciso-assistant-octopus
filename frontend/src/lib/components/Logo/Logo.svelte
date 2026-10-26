<script lang="ts">
	// Octopus Lab: logo "CISO Assistant by Octopus Lab" w wersji jasnej i ciemnej
	import logoLight from '$lib/assets/octopus-logo-light.svg';
	import logoDark from '$lib/assets/octopus-logo-dark.svg';
	import { BRAND } from '$lib/brand';

	interface Props {
		height?: number;
		width?: number;
	}

	// height zostaje dla zgodnosci z wywolaniami upstream; logo skaluje sie po szerokosci
	let { height = 200, width = 200 }: Props = $props();
</script>

<img
	class="c block dark:hidden"
	{width}
	style="height:auto; max-height:{height}px"
	src={logoLight}
	alt={BRAND.name}
	data-testid="logo-image"
/>
<img
	class="c hidden dark:block"
	{width}
	style="height:auto; max-height:{height}px"
	src={logoDark}
	alt={BRAND.name}
/>
