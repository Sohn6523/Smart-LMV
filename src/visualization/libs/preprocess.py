import numpy as np
import pandas as pd


def fit_timeindex(df):
    """
    A, B, C 모두 동일한 분단위 시간 축으로 변환
    """
    try:
        if "phase" in df.columns:
            # 중복시간 제거
            df_tmp = df.drop_duplicates(subset=["phase", "timestamp"], keep="first")

            xmin = df_tmp["timestamp"].min().replace(hour=0, minute=0)
            xmax = df_tmp["timestamp"].max().replace(hour=23, minute=59)

            # pd.date_range,explode 사용해서 빠진 시간 정보 채워 넣고, 만들어진 시간 정보에 원본 데이터 밀어 넣고 공백은 NaN으로
            df_tmp = (
                df_tmp.groupby(["phase"])["timestamp"]
                .apply(lambda x: pd.date_range(start=xmin, end=xmax, freq="min"))
                .explode()
                .reset_index()
                .merge(df_tmp, how="left", on=["phase", "timestamp"])
                .fillna(np.NaN)
            )
        else:
            # 중복시간 제거
            df_tmp = df.drop_duplicates(subset=["timestamp"], keep="first")

            xmin = df_tmp["timestamp"].min().replace(hour=0, minute=0)
            xmax = df_tmp["timestamp"].max().replace(hour=23, minute=59)

            # pd.date_range,explode 사용해서 빠진 시간 정보 채워 넣고, 만들어진 시간 정보에 원보 데이터 밀어 넣고 공백은 NaN으로
            df_datetime = pd.DataFrame(index=pd.date_range(start=xmin, end=xmax, freq="min", name="timestamp")).reset_index()
            df_tmp = pd.merge(df_datetime, df_tmp, how="left", on=["timestamp"]).fillna(np.NaN)
        return df_tmp
    except ValueError:
        print(f"Data length is {len(df)}")
        return df


def interpolate_timestamp(df):
    """
    통신 오류로 데이터 누락, A,B,C 동시에 누락되거나 일부만 누락되어 길이 차이로 연산과정에서 오류 발생 가능성 있음
    Timestamp에서 빠진 부분만 해당 시간을 생성하고 나머지 값을 보간한다.
    """
    # 이전의 행위로 컬럼 위치 변경 Phase-time-나머지 값, 이 나머지 값에 보간
    # 이전 단계에서 ffill, bfill 적용가능하나 spline을 사용할 거임
    # ffill, bfill 사용하면 아래 코드 필요 없음, 위 코드에 fillna(np.NaN) 대신 fillna(method='ffill')또는 fillna(method='bfill')으로 가능함
    _, _, *others = df.columns
    for col in others:
        df[col] = df[col].interpolate(method="spline", order=4)

    # spline 보간의 경우 00,01분 값이 nan으로 설정됨. 머리 아파서 bfill로 대체합시다.
    return df.fillna(method="bfill")
