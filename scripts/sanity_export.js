import { htmlToBlocks } from '@sanity/block-tools'
import { createClient } from '@sanity/client'
import * as dotenv from 'dotenv'
import { globbyStream as glob } from 'globby'
import { JSDOM } from 'jsdom'
import fs from 'node:fs/promises'
import path from 'node:path'

dotenv.config()

const client = createClient({
	projectId: '8hhpy0c8',
	dataset: 'development',
	apiVersion: '2023-05-25',
	useCdn: true,
	token: process.env.SANITY_TOKEN,
})

const $metadata = await fs.readFile('build/ag/nt/metadata.json', { encoding: 'utf-8' })
const metadata = JSON.parse($metadata)
const tb = await client.createOrReplace({ _id: 'ag-nt', _type: 'treebank', title: metadata.title })

for await (const f of glob('build/ag/nt/*.html')) {
	const html = await fs.readFile(f, { encoding: 'utf-8' })
	const ref = path.basename(f, '.html')
	await client.createOrReplace({
		_id: `ag-nt-${ref}`,
		_type: 'chunk',
		treebank: { _type: 'reference', _ref: tb._id },
		text: htmlToBlocks(html, null, {
			parseHtml: html => new JSDOM(html).window.document,
		}),
		ref,
	})
}
