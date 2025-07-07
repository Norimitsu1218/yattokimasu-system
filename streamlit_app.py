import streamlit as st
from datetime import datetime, timedelta
import json

# ページ設定
st.set_page_config(
    page_title="やっときますね - 約束履行支援システム",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
def init_session_state():
    """セッション状態の初期化"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    if 'trial_start_date' not in st.session_state:
        st.session_state.trial_start_date = datetime.now().date()
    
    if 'local_data' not in st.session_state:
        st.session_state.local_data = {
            'promises': [],
            'meetings': [],
            'backup_history': []
        }

def calculate_countdown():
    """無料体験のカウントダウン計算"""
    start_date = st.session_state.trial_start_date
    current_date = datetime.now().date()
    elapsed_days = (current_date - start_date).days
    remaining_days = max(7 - elapsed_days, 0)
    
    if remaining_days > 0:
        return f"残り{remaining_days}日", False
    else:
        return "体験期間終了", True

def show_login_page():
    """ログインページ（シンプル版）"""
    st.markdown("# 🤝 やっときますね")
    st.markdown("**約束を守ることの大事さを知っている人のための履行支援システム**")
    
    st.markdown("---")
    
    st.info("""
    💡 **この言葉の重み**
    
    「やっときますね」に込められた責任と覚悟を、システムが全力でサポートします。
    
    📊 約束履行率 32% → 95% への革命的改善
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        login_tab, register_tab = st.tabs(["ログイン", "新規登録"])
        
        with login_tab:
            st.markdown("### 🔑 ログイン")
            username = st.text_input("ユーザー名", key="login_username")
            password = st.text_input("パスワード", type="password", key="login_password")
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("ログイン", type="primary", use_container_width=True):
                    if username and password:
                        if len(password) >= 8:
                            st.session_state.logged_in = True
                            st.session_state.user_name = username
                            st.rerun()
                        else:
                            st.error("❌ パスワードは8文字以上である必要があります")
                    else:
                        st.error("❌ ユーザー名とパスワードを入力してください")
            
            with col_b:
                if st.button("デモアカウント", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.user_name = "体験ユーザー"
                    st.rerun()
        
        with register_tab:
            st.markdown("### 📝 新規登録")
            new_username = st.text_input("ユーザー名", key="reg_username")
            new_email = st.text_input("メールアドレス", key="reg_email")
            new_password = st.text_input("パスワード", type="password", key="reg_password")
            
            # パスワード要件表示
            if new_password:
                requirements = {
                    "8文字以上": len(new_password) >= 8,
                    "大文字1つ以上": any(c.isupper() for c in new_password),
                    "数字4つ以上": sum(c.isdigit() for c in new_password) >= 4
                }
                
                st.markdown("#### パスワード要件:")
                for req, met in requirements.items():
                    status = "✅" if met else "❌"
                    st.markdown(f"{status} {req}")
            
            if st.button("新規登録", type="primary", use_container_width=True):
                if new_username and new_email and new_password:
                    if (len(new_password) >= 8 and 
                        any(c.isupper() for c in new_password) and 
                        sum(c.isdigit() for c in new_password) >= 4):
                        
                        st.session_state.logged_in = True
                        st.session_state.user_name = new_username
                        st.success("✅ 登録完了！ログインしました")
                        st.rerun()
                    else:
                        st.error("❌ パスワードが要件を満たしていません")
                else:
                    st.error("❌ すべての項目を入力してください")
    
    st.success("🎁 **7日間無料体験** - 今すぐ始めて、約束履行率の劇的改善を体験してください")

def show_dashboard():
    """ダッシュボード表示"""
    countdown_text, is_expired = calculate_countdown()
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 25px 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(30, 60, 114, 0.2);
    ">
        <h1 style="margin: 0 0 8px 0; font-size: 32px; font-weight: 600;">
            やっときますね
        </h1>
        <p style="margin: 0; font-size: 14px; opacity: 0.9;">
            約束を守ることの大事さを知っている人のための履行支援システム - {st.session_state.user_name}様
        </p>
        <div style="
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 8px;
            margin-top: 15px;
        ">
            <div style="font-size: 14px; opacity: 0.9;">🎁 7日間無料体験中</div>
            <div style="font-size: 18px; font-weight: 600;">{countdown_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # メトリクス表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="約束履行率",
            value="95%",
            delta="63%改善"
        )
    
    with col2:
        st.metric(
            label="今月の商談",
            value="12件",
            delta="+3件"
        )
    
    with col3:
        st.metric(
            label="完了した約束",
            value="28件",
            delta="+5件"
        )
    
    with col4:
        st.metric(
            label="信頼度スコア",
            value="96点",
            delta="+12点"
        )
    
    # 機能紹介
    st.markdown("## 🚀 主な機能")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### 🤖 AI自動解析
        - Gemini AIによる商談内容解析
        - 約束事項の自動抽出
        - 重要度判定・期限管理
        """)
        
        st.success("""
        ### 📁 Google Drive連携
        - 顧客別フォルダ自動作成
        - 文書管理自動化
        - ファイル分類システム
        """)
    
    with col2:
        st.warning("""
        ### 📅 Calendar連携
        - 商談予定自動取得
        - リマインダー機能
        - スケジュール最適化
        """)
        
        st.info("""
        ### 📊 履行管理
        - 約束進捗追跡
        - 信頼度評価
        - 成果可視化・ランキング
        """)
    
    # 成果表示
    st.markdown("## 📈 導入効果")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <h3 style="color: #dc3545; margin: 0;">32%</h3>
            <p style="margin: 5px 0; color: #6c757d;">一般的な約束履行率</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3 style="margin: 0; font-size: 24px;">→</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: #d4edda; border-radius: 10px;">
            <h3 style="color: #155724; margin: 0;">95%</h3>
            <p style="margin: 5px 0; color: #155724;">やっときますね利用者</p>
        </div>
        """, unsafe_allow_html=True)

def show_simple_memo():
    """シンプルな商談メモ機能"""
    st.markdown("## 📝 商談メモ作成")
    
    # 基本情報
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("顧客名", placeholder="田中部長")
    with col2:
        company_name = st.text_input("会社名", placeholder="ABC商事")
    
    # 商談内容
    memo_content = st.text_area(
        "商談内容", 
        height=150,
        placeholder="商談で話し合った内容、決定事項、課題等を記録..."
    )
    
    # 約束事項
    st.markdown("### ✅ 約束事項")
    promise_content = st.text_input("約束内容", placeholder="見積書を来週までに送付")
    promise_deadline = st.date_input("期限", datetime.now().date() + timedelta(days=7))
    
    # 保存ボタン
    if st.button("💾 メモを保存", type="primary"):
        if client_name and company_name and memo_content:
            # セッションデータに保存
            memo_data = {
                'id': len(st.session_state.local_data['meetings']) + 1,
                'timestamp': datetime.now().isoformat(),
                'client': client_name,
                'company': company_name,
                'content': memo_content,
                'promise': promise_content,
                'deadline': promise_deadline.isoformat()
            }
            
            st.session_state.local_data['meetings'].append(memo_data)
            st.success("✅ 商談メモを保存しました！")
            st.balloons()
        else:
            st.error("❌ 必須項目を入力してください")

def show_saved_data():
    """保存データ確認"""
    st.markdown("## 📊 保存済みデータ")
    
    meetings = st.session_state.local_data.get('meetings', [])
    
    if meetings:
        st.markdown(f"### 📋 商談履歴 ({len(meetings)}件)")
        
        for meeting in reversed(meetings[-5:]):  # 最新5件を表示
            with st.expander(f"{meeting['company']} - {meeting['client']}様 ({meeting['timestamp'][:10]})"):
                st.markdown(f"**商談内容:** {meeting['content']}")
                if meeting.get('promise'):
                    st.markdown(f"**約束事項:** {meeting['promise']}")
                    st.markdown(f"**期限:** {meeting['deadline']}")
    else:
        st.info("まだ商談データがありません。商談メモタブから記録を開始してください。")

def show_main_app():
    """メインアプリケーション"""
    tab1, tab2, tab3, tab4 = st.tabs(["ダッシュボード", "商談メモ", "データ確認", "ログアウト"])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_simple_memo()
    
    with tab3:
        show_saved_data()
    
    with tab4:
        st.markdown("### ログアウト")
        st.markdown("システムからログアウトします。")
        
        if st.button("ログアウト実行", type="primary"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.success("ログアウトしました")
            st.rerun()

def main():
    """メイン関数"""
    init_session_state()
    
    if not st.session_state.get('logged_in', False):
        show_login_page()
        return
    
    show_main_app()

if __name__ == "__main__":
    main()
