import csv
import json

# CSVを読み込み（複数のエンコーディングを試す）
sales_data = []
encodings = ['utf-8', 'cp932', 'shift_jis', 'utf-8-sig']

for encoding in encodings:
    try:
        with open('plugin_data.csv', 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
            # ヘッダー行を確認
            if 'プラグイン名' in content or 'セール価格' in content:
                break
    except:
        continue

with open('plugin_data.csv', 'r', encoding=encoding, errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # キー名を取得（文字化け対策）
        keys = list(row.keys())
        
        # 各カラムの値を取得
        name = row.get('プラグイン名', row.get(keys[0], '')) if keys else ''
        sale_price_str = row.get('セール価格', row.get(keys[1], '0')) if len(keys) > 1 else '0'
        original_price = row.get('定価', row.get(keys[2], '')) if len(keys) > 2 else ''
        discount = row.get('セール率', row.get(keys[3], '')) if len(keys) > 3 else ''
        end_date = row.get('終了日', row.get(keys[4], '')) if len(keys) > 4 else ''
        product_url = row.get('商品URL', row.get(keys[5], '')) if len(keys) > 5 else ''
        image_url = row.get('画像URL', row.get(keys[6], '')) if len(keys) > 6 else ''
        
        # 価格から数字を抽出
        sale_price = int(''.join(filter(str.isdigit, str(sale_price_str)))) if sale_price_str else 0
        
        sales_data.append({
            'name': name,
            'salePrice': sale_price,
            'originalPrice': original_price,
            'discount': discount,
            'endDate': end_date,
            'productUrl': product_url,
            'imageUrl': image_url
        })

sales_json = json.dumps(sales_data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>おすすめセールプラグイン 毎日更新</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0a0a0f; color: #e0e0e0; padding: 20px; }
        h1 { text-align: center; margin-bottom: 20px; color: #fff; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1400px; margin: 0 auto; }
        .card { background: #1a1a24; border-radius: 12px; overflow: hidden; transition: transform 0.2s; }
        .card:hover { transform: translateY(-4px); }
        .card img { width: 100%; height: 160px; object-fit: cover; }
        .card-body { padding: 16px; }
        .card-title { font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #fff; }
        .price { color: #10b981; font-size: 20px; font-weight: 700; }
        .original { color: #666; text-decoration: line-through; font-size: 12px; margin-left: 8px; }
        .discount { background: #dc2626; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 8px; }
        .end-date { color: #f59e0b; font-size: 12px; margin-top: 8px; }
        .btn { display: block; text-align: center; background: #6366f1; color: #fff; padding: 10px; border-radius: 8px; text-decoration: none; margin-top: 12px; }
        .btn:hover { background: #818cf8; }
    </style>
</head>
<body>
    <h1>おすすめセールプラグイン 毎日更新</h1>
    <div class="grid" id="deals"></div>
    <script>
        const salesData = ''' + sales_json + ''';
        const container = document.getElementById('deals');
        salesData.forEach(deal => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <img src="${deal.imageUrl}" alt="${deal.name}" onerror="this.style.display='none'">
                <div class="card-body">
                    <div class="card-title">${deal.name}</div>
                    <div>
                        <span class="price">¥${deal.salePrice.toLocaleString()}</span>
                        <span class="original">${deal.originalPrice}</span>
                        <span class="discount">${deal.discount}</span>
                    </div>
                    <div class="end-date">${deal.endDate}</div>
                    <a href="${deal.productUrl}" target="_blank" class="btn">詳細を見る</a>
                </div>
            `;
            container.appendChild(card);
        });
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html with {len(sales_data)} items")
