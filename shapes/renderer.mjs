/** Original SysML SVG component helpers. SPDX-License-Identifier: Apache-2.0 */
const NS = 'http://www.w3.org/2000/svg';
let catalogPromise, spritePromise;
async function fetchText(path) {
  const response = await fetch(new URL(path, import.meta.url));
  if (!response.ok) throw new Error(`Cannot load ${path}: HTTP ${response.status}`);
  return response.text();
}
export function loadCatalog() {
  return catalogPromise ??= fetchText('catalog.json').then(JSON.parse).catch(error => {
    catalogPromise = undefined; throw error;
  });
}
function loadSprite() {
  return spritePromise ??= fetchText('shapes.svg').then(text => {
    const document = new DOMParser().parseFromString(text, 'image/svg+xml');
    if (document.querySelector('parsererror')) throw new Error('Invalid SVG sprite');
    return document;
  }).catch(error => { spritePromise = undefined; throw error; });
}
function dimensions(shape, options) {
  const width = options.width ?? shape.viewBox[2], height = options.height ?? shape.viewBox[3];
  if (![width, height].every(value => typeof value === 'number' && Number.isFinite(value) && value > 0))
    throw new Error('Shape width and height must be positive finite numbers');
  return {width, height};
}
/** Scale attachment coordinates into an xMidYMid meet viewport, including letterboxing. */
export function anchorPositions(shape, options = {}) {
  const {width, height} = dimensions(shape, options);
  if (![options.x ?? 0, options.y ?? 0].every(value => typeof value === 'number' && Number.isFinite(value)))
    throw new Error('Shape x and y must be finite numbers');
  const [vx, vy, vw, vh] = shape.viewBox;
  const scale = Math.min(width / vw, height / vh);
  const dx = (options.x ?? 0) + (width - vw * scale) / 2;
  const dy = (options.y ?? 0) + (height - vh * scale) / 2;
  return Object.fromEntries(Object.entries(shape.anchors).map(([name, [x, y]]) =>
    [name, {x: dx + (x - vx) * scale, y: dy + (y - vy) * scale}]));
}
/** Create an independent inline SVG. Label values are text, never markup. */
export async function createShape(id, options = {}) {
  const [catalog, sprite] = await Promise.all([loadCatalog(), loadSprite()]);
  const shape = catalog.shapes.find(shape => shape.id === id);
  if (!shape) throw new Error(`Unknown shape: ${id}`);
  const symbol = sprite.getElementById(shape.symbolId);
  if (!symbol) throw new Error(`Missing SVG symbol: ${id}`);
  const {width, height} = dimensions(shape, options);
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', shape.viewBox.join(' '));
  svg.setAttribute('width', width); svg.setAttribute('height', height);
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', options.title ?? shape.name);
  for (const child of symbol.children) svg.append(document.importNode(child, true));
  const title = svg.querySelector('title');
  if (title && options.title !== undefined) title.textContent = options.title;
  for (const [slot, text] of Object.entries(options.labels ?? {})) {
    if (!Object.hasOwn(shape.labelSlots, slot)) throw new Error(`Unknown label slot: ${slot}`);
    // data-slot values come from the known shape definition, not user input selectors.
    const target = [...svg.querySelectorAll('[data-slot]')].find(node => node.dataset.slot === slot);
    target.textContent = String(text);
  }
  const tokens = {stroke: 'stroke', fill: 'fill', text: 'text', strokeWidth: 'stroke-width', fontFamily: 'font'};
  for (const [key, value] of Object.entries(options.theme ?? {})) {
    if (!Object.hasOwn(tokens, key)) throw new Error(`Unknown theme option: ${key}`);
    svg.style.setProperty(`--sysml-${tokens[key]}`, String(value));
  }
  return svg;
}
