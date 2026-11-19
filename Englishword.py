# d:/
# cd eng_word
# conda activate engword
# streamlit run Englishword.py
import asyncio
import edge_tts
import streamlit as st
import pandas as pd
import os
# print(openpyxl.__version__)
# import openpyxl
# ==================== 内置单词表（可自行修改添加） ====================
# os.chdir("d:/eng_word")
WORDS_ALL=pd.read_excel('./Vocabulary.xlsx')

async def generate_audio(text, voice, rate):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    return audio_bytes

def get_audio(word):
    audio = asyncio.run(generate_audio(text=word, voice="en-GB-SoniaNeural", rate='+0%'))
    # time.sleep(0.05)
    st.audio(audio, format="audio/mp3", autoplay=False)
    
# 自动播放，不需要手动点
gv_list=WORDS_ALL['grade_volume'].drop_duplicates().tolist()
gv_choose=['七年级上册']

unitlist=WORDS_ALL.loc[lambda x :x['grade_volume'].isin(gv_choose)]['unit'].drop_duplicates().tolist()
# unit_choose=['Starter', 'Unit 1', 'Unit 2']
unit_choose= st.multiselect("选择单元：", unitlist)
n_test=20
if unit_choose:
    WORDS=(WORDS_ALL.loc[lambda x :x['grade_volume'].isin(gv_choose)]
           .loc[lambda x :x['unit'].isin(unit_choose)]
           .sample(n_test)).reset_index()
    # WORDS.columns
    # st.write(WORDS)
    #无限模式
    # current_index=random.randint(0, 19)
    # current_word = WORDS.iloc[current_index]
    # if st.button("🔊 朗读", use_container_width=True, type="primary"):#, on_click=get_audio
    #     get_audio(word=current_word["word"])
    #     st.write(current_index)
    #     st.write(current_word["word"])
    #     time.sleep(2)
    #     st.rerun()
    #有限模式
    # words = WORDS["word"]

    # 表头
    # col1, col2 = st.columns([2, 8])
    # col1.write("&zwnj;**单词**&zwnj;")
    # col2.write("&zwnj;**操作**&zwnj;")
    
    for current_index in range(len(WORDS)):
        c1, c2 ,c3= st.columns([1, 4,4], gap="small", wrap=False)
        #current_index=0
        cr_word=WORDS.iloc[current_index]#
        with c1:
            st.write(cr_word["word"])
        with c2:
            st.text(f'{cr_word["phonetic"]}\n{cr_word["word_class"]}{cr_word["meaning"]}')
        with c3:
            get_audio(cr_word["word"])
        

else:
    pass

    
# st.markdown("""
# <style>
# .stButton button {
#     font-size: 1.1rem;
#     padding: 0.6rem;
# }
# audio {
#     display: none; /* 隐藏多余的播放器控件，只保留自动播放 */
# }
# </style>
# """, unsafe_allow_html=True)    


# WORDS = [
#     {"word": "abandon", "phonetic": "/əˈbændən/", "meaning": "v. 放弃，抛弃"},
#     {"word": "ability", "phonetic": "/əˈbɪləti/", "meaning": "n. 能力，才能"},
#     {"word": "abroad", "phonetic": "/əˈbrɔːd/", "meaning": "adv. 在国外，到国外"},
#     {"word": "accept", "phonetic": "/əkˈsept/", "meaning": "v. 接受，同意"},
#     {"word": "achieve", "phonetic": "/əˈtʃiːv/", "meaning": "v. 实现，达到"},
#     {"word": "acquire", "phonetic": "/əˈkwaɪə(r)/", "meaning": "v. 获得，取得"},
#     {"word": "adapt", "phonetic": "/əˈdæpt/", "meaning": "v. 适应，改编"},
#     {"word": "adequate", "phonetic": "/ˈædɪkwət/", "meaning": "adj. 足够的，适当的"},
#     {"word": "adjust", "phonetic": "/əˈdʒʌst/", "meaning": "v. 调整，适应"},
#     {"word": "admit", "phonetic": "/ədˈmɪt/", "meaning": "v. 承认，准许进入"},
#     {"word": "adopt", "phonetic": "/əˈdɒpt/", "meaning": "v. 采用，收养"},
#     {"word": "advance", "phonetic": "/ədˈvɑːns/", "meaning": "v. 前进，进步"},
#     {"word": "advantage", "phonetic": "/ədˈvɑːntɪdʒ/", "meaning": "n. 优势，有利条件"},
#     {"word": "adventure", "phonetic": "/ədˈventʃə(r)/", "meaning": "n. 冒险，奇遇"},
#     {"word": "advertise", "phonetic": "/ˈædvətaɪz/", "meaning": "v. 做广告，宣传"},
#     {"word": "advise", "phonetic": "/ədˈvaɪz/", "meaning": "v. 建议，劝告"},
#     {"word": "affect", "phonetic": "/əˈfekt/", "meaning": "v. 影响，感染"},
#     {"word": "afford", "phonetic": "/əˈfɔːd/", "meaning": "v. 买得起，承担得起"},
#     {"word": "afraid", "phonetic": "/əˈfreɪd/", "meaning": "adj. 害怕的，担心的"},
#     {"word": "agree", "phonetic": "/əˈɡriː/", "meaning": "v. 同意，赞成"},
# ]