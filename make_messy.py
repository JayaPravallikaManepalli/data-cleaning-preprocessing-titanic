from pathlib import Path
import pandas as pd, numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data/source/titanic_source.csv'
OUTPUT=ROOT/'data/raw/titanic_messy.csv'

df=pd.read_csv(SOURCE)
for c in df.columns: df[c]=df[c].astype(object)

df=pd.concat([df,df.loc[[10,45,100,155,210,300,500,700]]],ignore_index=True)

for idx,delta in [(20,5.0),(60,-2.5)]:
    row=df.loc[idx].copy()
    row['Fare']=float(row['Fare'])+delta
    row['Name']=str(row['Name'])+' '
    df=pd.concat([df,pd.DataFrame([row])],ignore_index=True)

for idx in [30,31,32,33,34,35,36,37]: df.loc[idx,'Age']=np.nan
for idx in [70,71,72]: df.loc[idx,'Embarked']='NA'
for idx in [80,81,82,83,84]: df.loc[idx,'Cabin']=' '

for idx,v in {1:' FEMALE ',2:'FEMALE',3:'Female',4:'f',5:'F ',6:' MALE',7:'MALE ',8:'M',9:'m '}.items(): df.loc[idx,'Sex']=v
for idx,v in {10:'southampton',11:' SOUTHAMPTON ',12:'C ',13:'cherbourg',14:'Queenstown',15:' q '}.items(): df.loc[idx,'Embarked']=v

src=pd.read_csv(SOURCE)
for idx in [16,17,18,19,20]: df.loc[idx,'Pclass']=f"Class {int(src.loc[idx,'Pclass'])}"
for idx in [21,22,23,24]: df.loc[idx,'Survived']='Yes' if int(src.loc[idx,'Survived']) else 'No'
for idx in [25,26,27]:
    v=src.loc[idx,'Age']; df.loc[idx,'Age']=f"{v} years" if pd.notna(v) else 'unknown'
for idx in [28,29,30]: df.loc[idx,'Fare']=f"${src.loc[idx,'Fare']:.2f}"

for idx in [40,41,42,43,44]: df.loc[idx,'Name']='  '+str(df.loc[idx,'Name'])+'  '
for idx in [50,51,52]: df.loc[idx,'Ticket']=str(df.loc[idx,'Ticket']).lower()+' '

df.loc[90,'Age']=-5; df.loc[91,'Age']=140; df.loc[92,'Fare']=-10
df.loc[95,'PassengerId']=np.nan; df.loc[96,'PassengerId']=np.nan

OUTPUT.parent.mkdir(parents=True,exist_ok=True)
df.to_csv(OUTPUT,index=False)
print(f'Wrote {OUTPUT}')
