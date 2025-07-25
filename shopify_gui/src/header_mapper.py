from difflib import get_close_matches

shopify_headers = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags",
                   "Variant SKU", "Variant Price", "Variant Requires Shipping",
                   "Image Src", "Image Alt Text"]

def map_headers(user_headers):
    mapping = {}
    for col in user_headers:
        match = get_close_matches(col, shopify_headers, n=1, cutoff=0.6)
        mapping[col] = match[0] if match else None
    return mapping
