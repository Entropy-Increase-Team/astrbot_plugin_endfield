import asyncio
from core.client import EndfieldClient

async def main():
    client = EndfieldClient()
    # Fetch list
    list_res = await client.get_announcement_list()
    if not list_res or 'data' not in list_res:
        print("Failed to get list")
        return
        
    ann_list = list_res['data'].get('list', [])
    for group in ann_list:
        for ann in group.get('list', []):
            if '塔卫二畅游指南' in ann.get('title', ''):
                print(f"Found: {ann['title']}, AnnId: {ann['announceId']}")
                detail = await client.get_announcement_detail(ann['announceId'])
                if detail and 'data' in detail:
                    caption = detail['data'].get('captionHtml', '')
                    print("Caption HTML Snippet:")
                    print(caption[:1000])
                    import re
                    imgs = re.findall(r'<img[^>]+>', caption)
                    for img in imgs:
                        print(img)
                return

if __name__ == "__main__":
    asyncio.run(main())
