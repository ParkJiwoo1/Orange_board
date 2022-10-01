from openpyxl import load_workbook
load_wb = load_workbook("data.xlsx", data_only=True)
# 시트 이름으로 불러오기 
load_ws = load_wb['Sheet1']



# 모든 행 단위로 출력
data_name=[]
data_time=[]
data_des=[]
for row in load_ws.rows:
    data_name.append(row[0].value)
    data_time.append(row[1].value)
    data_des.append(row[2].value)
print(data_name)
print(data_time)
print(data_des)
    
if "테스트입니다." in data_des:
    print(data_des.index('테스트입니다.'))