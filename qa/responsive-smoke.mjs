import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";

const baseURL = "http://127.0.0.1:4173/index.html";
const cases = [
  { name: "mobile-430", width: 430, height: 932 },
  { name: "tablet-768", width: 768, height: 1024 },
  { name: "notebook-1024", width: 1024, height: 768 },
];

const browser = await chromium.launch({ headless: true });
const results = [];
await mkdir("qa/artifacts", { recursive: true });

for (const entry of cases) {
  const context = await browser.newContext({ viewport: { width: entry.width, height: entry.height } });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });

  await page.goto(baseURL, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(700);

  const metrics = await page.evaluate(() => {
    const nav = document.querySelector(".nav");
    const toggle = document.querySelector(".nav-toggle");
    const h1 = document.querySelector(".golden-hero h1");
    const firstMethod = document.querySelector(".method-grid article");
    return {
      innerWidth: window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      navDisplay: nav ? getComputedStyle(nav).display : null,
      toggleDisplay: toggle ? getComputedStyle(toggle).display : null,
      h1FontSize: h1 ? parseFloat(getComputedStyle(h1).fontSize) : 0,
      methodHeight: firstMethod ? firstMethod.getBoundingClientRect().height : 0,
    };
  });

  const failures = [];
  if (metrics.innerWidth !== entry.width) failures.push(`innerWidth ${metrics.innerWidth} != ${entry.width}`);
  if (metrics.scrollWidth > entry.width + 2) failures.push(`horizontal overflow ${metrics.scrollWidth}px > ${entry.width}px`);
  if (metrics.toggleDisplay === "none") failures.push("responsive navigation toggle is hidden");
  if (metrics.navDisplay !== "none") failures.push(`desktop navigation visible initially (${metrics.navDisplay})`);
  if (metrics.h1FontSize < 40) failures.push(`hero H1 too small (${metrics.h1FontSize}px)`);
  if (entry.width <= 430 && metrics.methodHeight > 190) failures.push(`mobile methodology card too tall (${metrics.methodHeight}px)`);
  if (errors.length) failures.push(`browser errors: ${errors.join(" | ")}`);

  await page.screenshot({ path: `qa/artifacts/home-${entry.name}.png`, fullPage: true });
  results.push({ ...entry, ...metrics, failures });
  await context.close();
}

await browser.close();
await writeFile("qa/artifacts/responsive-gate.json", JSON.stringify(results, null, 2) + "\n", "utf8");

const allFailures = results.flatMap((result) => result.failures.map((failure) => `${result.name}: ${failure}`));
if (allFailures.length) {
  console.error(allFailures.join("\n"));
  process.exit(1);
}
console.log("SENTRIVA responsive visual gate PASS");
