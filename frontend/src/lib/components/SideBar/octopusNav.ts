/*
 * Octopus Lab: menu boczne pod NIS2/KSC i ISO 27001 (uklad uzgodniony 26.10.2026, przebudowa 27.10.2026:
 * Centrum operacyjne na gorze, praca biezaca w Centrum operacyjnym, konfiguracja w Administracji).
 *
 * Plik upstream navData.ts zostaje bez zmian (latwiejsze aktualizacje). Tutaj wybieramy pozycje
 * po nazwie i ukladamy je w trzy kategorie na gorze. Wszystkie pozostale pozycje trafiaja do
 * kategorii "Dodatkowe" (najpierw te z listy EXTRA_FIRST, potem reszta w kolejnosci upstream).
 * Uprawnienia i flagi funkcji dzialaja jak w upstream. Nazwy pozycji pochodza z messages/*.json.
 */
import { navData as upstreamNav } from './navData';

type NavEntry = (typeof upstreamNav.items)[number]['items'][number];

// Kategorie rozwiniete przy pierwszym wejsciu (potem menu pamieta wybor uzytkownika)
export const OCTO_DEFAULT_OPEN = ['octoNavOperations'];

const LAYOUT: { name: string; items: string[] }[] = [
	{
		name: 'octoNavOperations',
		items: [
			'analytics',
			'myAssignments',
			'tasksReview',
			'tasks',
			'calendar',
			'incidents',
			'findings',
			'assets'
		]
	},
	{
		name: 'octoNavCompliance',
		items: [
			'frameworks',
			'threats',
			'policies',
			'riskScenarios',
			'riskMatrices',
			'riskAssessments',
			'riskAcceptances',
			'securityExceptions',
			'appliedControls',
			'entities',
			'entityAssessments',
			'contracts',
			'evidences',
			'reports',
			'complianceAssessments',
			'followUp'
		]
	},
	{
		name: 'octoNavAdmin',
		items: [
			'domains',
			'perimeters',
			'presets',
			'users',
			'userGroups',
			'libraries',
			'settings',
			'backupRestore'
		]
	}
];

// Na poczatku "Dodatkowe": pozycje uzywane w pracy z SZBI, ktorych nie ma w kategoriach wyzej
const EXTRA_FIRST = [
	'notifications',
	'referenceControls',
	'requirementMappingSets',
	'solutions',
	'tprmOverview',
	'criticality',
	'representatives',
	'labels',
	'assetClasses',
	'terminologies',
	'teams'
];

// Pozycje o tej samej nazwie w roznych miejscach upstream (np. dwa razy "Przeglad"): wlasna etykieta
const RENAME: Record<string, string> = {
	'/analytics/gdpr': 'octoNavGdprOverview'
};

const allEntries: NavEntry[] = upstreamNav.items
	.flatMap((group) => group.items as NavEntry[])
	.map((e) => (e.href && RENAME[e.href] ? ({ ...e, name: RENAME[e.href] } as NavEntry) : e));
const byName = new Map<string, NavEntry>();
for (const entry of allEntries) {
	if (entry.name && !byName.has(entry.name)) byName.set(entry.name, entry);
}
const pick = (names: string[]) =>
	names.map((n) => byName.get(n)).filter((e): e is NavEntry => Boolean(e));

const groups = LAYOUT.map((group) => ({ name: group.name, items: pick(group.items) }));
const used = new Set<NavEntry>(groups.flatMap((g) => g.items));
const extraFirst = pick(EXTRA_FIRST).filter((e) => !used.has(e));
extraFirst.forEach((e) => used.add(e));
const extraRest = allEntries.filter((e) => !used.has(e));

export const navData = {
	...upstreamNav,
	items: [...groups, { name: 'extra', items: [...extraFirst, ...extraRest] }]
} as typeof upstreamNav;
