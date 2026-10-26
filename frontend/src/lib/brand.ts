/*
 * Octopus Lab: jedno miejsce na nazwe produktu, linki i dane wsparcia.
 * CISO Assistant by Octopus Lab to CISO Assistant Community Edition (intuitem, AGPL v3)
 * z konfiguracja pod NIS2/KSC i ISO 27001 przygotowana przez Octopus Lab.
 */
import { getLocale } from '$paraglide/runtime';

export const BRAND = {
	name: 'CISO Assistant by Octopus Lab',
	shortName: 'CISO Assistant',
	vendor: 'Octopus Lab',
	vendorUrl: 'https://octopus-lab.pl',
	supportEmail: 'dr@octopus-lab.pl',
	// AGPL v3, par. 13: uzytkownicy instancji sieciowej musza miec dostep do kodu zrodlowego
	sourceUrl: 'https://github.com/rulkdo/ciso-assistant-octopus',
	upstreamName: 'CISO Assistant Community Edition (intuitem)',
	upstreamUrl: 'https://github.com/intuitem/ciso-assistant-community',
	upstreamVersion: 'v4.1.5'
} as const;

const LABELS = {
	pl: { source: 'Kod źródłowy (AGPL v3)', support: 'Wsparcie Octopus Lab' },
	en: { source: 'Source code (AGPL v3)', support: 'Octopus Lab support' }
} as const;

export function brandLabel(key: keyof (typeof LABELS)['en']): string {
	const lang = getLocale() === 'pl' ? 'pl' : 'en';
	return LABELS[lang][key];
}
