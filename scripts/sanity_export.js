import { createClient } from '@sanity/client'
import fs from 'node:fs/promises'

const client = createClient({
  projectId: 'YOUR_PROJECT_ID',
})

const $metadata = await fs.readFile('build/ag/nt/metadata.json', {
  encoding: 'utf-8',
})
const metadata = JSON.parse($metadata)

const chunks = []
for await (const f of globby(['build/ag/nt/*.html'])) {
  const html = await fs.readFile(f, { encoding: 'utf-8' })
  chunks.push({ filename: f, html })
}
