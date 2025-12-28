import csv
import json
import re

# CSVを読み込み
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
        original_price_str = row.get('定価', row.get(keys[2], '')) if len(keys) > 2 else ''
        discount = row.get('セール率', row.get(keys[3], '')) if len(keys) > 3 else ''
        end_date = row.get('終了日', row.get(keys[4], '')) if len(keys) > 4 else ''
        product_url = row.get('商品URL', row.get(keys[5], '')) if len(keys) > 5 else ''
        image_url = row.get('画像URL', row.get(keys[6], '')) if len(keys) > 6 else ''
        
        sale_price = int(''.join(filter(str.isdigit, str(sale_price_str)))) if sale_price_str else 0
        original_price = int(''.join(filter(str.isdigit, str(original_price_str)))) if original_price_str else 0
        savings = original_price - sale_price if original_price > sale_price else 0
        
        discount_match = re.search(r'(\d+)%', str(discount))
        discount_percent = int(discount_match.group(1)) if discount_match else 0
        
        sales_data.append({
            'name': name,
            'salePrice': sale_price,
            'originalPrice': original_price,
            'savings': savings,
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
    <title>DTMプラグインセール情報 | 毎日更新</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background: #0d0d12;
            color: #fff;
            min-height: 100vh;
        }
        
        .header {
            text-align: center;
            padding: 32px 20px 24px;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 6px;
        }
        
        .header p {
            color: #888;
            font-size: 13px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 16px 40px;
        }
        
        .filters {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid #333;
            border-radius: 20px;
            background: transparent;
            color: #888;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .filter-btn:hover {
            border-color: #666;
            color: #fff;
        }
        
        .filter-btn.active {
            background: #5b5bf0;
            border-color: #5b5bf0;
            color: #fff;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }
        
        .card {
            background: #16161d;
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }
        
        .card-urgent {
            border: 1px solid #ef4444;
        }
        
        .urgent-label {
            position: absolute;
            top: 8px;
            right: 8px;
            background: #ef4444;
            color: #fff;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
        }
        
        .card-image {
            width: 100%;
            height: 120px;
            object-fit: cover;
            background: #1a1a24;
        }
        
        .card-body {
            padding: 14px;
        }
        
        .card-title {
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 10px;
            line-height: 1.4;
            color: #eee;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 36px;
        }
        
        .price-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 6px;
        }
        
        .price-sale {
            font-size: 22px;
            font-weight: 700;
            color: #22c55e;
        }
        
        .price-original {
            font-size: 13px;
            color: #666;
            text-decoration: line-through;
        }
        
        .discount-badge {
            background: #dc2626;
            color: #fff;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 8px 0;
            border-top: 1px solid #222;
            font-size: 12px;
        }
        
        .savings {
            color: #22c55e;
        }
        
        .end-date {
            color: #888;
        }
        
        .end-date-urgent {
            color: #ef4444;
            font-weight: 500;
        }
        
        .cta-btn {
            display: block;
            width: 100%;
            padding: 12px;
            background: #5b5bf0;
            color: #fff;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            transition: background 0.2s;
        }
        
        .cta-btn:hover {
            background: #4a4ae0;
        }
        
        .cta-btn-urgent {
            background: linear-gradient(90deg, #ef4444, #f97316);
        }
        
        .cta-btn-urgent:hover {
            background: linear-gradient(90deg, #dc2626, #ea580c);
        }
        
        .footer {
            text-align: center;
            padding: 24px;
            color: #555;
            font-size: 11px;
        }
        
        .footer a { color: #5b5bf0; text-decoration: none; }
        
        @media (max-width: 640px) {
            .grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 20px; }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>🎹 DTMプラグインセール情報</h1>
        <p>Plugin Boutique セール情報を毎日自動更新</p>
    </header>
    
    <div class="container">
        <div class="filters">
            <button class="filter-btn active" data-filter="all">すべて</button>
            <button class="filter-btn" data-filter="50">50%OFF以上</button>
            <button class="filter-btn" data-filter="70">70%OFF以上</button>
            <button class="filter-btn" data-filter="90">90%OFF以上</button>
        </div>
        
        <div class="grid" id="deals"></div>
    </div>
    
    <footer class="footer">
        <p>データ: <a href="https://www.pluginboutique.com/" target="_blank">Plugin Boutique</a> | 価格は変動する場合があります</p>
    </footer>
    
    <script>
        const salesData = ''' + sales_json + ''';
        
        function parseEndDate(dateStr) {
            if (!dateStr) return new Date('2099-12-31');
            const match = dateStr.match(/Ends\\s+(\\d+)\\s+(\\w+)/);
            if (!match) return new Date('2099-12-31');
            const day = parseInt(match[1]);
            const monthStr = match[2];
            const months = {Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
            const month = months[monthStr] !== undefined ? months[monthStr] : 0;
            
            const now = new Date();
            let year = now.getFullYear();
            if (now.getMonth() >= 10 && month <= 2) year++;
            
            return new Date(year, month, day);
        }
        
        function getDaysRemaining(dateStr) {
            const end = parseEndDate(dateStr);
            const now = new Date();
            now.setHours(0,0,0,0);
            return Math.ceil((end - now) / (1000 * 60 * 60 * 24));
        }
        
        salesData.sort((a, b) => parseEndDate(a.endDate) - parseEndDate(b.endDate));
        
        let currentFilter = 'all';
        
        function renderDeals() {
            const container = document.getElementById('deals');
            container.innerHTML = '';
            
            const filtered = currentFilter === 'all' 
                ? salesData 
                : salesData.filter(d => d.discountPercent >= parseInt(currentFilter));
            
            filtered.forEach(deal => {
                const days = getDaysRemaining(deal.endDate);
                const isUrgent = days <= 3;
                
                const card = document.createElement('div');
                card.className = 'card' + (isUrgent ? ' card-urgent' : '');
                
                const endText = isUrgent ? `残り${days}日` : deal.endDate.replace('Ends ', '');
                
                card.innerHTML = `
                    ${isUrgent ? '<div class="urgent-label">まもなく終了</div>' : ''}
                    <img src="${deal.imageUrl}" alt="" class="card-image" onerror="this.style.display='none'">
                    <div class="card-body">
                        <div class="card-title">${deal.name}</div>
                        <div class="price-row">
                            <span class="price-sale">¥${deal.salePrice.toLocaleString()}</span>
                            <span class="price-original">¥${deal.originalPrice.toLocaleString()}</span>
                            <span class="discount-badge">${deal.discountPercent}%OFF</span>
                        </div>
                        <div class="info-row">
                            <span class="savings">¥${deal.savings.toLocaleString()} お得</span>
                            <span class="${isUrgent ? 'end-date-urgent' : 'end-date'}">${endText}</span>
                        </div>
                        <a href="${deal.productUrl}" target="_blank" class="cta-btn${isUrgent ? ' cta-btn-urgent' : ''}">
                            ${isUrgent ? '🔥 今すぐチェック' : '詳細を見る'}
                        </a>
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
