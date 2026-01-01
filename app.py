import streamlit as st

# --- ページ設定 ---
st.set_page_config(
    page_title="NotebookLM専用 資料構成プロンプトメーカー",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 定数・辞書定義（トンマナデータ） ---
STYLES = {
    "1. Strategic & Logical（戦略・コンサルティング）": {
        "desc": "経営層への報告、戦略提案。信頼感と論理性を重視。",
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
        "desc": "投資家向けピッチ、新製品発表。感情と未来を重視。",
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
    """YAML形式のテキストを生成する（改行を明示）"""
    visual = yaml_params["Visual Mood"]
    text = yaml_params["Text Tone"]
    
    # 改行コード \n を明示的に使用してフォーマット崩れを防ぐ
    return (
        f"## トンマナ設定 (Style Parameter)\n"
        f"- **Style Title:** {style_name}\n"
        f"- **Target Audience:** {target if target else '指定なし（文脈から判断）'}\n"
        f"- **Visual Mood:**\n"
        f"  - Base Color: {visual['Base Color']}\n"
        f"  - Vibe: {visual['Vibe']}\n"
        f"  - Density: {visual['Density']}\n"
        f"- **Text Tone:**\n"
        f"  - Voice: {text['Voice']}\n"
        f"  - Structure: {text['Structure']}\n"
        f"  - Keywords: {text['Keywords']}\n"
    )

def create_prompt(purpose, target, presenter, style_name, style_data):
    """最終的なプロンプトを作成する（議事録はここには含めない）"""
    
    yaml_section = generate_yaml_text(style_name, target, style_data["yaml_params"])
    presenter_info = f"- **Presenter:** {presenter}\n" if presenter else ""
    
    # NotebookLMのチャット欄に入力するための指示プロンプト
    prompt = (
        f"# プレゼン資料作成依頼\n\n"
        f"あなたはプロフェッショナルなプレゼンテーション資料作成のコンサルタントです。\n"
        f"**読み込ませた「ソース（議事録・メモ）」**と、以下の「要件定義（トンマナ）」に基づいて、\n"
        f"スライド構成案（アウトライン）と、各スライドの具体的なスクリプト（原稿）を作成してください。\n\n"
        f"---\n\n"
        f"## 1. プレゼンの前提情報\n"
        f"- **Purpose (目的):** {purpose}\n"
        f"{presenter_info}\n"
        f"{yaml_section}\n"
        f"---\n\n"
        f"## 2. 出力形式（Output Format）\n"
        f"Markdown形式で以下の構造で出力してください。\n\n"
        f"1. **タイトルスライド案**（キャッチーなタイトルとサブタイトル）\n"
        f"2. **スライド構成案**（スライド枚数は内容に応じて適切に調整）\n"
        f"   - 各スライドについて以下を記述:\n"
        f"     - **Slide X: [スライドタイトル]**\n"
        f"     - **Visualイメージ:** (指定されたVisual Moodに基づき、どんな図解や画像を配置すべきか具体的に指示)\n"
        f"     - **Main Message:** (このスライドで伝えたい唯一のメッセージ)\n"
        f"     - **Bullet Points:** (箇条書きで記載する要素。ソースの内容を反映すること)\n"
        f"     - **Script:** (プレゼンターが話すための原稿。指定されたVoice/Toneに従うこと)\n"
    )
    return prompt

# --- UI構築 ---

st.title("📘 NotebookLM専用 資料構成プロンプトメーカー")
st.markdown("""
議事録やメモから、プレゼン資料の構成案を一瞬で作成するためのアプリです。
**NotebookLM** に情報を読み込ませ、このアプリで作った「指示書（プロンプト）」を渡すだけで完了します。
""")

# 手順の概要を表示
with st.expander("使い方（全体の流れ）", expanded=True):
    st.markdown("""
    1. **【Step 1】** このアプリに議事録を入力し、**コピーしてNotebookLMの「ソース」に追加**します。
    2. **【Step 2, 3】** 資料の目的や雰囲気を設定します。
    3. **【Generate】** 生成されたプロンプトを**NotebookLMの「チャット」に送信**します。
    """)

st.divider()

# --- STEP 1: 素材の入力 ---
st.header("Step 1. 素材（議事録）の準備")
st.info("まずは、資料の元となるテキスト（議事録、メモ、文字起こし）をここに貼り付けて整理します。")

transcript = st.text_area(
    "議事録・メモ入力エリア",
    height=300,
    placeholder="ここにGeminiやZoomの文字起こし、または箇条書きのメモを貼り付けてください。\n\n（ここに入力した内容は、次のステップでNotebookLMのソースとして使います）"
)

# 素材コピー用の案内
if transcript:
    st.markdown("👇 **以下の手順を実行してください**")
    st.warning("1. 上記のテキストを全選択してコピーしてください。\n2. NotebookLMを開き、左上の「＋」→「テキストをコピーして貼り付け」でソースとして追加してください。")
    st.markdown("[📘 NotebookLM を開く](https://notebooklm.google/)")

st.divider()

# --- STEP 2: 前提情報の入力 ---
st.header("Step 2. 前提情報の入力")
st.caption("誰に向けて、何のために話すのかを設定します。")

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

# --- STEP 3: トンマナの選択 ---
st.header("Step 3. トンマナの選択")
st.caption("資料の「デザイン」と「文章の雰囲気」を決定します。")

style_key = st.radio(
    "雰囲気を選択",
    list(STYLES.keys()),
    index=0,
    horizontal=False
)

st.info(f"**選択中: {style_key}**\n\n{STYLES[style_key]['desc']}")

st.divider()

# 生成ボタン
if st.button("指示プロンプトを生成する 🚀", type="primary", use_container_width=True):
    if not transcript:
        st.error("⚠️ Step 1 で素材となるテキストを入力してください（NotebookLMにソースとして入れるためです）。")
    else:
        # プロンプト生成
        generated_prompt = create_prompt(
            purpose=purpose,
            target=target,
            presenter=presenter,
            style_name=style_key,
            style_data=STYLES[style_key]
        )
        
        st.divider()
        st.subheader("✅ 生成完了！")
        st.success("以下の手順でNotebookLMに入力してください")
        
        st.markdown("#### 手順①：ソースの確認")
        st.markdown("Step 1で入力した議事録が、NotebookLMの「ソース」に追加されていることを確認してください。")
        
        st.markdown("#### 手順②：チャットへの送信")
        st.markdown("以下のプロンプトをコピーして、**NotebookLMのチャットボックス**に貼り付けて送信してください。")
        
        # プロンプト表示（コピーボタン付き）
        st.code(generated_prompt, language="markdown")
        
        st.caption("※このプロンプトは、あなたが追加したソース（議事録）を参照して資料を作るように指示します。")
