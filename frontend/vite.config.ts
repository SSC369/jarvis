import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      // The user chooses when to reload (FR-41). "autoUpdate" would swap
      // the app under them mid-session, which the sub-plan explicitly rules
      // out.
      registerType: 'prompt',
      // generateSW cannot inspect a POST body (every GraphQL call is a POST
      // to the same /graphql URL, distinguished only by the JSON body's
      // operationName) because its runtime-caching config is serialized
      // into the built service worker rather than executed as real code.
      // injectManifest lets src/sw.ts read the body and build a cache key
      // from operationName + variables — see src/sw.ts.
      strategies: 'injectManifest',
      srcDir: 'src',
      filename: 'sw.ts',
      injectManifest: {
        // The generated service worker still needs the precache manifest;
        // injectManifest just means we own the fetch-handling logic.
        globPatterns: ['**/*.{js,css,html,svg,png,ico,woff2}'],
      },
      manifest: {
        name: 'Slashit',
        short_name: 'Slashit',
        description: 'Everything starts with a slash.',
        start_url: '/',
        display: 'standalone',
        // Matches tokens.css's light-mode --color-background / --color-foreground.
        background_color: '#faf8f4',
        theme_color: '#2f2823',
        icons: [
          { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
          {
            src: '/icons/icon-512-maskable.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
      devOptions: {
        // Lets `npm run dev` register a real service worker for manual
        // testing; production behaviour is still verified against a real
        // `vite build` + `vite preview`, never dev mode alone.
        enabled: true,
        type: 'module',
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
