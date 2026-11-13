# Standard.site publishing

Publishes Pelican articles through [Sequoia](https://sequoia.pub/). Requires
Node.js 22+ and the site's Python/Ruby dependencies. Run commands from the repo root:

```sh
npm --prefix publishing ci --ignore-scripts
make build
npm --prefix publishing run standard:preview
```

Preview works offline. Configuration is in [sequoia.json](sequoia.json);
dependencies, generated exports, and publishing state stay in this directory.
The publication key was generated once with the AT Protocol SDK's `TID.nextStr()`
and is reused across deployments.
Article covers use the same `OPENGRAPH_IMAGE` as the website (`avatar-opengraph.png`).
Publishing adds a `site.standard.publication` discovery link to every HTML page;
the `.well-known` endpoint remains the publication verification source.

To deploy:

1. Create a [Bluesky app password](https://bsky.app/settings/app-passwords) for
   `kevinyap.ca`, then save it using the interactive prompt:

   ```sh
   gh secret set ATP_APP_PASSWORD --repo iKevinY/iKevinY.github.io
   ```

2. Commit and push these changes to `src`. CI creates the configured publication
   if absent, publishes the articles, verifies the generated links, and deploys
   to `gh-pages`. No separate `sequoia init` is needed. Later runs reuse the records.

3. Wait for **Pelican Build** and the GitHub Pages deployment to finish, then run:

   ```sh
   npm --prefix publishing run standard:verify-live
   ```

   This read-only check needs no credentials. It checks the deployed
   [publication endpoint](https://kevinyap.ca/.well-known/site.standard.publication),
   the actual publication and document records on your PDS, and every article's
   deployed verification links. Expect confirmation of the publication URI and
   21 live articles. See [Standard.site verification](https://standard.site/docs/verification/).

For local publishing, set `ATP_APP_PASSWORD` in your environment, build, and run
`npm --prefix publishing run standard:publish`. `standard:verify` checks local output.
`ATP_IDENTIFIER` defaults to `kevinyap.ca`; `PDS_URL` overrides PDS discovery.

`bluesky.enabled: false` is required: publishing stops if auto-posting is enabled
or unspecified. Removed articles are not automatically deleted from the PDS.
Without the secret, CI deploys the ordinary site and reports Standard.site
publishing as inactive.

Sequoia 0.5.8 has upstream Zod and glob/minimatch audit advisories; its bundled
dependencies cannot be patched with npm overrides.
