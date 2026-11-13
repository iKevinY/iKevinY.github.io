import { AtpAgent } from '@atproto/api';
import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir, realpath, readdir } from 'node:fs/promises';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const publishing = fileURLToPath(new URL('./', import.meta.url));
const readJson = async (filename) => JSON.parse(await readFile(filename, 'utf8'));

function runSequoia(args, env = process.env) {
  const cli = path.join(publishing, 'node_modules/sequoia-cli/dist/index.js');
  const result = spawnSync(process.execPath, [cli, ...args], {
    cwd: publishing, env, encoding: 'utf8', maxBuffer: 10 * 1024 * 1024,
  });
  process.stdout.write(result.stdout || '');
  process.stderr.write(result.stderr || '');
  // Sequoia 0.5.8 reports individual publication errors with exit status zero.
  const syncFailed = args[0] === 'sync' && !result.stdout?.includes('Sync complete!');
  const imageUploadFailed = result.stderr?.includes('Error uploading image');
  if (result.error || result.status !== 0 || syncFailed || imageUploadFailed || /Errors:\s*[1-9]\d*/.test(result.stdout)) {
    throw new Error(`Sequoia ${args[0]} failed`, { cause: result.error });
  }
  return result.stdout;
}

export function publicationParts(config) {
  const match = config.publicationUri.match(/^at:\/\/(did:plc:[a-z2-7]+)\/site\.standard\.publication\/([a-zA-Z0-9._~:-]+)$/);
  if (!match) throw new Error('Invalid publicationUri in sequoia.json');
  if (!/^[234567abcdefghij][234567abcdefghijklmnopqrstuvwxyz]{12}$/.test(match[2])) {
    throw new Error('publicationUri must use a valid TID record key in sequoia.json');
  }
  return { did: match[1], rkey: match[2] };
}

async function fetchChecked(url) {
  const response = await fetch(url, { signal: AbortSignal.timeout(15000) });
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${url}`);
  return response;
}

async function resolvePds(did) {
  let service = process.env.PDS_URL;
  if (!service) {
    const response = await fetchChecked(`https://plc.directory/${did}`);
    const document = await response.json();
    service = document.service?.find((entry) => entry.type === 'AtprotoPersonalDataServer')?.serviceEndpoint;
    if (!service) throw new Error('No PDS found in the publication author’s DID document.');
  }
  return service;
}

async function ensurePublication(config) {
  const { did, rkey } = publicationParts(config);
  if (!process.env.ATP_APP_PASSWORD) {
    throw new Error('Set ATP_APP_PASSWORD to an AT Protocol app password before publishing.');
  }
  const service = await resolvePds(did);
  const agent = new AtpAgent({ service });
  const identifier = process.env.ATP_IDENTIFIER || config.identity;
  const session = await agent.login({ identifier, password: process.env.ATP_APP_PASSWORD });
  if (session.data.did !== did) throw new Error('The authenticated account does not own publicationUri.');

  // Reuse this exact publication. Never modify another publication on the account.
  let existing;
  try {
    existing = await agent.com.atproto.repo.getRecord({
      repo: did, collection: 'site.standard.publication', rkey,
    });
  } catch (error) {
    if (error.error !== 'RecordNotFound') throw error;
  }
  if (existing) {
    if (existing.data.value.url !== config.siteUrl) {
      throw new Error('Existing publication URL differs from siteUrl; refusing to overwrite it.');
    }
  } else {
    // Check for a publication made by another client before creating a new one.
    let cursor;
    do {
      const page = await agent.com.atproto.repo.listRecords({
        repo: did, collection: 'site.standard.publication', limit: 100, cursor,
      });
      const sameSite = page.data.records.find((record) => record.value.url === config.siteUrl);
      if (sameSite) throw new Error(`Publication already exists. Set publicationUri to ${sameSite.uri}`);
      cursor = page.data.cursor;
    } while (cursor);
    const icon = await agent.uploadBlob(await readFile(path.join(root, 'content/images/icons/avatar.png')), {
      encoding: 'image/png',
    });
    await agent.com.atproto.repo.createRecord({
      repo: did, collection: 'site.standard.publication', rkey,
      record: {
        $type: 'site.standard.publication', url: config.siteUrl, name: 'Kevin Yap',
        createdAt: new Date().toISOString(),
        description: 'Website and blog of Kevin Yap, a software engineer from Vancouver, Canada.',
        icon: icon.data.blob, preferences: { showInDiscover: true },
      },
    });
    console.log(`Created publication: ${config.publicationUri}`);
  }
  return { ...process.env, ATP_IDENTIFIER: identifier, PDS_URL: service };
}

function linkTargets(html, relation) {
  const head = html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i)?.[1] || '';
  return [...head.matchAll(/<link\b([^>]+)>/gi)].flatMap((match) => {
    const attrs = Object.fromEntries([...match[1].matchAll(/([\w:-]+)\s*=\s*(["'])(.*?)\2/g)]
      .map((attr) => [attr[1].toLowerCase(), attr[3]]));
    return attrs.rel === relation ? [attrs.href] : [];
  });
}

async function htmlFiles(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await htmlFiles(filename));
    else if (entry.isFile() && entry.name.endsWith('.html')) files.push(filename);
  }
  return files;
}

async function injectPublicationDiscovery(config) {
  const output = path.resolve(publishing, config.outputDir);
  for (const filename of await htmlFiles(output)) {
    const html = await readFile(filename, 'utf8');
    const targets = linkTargets(html, 'site.standard.publication');
    if (targets.length === 1 && targets[0] === config.publicationUri) continue;
    if (targets.length || !/<\/head>/i.test(html)) {
      throw new Error(`Cannot add publication discovery link: ${path.relative(output, filename)}`);
    }
    const tag = `<link rel="site.standard.publication" href="${config.publicationUri}">`;
    await writeFile(filename, html.replace(/<\/head>/i, `  ${tag}\n</head>`));
  }
}

export async function verify(config, manifest, base = publishing) {
  const { did } = publicationParts(config);
  const state = await readJson(path.join(base, '.sequoia-state.json'));
  const output = path.resolve(base, config.outputDir);
  const endpoint = await readFile(path.join(output, '.well-known/site.standard.publication'), 'utf8');
  if (endpoint.trim() !== config.publicationUri) throw new Error('Publication verification endpoint is incorrect.');
  for (const post of manifest) {
    const entry = state.posts[post.file];
    if (!entry?.atUri?.startsWith(`at://${did}/site.standard.document/`)) {
      throw new Error(`Missing published document: ${post.path}`);
    }
    const raw = await readFile(path.join(base, post.file));
    const hash = createHash('sha256').update(raw);
    // Sequoia includes the cover's base64 bytes in its content hash.
    if (post.coverImage) hash.update(await readFile(path.resolve(base, post.coverImage), 'base64'));
    if (entry.contentHash !== hash.digest('hex')) throw new Error(`Publication state is stale: ${post.path}`);
    const html = await readFile(path.join(output, post.saveAs), 'utf8');
    for (const [relation, uri] of [
      ['site.standard.document', entry.atUri], ['site.standard.publication', config.publicationUri],
    ]) {
      const targets = linkTargets(html, relation);
      if (targets.length !== 1 || targets[0] !== uri) {
        throw new Error(`Missing or incorrect ${relation} link: ${post.path}`);
      }
    }
  }
  const pages = await htmlFiles(output);
  for (const filename of pages) {
    const targets = linkTargets(await readFile(filename, 'utf8'), 'site.standard.publication');
    if (targets.length !== 1 || targets[0] !== config.publicationUri) {
      throw new Error(`Missing or incorrect publication discovery link: ${path.relative(output, filename)}`);
    }
  }
  console.log(`Verified publication endpoint, ${manifest.length} article links, and discovery links on ${pages.length} pages.`);
}

async function verifyLive(config, manifest) {
  const { did, rkey } = publicationParts(config);
  const endpoint = new URL('/.well-known/site.standard.publication', config.siteUrl);
  if ((await (await fetchChecked(endpoint)).text()).trim() !== config.publicationUri) {
    throw new Error('Live publication verification endpoint is incorrect.');
  }
  const service = await resolvePds(did);
  async function query(method, params) {
    const url = new URL(`/xrpc/com.atproto.repo.${method}`, service);
    url.search = new URLSearchParams(params).toString();
    return (await fetchChecked(url)).json();
  }
  const publication = await query('getRecord', { repo: did, collection: 'site.standard.publication', rkey });
  if (publication.uri !== config.publicationUri || publication.value.url !== config.siteUrl) {
    throw new Error('Live publication record does not match this site.');
  }
  const documents = new Map();
  let cursor;
  do {
    const page = await query('listRecords', {
      repo: did, collection: 'site.standard.document', limit: '100', ...(cursor ? { cursor } : {}),
    });
    for (const record of page.records) {
      if (record.value.site !== config.publicationUri) continue;
      if (documents.has(record.value.path)) throw new Error(`Duplicate live documents: ${record.value.path}`);
      documents.set(record.value.path, record);
    }
    cursor = page.cursor;
  } while (cursor);
  for (const post of manifest) {
    const document = documents.get(post.path);
    if (!document?.uri.startsWith(`at://${did}/site.standard.document/`)) {
      throw new Error(`Missing live document: ${post.path}`);
    }
    if (post.coverImage && !document.value.coverImage?.ref?.$link) {
      throw new Error(`Missing live document cover image: ${post.path}`);
    }
    const html = await (await fetchChecked(new URL(post.path, config.siteUrl))).text();
    for (const [relation, uri] of [
      ['site.standard.document', document.uri], ['site.standard.publication', config.publicationUri],
    ]) {
      const targets = linkTargets(html, relation);
      if (targets.length !== 1 || targets[0] !== uri) {
        throw new Error(`Missing or incorrect live ${relation} link: ${post.path}`);
      }
    }
  }
  console.log(`Verified live publication ${config.publicationUri} and ${manifest.length} live articles.`);
}

async function main() {
  const command = process.argv[2];
  if (!['preview', 'publish', 'verify', 'verify-live'].includes(command)) {
    throw new Error('Usage: node publishing/standard-site.mjs <preview|publish|verify|verify-live>');
  }
  const config = await readJson(path.join(publishing, 'sequoia.json'));
  publicationParts(config);
  if (config.bluesky?.enabled !== false) {
    throw new Error('Bluesky auto-posting must remain explicitly disabled (bluesky.enabled: false).');
  }
  const manifest = await readJson(path.join(publishing, '.sequoia/manifest.json'));
  if (!manifest.length) throw new Error('No published articles exported. Run make build first.');
  if (command === 'verify-live') {
    await verifyLive(config, manifest);
  } else if (command === 'preview') {
    // Sequoia requires credentials even for dry runs. Explicit offline credentials
    // avoid both a login prompt and network access; --dry-run never authenticates.
    runSequoia(['publish', '--force', '--dry-run', '--verbose'], {
      ...process.env, ATP_IDENTIFIER: config.identity, ATP_APP_PASSWORD: 'offline-preview',
      PDS_URL: 'https://example.invalid',
    });
  } else if (command === 'publish') {
    const env = await ensurePublication(config);
    // Sync must succeed before publishing: the CLI's automatic sync tolerates
    // failure and could create duplicate records on a fresh checkout.
    runSequoia(['sync', '--update-frontmatter'], env);
    // Sync hashes current local content. Force updates so edits on fresh CI
    // checkouts reach the PDS even when sync has just restored the state.
    const published = runSequoia(['publish', '--force'], env);
    const created = Number(published.match(/Published:\s*(\d+)/)?.[1]);
    const updated = Number(published.match(/Updated:\s*(\d+)/)?.[1]);
    if (created + updated !== manifest.length) throw new Error('Sequoia did not publish every exported article.');
    runSequoia(['inject'], env);
    await injectPublicationDiscovery(config);
    const output = path.resolve(publishing, config.outputDir);
    await mkdir(path.join(output, '.well-known'), { recursive: true });
    await writeFile(path.join(output, '.well-known/site.standard.publication'), `${config.publicationUri}\n`);
    await writeFile(path.join(output, '.nojekyll'), '');
    await verify(config, manifest);
  } else {
    await verify(config, manifest);
  }
}

if (process.argv[1] && await realpath(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
