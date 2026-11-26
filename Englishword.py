# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:16:45 2026

@author: 80925
"""

import streamlit as st
import edge_tts
import asyncio
import io
import time
import pandas as pd
# ==============================================
# 页面基础配置
# ==============================================
st.set_page_config(
    page_title="单词朗读工具",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================
# 1. 初始化状态 & 模拟单元单词数据（可替换为你自己的词表）
# ==============================================
@st.cache_data
def load_data():
    return pd.read_excel('./Vocabulary.xlsx')

WORDS_ALL=load_data()   

gv_list=WORDS_ALL['grade_volume'].drop_duplicates().tolist()
gv_choose=['七年级上册']


# unit_choose=['Starter', 'Unit 1', 'Unit 2']
# n_test=20

@st.cache_data
def load_unitdata(unit):
    WORDS=(WORDS_ALL.loc[lambda x :x['grade_volume'].isin(gv_choose)]
           .loc[lambda x :x['unit'].isin(unit)])
    return WORDS


if "current_unit" not in st.session_state:
    st.session_state.current_unit = 'test'
if "selected_voice" not in st.session_state:
    st.session_state.selected_voice = "en-GB-SoniaNeural" # 默认英式女声
if "playing_word" not in st.session_state:
    st.session_state.playing_word = None

# ==============================================
# 2. 缓存音频生成（同单词+同声音只生成一次，无重复等待）
# ==============================================
@st.cache_data
def generate_audio(word: str, voice_id: str):
    async def _fetch_audio():
        try:
            communicate = edge_tts.Communicate(word, voice_id, rate="+0%")
            buf = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
            buf.seek(0)
            return buf.read()
        except Exception as e:
            return None
    return asyncio.run(_fetch_audio())

# ==============================================
# 3. col2 局部刷新片段（仅声音选择/朗读按钮触发）
# ==============================================
@st.fragment
def col2_pronunciation_panel(word_sldf,voice,tabtype):#word_selected_df
    
    # ==============================================
    
    # 验证标识：col2重跑时间，每次声音切换/朗读都会更新
    # st.caption(f"🔄 col2 最近刷新: {time.strftime('%H:%M:%S')}")
    # st.divider()

    # 每个单词对应独立的读音条，与col1单词一一对应
    for current_index in range(len(word_sldf)):
        cr_word=word_sldf.iloc[current_index]#
        word=cr_word["word"]
    
        col_word_btn,col_word_pc, col4= st.columns([2, 3,3], gap="small", wrap=False)
        with col_word_btn:
            # 固定高度占位，避免点击后布局跳动
            st.write(word)
        with col_word_pc:    
            st.text(f'{cr_word["phonetic"]}\n{cr_word["word_class"]}{cr_word["meaning"]}')

        with col4:
            with st.container(height=40, border=False):
                # if st.session_state.playing_word == word:
                    audio_bytes = generate_audio(word, voice)
                    if audio_bytes:
                        # 按钮点击触发播放，完全符合浏览器自动播放策略，100%有声音
                        st.audio(audio_bytes, format="audio/mp3", autoplay=False, start_time=0)
                    else:
                        st.error("音频加载失败，请检查网络")
# ==============================================
# 4. 主页面布局
# ==============================================
# 全局单元选择（切换单元时触发全页面重跑，col1+col2同步刷新）
# 可选语音配置
VOICE_OPTIONS = {
    "🇬🇧 英式女声 (Sonia)": "en-GB-SoniaNeural",
    "🇬🇧 英式男声 (Ryan)": "en-GB-RyanNeural",
    "🇺🇸 美式女声 (Jenny)": "en-US-JennyNeural",
    "🇺🇸 美式男声 (Guy)": "en-US-GuyNeural",
    "🇨🇳 中文女声 (晓晓-通用)": "zh-CN-XiaoxiaoNeural",
    "🇨🇳 中文男声 (云希-年轻)": "zh-CN-YunxiNeural",
}
voice_names = list(VOICE_OPTIONS.keys())
voice_id_to_name = {v: k for k, v in VOICE_OPTIONS.items()}

# 声音选择下拉框（交互仅触发本片段重跑，col1完全不动）
current_voice_name = voice_id_to_name.get(
    st.session_state.selected_voice,
    voice_names[0]
)


unitlist=WORDS_ALL.loc[lambda x :x['grade_volume'].isin(gv_choose)]['unit'].drop_duplicates().tolist()
with st.sidebar:
    st.header("⚙️ 设置")
    selected_unit= st.multiselect("选择单元：", unitlist,key="unit_selector",default=['test'])#,index=unitlist.index(st.session_state.key_unit)
    selected_name = st.selectbox(
        "选择朗读音色",
        options=voice_names,
        index=voice_names.index(current_voice_name),
        key="voice_selector"
    )
    st.session_state.selected_voice = VOICE_OPTIONS[selected_name]
# 单元变化时重置播放状态
if selected_unit != st.session_state.current_unit:
    st.session_state.current_unit = selected_unit
    st.session_state.playing_word = None
    st.rerun()

if st.session_state.current_unit:
    # 获取当前单元单词列表
    word_sldf = load_unitdata(unit=st.session_state.unit_selector)
    
    tab_learn, tab_exam = st.tabs(["📚 学习模式", "📝 考核模式"])
    with tab_learn:
        # 行为：切换声音/点朗读时局部独立刷新；切换单元时跟随全局刷新
        # --------------------------
        col2_pronunciation_panel(word_sldf,voice=st.session_state.selected_voice,tabtype='learn')
        
    with tab_exam:
        # 行为：切换声音/点朗读时局部独立刷新；切换单元时跟随全局刷新
        # --------------------------
        n_test= st.selectbox( "选择朗读音色",options=[1,15,20,25,30],index=0)
        col2_pronunciation_panel(word_sldf.sample(n_test),voice=st.session_state.selected_voice,tabtype='test')
