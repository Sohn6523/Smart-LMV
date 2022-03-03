from re import S
import streamlit as st
import streamlit_modal as modal
import streamlit.components.v1 as components


if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# 초기 설정
st.set_page_config(page_title="test", layout="wide")

sidebar = st.sidebar
sidebar.header("메뉴")

st.write("업데이트 날짜 : 2022-02-25, 09:00:00")

st.header("AI예측")
st.write("ddddddddddd")

#st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    st.header("공정별 요약")
    st.subheader("1,2 전기실")
    with st.expander("1. Annealer : 동일한 공정이나 4개 모두 다른 부하. 사용하는 전류 패턴도 모두 다르며 특별한 공통점을 찾을 수 없음"):
        open_modal = st.button("SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_17.ACBOCR_S")
        if open_modal:
            st.session_state['key'] = 'SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_17.ACBOCR_S'
            modal.open()

        open_modal_2 = st.button("SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_18.ACBOCR_S")
        if open_modal_2:
            st.session_state['key'] = 'SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_18.ACBOCR_S'
            modal.open()

        if modal.is_open():
            with modal.container():
                st.subheader("상세내용확인")

                ddd = st.session_state.key
                if ddd == 'SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_17.ACBOCR_S':
                    st.write('SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_17.ACBOCR_S')
                    st.image('assets/process/SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_17.ACBOCR_S.png')

                elif ddd == 'SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_18.ACBOCR_S':
                    st.write('SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_18.ACBOCR_S')
                    st.image('assets/process/SmartMV.LSM_JH.FEMS.1ST_ELEC.LV.ACB_18.ACBOCR_S.png')
    with st.expander("2. Cascade : 평균 TDD 약 8% (0~ 약 30% 까지 계속 변화함)"):
        st.write("ddd")
    with st.expander("3. Casting : 2전기실의 부하 종류가 모두 달라 특별한 공통점을 찾을 수 없음, 2 전기실 TDD는 낮은 편 10% 내외"):
        st.write("ddd")

with col2:
    st.header("노드별 요약")
    st.subheader("1전기실")
    with st.expander("LC1"):
        st.write("ddd")
    with st.expander("LC2"):
        st.write("ddd")
    with st.expander("LC3"):
        st.write("ddd")
    with st.expander("LC4"):
        st.write("ddd")

    st.subheader("2전기실")
    with st.expander("LC13"):
        st.write("SmartMV.LSM_JH.FEMS.2ND_ELEC.LV.LC_13.01_MCCB")
        st.write("SmartMV.LSM_JH.FEMS.2ND_ELEC.LV.LC_13.02_MCCB")
        st.write("SmartMV.LSM_JH.FEMS.2ND_ELEC.LV.LC_13.03_MCCB")
    with st.expander("LC22"):
        st.write("ddd")


# open_modal = st.button("Open")
# if open_modal:
#     st.session_state['key'] = '1'
#     modal.open()

# open_modal_2 = st.button("Open2")
# if open_modal_2:
#     st.session_state['key'] = '2'
#     modal.open()

# if modal.is_open():
#     with modal.container():
#         st.write("Text goes here")

#         ddd = st.session_state.key
#         if ddd == '1':
#             st.write('111111111111')

#             html_string = '''
#             <h1>HTML string in RED11</h1>

#             <script language="javascript">
#             document.querySelector("h1").style.color = "red";
#             </script>
#             '''
#             components.html(html_string)

#             st.write("Some fancy text")
#             value = st.checkbox("Check me")
#             st.write(f"Checkbox checked: {value}")
#         elif ddd == '2':
#             st.write('22222222222')

#             html_string = '''
#             <h1>HTML string in RED22</h1>

#             <script language="javascript">
#             document.querySelector("h1").style.color = "red";
#             </script>
#             '''
#             components.html(html_string)

#             st.write("Some fancy text")
#             value = st.checkbox("Check me")
#             st.write(f"Checkbox checked: {value}")