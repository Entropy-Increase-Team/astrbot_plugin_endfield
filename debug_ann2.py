import asyncio
import httpx

async def main():
    base_url = "https://end-api.shallow.ink"
    async with httpx.AsyncClient() as client:
        # Fetch list
        resp = await client.get(f"{base_url}/api/announcements", params={"page": 1, "page_size": 20})
        list_res = resp.json()
        if not list_res or 'data' not in list_res:
            print("Failed to get list")
            return
            
        ann_list = list_res['data'].get('list', [])
        for ann in ann_list:
            if '畅游指南' in ann.get('title', ''):
                print(f"Found: {ann['title']}, AnnId: {ann['announceId']}")
                detail_resp = await client.get(f"{base_url}/api/announcements/{ann['announceId']}")
                detail = detail_resp.json()
                if detail and 'data' in detail:
                    caption = detail['data'].get('captionHtml', '')
                    print("Caption HTML Snippet length:", len(caption))
                    import re
                    imgs = re.findall(r'<img[^>]+>', caption)
                    print(f"Found {len(imgs)} images:")
                    for img in imgs:
                        print(img)
                return

if __name__ == "__main__":
    asyncio.run(main())
