import streamlit as st

# ページ設定
st.set_page_config(
    page_title="プレゼン資料構成生成メーカー",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 定数・辞書定義（トンマナデータ） ---
STYLES = {
    "1. Strategic & Logical（戦略・コンサルティング）": {
        "desc": "経営層への報告、戦略提案、信頼感と論理性を重視。",
        "keywords": "信頼、知性、断定的、ロジカル、PREP法",
        "yaml_params": {
            "Visual Mood": {
                "Base Color": "Navy Blue, Dark Gray, White",
                "Vibe": "信頼感, 堅実, プロフェッショナル",
                "Density": "情報量は多めだが、グリッドで整列・構造化されていること"
            },
            "Text Tone": {
                "Voice": "論理的かつ断定的（「〜である」調）",
                "Structure": "結論（Answer）→ 根拠（Why）→ 詳細（Detail）",
                "Keywords": "ROI, シナジー, 最適化, ガバナンス, 定量的"
            }
        }
    },
    "2. Visionary & Minimal（ビジョナリー・ピッチ）": {
        "desc": "投資家向けピッチ、新製品発表。感情と未来を想起させる。",
        "keywords": "情熱、未来、シンプル、ストーリーテリング",
        "yaml_params": {
            "Visual Mood": {
                "Base Color": "Black background with Vivid Accent or Pure White",
                "Vibe": "革新的, エモーショナル, インパクト",
                "Density": "極めて少ない。1スライド1メッセージ。画像・図解メイン"
            },
            "Text Tone": {
                "Voice": "情熱的、短文、問いかけを含む（Steve Jobsスタイル）",
                "Structure": "Why（なぜやるのか）から始まり、Vision（未来）で終わる",
                "Keywords": "Revolution, Future, Imagine, Change"
            }
        }
    },
    "3. Friendly & Pop（親しみ・カジュアル）": {
        "desc": "社内イベント、若手向け、BtoC提案。共感重視。",
        "keywords": "親しみ、パステル、共感、柔らかい",
        "yaml_params": {
            "Visual Mood": {
                "Base Color": "Pastel Colors, Warm Colors (Orange/Yellow)",
                "Vibe": "親しみやすい, 楽しい, 柔らかい",
                "Density": "イラスト多用、余白多め、曲線的なデザイン"
            },
            "Text Tone": {
                "Voice": "「です・ます」調、語りかけるような口調、共感重視",
                "Structure": "クイズや例え話を交えたインタラクティブな構成",
                "Keywords": "みんなで, 楽しさ, つながり, 成長"
            }
        }
    },
    "4. Formal & Detailed（官公庁・堅実・マニュアル）": {
        "desc": "詳細仕様書、金融、官公庁。網羅性と正確性重視。",
        "keywords": "堅実、詳細、正確、マニュアル",
        "yaml_params": {
            "Visual Mood": {
                "Base Color": "Blue, Green (Calm single colors)",
                "Vibe": "真面目, 正確, 公的",
                "Density": "文字量多い。枠線や表組み（Table）を多用し網羅的に"
            },
            "Text Tone": {
                "Voice": "堅い敬語（〜致します）、説明的、客観的",
                "Structure": "起承転結。注釈や出典を明確に記載する",
                "Keywords": "遵守, 規定, 詳細, 手順, エビデンス"
            }
        }
    },
    "5. Futuristic & Cyber（テック・先進的）": {
        "desc": "Web3, AI, エンジニア向け。最先端技術感。",
        "keywords": "テック、ダークモード、革新、専門的",
        "yaml_params": {
            "Visual Mood": {
                "Base Color": "Dark Mode (Black/Deep Blue) + Neon (Cyan/Magenta)",
                "Vibe": "先進的, デジタル, クール",
                "Density": "アイソメトリック図解、幾何学模様、データビジュアライゼーション"
            },
            "Text Tone": {
                "Voice": "専門用語を使用、スマート、革新的",
                "Structure": "Features（機能）とBenefits（技術的利点）の対比",
                "Keywords": "Scalability, Architecture, Protocol, Next-Gen"
            }
        }
    },
    "6. Elegant & Sophisticated（ラグジュアリー・高品位）": {
        "desc": "ブランド提案、高所得者向け。世界観と品格。",
        "keywords": "洗練、余白、高級感、情緒的",
        "yaml_params": {
            "Visual Mood": {
                "Base Color": "Gold, Beige, Black, White",
                "Vibe": "洗練, 上品, 高品質",
                "Density": "余白（Whitespace）を贅沢に使う。文字は最小限"
            },
            "Text Tone": {
                "Voice": "洗練された表現、形容詞を効果的に使う、詩的",
                "Structure": "機能よりも「情緒的価値（Emotional Value）」を訴求",
                "Keywords": "Experience, Quality, Philosophy, Aesthetics"
            }
        }
    }
}

# --- 関数定義 ---

def generate_yaml_text(style_name, target, yaml_params):
    """YAML形式のテキストを生成する"""
    visual = yaml_params["Visual Mood"]
    text = yaml_params["Text Tone"]
    
    yaml_text = f"""## トンマナ設定 (Style Parameter)
- **Style Title:** {style_name}
- **Target Audience:** {target if target else "指定なし（文脈から判断）"}
- **Visual Mood:**
  - Base Color: {visual['Base Color']}
  - Vibe: {visual['Vibe']}
  - Density: {visual['Density']}
- **Text Tone:**
  - Voice: {text['Voice']}
  - Structure: {text['Structure']}
  - Keywords: {text['Keywords']}
"""
    return yaml_text

def create_prompt(transcript, purpose, target, presenter, style_name, style_data):
    """最終的なプロンプトを作成する"""
    
    yaml_section = generate_yaml_text(style_name, target, style_data["yaml_params"])
    
    presenter_info = f"- **Presenter:** {presenter}" if presenter else ""
    
    prompt = f"""
# プレゼン資料作成依頼

あなたはプロフェッショナルなプレゼンテーション資料作成のコンサルタントです。
以下の「インプット情報（議事録・メモ）」と「要件定義（トンマナ）」に基づいて、
スライド構成案（アウトライン）と、各スライドの具体的なスクリプト（原稿）を作成してください。

---

## 1. プレゼンの前提情報
- **Purpose (目的):** {purpose}
{presenter_info}

{yaml_section}

---

## 2. インプット情報（議事録・メモ）
以下のテキスト内容を情報のソースとして使用してください。
不足している情報は、トンマナに合わせて適切なプレースホルダー（[ここにXXのデータを入れる]等）を設置してください。

```text
{transcript}
3. 出力形式（Output Format）
Markdown形式で以下の構造で出力してください。

タイトルスライド案（キャッチーなタイトルとサブタイトル）

スライド構成案（スライド枚数は内容に応じて適切に調整）

各スライドについて以下を記述:

Slide X: [スライドタイトル]

Visualイメージ: (指定されたVisual Moodに基づき、どんな図解や画像を配置すべきか具体的に指示)

Main Message: (このスライドで伝えたい唯一のメッセージ)

Bullet Points: (箇条書きで記載する要素)

Script: (プレゼンターが話すための原稿。指定されたVoice/Toneに従うこと)

""" 
    return prompt

# --- UI構築 ---

st.title("📑 資料作成特化型 プロンプトメーカー")
st.markdown("""
> 「どんな資料を作成して良いのかわからん」を解決します。
> 議事録を貼って、トンマナを選ぶだけ。あとはAI（Gemini, ChatGPT, NotebookLM）がやってくれます。
""")

st.divider()

# --- STEP 1: 素材の入力 ---
st.header("Step 1. 素材の入力")
st.caption("議事録、メモ、Zoomの文字起こしなどを貼り付けてください。")

transcript = st.text_area(
    "インプット情報",
    height=400,
    label_visibility="collapsed",
    placeholder="ここにGeminiやZoomの文字起こし、または箇条書きのメモを貼り付けてください。\n\n例：\n・今回のプロジェクトの目的は売上20%アップ\n・課題は新規顧客の獲得コスト\n・解決策としてSNS広告の強化を提案したい..."
)

st.divider()

# --- STEP 2: 前提情報の入力 ---
st.header("Step 2. 前提情報の入力")
st.caption("誰に向けて、何のために話すのかを設定します。")

# 入力項目を見やすく並べる
col_p1, col_p2 = st.columns(2)

with col_p1:
    purpose = st.selectbox(
        "資料の目的",
        ["営業・商談", "社内承認・決裁", "社内提案・企画", "他社への企画提案", "社内報告（進捗・完了）", "社内勉強会・ナレッジ共有", "その他（自分で記述）"]
    )
    if purpose == "その他（自分で記述）":
        purpose = st.text_input("具体的な目的を入力してください")

with col_p2:
    target = st.text_input("プレゼンの対象者", placeholder="例：経営企画部 部長、クライアント担当者（省略可）")
    presenter = st.text_input("自分の所属・名前", placeholder="タイトルスライド用（省略可）")

st.divider()

# --- STEP 3: トンマナの選択 ---
st.header("Step 3. トンマナの選択")
st.caption("資料の「デザイン」と「文章の雰囲気」を決定します。")

style_key = st.radio(
    "雰囲気を選択",
    list(STYLES.keys()),
    index=0,
    horizontal=False
)

# 選択されたスタイルの詳細を表示
st.info(f"**選択中: {style_key}**\n\n{STYLES[style_key]['desc']}")

st.divider()

# 生成ボタン
if st.button("プロンプトを生成する 🚀", type="primary", use_container_width=True):
    if not transcript:
        st.warning("⚠️ Step 1 で素材となるテキストを入力してください。")
    else:
        # プロンプト生成処理
        generated_prompt = create_prompt(
            transcript=transcript,
            purpose=purpose,
            target=target,
            presenter=presenter,
            style_name=style_key,
            style_data=STYLES[style_key]
        )

        st.success("✅ プロンプトを生成しました！以下のコードをコピーしてAIツールで使用してください。")

        # タブでツールごとの使い方を分ける
        tab1, tab2, tab3 = st.tabs(["NotebookLM", "Gemini 1.5 / Canvas", "ChatGPT / Claude"])

        with tab1:
            st.markdown("### 📘 NotebookLMでの使い方")
            st.markdown("""
            1. [NotebookLM](https://notebooklm.google/) を開く。
            2. 左側の「ソースを追加」から、「テキストをコピーして貼り付け」を選び、**議事録（素材）のみ** を貼り付けるか、議事録ファイルをアップロードする。
            3. 以下のプロンプトをチャットボックスに貼り付けて送信する。
            *(※NotebookLMはソースを参照する力が強いため、議事録はソースとして読ませるのがベストです)*
            """)
            st.code(generated_prompt, language="markdown")

        with tab2:
            st.markdown("### 💎 Gemini (Advanced/Canvas) での使い方")
            st.markdown("""
            1. [Gemini](https://gemini.google.com/) を開く（Canvas機能推奨）。
            2. 以下のプロンプトをそのまま貼り付けて送信する。
            """)
            st.code(generated_prompt, language="markdown")
            
        with tab3:
            st.markdown("### 🤖 ChatGPT / Claude での使い方")
            st.markdown("""
            1. ChatGPT または Claude のチャット欄を開く。
            2. 以下のプロンプトをそのまま貼り付けて送信する。
            """)
            st.code(generated_prompt, language="markdown")
