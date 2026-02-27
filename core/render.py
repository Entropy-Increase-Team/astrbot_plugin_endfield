import os
from astrbot.api.star import Star
from typing import Dict, Any, Optional

class Renderer:
    def __init__(self, res_path: str, plugin: Star):
        self.plugin = plugin
        self.res_path = res_path
        self._browser = None
        self._playwright = None

    def get_template(self, name: str) -> str:
        path = os.path.join(self.res_path, name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    async def render_html(self, template_name: str, data: Dict[str, Any], options: Optional[Dict] = None) -> Optional[str]:
        """Entry point for rendering HTML templates to images using Playwright."""
        tmpl_content = self.get_template(template_name)
        if not tmpl_content:
            return None
            
        adapted = self._adapt_template(tmpl_content)
        adapted = self._inline_assets(adapted)
        html_content = self._render_jinja(adapted, data)
        if not html_content:
            return None
            
        return await self._screenshot(html_content, template_name, options)

    def _adapt_template(self, content: str) -> str:
        """Converts Yunzai (art-template) syntax to Jinja2."""
        import re
        adapted = content.replace("$value", "item")
        
        def fix_condition(match):
            cond = match.group(1).replace("===", "==").replace("!==", "!=").replace("&&", "and").replace("||", "or").replace("null", "none").replace(".length", "|length")
            cond = re.sub(r'!\s*([\w\.]+)', r'not \1', cond)
            return f"{{% if {cond} %}}"
            
        adapted = re.sub(r'\{\{if\s+(.+?)\}\}', fix_condition, adapted)
        adapted = adapted.replace("{{/if}}", "{% endif %}").replace("{{else}}", "{% else %}")
        adapted = re.sub(r'\{\{else if\s+(.+?)\}\}', lambda m: fix_condition(m).replace("if", "elif"), adapted)
        adapted = re.sub(r'\{\{@\s*([\w\.]+)\s*\}\}', r'{{\1|safe}}', adapted)
        adapted = re.sub(r'\{\{([^%\}]+?)\}\}', lambda m: f"{{{{{m.group(1).replace('||', 'or').replace('&&', 'and').replace('null', 'none')}}}}}", adapted)
        
        def replace_each(match):
            inner = match.group(1).strip().split()
            if len(inner) >= 2:
                return f"{{% for {inner[1]} in {inner[0]} %}}"
            return f"{{% for item in {inner[0]} %}}"
            
        adapted = re.sub(r'\{\{\s*each\s+(.+?)\s*\}\}', replace_each, adapted)
        return adapted.replace("{{/each}}", "{% endfor %}")

    def _inline_assets(self, html: str) -> str:
        """Inlines CSS and Images to ensure Playwright renders them correctly."""
        import re, base64, mimetypes
        
        def inline_css(match):
            path = os.path.join(self.res_path, match.group(1))
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f"<style>\n{f.read()}\n</style>"
            return ""
            
        def inline_image(match):
            path = os.path.join(self.res_path, match.group(1))
            if os.path.exists(path):
                mime = mimetypes.guess_type(path)[0] or "image/png"
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                    return f'src="data:{mime};base64,{b64}"' if match.group(0).startswith('src') else f'url(data:{mime};base64,{b64})'
            return match.group(0)

        html = re.sub(r'<link\s+rel="stylesheet"\s+href="\{\{(?:_res_path|pluResPath)\}\}([^"]+\.css)">', inline_css, html)
        html = re.sub(r'src="\{\{(?:_res_path|pluResPath)\}\}([^"]+\.(?:png|jpg|jpeg|gif|svg|webp))"', inline_image, html)
        html = re.sub(r'url\(\s*[\'"]?\{\{(?:_res_path|pluResPath)\}\}([^)"]+?)[\'"]?\s*\)', inline_image, html)
        return html

    def _render_jinja(self, template_str: str, data: Dict[str, Any]) -> Optional[str]:
        """Renders the adapted template with data using Jinja2."""
        import jinja2
        try:
            env = jinja2.Environment(autoescape=True)
            data_copy = data.copy()
            data_copy["_res_path"] = data_copy.get("pluResPath", "X")
            return env.from_string(template_str).render(**data_copy)
        except Exception as e:
            from astrbot.api import logger
            logger.error(f"[Endfield Render] Jinja2 error: {e}")
            return None

    async def _screenshot(self, html: str, name: str, options: Optional[Dict]) -> Optional[str]:
        """Uses Playwright to capture a screenshot of the rendered HTML."""
        from playwright.async_api import async_playwright
        import uuid, time
        
        output_dir = os.path.abspath(os.path.join(self.res_path, "..", "render_cache"))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"render_{uuid.uuid4().hex[:8]}.png")
        
        for f in os.listdir(output_dir):
            if f.startswith("render_") and time.time() - os.path.getmtime(os.path.join(output_dir, f)) > 300:
                try: 
                    os.remove(os.path.join(output_dir, f))
                except Exception as e: 
                    from astrbot.api import logger
                    logger.debug(f"[Endfield Render] Failed to clean cache file {f}: {e}")

        try:
            if not self._playwright:
                self._playwright = await async_playwright().start()
            if not self._browser:
                self._browser = await self._playwright.chromium.launch()
                
            context = await self._browser.new_context(device_scale_factor=2, viewport={"width": 850, "height": 800})
            page = await context.new_page()
            
            temp_html = os.path.join(os.path.dirname(os.path.abspath(os.path.join(self.res_path, name))), f"tmp_{uuid.uuid4().hex[:8]}.html")
            with open(temp_html, "w", encoding="utf-8") as f: f.write(html)
            
            try:
                await page.goto(f"file:///{temp_html.replace(chr(92), '/')}", wait_until="load", timeout=15000)
                await page.wait_for_timeout(100)
                el = await page.evaluate_handle("document.body.firstElementChild")
                box = await el.bounding_box() if el else None
                if box:
                    await page.set_viewport_size({"width": int(box["width"]) + 2, "height": int(box["height"]) + 2})
                    await page.screenshot(path=output_path, clip=box)
                else:
                    await page.screenshot(path=output_path, full_page=True)
                if el: await el.dispose()
            finally:
                if os.path.exists(temp_html): os.remove(temp_html)
                await page.close()
                await context.close()
                
            return output_path
        except Exception as e:
            from astrbot.api import logger
            logger.error(f"[Endfield Render] Playwright error: {e}")
            return None
            
    async def close(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
