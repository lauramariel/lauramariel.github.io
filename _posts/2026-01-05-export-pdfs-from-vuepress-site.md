---
layout: post
title:  "Exporting PDFs from VuePress Site"
date: 2026-01-05 22:27:06 -0800
categories: vuepress, javascript
---

## How to create PDFs of vuepress site

### Install required module and related binaries

In project folder, install playwright
```
npm install -D playwright
npx playwright install chromium
```

### Create .mjs script to export PDFs
```
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

(async () => {
  const browser = await chromium.launch({ args: ['--ignore-certificate-errors'] });
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  const page = await context.newPage();

  const baseUrl = 'https://localhost:8080';
  console.log(`Connecting to ${baseUrl}...`);

  // 1. Load the homepage first to get access to the Vue/VuePress instance
  await page.goto(baseUrl, { waitUntil: 'networkidle' });

  // 2. Extract all route paths from the VuePress router
  // This works for VuePress 2.x/VitePress environments
  const routes = await page.evaluate(() => {
    // VuePress 2 stores routes in a global or accessible via the client-side API
    // We can extract them by looking at all registered links or the router instance
    return Array.from(document.querySelectorAll('a'))
      .map(a => a.getAttribute('href'))
      .filter(href => href && href.startsWith('/') && !href.includes(':') && !href.includes('#'))
      .filter((value, index, self) => self.indexOf(value) === index); // Unique values only
  });

  console.log(`Found ${routes.length} pages to export.`);

  // Create an output directory
  const outputDir = './exported_pdfs';
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

  // 3. Loop through each route and save as PDF
  for (const route of routes) {
    const url = `${baseUrl}${route}`;
    const fileName = route === '/' ? 'index.pdf' : `${route.replace(/\//g, '_').replace('.html', '')}.pdf`;
    const filePath = path.join(outputDir, fileName);

    console.log(`Exporting: ${route} -> ${filePath}`);

    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      
      // Wait for content hydration
      await page.waitForSelector('.theme-default-content', { state: 'visible', timeout: 5000 });
      
      await page.emulateMedia({ media: 'screen' });

      // Remove sidebar from rendered pages
      await page.addStyleTag({
        content: `
        .sidebar, .navbar, .page-nav { display: none !important; }
        .page { padding: 0 !important; }
        .theme-default-content { max-width: 100% !important; margin: 0 !important; }
        `
      });

      await page.pdf({
        path: filePath,
        format: 'A4',
        printBackground: true,
        margin: { top: '20px', right: '20px', bottom: '20px', left: '20px' }
      });
    } catch (err) {
      console.error(`Failed to export ${route}:`, err.message);
    }
  }

  await browser.close();
  console.log('All pages exported successfully!');
})();
```

### Start local VuePress server
```
npm run dev 
```

### Run the script
Playwright will launch the site in headless mode via Chromium, render each page, and save the files to the outputDir defined in the script.
```
node export.mjs
```

### How to combine PDFs

I installed GhostScript and tried various options but the images kept rendering blank.

ChatGPT recommended `pdfunite` by Poppler and that worked perfectly :)

```
brew install poppler
pdfunite *.pdf combined.pdf
```