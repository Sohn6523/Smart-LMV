# python 3.8.7
from collections import defaultdict
import datetime
from pyparsing import col
import streamlit as st
import pandas as pd

from libs import DB, query_get_thdval, query_get_tddval, query_get_other, query_get_currentval, query_get_voltageval, query_get_thdval_h_m_timestamp
from libs import plot_range, plot_detail
from libs import fit_timeindex

# 로컬디비 
HOST = "127.0.0.1"
PORT = 3307
DATABASE = "SMARTSYSTEM"
USER = "root"
PWD = "1562"

columns = ["timestamp", "sourceId", "value(event)", "eventType", "message_ko", "activeState", "severity"]
df_event = pd.DataFrame(
    columns = columns
)
with DB(HOST, PORT, DATABASE, USER, PWD) as db: # event정보 받아오기 
    query = f"SELECT date_format(`timestamp`, '%Y-%m-%d %H:%m') , `sourceId`, `value`, `eventType`, `message_ko`, `activeState`, `severity` FROM event2"
    db.execute(query)
    rows = db.fetchall()
    #print(rows)
    df_tmp = pd.DataFrame(rows, columns = columns)
    df_event = pd.concat([df_event, df_tmp])
    df_event = df_event.reset_index(drop=True)
#print(df_event)


# 초기 설정
st.set_page_config(page_title="SmartLMV", layout="wide")

# 데이터 관련 함수
@st.cache
def get_tags():
    df_namekey = pd.read_excel("./ref/query/thdia_namekeyinfo.xlsx", "Sheet1")
    df_tag = df_namekey[["browsePath", "id"]]
    return df_tag.values.tolist()

@st.cache
def get_tablenames():
    df_tablenames = pd.read_csv("./ref/tablename.csv")
    df_tablenames = df_tablenames.dropna(how="any")
    df_tablenames = df_tablenames.reset_index(drop=True)
    return df_tablenames
    
def get_date(date:str="2022-01-28"):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()

@st.cache
def get_dtype(columns: list):
    dict_dtype = defaultdict(lambda: "float64") # 기본type은 float 
    dict_dtype["timestamp"] = "datetime64[s]"
    
    for column in columns:
        if column == "phase":
            dict_dtype[column] = "string"
        print(dict_dtype[column])
    return dict(dict_dtype)

@st.cache
def get_columns(add_columns :list = []):
    return ["timestamp", "value", "minValue", "maxValue"] + add_columns

@st.cache(allow_output_mutation=True, max_entries=2)
def get_data_all_phase(queryfuncs: list, index, start_date, end_date):
    browsepath, id = get_tags()[index]    
    print(f"browsepath = {browsepath}")
    print(f"id = {id}")

    # if 'id' not in st.session_state:
    #     st.session_state['id'] = id
    
    columns = get_columns(["phase"])
    dtypes = get_dtype(columns)
    
    with DB(HOST, PORT, DATABASE, USER, PWD) as db:
        query_list = []
        # functions = (query_get_thdval, query_get_tddval)
        results = [pd.DataFrame(columns=columns) for _ in range(len(queryfuncs))]

        for phase in ["A", "B", "C"]:
            for idx, func in enumerate(queryfuncs):
                query = func(phase, id, start_date, end_date)
                query_list.append(query)

                db.execute(query)
                #print(query)
                rows = db.fetchall()

                df_tmp = pd.DataFrame(rows, columns=columns)
                results[idx] = pd.concat([results[idx], df_tmp])

        results = [fit_timeindex(df_tmp.reset_index(drop=True).astype(dtypes)) for df_tmp in results]
        
    return results, query_list

@st.cache(max_entries=2)
def get_data_without_phase(tablenames, index, start_date, end_date):
    browsepath, id = get_tags()[index]    
    print(f"browsepath = {browsepath}")
    print(f"id = {id}")
    
    columns = get_columns()
    dtypes = get_dtype(columns)
    
    with DB(HOST, PORT, DATABASE, USER, PWD) as db:
        query_list = []
        results = [pd.DataFrame(columns=columns) for _ in range(len(tablenames))]
        
        for idx, tablename in enumerate(tablenames):
            query = query_get_other(tablename, id, start_date, end_date)
            query_list.append(query)

            db.execute(query)
            print(query)
            rows = db.fetchall()

            df_tmp = pd.DataFrame(rows, columns=columns)
            results[idx] = pd.concat([results[idx], df_tmp])

        results = [fit_timeindex(df_tmp.reset_index(drop=True).astype(dtypes)) for df_tmp in results]
        
    return results, query_list

# 콜백 함수
def on_run_clicked():
    st.session_state.data_loaded = True
    
def on_setting_changed():
    st.session_state.data_loaded = False
    
# 페이지
def body(harmonic_data, target_data, query_list):
    st.title("전류 THD")
    
    st.subheader("전류-전압 그래프")
    st.write("좌측: 전류, 우측: 전압")
    for result, col in zip(other_data, st.columns(2)):
        fig_range = plot_detail(result)
        #col.plotly_chart(fig_range, use_container_width=True)
    
    st.subheader("전류 THD-TDD 그래프")
    st.write("좌측: 전류 THD, 우측: 전류 TDD")
    for result, col in zip(harmonic_data, st.columns(2)):
        fig_trend = plot_detail(result)
        #col.plotly_chart(fig_trend, use_container_width=True)

    st.header("Query")
    st.code("\n".join(query_list), language="sql")

    st.success(f"Done {browsepath} ({id})")

if __name__ == "__main__":
    if "tag_idx" not in st.session_state:
        st.session_state.tag_idx = 0
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "selected_plot" not in st.session_state:
        st.session_state.selected_plot = []
    
    sidebar = st.sidebar
    sidebar.header("Setting")

    start_date = sidebar.date_input("Start date", value=get_date(), on_change=on_setting_changed).strftime("%Y-%m-%d")
    end_date = sidebar.date_input("End date", value=get_date("2022-02-03"), on_change=on_setting_changed).strftime("%Y-%m-%d")

    list_tags = get_tags()
    sidebar.number_input("Tag index", min_value=0, max_value=len(list_tags)-1, step=1, format="%d", value=st.session_state.tag_idx, key="tag_idx", on_change=on_setting_changed)

    tag_idx = sidebar.selectbox("Tag name", range(len(list_tags)), index=st.session_state.tag_idx, format_func=lambda i: ".".join(list_tags[i][0].split(".")[3:]), key="tag_idx", on_change=on_setting_changed)

    tags_name_list = []
    for a in list_tags:
        tags_name_list.append(a[0])

    def find_same_lv_list(name):
        global same_level_mccb_list

        col1, col2 = st.columns([1,1])
        #get_all_data_btn = st.button("Get all data", on_click=on_run_clicked)
        for a in tags_name_list:
            if a.split('.')[5] == name:
                same_level_mccb_list.append(a)
        with col1:
            with st.expander(f"{name} : 동일레벨 mccb 확인"):
                st.write(same_level_mccb_list)

        from PIL import Image
        try:
            with col2:
                with st.expander("도면 확인"):
                    image = Image.open(f'assets/{name}.PNG')
                    st.image(image, caption='2전기실 도면')
        except Exception as e:
            print(e)
    # TODO: 2전기실 
    same_level_mccb_list = []
    if list_tags[tag_idx][0].split('.')[5] == "LC_12": # 좀 이상함 
        find_same_lv_list("LC_12")
    elif list_tags[tag_idx][0].split('.')[5] == "LC_13":
        find_same_lv_list("LC_13")
    elif list_tags[tag_idx][0].split('.')[5] == "LC_22":
        find_same_lv_list("LC_22")
    elif list_tags[tag_idx][0].split('.')[5] == "LC_32":
        find_same_lv_list("LC_32")
    
    browsepath, id = list_tags[st.session_state.tag_idx]

    # df_tablenames = get_tablenames()
    # tables_idx = sidebar.multiselect("Table", options=range(len(df_tablenames)), format_func=lambda i: df_tablenames["DESCRIPTION"][i], on_change=on_setting_changed)
    # target_tables = df_tablenames["TABLE_NAME"][tables_idx].to_list()

    get_data_btn = sidebar.button("Get data", on_click=on_run_clicked)
    if st.session_state.data_loaded:
        # query_list = []
        
        # functions = (query_get_thdval, query_get_tddval) # thd, tdd 
        # harmonic_data, query_tmp = get_data_all_phase(functions, st.session_state.tag_idx, start_date, end_date)
        # query_list += query_tmp
        
        # functions = (query_get_currentval, query_get_voltageval) # 전류, 전압 
        # other_data, query_tmp = get_data_all_phase(functions, st.session_state.tag_idx, start_date, end_date)
        # query_list += query_tmp

        # body(harmonic_data, other_data, query_list)

        with st.expander("event 테이블[분 단위][전체기간]"):
            #st.header("event 테이블[분 단위][전체기간]")
            #st.write(f"browsepath={browsepath}")
            st.write(f"id={id}")
            df_event = df_event.loc[df_event['sourceId'] == id]
            st.dataframe(df_event)  

        query = query_get_thdval_h_m_timestamp("A", id, start_date, end_date)
        #st.write(query)
        columns = ["timestamp", "value", "minValue", "maxValue", "phase"]
        df_thdia1min = pd.DataFrame(columns=columns)
        with DB(HOST, PORT, DATABASE, USER, PWD) as db:
            db.execute(query)
            rows = db.fetchall()
            #print(rows)
            df_tmp = pd.DataFrame(rows, columns = columns)
            df_thdia1min = pd.concat([df_thdia1min, df_tmp])
            df_thdia1min = df_thdia1min.reset_index(drop=True)
            with st.expander("thdia1min 테이블[분 단위]"):
                #st.header("thdia1min 테이블[분 단위]")
                st.dataframe(df_thdia1min)

        df_thdia1min = df_thdia1min.merge(df_event, on="timestamp", how="left")
        with st.expander("조인 테이블[분 단위]"):
            #st.header("조인 테이블[분 단위]")
            st.dataframe(df_thdia1min)