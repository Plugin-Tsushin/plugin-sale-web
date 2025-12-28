import csv
import json
import re

# CSVを読み込み（複数のエンコーディングを試す）
sales_data = []
encodings = ['utf-8', 'cp932', 'shift_jis', 'utf-8-sig']

for encoding in encodings:
    try:
        with open('plugin_data.csv', 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
            if 'プラグイン名' in content or 'セール価格' in content:
                break
    except:
        continue

with open('plugin_data.csv', 'r', encoding=encoding, errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        keys = list(row.keys())
        
        name = row.get('プラグイン名', row.get(keys[0], '')) if keys else ''
        sale_price_str = row.get('セール価格', row.get(keys[1], '0')) if len(keys) > 1 else '0'
        original_price = row.get('定価', row.get(keys[2], '')) if len(keys) > 2 else ''
        discount = row.get('セール率', row.get(keys[3], '')) if len(keys) > 3 else ''
        end_date = row.get('終了日', row.get(keys[4], '')) if len(keys) > 4 else ''
        product_url = row.get('商品URL', row.get(keys[5], '')) if len(keys) > 5 else ''
        image_url = row.get('画像URL', row.get(keys[6], '')) if len(keys) > 6 else ''
        
        sale_price = int(''.join(filter(str.isdigit, str(sale_price_str)))) if sale_price_str else 0
        
        discount_match = re.search(r'(\d+)%', str(discount))
        discount_percent = int(discount_match.group(1)) if discount_match else 0
        
        sales_data.append({
            'name': name,
            'salePrice': sale_price,
            'originalPrice': original_price,
            'discount': discount,
            'discountPercent': discount_percent,
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
        .filters { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .filter-btn { padding: 8px 16px; border: none; border-radius: 20px; cursor: pointer; font-size: 14px; transition: all 0.2s; background: #2a2a3a; color: #e0e0e0; }
        .filter-btn:hover { background: #3a3a4a; }
        .filter-btn.active { background: #6366f1; color: #fff; }
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
    <div class="filters">
        <button class="filter-btn active" data-filter="all">すべて</button>
        <button class="filter-btn" data-filter="50">50%OFF以上</button>
        <button class="filter-btn" data-filter="70">70%OFF以上</button>
        <button class="filter-btn" data-filter="90">90%OFF以上</button>
    </div>
    <div class="grid" id="deals"></div>
    <script>
        const salesData = ''' + sales_json + ''';
        
        // 終了日でソート（早い順）- 年またぎ対応
        function parseEndDate(dateStr) {
            if (!dateStr) return new Date('2099-12-31');
            const match = dateStr.match(/Ends\\s+(\\d+)\\s+(\\w+)/);
            if (!match) return new Date('2099-12-31');
            const day = parseInt(match[1]);
            const monthStr = match[2];
            const months = {Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
            const month = months[monthStr] !== undefined ? months[monthStr] : 0;
            
            const now = new Date();
            const currentMonth = now.getMonth();
            const currentYear = now.getFullYear();
            
            // 現在が12月で、終了日が1-3月の場合は来年
            let year = currentYear;
            if (currentMonth >= 10 && month <= 2) {
                year = currentYear + 1;
            }
            // 現在が1-2月で、終了日が12月の場合は今年（既に過ぎている可能性）
            if (currentMonth <= 1 && month === 11) {
                year = currentYear;
            }
            
            return new Date(year, month, day);
        }
        
        salesData.sort((a, b) => parseEndDate(a.endDate) - parseEndDate(b.endDate));
        
        let currentFilter = 'all';
        
        function renderDeals() {
            const container = document.getElementById('deals');
            container.innerHTML = '';
            
            const filtered = currentFilter === 'all' 
                ? salesData 
                : salesData.filter(deal => deal.discountPercent >= parseInt(currentFilter));
            
            filtered.forEach(deal => {
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
        }
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderDeals();
            });
        });
        
        renderDeals();
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html with {len(sales_data)} items")
