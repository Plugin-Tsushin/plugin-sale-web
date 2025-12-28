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

# 定番プラグインリスト
POPULAR_PLUGINS = [
    'melodyne', 'ozone', 'neutron', 'fabfilter', 'ssl', 'waves', 
    'izotope', 'soundtoys', 'valhalla', 'serum', 'omnisphere',
    'kontakt', 'massive', 'spire', 'diva', 'pro-q', 'pro-l',
    'soothe', 'gullfoss', 'trackspacer', 'oxford', 'sonnox'
]

# 初心者向けプラグインリスト
BEGINNER_PLUGINS = [
    'essential', 'lite', 'elements', 'intro', 'le', 'starter',
    'basic', 'ez', 'simple'
]

def get_category(name):
    name_lower = name.lower()
    if 'comp' in name_lower:
        return {'icon': '🎚️', 'label': 'コンプ', 'target': 'ミキシング向け'}
    elif 'eq' in name_lower or 'equalizer' in name_lower:
        return {'icon': '🎛️', 'label': 'EQ', 'target': 'ミキシング向け'}
    elif 'reverb' in name_lower:
        return {'icon': '🌊', 'label': 'リバーブ', 'target': 'ミキシング向け'}
    elif 'delay' in name_lower:
        return {'icon': '⏱️', 'label': 'ディレイ', 'target': 'ミキシング向け'}
    elif 'synth' in name_lower:
        return {'icon': '🎹', 'label': 'シンセ', 'target': '作曲向け'}
    elif 'drum' in name_lower or 'beat' in name_lower:
        return {'icon': '🥁', 'label': 'ドラム', 'target': '作曲向け'}
    elif 'bass' in name_lower:
        return {'icon': '🎸', 'label': 'ベース', 'target': '作曲向け'}
    elif 'vocal' in name_lower or 'voice' in name_lower:
        return {'icon': '🎤', 'label': 'ボーカル', 'target': 'ボーカルMix向け'}
    elif 'melodyne' in name_lower:
        return {'icon': '🎤', 'label': 'ピッチ補正', 'target': 'ボーカルMix向け'}
    elif 'piano' in name_lower or 'key' in name_lower:
        return {'icon': '🎹', 'label': 'ピアノ', 'target': '作曲向け'}
    elif 'guitar' in name_lower or 'amp' in name_lower:
        return {'icon': '🎸', 'label': 'ギター', 'target': 'ギタリスト向け'}
    elif 'mastering' in name_lower or 'ozone' in name_lower:
        return {'icon': '💿', 'label': 'マスタリング', 'target': 'マスタリング向け'}
    elif 'limiter' in name_lower:
        return {'icon': '📊', 'label': 'リミッター', 'target': 'マスタリング向け'}
    elif 'saturator' in name_lower or 'distortion' in name_lower:
        return {'icon': '🔥', 'label': 'サチュレーション', 'target': 'ミキシング向け'}
    elif 'chorus' in name_lower or 'flanger' in name_lower or 'phaser' in name_lower:
        return {'icon': '🌀', 'label': 'モジュレーション', 'target': 'サウンドデザイン向け'}
    elif 'bundle' in name_lower:
        return {'icon': '📦', 'label': 'バンドル', 'target': 'コスパ重視'}
    elif 'channel' in name_lower or 'strip' in name_lower:
        return {'icon': '🎚️', 'label': 'チャンネルストリップ', 'target': 'ミキシング向け'}
    elif 'scaler' in name_lower or 'chord' in name_lower:
        return {'icon': '🎼', 'label': 'コード補助', 'target': '作曲向け'}
    elif 'metering' in name_lower or 'meter' in name_lower:
        return {'icon': '📈', 'label': 'メーター', 'target': 'ミキシング向け'}
    else:
        return {'icon': '🎵', 'label': 'エフェクト', 'target': 'ミキシング向け'}

def is_popular(name):
    name_lower = name.lower()
    return any(p in name_lower for p in POPULAR_PLUGINS)

def is_beginner(name):
    name_lower = name.lower()
    return any(b in name_lower for b in BEGINNER_PLUGINS)

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
        
        category = get_category(name)
        
        sales_data.append({
            'name': name,
            'salePrice': sale_price,
            'originalPrice': original_price,
            'savings': savings,
            'discountPercent': discount_percent,
            'endDate': end_date,
            'productUrl': product_url,
            'imageUrl': image_url,
            'categoryIcon': category['icon'],
            'categoryLabel': category['label'],
            'target': category['target'],
            'isPopular': is_popular(name),
            'isBeginner': is_beginner(name)
        })

sales_json = json.dumps(sales_data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTMプラグインセール情報 | 毎日更新</title>
    <meta name="description" content="Plugin Boutiqueの最新セール情報を毎日自動更新。人気プラグインをお得にゲット！">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background: #0a0a0f;
            color: #fff;
            min-height: 100vh;
            padding-bottom: 80px;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px 24px;
            background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%);
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header p {
            color: #666;
            font-size: 13px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 16px 40px;
        }
        
        /* 信頼性バー */
        .trust-section {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid #2a2a4a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }
        
        .trust-title {
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
            color: #888;
        }
        
        .trust-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }
        
        .trust-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #ccc;
        }
        
        .trust-icon {
            font-size: 18px;
        }
        
        /* おすすめ枠 */
        .picks-section {
            margin-bottom: 32px;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .picks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
            gap: 12px;
        }
        
        .pick-card {
            background: linear-gradient(135deg, #1f1f35 0%, #1a1a2e 100%);
            border: 1px solid #3a3a5a;
            border-radius: 12px;
            padding: 16px;
            transition: all 0.2s;
            position: relative;
            overflow: hidden;
        }
        
        .pick-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #f59e0b, #ef4444);
        }
        
        .pick-card:hover {
            border-color: #5b5bf0;
            transform: translateY(-2px);
        }
        
        .pick-tags {
            display: flex;
            gap: 6px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        
        .pick-tag {
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
        }
        
        .pick-tag-urgent {
            background: #ef4444;
            color: #fff;
        }
        
        .pick-tag-discount {
            background: #22c55e;
            color: #fff;
        }
        
        .pick-tag-popular {
            background: #f59e0b;
            color: #000;
        }
        
        .pick-tag-beginner {
            background: #3b82f6;
            color: #fff;
        }
        
        .pick-name {
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 6px;
            line-height: 1.4;
        }
        
        .pick-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            font-size: 12px;
            flex-wrap: wrap;
        }
        
        .pick-category {
            background: #2a2a3a;
            padding: 3px 8px;
            border-radius: 4px;
            color: #aaa;
        }
        
        .pick-target {
            color: #888;
        }
        
        .pick-prices {
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .pick-price-sale {
            font-size: 22px;
            font-weight: 900;
            color: #22c55e;
        }
        
        .pick-price-original {
            font-size: 13px;
            color: #555;
            text-decoration: line-through;
        }
        
        .pick-savings {
            font-size: 12px;
            color: #22c55e;
            margin-bottom: 12px;
        }
        
        .pick-cta {
            display: block;
            width: 100%;
            padding: 12px;
            background: linear-gradient(90deg, #ef4444, #f59e0b);
            color: #fff;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            transition: all 0.2s;
        }
        
        .pick-cta:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
        
        /* フィルター */
        .filters {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border: 1px solid #2a2a3a;
            border-radius: 25px;
            background: transparent;
            color: #888;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .filter-btn:hover {
            border-color: #5b5bf0;
            color: #5b5bf0;
        }
        
        .filter-btn.active {
            background: #5b5bf0;
            border-color: #5b5bf0;
            color: #fff;
        }
        
        /* セール一覧 */
        .deals-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .deal-card {
            background: #14141c;
            border-radius: 10px;
            padding: 16px 20px;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 16px;
            align-items: center;
            transition: all 0.2s;
            border: 1px solid transparent;
            cursor: pointer;
        }
        
        .deal-card:hover {
            background: #1a1a24;
            border-color: #2a2a3a;
        }
        
        .deal-card-urgent {
            border-left: 3px solid #ef4444;
            background: linear-gradient(90deg, rgba(239,68,68,0.1) 0%, #14141c 30%);
        }
        
        .deal-info { min-width: 0; }
        
        .deal-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
            flex-wrap: wrap;
        }
        
        .deal-tags {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }
        
        .tag {
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 700;
        }
        
        .tag-category {
            background: #1e1e2a;
            color: #888;
        }
        
        .tag-popular {
            background: #f59e0b;
            color: #000;
        }
        
        .tag-beginner {
            background: #3b82f6;
            color: #fff;
        }
        
        .tag-discount {
            background: #dc2626;
            color: #fff;
        }
        
        .tag-urgent {
            background: #ef4444;
            color: #fff;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .deal-name {
            font-size: 14px;
            font-weight: 600;
            color: #fff;
            line-height: 1.4;
        }
        
        .deal-target {
            font-size: 11px;
            color: #666;
            margin-top: 2px;
        }
        
        .deal-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 13px;
            margin-top: 8px;
        }
        
        .deal-prices {
            display: flex;
            align-items: baseline;
            gap: 6px;
        }
        
        .price-sale {
            font-size: 20px;
            font-weight: 900;
            color: #22c55e;
        }
        
        .price-original {
            font-size: 12px;
            color: #555;
            text-decoration: line-through;
        }
        
        .deal-savings {
            color: #22c55e;
            font-size: 12px;
            font-weight: 500;
        }
        
        .deal-end {
            color: #666;
            font-size: 12px;
        }
        
        .deal-end-urgent {
            color: #ef4444;
            font-weight: 600;
            font-size: 12px;
        }
        
        .deal-action { flex-shrink: 0; }
        
        .cta-btn {
            display: inline-block;
            padding: 12px 16px;
            background: #5b5bf0;
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.2s;
            white-space: nowrap;
            text-align: center;
        }
        
        .cta-btn:hover {
            background: #4a4ae0;
            transform: translateY(-1px);
        }
        
        .cta-btn-urgent {
            background: linear-gradient(90deg, #ef4444, #f59e0b);
        }
        
        /* FAQ */
        .faq-section {
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid #1e1e2a;
        }
        
        .faq-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .faq-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .faq-item {
            background: #14141c;
            border-radius: 10px;
            padding: 16px 20px;
        }
        
        .faq-q {
            font-size: 14px;
            font-weight: 700;
            color: #5b5bf0;
            margin-bottom: 8px;
        }
        
        .faq-a {
            font-size: 13px;
            color: #aaa;
            line-height: 1.7;
        }
        
        /* フッター */
        .footer {
            text-align: center;
            padding: 32px 20px;
            color: #444;
            font-size: 11px;
        }
        
        .footer a {
            color: #5b5bf0;
            text-decoration: none;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #555;
        }
        
        /* スマホ対応 */
        @media (max-width: 640px) {
            body { padding-bottom: 100px; }
            .header { padding: 32px 16px 20px; }
            .header h1 { font-size: 20px; }
            
            .trust-grid { grid-template-columns: 1fr; gap: 8px; }
            .trust-item { font-size: 12px; }
            
            .picks-grid { grid-template-columns: 1fr; }
            
            .deal-card {
                grid-template-columns: 1fr;
                gap: 12px;
                padding: 14px;
            }
            
            .deal-name { font-size: 13px; }
            .price-sale { font-size: 18px; }
            
            .cta-btn {
                width: 100%;
                padding: 14px;
            }
            
            .filter-btn {
                padding: 8px 14px;
                font-size: 12px;
            }
        }
        
        /* モバイル固定フッター */
        .mobile-footer {
            display: none;
        }
        
        @media (max-width: 640px) {
            .mobile-footer {
                display: block;
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(10, 10, 15, 0.95);
                backdrop-filter: blur(10px);
                padding: 12px 16px;
                border-top: 1px solid #2a2a3a;
                z-index: 1000;
            }
            
            .mobile-footer-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
            }
            
            .mobile-footer-text {
                font-size: 12px;
                color: #888;
            }
            
            .mobile-footer-text strong {
                color: #22c55e;
                font-size: 14px;
            }
            
            .mobile-footer-btn {
                padding: 12px 20px;
                background: #5b5bf0;
                color: #fff;
                text-decoration: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 700;
                white-space: nowrap;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>🎹 DTMプラグインセール情報</h1>
        <p>Plugin Boutique のセール情報を毎日自動更新</p>
    </header>
    
    <div class="container">
        <!-- 信頼性セクション -->
        <div class="trust-section">
            <div class="trust-title">🔒 安心してお買い物いただけます</div>
            <div class="trust-grid">
                <div class="trust-item">
                    <span class="trust-icon">✅</span>
                    <span>公式ストアへ直接リンク</span>
                </div>
                <div class="trust-item">
                    <span class="trust-icon">💳</span>
                    <span>日本のクレジットカード対応</span>
                </div>
                <div class="trust-item">
                    <span class="trust-icon">📧</span>
                    <span>購入後すぐにライセンス届く</span>
                </div>
                <div class="trust-item">
                    <span class="trust-icon">↩️</span>
                    <span>30日間返金保証あり</span>
                </div>
            </div>
        </div>
        
        <!-- おすすめピック -->
        <div class="picks-section" id="picks-section"></div>
        
        <!-- フィルター -->
        <div class="section-title">📋 セール一覧</div>
        <div class="filters">
            <button class="filter-btn active" data-filter="all">すべて</button>
            <button class="filter-btn" data-filter="50">50%OFF以上</button>
            <button class="filter-btn" data-filter="70">70%OFF以上</button>
            <button class="filter-btn" data-filter="90">90%OFF以上</button>
        </div>
        
        <!-- セール一覧 -->
        <div class="deals-list" id="deals"></div>
        
        <!-- FAQ -->
        <div class="faq-section">
            <div class="faq-title">❓ よくある質問</div>
            <div class="faq-list">
                <div class="faq-item">
                    <div class="faq-q">Q. 海外サイトでの購入は安全ですか？</div>
                    <div class="faq-a">A. Plugin Boutiqueは世界最大級のプラグイン販売サイトで、100万人以上が利用しています。SSL暗号化通信、PayPal対応で安心して購入できます。</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q. 届くまでどれくらいかかりますか？</div>
                    <div class="faq-a">A. デジタル製品のため、購入完了後すぐにメールでライセンスキーが届きます。通常は数分以内です。</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q. 日本語で使えますか？</div>
                    <div class="faq-a">A. プラグイン自体は英語UIのものが多いですが、操作はシンプルです。YouTubeで「プラグイン名 + 使い方」で検索すると日本語解説動画が見つかります。</div>
                </div>
                <div class="faq-item">
                    <div class="faq-q">Q. セール価格はいつまでですか？</div>
                    <div class="faq-a">A. 各製品に「残り○日」と表示しています。終了日を過ぎると通常価格に戻るため、お早めの購入をおすすめします。</div>
                </div>
            </div>
        </div>
    </div>
    
    <footer class="footer">
        <p>データ: <a href="https://www.pluginboutique.com/" target="_blank">Plugin Boutique</a> | 価格は変動する場合があります</p>
    </footer>
    
    <!-- モバイル固定フッター -->
    <div class="mobile-footer" id="mobile-footer" style="display:none;">
        <div class="mobile-footer-content">
            <div class="mobile-footer-text">
                <span id="footer-deal-name"></span><br>
                <strong id="footer-deal-price"></strong>
            </div>
            <a href="#" id="footer-deal-link" class="mobile-footer-btn" target="_blank">購入する</a>
        </div>
    </div>
    
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
        
        // おすすめピック
        function renderPicks() {
            const picks = salesData
                .filter(d => d.discountPercent >= 60 && getDaysRemaining(d.endDate) <= 7)
                .slice(0, 3);
            
            if (picks.length === 0) return;
            
            const section = document.getElementById('picks-section');
            section.innerHTML = '<div class="section-title">🔥 今週のおすすめ（まもなく終了）</div><div class="picks-grid">' +
                picks.map(deal => {
                    const days = getDaysRemaining(deal.endDate);
                    let tags = '<span class="pick-tag pick-tag-urgent">残り' + days + '日</span>';
                    tags += '<span class="pick-tag pick-tag-discount">' + deal.discountPercent + '%OFF</span>';
                    if (deal.isPopular) tags += '<span class="pick-tag pick-tag-popular">定番</span>';
                    if (deal.isBeginner) tags += '<span class="pick-tag pick-tag-beginner">初心者向け</span>';
                    
                    return '<div class="pick-card">' +
                        '<div class="pick-tags">' + tags + '</div>' +
                        '<div class="pick-name">' + deal.name + '</div>' +
                        '<div class="pick-meta">' +
                            '<span class="pick-category">' + deal.categoryIcon + ' ' + deal.categoryLabel + '</span>' +
                            '<span class="pick-target">' + deal.target + '</span>' +
                        '</div>' +
                        '<div class="pick-prices">' +
                            '<span class="pick-price-sale">¥' + deal.salePrice.toLocaleString() + '</span>' +
                            '<span class="pick-price-original">¥' + deal.originalPrice.toLocaleString() + '</span>' +
                        '</div>' +
                        '<div class="pick-savings">💰 ¥' + deal.savings.toLocaleString() + ' お得！</div>' +
                        '<a href="' + deal.productUrl + '" target="_blank" class="pick-cta">¥' + deal.salePrice.toLocaleString() + 'で公式購入 →</a>' +
                    '</div>';
                }).join('') + '</div>';
        }
        
        let currentFilter = 'all';
        
        function renderDeals() {
            const container = document.getElementById('deals');
            container.innerHTML = '';
            
            const filtered = currentFilter === 'all' 
                ? salesData 
                : salesData.filter(d => d.discountPercent >= parseInt(currentFilter));
            
            if (filtered.length === 0) {
                container.innerHTML = '<div class="empty-state">該当するセールはありません</div>';
                return;
            }
            
            filtered.forEach(deal => {
                const days = getDaysRemaining(deal.endDate);
                const isUrgent = days <= 3;
                
                const card = document.createElement('div');
                card.className = 'deal-card' + (isUrgent ? ' deal-card-urgent' : '');
                
                let tags = '<span class="tag tag-category">' + deal.categoryIcon + ' ' + deal.categoryLabel + '</span>';
                if (deal.isPopular) tags += '<span class="tag tag-popular">定番</span>';
                if (deal.isBeginner) tags += '<span class="tag tag-beginner">初心者向け</span>';
                tags += '<span class="tag tag-discount">' + deal.discountPercent + '%OFF</span>';
                if (isUrgent) tags += '<span class="tag tag-urgent">残り' + days + '日</span>';
                
                const endText = days <= 7 ? '残り' + days + '日' : deal.endDate.replace('Ends ', '');
                const endClass = isUrgent ? 'deal-end-urgent' : 'deal-end';
                const ctaClass = isUrgent ? 'cta-btn cta-btn-urgent' : 'cta-btn';
                
                card.innerHTML = 
                    '<div class="deal-info">' +
                        '<div class="deal-header">' +
                            '<div class="deal-tags">' + tags + '</div>' +
                        '</div>' +
                        '<div class="deal-name">' + deal.name + '</div>' +
                        '<div class="deal-target">' + deal.target + '</div>' +
                        '<div class="deal-meta">' +
                            '<div class="deal-prices">' +
                                '<span class="price-sale">¥' + deal.salePrice.toLocaleString() + '</span>' +
                                '<span class="price-original">¥' + deal.originalPrice.toLocaleString() + '</span>' +
                            '</div>' +
                            '<span class="deal-savings">¥' + deal.savings.toLocaleString() + ' お得</span>' +
                            '<span class="' + endClass + '">' + endText + '</span>' +
                        '</div>' +
                    '</div>' +
                    '<div class="deal-action">' +
                        '<a href="' + deal.productUrl + '" target="_blank" class="' + ctaClass + '">¥' + deal.salePrice.toLocaleString() + 'で購入</a>' +
                    '</div>';
                
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
        
        renderPicks();
        renderDeals();
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html with {len(sales_data)} items")
