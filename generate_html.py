import csv
import json

# CSVを読み込み
sales_data = []
with open('plugin_data.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        sale_price_str = row.get('セール価格', '0')
        sale_price = int(''.join(filter(str.isdigit, sale_price_str))) if sale_price_str else 0
        
        sales_data.append({
            'name': row.get('プラグイン名', ''),
            'salePrice': sale_price,
            'originalPrice': row.get('定価', ''),
            'discount': row.get('セール率', ''),
            'endDate': row.get('終了日', ''),
            'productUrl': row.get('商品URL', ''),
            'imageUrl': row.get('画像URL', '')
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
