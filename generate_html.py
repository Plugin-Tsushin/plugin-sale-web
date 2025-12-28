import csv
import json
import re
from datetime import datetime, timedelta

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
            'originalPrice': original_price_str,
            'originalPriceNum': original_price,
            'savings': savings,
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
    <title>DTMプラグインセール情報 | 毎日自動更新</title>
    <meta name="description" content="Plugin Boutiqueのお得なDTMプラグインセール情報を毎日自動更新。終了間近のセールを見逃さない！">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0f0f13;
            --bg-secondary: #1a1a23;
            --bg-card: #1e1e2a;
            --bg-card-hover: #252533;
            --accent: #6366f1;
            --accent-hover: #818cf8;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --text-muted: #6b6b7b;
            --border: #2a2a3a;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', 'Noto Sans JP', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 40px 20px;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .filters {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 24px;
            flex-wrap: wrap;
            padding: 16px;
            background: var(--bg-secondary);
            border-radius: 12px;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border: 2px solid var(--border);
            border-radius: 25px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s;
            background: transparent;
            color: var(--text-secondary);
        }
        
        .filter-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }
        
        .filter-btn.active {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }
        
        .filter-btn .count {
            background: rgba(255,255,255,0.2);
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            margin-left: 6px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--accent);
        }
        
        .stat-label {
            font-size: 12px;
            color: var(--text-muted);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .card {
            background: var(--bg-card);
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.3s;
            border: 1px solid var(--border);
            position: relative;
        }
        
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border-color: var(--accent);
        }
        
        .card-badges {
            position: absolute;
            top: 12px;
            left: 12px;
            display: flex;
            gap: 6px;
            z-index: 10;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        .badge-urgent {
            background: var(--danger);
            color: white;
            animation: pulse 2s infinite;
        }
        
        .badge-hot {
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            color: white;
        }
        
        .badge-super {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: white;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .card-image {
            width: 100%;
            height: 140px;
            object-fit: cover;
            background: var(--bg-secondary);
        }
        
        .card-image-placeholder {
            width: 100%;
            height: 140px;
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-size: 12px;
        }
        
        .card-body {
            padding: 16px;
        }
        
        .card-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--text-primary);
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .price-section {
            margin-bottom: 12px;
        }
        
        .price-current {
            font-size: 26px;
            font-weight: 800;
            color: var(--success);
        }
        
        .price-original {
            font-size: 14px;
            color: var(--text-muted);
            text-decoration: line-through;
            margin-left: 8px;
        }
        
        .discount-tag {
            display: inline-block;
            background: var(--danger);
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 700;
            margin-left: 8px;
        }
        
        .savings {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 8px;
            padding: 8px 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .savings-icon {
            font-size: 16px;
        }
        
        .savings-text {
            font-size: 13px;
            color: var(--success);
            font-weight: 600;
        }
        
        .end-date {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 14px;
            padding: 8px 12px;
            background: var(--bg-secondary);
            border-radius: 8px;
            font-size: 13px;
        }
        
        .end-date-icon {
            font-size: 14px;
        }
        
        .end-date-text {
            color: var(--text-secondary);
        }
        
        .end-date-urgent {
            color: var(--danger);
            font-weight: 600;
        }
        
        .end-date-warning {
            color: var(--warning);
            font-weight: 600;
        }
        
        .cta-btn {
            display: block;
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, var(--accent) 0%, #8b5cf6 100%);
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 10px;
            font-weight: 700;
            font-size: 14px;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .cta-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }
        
        .cta-btn-hot {
            background: linear-gradient(135deg, #ef4444 0%, #f59e0b 100%);
        }
        
        .cta-btn-hot:hover {
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
        }
        
        .footer {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
            font-size: 12px;
        }
        
        .footer a {
            color: var(--accent);
            text-decoration: none;
        }
        
        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
        }
        
        @media (max-width: 640px) {
            .header h1 { font-size: 22px; }
            .grid { grid-template-columns: 1fr; }
            .filters { gap: 6px; }
            .filter-btn { padding: 8px 14px; font-size: 12px; }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>🎹 DTMプラグインセール情報</h1>
        <p>Plugin Boutiqueのお得なセール情報を毎日自動更新</p>
    </header>
    
    <div class="container">
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value" id="total-count">0</div>
                <div class="stat-label">セール中</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="urgent-count">0</div>
                <div class="stat-label">まもなく終了</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="hot-count">0</div>
                <div class="stat-label">70%OFF以上</div>
            </div>
        </div>
        
        <div class="filters">
            <button class="filter-btn active" data-filter="all">すべて</button>
            <button class="filter-btn" data-filter="50">50%OFF以上</button>
            <button class="filter-btn" data-filter="70">70%OFF以上</button>
            <button class="filter-btn" data-filter="90">90%OFF以上</button>
        </div>
        
        <div class="grid" id="deals"></div>
    </div>
    
    <footer class="footer">
        <p>データ提供元: <a href="https://www.pluginboutique.com/" target="_blank">Plugin Boutique</a></p>
        <p style="margin-top: 8px;">※価格は変動する場合があります。最新情報は公式サイトでご確認ください。</p>
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
            const currentMonth = now.getMonth();
            const currentYear = now.getFullYear();
            
            let year = currentYear;
            if (currentMonth >= 10 && month <= 2) {
                year = currentYear + 1;
            }
            
            return new Date(year, month, day);
        }
        
        function getDaysRemaining(dateStr) {
            const endDate = parseEndDate(dateStr);
            const now = new Date();
            now.setHours(0, 0, 0, 0);
            const diffTime = endDate - now;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            return diffDays;
        }
        
        salesData.sort((a, b) => parseEndDate(a.endDate) - parseEndDate(b.endDate));
        
        // Stats
        document.getElementById('total-count').textContent = salesData.length;
        document.getElementById('urgent-count').textContent = salesData.filter(d => getDaysRemaining(d.endDate) <= 3).length;
        document.getElementById('hot-count').textContent = salesData.filter(d => d.discountPercent >= 70).length;
        
        let currentFilter = 'all';
        
        function renderDeals() {
            const container = document.getElementById('deals');
            container.innerHTML = '';
            
            const filtered = currentFilter === 'all' 
                ? salesData 
                : salesData.filter(deal => deal.discountPercent >= parseInt(currentFilter));
            
            // Update filter counts
            document.querySelectorAll('.filter-btn').forEach(btn => {
                const filter = btn.dataset.filter;
                let count;
                if (filter === 'all') {
                    count = salesData.length;
                } else {
                    count = salesData.filter(d => d.discountPercent >= parseInt(filter)).length;
                }
                const existingCount = btn.querySelector('.count');
                if (existingCount) existingCount.remove();
                const countSpan = document.createElement('span');
                countSpan.className = 'count';
                countSpan.textContent = count;
                btn.appendChild(countSpan);
            });
            
            if (filtered.length === 0) {
                container.innerHTML = '<div class="no-results">該当するセールがありません</div>';
                return;
            }
            
            filtered.forEach(deal => {
                const daysRemaining = getDaysRemaining(deal.endDate);
                const isUrgent = daysRemaining <= 3;
                const isWarning = daysRemaining <= 7 && daysRemaining > 3;
                const isHot = deal.discountPercent >= 70;
                const isSuper = deal.discountPercent >= 90;
                
                const card = document.createElement('div');
                card.className = 'card';
                
                let badges = '';
                if (isUrgent) badges += '<span class="badge badge-urgent">残り' + daysRemaining + '日</span>';
                if (isSuper) badges += '<span class="badge badge-super">激安</span>';
                else if (isHot) badges += '<span class="badge badge-hot">注目</span>';
                
                let endDateClass = 'end-date-text';
                let endDateText = deal.endDate;
                if (isUrgent) {
                    endDateClass = 'end-date-urgent';
                    endDateText = '⚠️ 残り' + daysRemaining + '日で終了!';
                } else if (isWarning) {
                    endDateClass = 'end-date-warning';
                    endDateText = '残り' + daysRemaining + '日 (' + deal.endDate + ')';
                }
                
                const ctaBtnClass = (isUrgent || isSuper) ? 'cta-btn cta-btn-hot' : 'cta-btn';
                const ctaText = isUrgent ? '🔥 今すぐチェック →' : 'セール価格で見る →';
                
                card.innerHTML = `
                    <div class="card-badges">${badges}</div>
                    ${deal.imageUrl ? 
                        `<img src="${deal.imageUrl}" alt="${deal.name}" class="card-image" onerror="this.outerHTML='<div class=\\'card-image-placeholder\\'>🎹 ${deal.name.substring(0,20)}</div>'">` : 
                        `<div class="card-image-placeholder">🎹 ${deal.name.substring(0,20)}</div>`
                    }
                    <div class="card-body">
                        <div class="card-title">${deal.name}</div>
                        <div class="price-section">
                            <span class="price-current">¥${deal.salePrice.toLocaleString()}</span>
                            <span class="price-original">${deal.originalPrice}</span>
                            <span class="discount-tag">${deal.discountPercent}%OFF</span>
                        </div>
                        ${deal.savings > 0 ? `
                        <div class="savings">
                            <span class="savings-icon">💰</span>
                            <span class="savings-text">¥${deal.savings.toLocaleString()} お得!</span>
                        </div>
                        ` : ''}
                        <div class="end-date">
                            <span class="end-date-icon">📅</span>
                            <span class="${endDateClass}">${endDateText}</span>
                        </div>
                        <a href="${deal.productUrl}" target="_blank" rel="noopener" class="${ctaBtnClass}">${ctaText}</a>
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
